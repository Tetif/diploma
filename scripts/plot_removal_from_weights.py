"""
Скрипт для выбора сохранённых influence-весов и построения кривой метрики
при разном проценте удаления данных для стратегий:
  - lowest / highest / random
  - extremes / median
  - few_bad_then_random / few_median_then_random / few_good_then_random

В коде задаются:
  DEFAULT_WEIGHTS_PATH — путь к папке или файлу influence_weights.pkl
  SELECTED_STRATEGIES  — список стратегий (см. выше)
  SELECTED_METHODS     — список методов (None = все доступные в файле)

Запуск:
  Из IDE: Run Python File / F5 — используются настройки из кода (DEFAULT_WEIGHTS_PATH, SELECTED_STRATEGIES, SELECTED_METHODS).
  Из терминала:
    python scripts/plot_removal_from_weights.py
    python scripts/plot_removal_from_weights.py --weights path/to/weights --method ArnoldiInfluence
    python scripts/plot_removal_from_weights.py --list   # список найденных influence_weights.pkl
"""
import argparse
import sys
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm

# Ensure project root is on path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Путь к папке с весами или к файлу influence_weights.pkl (можно задать в коде вместо --weights).
# Относительный путь — от корня проекта. Пример: _project_root / "experiment_logs" / "2025-01-15" / "12-00-00"
DEFAULT_WEIGHTS_PATH = "experiment_logs/2026-03-07/17-29-05"

# Методы влияния для графика: None = все доступные в файле весов; иначе список, например ["ArnoldiInfluence", "LissaInfluence"].
SELECTED_METHODS = ["Influence",
                    # "LissaInfluence",
                    # 'NystroemSketchInfluence'
                    ]

# Базовая папка для сохранения графиков и CSV (под неё создаётся подпапка с датой-временем и именем датасета/метода).
REMOVAL_PLOT_OUTPUT_DIR = "../removal_plot_output"

from config.settings import (
    EXPERIMENT_CONFIG,
    REMOVAL_STRATEGIES,
    RANDOM_STATE,
    get_model_config,
    EXPERIMENTS_BASE_DIR,
    DISTILLATION_CONFIG,
    DEVICE,
    MODEL_RUN_CONFIG,
    get_n_remove_list,
)
from config import DatasetRegistry
from data.loader import DataLoaderFactory
from data.preprocessing import PreprocessorFactory
from experiments.runner import ExperimentRunner
from influence.io import load_influence_weights
from utils.helpers import set_random_seeds, sample_data
from visualization.plots import plot_results_enhanced, save_removal_metrics_csv


SELECTED_STRATEGIES = MODEL_RUN_CONFIG.get("removal_strategies", REMOVAL_STRATEGIES)


def find_weights_files(base_dir: Path) -> list[tuple[Path, dict]]:
    """Сканирует base_dir рекурсивно, находит influence_weights.pkl и возвращает (path, metadata)."""
    found = []
    base_dir = Path(base_dir)
    if not base_dir.exists():
        return found
    for p in base_dir.rglob("influence_weights.pkl"):
        try:
            _, meta = load_influence_weights(p)
            found.append((p, meta))
        except Exception:
            continue
    return found


def prepare_data(dataset_name: str):
    """
    Воспроизводит загрузку и сплит данных как в main.py.
    Возвращает X_train, y_train, X_test, y_test, X_val, y_val, preprocessor, model_params, n_epochs, dataset_config.
    """
    set_random_seeds(RANDOM_STATE)
    dataset_config = DatasetRegistry.get(dataset_name)
    X, y, cfg = DataLoaderFactory.load_dataset(dataset_config, None)
    if cfg.task_type in ['binary_classification', 'multiclass_classification']:
        if y.dtype == 'object' or y.dtype.name == 'object':
            le = LabelEncoder()
            y = pd.Series(le.fit_transform(y), index=y.index)
    X_temp, X_val, y_temp, y_val = train_test_split(
        X, y, test_size=cfg.val_size, random_state=RANDOM_STATE, stratify=y if cfg.stratify else None
    )
    n = EXPERIMENT_CONFIG['sample_size_percentage'] / 100.0
    X_sample, y_sample = sample_data(X_temp, y_temp, sample_fraction=n)
    X_train, X_test, y_train, y_test = train_test_split(
        X_sample, y_sample, test_size=EXPERIMENT_CONFIG['test_size'], random_state=RANDOM_STATE
    )
    preprocessor = PreprocessorFactory.create(dataset_config, None)
    preprocessor.fit(X_train)
    X_train_processed = preprocessor.transform(X_train)
    if hasattr(X_train_processed, 'toarray'):
        X_train_processed = X_train_processed.toarray()
    actual_input_size = X_train_processed.shape[1]
    model_type = MODEL_RUN_CONFIG['model_type']
    model_params = {
        'model_type': model_type,
        'model_architecture': MODEL_RUN_CONFIG['model_architecture'],
        'input_size': actual_input_size,
        'device': DEVICE,
        'task_type': cfg.task_type,
        'use_distillation': DISTILLATION_CONFIG['use_distillation'],
        'distillation_epochs': DISTILLATION_CONFIG['distillation_epochs'],
        'temperature': DISTILLATION_CONFIG['temperature'],
        'student_architecture': DISTILLATION_CONFIG['student_architecture'],
    }
    try:
        dataset_model_config = get_model_config(dataset_name, model_type)
    except ValueError:
        from config.settings import DATASET_MODEL_CONFIGS
        dataset_model_config = DATASET_MODEL_CONFIGS.get(dataset_name, {}).get(model_type, {})
    for key, value in dataset_model_config.items():
        if key not in model_params or key in ['learning_rate', 'num_leaves', 'max_depth', 'iterations', 'n_estimators', 'layers', 'dropout']:
            model_params[key] = value
    n_epochs = 500 if model_params.get('model_type') == 'pytorch' or model_params.get('use_distillation') else 1
    return X_train, y_train, X_test, y_test, X_val, y_val, preprocessor, model_params, n_epochs, dataset_config


