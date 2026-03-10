import argparse
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
import pandas as pd
from tqdm import tqdm

# Ensure project root is on path (same pattern as plot_removal_from_weights.py)
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from config import (  # type: ignore
    EXPERIMENTS_BASE_DIR,
    RANDOM_STATE,
    EXPERIMENT_CONFIG,
    DISTILLATION_CONFIG,
    DEVICE,
    DatasetRegistry,
)
from config.settings import (  # type: ignore
    get_model_config,
    get_influence_params,
    get_n_remove_list,
)
from data.loader import DataLoaderFactory  # type: ignore
from data.preprocessing import PreprocessorFactory  # type: ignore
from experiments.runner import ExperimentRunner  # type: ignore
from experiments.logger import ExperimentLogger  # type: ignore
from influence.methods import InfluenceMethods  # type: ignore
from influence.utils import get_influence_statistics  # type: ignore
from scripts.plot_removal_from_weights import (  # type: ignore
    run_removal_experiments,
)
from utils.helpers import set_random_seeds, sample_data  # type: ignore
from visualization.plots import (  # type: ignore
    save_removal_metrics_csv,
    plot_results_enhanced,
)


SUPPORTED_MODEL_TYPES = ("xgboost", "lightgbm", "random_forest", "catboost")
DEFAULT_INFLUENCE_METHODS = ("Influence", "LissaInfluence", "NystroemSketchInfluence")


@dataclass
class StudyConfig:
    dataset_name: str
    model_type: str
    sample_fraction: float
    mode: str
    influence_methods: List[str]


