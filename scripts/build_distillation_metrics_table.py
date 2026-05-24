"""
Сводная таблица метрик: tree-модели (teacher) против дистиллированного ученика (student).

Запуск (из корня репозитория):
  python scripts/build_distillation_metrics_table.py
  python scripts/build_distillation_metrics_table.py --tabular-only
  python scripts/build_distillation_metrics_table.py --exclude-datasets mnist,cifar10
В процессе выводится прогресс tqdm: сколько комбинаций «датасет × модель» осталось,
в postfix — текущий датасет, тип модели и фаза (baseline / KD).
Выходные файлы по умолчанию:
  distillation_metrics_table.csv
  distillation_metrics_table.md

Использует тот же сплит/предобработку, что main.py и ExperimentRunner.train_and_evaluate
(метрика — primary для типа задачи из METRIC_CONFIG; финальное значение — на holdout validation).

По умолчанию включён быстрый режим дистилляции (≈ секунды–десятки секунд на комбинацию при GPU /
умеренном sample-pct): мало эпох KD и early stopping по val. Для «качества как в эксперименте»
передайте --full-distill (и при необходимости --distillation-epochs).
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Tuple

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder

from config import DatasetRegistry
from config.settings import (
    DEVICE,
    DISTILLATION_CONFIG,
    EXPERIMENT_CONFIG,
    MODEL_RUN_CONFIG,
    RANDOM_STATE,
    get_metric_metadata,
    get_model_config,
    get_selected_metric,
)
from data.loader import DataLoaderFactory
from data.preprocessing import PreprocessorFactory
from experiments.logger import ExperimentLogger
from experiments.runner import ExperimentRunner
from utils.helpers import sample_data, set_random_seeds, split_data
from tqdm import tqdm

TREE_MODEL_TYPES = ["lightgbm", "xgboost", "random_forest", "catboost"]

# Быстрая таблица: ограниченные эпохи KD и ранний стоп по val (основное время ≠ деревья).
FAST_DISTILL_EPOCH_CAP = 80
FAST_DISTILL_PATIENCE = 12
FAST_DISTILL_MIN_DELTA = 1e-5


def default_student_architecture(dataset_name: str) -> str:
    if dataset_name in ("mnist", "cifar10"):
        return "cnn_small"
    return str(DISTILLATION_CONFIG.get("student_architecture", "simple"))


def prepare_arrays(
    dataset_name: str,
    sample_pct: float,
    logger: Optional[ExperimentLogger] = None,
) -> Tuple[Any, ...]:
    set_random_seeds(RANDOM_STATE)
    dataset_config = DatasetRegistry.get(dataset_name)
    if logger is None:
        logger = ExperimentLogger(base_dir="__distill_table_logs__")

    X, y, cfg = DataLoaderFactory.load_dataset(dataset_config, logger)

    if cfg.task_type in ["binary_classification", "multiclass_classification"]:
        if y.dtype == "object" or getattr(y.dtype, "name", None) == "object":
            le = LabelEncoder()
            y = pd.Series(le.fit_transform(y), index=y.index)

    X_temp, X_holdout, y_temp, y_holdout = split_data(
        X,
        y,
        test_size=cfg.val_size,
        random_state=RANDOM_STATE,
        stratify=y if cfg.stratify else None,
        time_series=cfg.use_time_split,
    )

    X_sample, y_sample = sample_data(
        X_temp,
        y_temp,
        sample_fraction=sample_pct / 100.0,
        preserve_order=cfg.use_time_split,
    )

    X_train, X_test, y_train, y_test = split_data(
        X_sample,
        y_sample,
        test_size=EXPERIMENT_CONFIG["test_size"],
        random_state=RANDOM_STATE,
        stratify=y_sample if cfg.stratify else None,
        time_series=cfg.use_time_split,
    )

    preprocessor = PreprocessorFactory.create(dataset_config, logger)
    preprocessor.fit(X_train)

    # train_and_evaluate сам делает preprocessor.transform(...)
    Xt = preprocessor.transform(X_train)
    if hasattr(Xt, "toarray"):
        Xt = Xt.toarray()
    input_size = int(np.asarray(Xt).shape[1])

    return X_train, X_test, X_holdout, y_train, y_test, y_holdout, cfg, preprocessor, dataset_config, input_size


def merge_model_hyperparams(dataset_name: str, model_type: str, task_type: str) -> Dict[str, Any]:
    base = {
        "model_type": model_type,
        "input_size": None,
        "device": DEVICE,
        "task_type": task_type,
        "removal_strategies": MODEL_RUN_CONFIG.get("removal_strategies", ["random"]),
        "removal_per_class": MODEL_RUN_CONFIG.get("removal_per_class", False),
        "removal_stratify_target": MODEL_RUN_CONFIG.get("removal_stratify_target", False),
        "removal_stratify_n_bins": MODEL_RUN_CONFIG.get("removal_stratify_n_bins", 10),
    }
    ds_cfg = get_model_config(dataset_name, model_type)
    for k, v in ds_cfg.items():
        if k not in base:
            base[k] = v
    return base


def run_one_variant(
    runner: ExperimentRunner,
    preprocessor,
    model_params: Dict[str, Any],
    X_train,
    X_test,
    X_holdout,
    y_train,
    y_test,
    y_holdout,
    n_epochs: int,
) -> float:
    history, _, _ = runner.train_and_evaluate(
        preprocessor,
        model_params,
        X_train,
        y_train,
        X_test,
        y_test,
        X_holdout,
        y_holdout,
        n_epochs=n_epochs,
    )
    return float(history["final_metric"])


def markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    def esc(x: str) -> str:
        return str(x).replace("|", "\\|")

    sep = "| " + " | ".join(headers) + " |"
    line = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = "\n".join("| " + " | ".join(esc(c) for c in r) + " |" for r in rows)
    return sep + "\n" + line + "\n" + body + "\n"


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Таблица baseline tree vs distilled student.")
    p.add_argument(
        "--datasets",
        type=str,
        default="",
        help="Список датасетов через запятую; пусто = все из DatasetRegistry.",
    )
    p.add_argument(
        "--exclude-datasets",
        type=str,
        default="",
        help="Не запускать эти датасеты (имена через запятую, регистр не важен), напр. mnist,cifar10.",
    )
    p.add_argument(
        "--tabular-only",
        action="store_true",
        help="Удобный алиас: исключить mnist и cifar10 (--exclude-datasets mnist,cifar10).",
    )
    p.add_argument(
        "--sample-pct",
        type=float,
        default=float(EXPERIMENT_CONFIG.get("sample_size_percentage", 100)),
        help="Доля данных после отделения holdout (как в EXPERIMENT_CONFIG).",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=Path("."),
        help="Каталог для CSV/MD.",
    )
    p.add_argument(
        "--distillation-epochs",
        type=int,
        default=None,
        help="Эпохи KD (по умолчанию: быстрый режим — cap; полный режим — из DISTILLATION_CONFIG).",
    )
    p.add_argument(
        "--full-distill",
        action="store_true",
        help="Полная дистилляция как в конфиге (медленнее); иначе — быстрый режим.",
    )
    args = p.parse_args(argv)

    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
    dev_human = DEVICE
    if str(DEVICE).startswith("cuda") and torch.cuda.is_available():
        try:
            dev_human = f"{DEVICE}:{torch.cuda.get_device_name(0)}"
        except Exception:
            pass
    tqdm.write(f"[distill-metrics] backend={dev_human} (CUDA available={torch.cuda.is_available()})")

    if args.datasets.strip():
        datasets = [d.strip() for d in args.datasets.split(",") if d.strip()]
    else:
        datasets = sorted(DatasetRegistry.list())

    to_exclude: List[str] = []
    if args.tabular_only:
        to_exclude.extend(["mnist", "cifar10"])
    if args.exclude_datasets.strip():
        to_exclude.extend(d.strip() for d in args.exclude_datasets.split(",") if d.strip())
    if to_exclude:
        banned = {x.lower() for x in to_exclude}
        registry_l = {n.lower() for n in DatasetRegistry.list()}
        unknown = banned - registry_l
        if unknown:
            tqdm.write(f"[distill-metrics] warning: в --exclude не из реестра: {sorted(unknown)}")
        datasets = [d for d in datasets if d.lower() not in banned]

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = out_dir / f"distillation_metrics_table_{stem}.csv"
    md_path = out_dir / f"distillation_metrics_table_{stem}.md"

    silent_logger = ExperimentLogger(base_dir="__distill_table_logs__")
    runner = ExperimentRunner(logger=None)

    records: List[Dict[str, Any]] = []

    distill_epochs_eff = int(DISTILLATION_CONFIG["distillation_epochs"])
    distill_patience: Optional[int] = None
    distill_min_delta: Optional[float] = None

    if args.full_distill:
        if args.distillation_epochs is not None:
            distill_epochs_eff = int(args.distillation_epochs)
    else:
        # быстрый режим: мало полных проходов; раньше выходим по val KD-loss
        distill_epochs_eff = (
            int(args.distillation_epochs)
            if args.distillation_epochs is not None
            else int(FAST_DISTILL_EPOCH_CAP)
        )
        distill_patience = int(FAST_DISTILL_PATIENCE)
        distill_min_delta = float(FAST_DISTILL_MIN_DELTA)

    n_models = len(TREE_MODEL_TYPES)
    total_combos = len(datasets) * n_models

    with tqdm(
        total=total_combos,
        desc="Сводная таблица (датасет × модель)",
        unit="combo",
        miniters=1,
        mininterval=0.5,
        dynamic_ncols=True,
    ) as combo_bar:

        for dataset_name in datasets:
            try:
                combo_bar.set_postfix(load=f"{dataset_name}…", phase="prep", refresh=False)
                (
                    X_train,
                    X_test,
                    X_holdout,
                    y_train,
                    y_test,
                    y_holdout,
                    cfg,
                    preprocessor,
                    _ds_cfg_full,
                    input_size,
                ) = prepare_arrays(dataset_name, args.sample_pct, silent_logger)
            except Exception as e:
                records.append(
                    {
                        "dataset": dataset_name,
                        "task_type": "error",
                        "metric_name": "",
                        "model_type": "",
                        "baseline_holdout_metric": "",
                        "student_holdout_metric": "",
                        "delta_student_minus_baseline": "",
                        "higher_is_better": "",
                        "note": repr(e),
                        "student_architecture": "",
                    }
                )
                combo_bar.update(n_models)
                continue

            available_metrics = list(getattr(cfg, "metrics", []) or [])
            metric_name = get_selected_metric(cfg.task_type, available_metrics)
            hi = str(get_metric_metadata(metric_name)["higher_is_better"])

            student_arch = default_student_architecture(dataset_name)

            def resolve_num_class(mc_raw: Dict[str, Any]) -> Optional[int]:
                if cfg.task_type != "multiclass_classification":
                    return None
                yt = np.asarray(y_train).ravel().astype(np.int64)
                uniq = np.unique(yt)
                nc_seen = int(len(uniq))
                lo = int(uniq.min()) if uniq.size else 0
                hi_lab = int(uniq.max()) if uniq.size else 0
                span = hi_lab - lo + 1 if uniq.size else nc_seen
                cfg_nc = mc_raw.get("num_class")
                try:
                    cfg_nc_int = int(cfg_nc) if cfg_nc is not None else None
                except (TypeError, ValueError):
                    cfg_nc_int = None
                # Совпадает с логикой датасетов с фиксированным K классов и жёсткими метками 0…K−1.
                return max(nc_seen, span, cfg_nc_int or 0, 2)

            for mt in TREE_MODEL_TYPES:
                try:
                    raw = merge_model_hyperparams(dataset_name, mt, cfg.task_type)
                except ValueError as e:
                    records.append(
                        {
                            "dataset": dataset_name,
                            "task_type": cfg.task_type,
                            "metric_name": metric_name,
                            "model_type": mt,
                            "baseline_holdout_metric": "",
                            "student_holdout_metric": "",
                            "delta_student_minus_baseline": "",
                            "higher_is_better": hi,
                            "note": f"no_config: {e}",
                            "student_architecture": student_arch,
                        }
                    )
                    combo_bar.update(1)
                    continue

                baseline_params = dict(raw)
                baseline_params["input_size"] = input_size
                baseline_params["use_distillation"] = False
                baseline_params["available_metrics"] = available_metrics

                distill_params = dict(baseline_params)
                distill_params["use_distillation"] = True
                distill_params["distillation_epochs"] = distill_epochs_eff
                distill_params["temperature"] = float(DISTILLATION_CONFIG["temperature"])
                distill_params["student_architecture"] = student_arch
                if distill_patience is not None:
                    distill_params["distillation_patience"] = distill_patience
                if distill_min_delta is not None:
                    distill_params["distillation_min_delta"] = distill_min_delta

                if cfg.task_type == "multiclass_classification":
                    ncc = resolve_num_class(raw)
                    if ncc is not None:
                        baseline_params["num_class"] = ncc
                        distill_params["num_class"] = ncc

                # epoch count передаётся в runner; для деревьев и дистилляции обучение
                # длины эпох задаётся их собственными fit (дистилляция — distillation_epochs).
                n_epochs_passed = 1

                note = ""

                try:
                    combo_bar.set_postfix(ds=dataset_name, model=mt, phase="baseline", refresh=True)
                    b_met = run_one_variant(
                        runner,
                        preprocessor,
                        baseline_params,
                        X_train,
                        X_test,
                        X_holdout,
                        y_train,
                        y_test,
                        y_holdout,
                        n_epochs_passed,
                    )
                except Exception as e:
                    b_met = np.nan
                    note = f"baseline_err: {e!r}"

                try:
                    combo_bar.set_postfix(ds=dataset_name, model=mt, phase="KD", refresh=True)
                    s_met = run_one_variant(
                        runner,
                        preprocessor,
                        distill_params,
                        X_train,
                        X_test,
                        X_holdout,
                        y_train,
                        y_test,
                        y_holdout,
                        n_epochs_passed,
                    )
                except Exception as e:
                    s_met = np.nan
                    note = (note + " " if note else "") + f"student_err: {e!r}"

                delta = ""
                if np.isfinite(b_met) and np.isfinite(s_met):
                    delta = f"{float(s_met) - float(b_met):.6g}"

                records.append(
                    {
                        "dataset": dataset_name,
                        "task_type": cfg.task_type,
                        "metric_name": metric_name,
                        "model_type": mt,
                        "baseline_holdout_metric": f"{b_met:.6g}" if np.isfinite(b_met) else "",
                        "student_holdout_metric": f"{s_met:.6g}" if np.isfinite(s_met) else "",
                        "delta_student_minus_baseline": delta,
                        "higher_is_better": hi,
                        "note": note.strip(),
                        "student_architecture": student_arch,
                        "sample_pct": str(args.sample_pct),
                    }
                )
                combo_bar.update(1)

    fieldnames = [
        "dataset",
        "task_type",
        "metric_name",
        "model_type",
        "baseline_holdout_metric",
        "student_holdout_metric",
        "delta_student_minus_baseline",
        "higher_is_better",
        "student_architecture",
        "sample_pct",
        "note",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in records:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    # Markdown (основная часть таблицы)
    md_headers = [
        "Датасет",
        "Задача",
        "Метрика",
        "Модель",
        "Teacher (holdout)",
        "Student (holdout)",
        "Δ",
        "↑лучше",
        "Student arch",
        "Выборка %",
        "Коммент.",
    ]
    md_rows = []
    for r in records:
        md_rows.append(
            [
                r["dataset"],
                r["task_type"],
                r.get("metric_name", ""),
                r["model_type"],
                r["baseline_holdout_metric"],
                r["student_holdout_metric"],
                r["delta_student_minus_baseline"],
                r["higher_is_better"],
                r["student_architecture"],
                str(r.get("sample_pct", "")),
                str(r.get("note", ""))[:120],
            ]
        )

    prelude = (
        f"# Сравнение baseline tree vs дистиллированная нейросеть\n\n"
        f"- Сплиты и препроцессинг как в `main.py` (holdout = `cfg.val_size` после загрузки).\n"
        f"- Метрика: основная для типа задачи (`METRIC_CONFIG`), финальное значение — на holdout.\n"
        f"- Δ = student − teacher; при `↑лучше=False` положительная Δ означает ухудшение студента.\n"
        f"- Сгенерировано: `{stem}`, sample_pct={args.sample_pct}, "
        f"distill_epochs={distill_epochs_eff}, full_distill={bool(args.full_distill)}.\n\n"
    )

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(prelude)
        f.write(markdown_table(md_headers, md_rows))

    print(f"Wrote {csv_path.resolve()}")
    print(f"Wrote {md_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