def run_removal_experiments(
    runner: ExperimentRunner,
    weights_by_method: dict,
    strategies: list,
    n_remove_list: list,
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
    preprocessor,
    model_params: dict,
    n_epochs: int,
    dataset_config,
):
    """
    Запускает эксперименты удаления для выбранных методов и стратегий.
    weights_by_method: {имя_метода: массив весов}.
    strategies: список из
        'lowest', 'highest', 'random', 'extremes', 'median',
        'few_bad_then_random', 'few_median_then_random', 'few_good_then_random'.
    Возвращает (results, random_run_results).
    """
    results = {}
    random_run_results = {}
    n_classes_expected = None
    if dataset_config and dataset_config.task_type in ['binary_classification', 'multiclass_classification']:
        n_classes_expected = int(y_train.nunique())

    # Baseline один раз
    history_baseline, _ = runner.train_and_evaluate(
        preprocessor, model_params, X_train, y_train, X_test, y_test, X_val, y_val, n_epochs
    )
    results["orig"] = history_baseline

    for method_name, weights in weights_by_method.items():
        weights = np.asarray(weights)
        if "lowest" in strategies:
            plot_method = f"{method_name}_lowest"
            results[f"{plot_method}_0"] = results["orig"]
            idx_sorted = np.argsort(weights)
            for pct in tqdm(n_remove_list, desc=f"{plot_method} removal", leave=False):
                n_to_remove = int(len(X_train) * pct / 100)
                n_to_remove = max(1, min(n_to_remove, len(X_train) - 10))
                remove_idx = idx_sorted[:n_to_remove]
                keep_mask = np.ones(len(X_train), dtype=bool)
                keep_mask[remove_idx] = False
                X_sub = X_train.iloc[keep_mask]
                y_sub = y_train.iloc[keep_mask]
                if len(X_sub) < 10 or (n_classes_expected is not None and y_sub.nunique() < n_classes_expected):
                    continue
                history, _ = runner.train_and_evaluate(
                    preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
                )
                results[f"{plot_method}_{pct}pct"] = history
        if "highest" in strategies:
            plot_method = f"{method_name}_highest"
            results[f"{plot_method}_0"] = results["orig"]
            idx_sorted = np.argsort(weights)[::-1]
            for pct in tqdm(n_remove_list, desc=f"{plot_method} removal", leave=False):
                n_to_remove = int(len(X_train) * pct / 100)
                n_to_remove = max(1, min(n_to_remove, len(X_train) - 10))
                remove_idx = idx_sorted[:n_to_remove]
                keep_mask = np.ones(len(X_train), dtype=bool)
                keep_mask[remove_idx] = False
                X_sub = X_train.iloc[keep_mask]
                y_sub = y_train.iloc[keep_mask]
                if len(X_sub) < 10 or (n_classes_expected is not None and y_sub.nunique() < n_classes_expected):
                    continue
                history, _ = runner.train_and_evaluate(
                    preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
                )
                results[f"{plot_method}_{pct}pct"] = history
        if "extremes" in strategies:
            plot_method = f"{method_name}_extremes"
            results[f"{plot_method}_0"] = results["orig"]
            idx_sorted = np.argsort(weights)
            for pct in tqdm(n_remove_list, desc=f"{plot_method} removal", leave=False):
                n_to_remove = int(len(X_train) * pct / 100)
                n_to_remove = max(1, min(n_to_remove, len(X_train) - 10))
                n_low = n_to_remove // 2
                n_high = n_to_remove - n_low
                remove_idx = np.concatenate([idx_sorted[:n_low], idx_sorted[-n_high:]])
                keep_mask = np.ones(len(X_train), dtype=bool)
                keep_mask[remove_idx] = False
                X_sub = X_train.iloc[keep_mask]
                y_sub = y_train.iloc[keep_mask]
                if len(X_sub) < 10 or (n_classes_expected is not None and y_sub.nunique() < n_classes_expected):
                    continue
                history, _ = runner.train_and_evaluate(
                    preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
                )
                results[f"{plot_method}_{pct}pct"] = history
        if "median" in strategies:
            plot_method = f"{method_name}_median"
            results[f"{plot_method}_0"] = results["orig"]
            idx_sorted = np.argsort(weights)
            n_train = len(idx_sorted)
            for pct in tqdm(n_remove_list, desc=f"{plot_method} removal", leave=False):
                n_to_remove = int(n_train * pct / 100)
                n_to_remove = max(1, min(n_to_remove, n_train - 10))
                mid = n_train // 2
                half = n_to_remove // 2
                start = max(0, mid - half)
                end = min(n_train, start + n_to_remove)
                if end - start < n_to_remove:
                    if start == 0:
                        end = n_to_remove
                    else:
                        start = end - n_to_remove
                remove_idx = idx_sorted[start:end]
                keep_mask = np.ones(len(X_train), dtype=bool)
                keep_mask[remove_idx] = False
                X_sub = X_train.iloc[keep_mask]
                y_sub = y_train.iloc[keep_mask]
                if len(X_sub) < 10 or (n_classes_expected is not None and y_sub.nunique() < n_classes_expected):
                    continue
                history, _ = runner.train_and_evaluate(
                    preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
                )
                results[f"{plot_method}_{pct}pct"] = history
        # Смешанные стратегии: немного детерминированного удаления + остальное случайно
        if "few_bad_then_random" in strategies:
            plot_method = f"{method_name}_few_bad_rand"
            results[f"{plot_method}_0"] = results["orig"]
            idx_sorted = np.argsort(weights)  # «плохие» — с наименьшим влиянием
            n_train = len(idx_sorted)
            fixed_frac = 0.1  # доля выборки, удаляемая детерминированно (10%)
            for pct in tqdm(n_remove_list, desc=f"{plot_method} removal", leave=False):
                n_total = int(n_train * pct / 100)
                n_total = max(1, min(n_total, n_train - 10))
                n_fixed = min(int(fixed_frac * n_train), n_total)
                if n_fixed <= 0:
                    n_fixed = min(1, n_total)
                det_idx = idx_sorted[:n_fixed]
                remaining = np.setdiff1d(np.arange(n_train), det_idx, assume_unique=True)
                n_rand = n_total - n_fixed
                if n_rand > 0 and len(remaining) >= n_rand:
                    np.random.seed(RANDOM_STATE + pct)
                    rand_idx = np.random.choice(remaining, size=n_rand, replace=False)
                    remove_idx = np.concatenate([det_idx, rand_idx])
                else:
                    remove_idx = det_idx
                keep_mask = np.ones(n_train, dtype=bool)
                keep_mask[remove_idx] = False
                X_sub = X_train.iloc[keep_mask]
                y_sub = y_train.iloc[keep_mask]
                if len(X_sub) < 10 or (n_classes_expected is not None and y_sub.nunique() < n_classes_expected):
                    continue
                history, _ = runner.train_and_evaluate(
                    preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
                )
                results[f"{plot_method}_{pct}pct"] = history
        if "few_median_then_random" in strategies:
            plot_method = f"{method_name}_few_median_rand"
            results[f"{plot_method}_0"] = results["orig"]
            idx_sorted = np.argsort(weights)
            n_train = len(idx_sorted)
            fixed_frac = 0.1
            for pct in tqdm(n_remove_list, desc=f"{plot_method} removal", leave=False):
                n_total = int(n_train * pct / 100)
                n_total = max(1, min(n_total, n_train - 10))
                n_fixed = min(int(fixed_frac * n_train), n_total)
                if n_fixed <= 0:
                    n_fixed = min(1, n_total)
                mid = n_train // 2
                half = n_fixed // 2
                start = max(0, mid - half)
                end = min(n_train, start + n_fixed)
                if end - start < n_fixed:
                    if start == 0:
                        end = n_fixed
                    else:
                        start = end - n_fixed
                det_idx = idx_sorted[start:end]
                remaining = np.setdiff1d(np.arange(n_train), det_idx, assume_unique=True)
                n_rand = n_total - n_fixed
                if n_rand > 0 and len(remaining) >= n_rand:
                    np.random.seed(RANDOM_STATE + pct + 1000)
                    rand_idx = np.random.choice(remaining, size=n_rand, replace=False)
                    remove_idx = np.concatenate([det_idx, rand_idx])
                else:
                    remove_idx = det_idx
                keep_mask = np.ones(n_train, dtype=bool)
                keep_mask[remove_idx] = False
                X_sub = X_train.iloc[keep_mask]
                y_sub = y_train.iloc[keep_mask]
                if len(X_sub) < 10 or (n_classes_expected is not None and y_sub.nunique() < n_classes_expected):
                    continue
                history, _ = runner.train_and_evaluate(
                    preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
                )
                results[f"{plot_method}_{pct}pct"] = history
        if "few_good_then_random" in strategies:
            plot_method = f"{method_name}_few_good_rand"
            results[f"{plot_method}_0"] = results["orig"]
            idx_sorted = np.argsort(weights)[::-1]  # «хорошие» — с наибольшим влиянием
            n_train = len(idx_sorted)
            fixed_frac = 0.1
            for pct in tqdm(n_remove_list, desc=f"{plot_method} removal", leave=False):
                n_total = int(n_train * pct / 100)
                n_total = max(1, min(n_total, n_train - 10))
                n_fixed = min(int(fixed_frac * n_train), n_total)
                if n_fixed <= 0:
                    n_fixed = min(1, n_total)
                det_idx = idx_sorted[:n_fixed]
                remaining = np.setdiff1d(np.arange(n_train), det_idx, assume_unique=True)
                n_rand = n_total - n_fixed
                if n_rand > 0 and len(remaining) >= n_rand:
                    np.random.seed(RANDOM_STATE + pct + 2000)
                    rand_idx = np.random.choice(remaining, size=n_rand, replace=False)
                    remove_idx = np.concatenate([det_idx, rand_idx])
                else:
                    remove_idx = det_idx
                keep_mask = np.ones(n_train, dtype=bool)
                keep_mask[remove_idx] = False
                X_sub = X_train.iloc[keep_mask]
                y_sub = y_train.iloc[keep_mask]
                if len(X_sub) < 10 or (n_classes_expected is not None and y_sub.nunique() < n_classes_expected):
                    continue
                history, _ = runner.train_and_evaluate(
                    preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
                )
                results[f"{plot_method}_{pct}pct"] = history

    if "random" in strategies:
        n_random_runs = EXPERIMENT_CONFIG.get("n_random_runs", 1)
        for run_idx in tqdm(range(n_random_runs), desc="Random removal", leave=False):
            for pct in n_remove_list:
                n_to_remove = int(len(X_train) * pct / 100)
                n_to_remove = max(1, min(n_to_remove, len(X_train) - 10))
                np.random.seed(RANDOM_STATE + run_idx)
                remove_idx = np.random.choice(len(X_train), size=n_to_remove, replace=False)
                keep_mask = np.ones(len(X_train), dtype=bool)
                keep_mask[remove_idx] = False
                X_sub = X_train.iloc[keep_mask]
                y_sub = y_train.iloc[keep_mask]
                if len(X_sub) < 10 or (n_classes_expected is not None and y_sub.nunique() < n_classes_expected):
                    continue
                history, _ = runner.train_and_evaluate(
                    preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
                )
                if pct not in random_run_results:
                    random_run_results[pct] = []
                random_run_results[pct].append(history["final_mae"])
        for pct, mae_values in random_run_results.items():
            if mae_values:
                results[f"random_{pct}pct"] = {"final_mae": np.median(mae_values)}

    return results, random_run_results