def _parse_list_arg(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _select_datasets(arg: str) -> List[str]:
    available = list(DatasetRegistry.list())
    if arg.lower() in ("all", "all-tabular"):
        selected = []
        for name in available:
            cfg = DatasetRegistry.get(name)
            # Основной фокус — табличные датасеты; но при необходимости можно расширить
            if getattr(cfg, "data_type", None) == "tabular":
                selected.append(name)
        return selected

    requested = _parse_list_arg(arg)
    unknown = [d for d in requested if d not in available]
    if unknown:
        raise ValueError(f"Unknown datasets: {unknown}. Available: {available}")
    return requested


def _build_study_grid(
    datasets: List[str],
    model_types: List[str],
    sample_fractions: List[float],
    mode: str,
    influence_methods: List[str],
) -> List[StudyConfig]:
    if not model_types:
        model_types = ["xgboost"]
    for mt in model_types:
        if mt not in SUPPORTED_MODEL_TYPES:
            raise ValueError(f"Unsupported model_type '{mt}'. Supported: {SUPPORTED_MODEL_TYPES}")

    if not sample_fractions:
        sample_fractions = [0.1]

    configs: List[StudyConfig] = []
    for ds in datasets:
        for mt in model_types:
            # Для больших датасетов по умолчанию оставляем только самый лёгкий конфиг в quick-режиме
            for sf in sample_fractions:
                configs.append(
                    StudyConfig(
                        dataset_name=ds,
                        model_type=mt,
                        sample_fraction=sf,
                        mode=mode,
                        influence_methods=list(influence_methods),
                    )
                )
    return configs


def _effective_sample_fraction(user_fraction: float) -> float:
    """
    Итоговая доля от X_temp после holdout:
    EXPERIMENT_CONFIG['sample_size_percentage']/100 * user_fraction.
    """
    base = EXPERIMENT_CONFIG.get("sample_size_percentage", 100) / 100.0
    return max(1e-6, min(1.0, base * user_fraction))


def _prepare_data_for_study(
    dataset_name: str,
    sample_fraction: float,
    model_type: str,
):
    """
    Адаптированная версия prepare_data из plot_removal_from_weights.py
    с поддержкой дополнительного sample_fraction (например, 0.1 = 10%).
    """
    set_random_seeds(RANDOM_STATE)
    dataset_config = DatasetRegistry.get(dataset_name)

    X, y, cfg = DataLoaderFactory.load_dataset(dataset_config, logger=None)

    # Кодировка целевой переменной для классификации
    if cfg.task_type in ["binary_classification", "multiclass_classification"]:
        if y.dtype == "object" or getattr(y.dtype, "name", "") == "object":
            from sklearn.preprocessing import LabelEncoder

            le = LabelEncoder()
            y = pd.Series(le.fit_transform(y), index=y.index)

    from sklearn.model_selection import train_test_split

    X_temp, X_val, y_temp, y_val = train_test_split(
        X,
        y,
        test_size=cfg.val_size,
        random_state=RANDOM_STATE,
        stratify=y if cfg.stratify else None,
    )

    eff_fraction = _effective_sample_fraction(sample_fraction)
    X_sample, y_sample = sample_data(X_temp, y_temp, sample_fraction=eff_fraction)

    X_train, X_test, y_train, y_test = train_test_split(
        X_sample,
        y_sample,
        test_size=EXPERIMENT_CONFIG["test_size"],
        random_state=RANDOM_STATE,
    )

    preprocessor = PreprocessorFactory.create(dataset_config, logger=None)
    preprocessor.fit(X_train)
    X_train_processed = preprocessor.transform(X_train)
    if hasattr(X_train_processed, "toarray"):
        X_train_processed = X_train_processed.toarray()
    actual_input_size = X_train_processed.shape[1]

    model_params: Dict[str, Any] = {
        "model_type": model_type,
        "model_architecture": "simple",
        "input_size": actual_input_size,
        "device": DEVICE,
        "task_type": cfg.task_type,
        "use_distillation": DISTILLATION_CONFIG["use_distillation"],
        "distillation_epochs": DISTILLATION_CONFIG["distillation_epochs"],
        "temperature": DISTILLATION_CONFIG["temperature"],
        "student_architecture": DISTILLATION_CONFIG["student_architecture"],
    }

    try:
        dataset_model_config = get_model_config(dataset_name, model_type)
    except ValueError:
        dataset_model_config = {}

    for key, value in dataset_model_config.items():
        if key not in model_params or key in [
            "learning_rate",
            "num_leaves",
            "max_depth",
            "iterations",
            "n_estimators",
            "layers",
            "dropout",
        ]:
            model_params[key] = value

    # Решение о числе эпох: для деревьев — 1, для pytorch — больше
    if model_params.get("model_type") == "pytorch" or model_params.get("use_distillation", False):
        n_epochs = EXPERIMENT_CONFIG.get("n_epochs", 500)
    else:
        n_epochs = 1

    return (
        X_train,
        y_train,
        X_test,
        y_test,
        X_val,
        y_val,
        preprocessor,
        model_params,
        n_epochs,
        dataset_config,
        eff_fraction,
    )


def _compute_influence_weights(
    logger: ExperimentLogger,
    runner: ExperimentRunner,
    dataset_config,
    X_train,
    y_train,
    X_test,
    y_test,
    X_val,
    y_val,
    preprocessor,
    model_params: Dict[str, Any],
    n_epochs: int,
    influence_methods: List[str],
):
    """
    Обучает базовую модель и считает influence-веса с помощью InfluenceMethods.
    Возвращает (scores, scores_raw).
    """
    history, model = runner.train_and_evaluate(
        preprocessor,
        model_params,
        X_train,
        y_train,
        X_test,
        y_test,
        X_val,
        y_val,
        n_epochs,
    )
    runner.results["orig"] = history

    from sklearn.pipeline import Pipeline

    pipeline = Pipeline(
        [
            ("preproc", preprocessor),
            ("model", model),
        ]
    )

    influence = InfluenceMethods(logger, dataset_config=dataset_config)
    methods, _ = influence.setup_methods(
        pipeline,
        X_train,
        y_train,
        X_test,
        y_test,
        preprocessor,
        methods_to_use=influence_methods,
    )

    scores, scores_raw = influence.compute_scores(
        methods,
        X_train,
        y_train,
        preprocessor,
        X_test,
        y_test,
        pipeline,
    )

    if scores_raw:
        dataset_name = getattr(dataset_config, "name", "unknown")
        n_remove_list = get_n_remove_list()
        logger.save_influence_weights_to_experiment_dir(
            scores_raw,
            dataset_name=dataset_name,
            n_train=len(X_train),
            n_remove_list=n_remove_list,
        )

        influence_stats = get_influence_statistics(scores_raw)
        model_metrics = {
            "baseline_mae": history.get("final_mae"),
            "best_validation_mae": history.get("best_val_mae"),
            "best_epoch": history.get("best_epoch"),
            "total_training_epochs": n_epochs,
            "model_type": model_params.get("model_type"),
            "used_distillation": model_params.get("use_distillation", False),
        }
        config_stub = {
            "debug_mode": False,
            "model_params": model_params,
            "training_params": EXPERIMENT_CONFIG.copy(),
            "dataset": {
                "name": getattr(dataset_config, "name", ""),
                "task_type": getattr(dataset_config, "task_type", ""),
                "target_column": getattr(dataset_config, "target_column", ""),
            },
        }
        logger.save_config(config_stub)
        logger.generate_summary(config_stub, model_metrics, influence_stats, scores, scores_raw)

    return scores, scores_raw, history


def _run_single_study_config(
    cfg: StudyConfig,
    master_log_path: Path,
):
    """
    Запускает полный цикл для одной конфигурации:
    - подготовка данных (с заданной sample_fraction),
    - расчёт influence-весов,
    - эксперименты с удалением (несколько стратегий + random),
    - сохранение CSV и графиков.
    """
    start_time = time.time()

    base_dir = Path(EXPERIMENTS_BASE_DIR) / "large_study"
    experiment_name = f"{cfg.dataset_name}_{cfg.model_type}_sf{cfg.sample_fraction:.3f}"
    logger = ExperimentLogger(base_dir=str(base_dir), experiment_name=experiment_name)

    with master_log_path.open("a", encoding="utf-8") as ml:
        ml.write(
            f"[START] {experiment_name} | influence_methods={cfg.influence_methods} | mode={cfg.mode}\n"
        )

    (
        X_train,
        y_train,
        X_test,
        y_test,
        X_val,
        y_val,
        preprocessor,
        model_params,
        n_epochs,
        dataset_config,
        eff_fraction,
    ) = _prepare_data_for_study(cfg.dataset_name, cfg.sample_fraction, cfg.model_type)

    # Ограничение: не использовать тяжёлую pytorch модель для больших датасетов
    if cfg.model_type == "pytorch":
        raise ValueError("PyTorch models are not supported in large study script (too slow for big datasets).")

    runner = ExperimentRunner(logger)

    scores, scores_raw, baseline_history = _compute_influence_weights(
        logger,
        runner,
        dataset_config,
        X_train,
        y_train,
        X_test,
        y_test,
        X_val,
        y_val,
        preprocessor,
        model_params,
        n_epochs,
        cfg.influence_methods,
    )

    weights_by_method = {m: np.asarray(w) for m, w in scores_raw.items() if m in cfg.influence_methods}
    if not weights_by_method:
        logger.log_message("No influence weights computed for requested methods; skipping removal experiments.")
        duration = time.time() - start_time
        with master_log_path.open("a", encoding="utf-8") as ml:
            ml.write(f"[SKIP] {experiment_name} | duration={duration:.2f}s (no weights)\n")
        return

    # Проверить совпадение длины весов и X_train
    first_weights = next(iter(weights_by_method.values()))
    if len(first_weights) != len(X_train):
        logger.log_message(
            f"Length mismatch between X_train ({len(X_train)}) and weights ({len(first_weights)}); skipping."
        )
        duration = time.time() - start_time
        with master_log_path.open("a", encoding="utf-8") as ml:
            ml.write(f"[MISMATCH] {experiment_name} | duration={duration:.2f}s\n")
        return

    n_remove_list = get_n_remove_list()

    logger.log_message(
        f"Running removal experiments for dataset={cfg.dataset_name}, model={cfg.model_type}, "
        f"sample_fraction={eff_fraction:.4f}, methods={cfg.influence_methods}"
    )

    # Выбор стратегий: в полном режиме используем все, в quick — сокращённый набор
    from scripts.plot_removal_from_weights import SELECTED_STRATEGIES  # type: ignore

    if cfg.mode == "quick":
        strategies = ["lowest", "highest", "random"]
        # Укороченный список процентов удаления
        n_remove_list = [1, 5, 10, 20, 30, 40, 50]
    else:
        strategies = list(SELECTED_STRATEGIES)

    results, random_run_results = run_removal_experiments(
        runner,
        weights_by_method,
        strategies,
        n_remove_list,
        X_train,
        y_train,
        X_test,
        y_test,
        X_val,
        y_val,
        preprocessor,
        model_params,
        n_epochs,
        dataset_config,
    )

    # Сохраняем results.pkl для агрегатора (aggregate_large_study_results.py)
    logger.save_results(
        results,
        scores,
        scores_raw,
        n_remove_list,
        random_run_results=random_run_results,
    )

    # Сохранение removal-метрик и графика
    removal_csv_path = logger.experiment_dir / "removal_metrics.csv"
    save_removal_metrics_csv(results, n_remove_list, removal_csv_path)

    plot_results_enhanced(results, n_remove_list, logger=logger, random_run_results=random_run_results)

    duration = time.time() - start_time
    with master_log_path.open("a", encoding="utf-8") as ml:
        ml.write(f"[DONE] {experiment_name} | duration={duration:.2f}s\n")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Large-scale influence study: compare influence-based and random removal "
            "across multiple datasets, models and hyperparameters."
        )
    )
    parser.add_argument(
        "--datasets",
        type=str,
        default="all-tabular",
        help="Comma-separated dataset names or 'all'/'all-tabular' (default: all-tabular).",
    )
    parser.add_argument(
        "--model-types",
        type=str,
        default="xgboost",
        help="Comma-separated model types to use (subset of: xgboost, lightgbm, random_forest, catboost).",
    )
    parser.add_argument(
        "--sample-fractions",
        type=str,
        default="0.1",
        help="Comma-separated fractions (0-1) of remaining data after holdout to use for training (default: 0.1).",
    )
    parser.add_argument(
        "--influence-methods",
        type=str,
        default=",".join(DEFAULT_INFLUENCE_METHODS),
        help="Comma-separated influence methods (default: Influence,LissaInfluence,NystroemSketchInfluence).",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["quick", "full"],
        default="quick",
        help="Study mode: 'quick' (fewer configs, fewer removal points) or 'full'.",
    )
    args = parser.parse_args()

    datasets = _select_datasets(args.datasets)
    model_types = _parse_list_arg(args.model_types)
    sample_fractions = [float(x) for x in _parse_list_arg(args.sample_fractions)]
    influence_methods = _parse_list_arg(args.influence_methods) or list(DEFAULT_INFLUENCE_METHODS)

    grid = _build_study_grid(datasets, model_types, sample_fractions, args.mode, influence_methods)

    base_dir = Path(EXPERIMENTS_BASE_DIR) / "large_study"
    base_dir.mkdir(parents=True, exist_ok=True)
    master_log_path = base_dir / "study_master_log.txt"

    total = len(grid)
    start_time = time.time()

    print(
        f"Starting large influence study with {total} configurations "
        f"(datasets={datasets}, models={model_types}, sample_fractions={sample_fractions}, "
        f"influence_methods={influence_methods}, mode={args.mode})."
    )
    print(f"Results will be stored under: {base_dir}")

    for idx, cfg in enumerate(grid, start=1):
        cfg_start = time.time()
        print(
            f"\n=== [{idx}/{total}] dataset={cfg.dataset_name}, model={cfg.model_type}, "
            f"sample_fraction={cfg.sample_fraction:.3f}, mode={cfg.mode} ==="
        )
        try:
            _run_single_study_config(cfg, master_log_path)
        except Exception as e:
            duration = time.time() - cfg_start
            with master_log_path.open("a", encoding="utf-8") as ml:
                ml.write(
                    f"[ERROR] {cfg.dataset_name}_{cfg.model_type}_sf{cfg.sample_fraction:.3f} "
                    f"| error={type(e).__name__}: {e} | duration={duration:.2f}s\n"
                )
            print(f"ERROR in config {cfg}: {e}")

        elapsed = time.time() - start_time
        avg_per_cfg = elapsed / idx
        remaining = (total - idx) * avg_per_cfg
        print(
            f"Elapsed: {elapsed/60.0:.1f} min, "
            f"approx remaining: {remaining/60.0:.1f} min "
            f"(avg per config: {avg_per_cfg/60.0:.2f} min)"
        )

    print("Large influence study finished.")


if __name__ == "__main__":
    main()