def main():
    parser = argparse.ArgumentParser(
        description="Plot metric vs removal % from saved influence weights (strategies: lowest, highest, random, extremes, median)"
    )
    parser.add_argument(
        "--weights",
        type=Path,
        default=None,
        help="Path to influence_weights.pkl (or directory to search for latest). If omitted, uses DEFAULT_WEIGHTS_PATH from code.",
    )
    parser.add_argument(
        "--method",
        type=str,
        default=None,
        help="Single influence method (e.g. ArnoldiInfluence). If omitted, uses SELECTED_METHODS from code or all available.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available influence_weights.pkl under experiment_logs and exit.",
    )
    parser.add_argument(
        "--no-random",
        action="store_true",
        help="Exclude 'random' from strategies (overrides SELECTED_STRATEGIES for random only).",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not call plt.show() (e.g. for saving only).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Folder to save plot and CSV into. Default: REMOVAL_PLOT_OUTPUT_DIR / <dataset>_<timestamp>.",
    )
    args = parser.parse_args()

    if args.list:
        base = _project_root / EXPERIMENTS_BASE_DIR
        found = find_weights_files(base)
        if not found:
            print(f"No influence_weights.pkl found under {base}")
            return
        print("Available influence_weights.pkl:")
        for p, meta in sorted(found, key=lambda x: x[0]):
            ds = meta.get("dataset_name", "?")
            n = meta.get("n_train", "?")
            methods = meta.get("methods", [])
            ts = meta.get("timestamp", "")
            print(f"  {p}")
            print(f"    dataset={ds}, n_train={n}, methods={methods}, timestamp={ts}")
        return

    weights_input = args.weights
    if not weights_input and DEFAULT_WEIGHTS_PATH is not None:
        weights_input = DEFAULT_WEIGHTS_PATH
    if not weights_input:
        parser.error("--weights PATH is required (or set DEFAULT_WEIGHTS_PATH in code, or use --list)")

    weights_path = Path(weights_input)
    if not weights_path.is_absolute():
        weights_path = (_project_root / weights_path).resolve()
    if weights_path.is_dir():
        found = find_weights_files(weights_path)
        if not found:
            print(f"No influence_weights.pkl in {weights_path}")
            return
        weights_path = found[-1][0]
        print(f"Using {weights_path}")

    scores_raw, metadata = load_influence_weights(weights_path)
    available_methods = list(scores_raw.keys())

    # Какие методы строить: из CLI (один) или из конфига (список / все)
    if args.method is not None:
        methods_to_use = [args.method]
    else:
        methods_to_use = SELECTED_METHODS
    if methods_to_use is None:
        methods_to_use = available_methods

    methods_to_use = [m for m in methods_to_use if m in scores_raw]
    if not methods_to_use:
        requested = args.method if args.method is not None else SELECTED_METHODS
        print(f"No selected methods found in weights. Requested: {requested}; available: {available_methods}")
        return

    # Стратегии: из конфига, при необходимости убираем random по флагу
    strategies = list(SELECTED_STRATEGIES)
    if args.no_random and "random" in strategies:
        strategies = [s for s in strategies if s != "random"]

    weights_by_method = {m: np.asarray(scores_raw[m]) for m in methods_to_use}
    dataset_name = metadata.get("dataset_name")
    if not dataset_name:
        print("metadata lacks dataset_name; cannot reproduce data split.")
        return
    n_remove_list = metadata.get("n_remove_list")
    if not n_remove_list:
        n_remove_list = get_n_remove_list()

    print("Preparing data (same split as main)...")
    X_train, y_train, X_test, y_test, X_val, y_val, preprocessor, model_params, n_epochs, dataset_config = prepare_data(
        dataset_name
    )
    first_weights = next(iter(weights_by_method.values()))
    if len(X_train) != len(first_weights):
        print(f"Length mismatch: X_train has {len(X_train)} rows, weights have {len(first_weights)}. Wrong run?")
        return
    print(f"Running removal: methods={methods_to_use}, strategies={strategies}, n_remove_list={n_remove_list[:5]}...")
    runner = ExperimentRunner(logger=None)
    results, random_run_results = run_removal_experiments(
        runner,
        weights_by_method,
        strategies,
        n_remove_list,
        X_train, y_train, X_test, y_test, X_val, y_val,
        preprocessor, model_params, n_epochs, dataset_config,
    )

    if args.output is not None:
        out_dir = Path(args.output)
        if not out_dir.is_absolute():
            out_dir = _project_root / out_dir
    else:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        methods_label = "_".join(methods_to_use) if len(methods_to_use) <= 2 else "multi"
        subdir = f"{dataset_name}_{methods_label}_{ts}"
        out_dir = _project_root / REMOVAL_PLOT_OUTPUT_DIR / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Saving plot and CSV to: {out_dir}")

    csv_path = out_dir / "removal_metrics.csv"
    save_removal_metrics_csv(results, n_remove_list, csv_path)
    print(f"CSV saved: {csv_path}")

    print("Plotting...")
    import matplotlib.pyplot as plt
    plot_results_enhanced(results, n_remove_list, logger=None, random_run_results=random_run_results)
    plot_path = out_dir / "removal_plot.png"
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    print(f"Plot saved: {plot_path}")
    if not args.no_show:
        plt.show()


if __name__ == "__main__":
    main()
