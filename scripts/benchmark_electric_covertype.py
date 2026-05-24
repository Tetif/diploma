#!/usr/bin/env python3
"""
Quick baseline comparison for electric / covertype (same splits as experiments).
Usage: python scripts/benchmark_electric_covertype.py [--sample 20] [--dataset electric|covertype|both]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import config.settings as settings  # noqa: E402
from config import DatasetRegistry  # noqa: E402
from config.settings import get_model_config  # noqa: E402
from data.loader import DataLoaderFactory  # noqa: E402
from experiments.runner import ExperimentRunner  # noqa: E402
from data.preprocessing.factory import PreprocessorFactory  # noqa: E402
from utils.helpers import sample_data, split_data  # noqa: E402


def prepare_data(dataset_name: str, sample_pct: float):
    cfg = DatasetRegistry.get(dataset_name)
    X, y, cfg = DataLoaderFactory.load_dataset(cfg)
    rs = settings.RANDOM_STATE

    X_temp, X_holdout, y_temp, y_holdout = split_data(
        X,
        y,
        test_size=float(settings.EXPERIMENT_CONFIG.get("val_size", 0.1)),
        random_state=rs,
        stratify=y if cfg.stratify else None,
        time_series=cfg.use_time_split,
    )
    X_sample, y_sample = sample_data(
        X_temp,
        y_temp,
        sample_fraction=sample_pct / 100.0,
        random_state=rs,
        preserve_order=cfg.use_time_split,
    )
    X_train, X_test, y_train, y_test = split_data(
        X_sample,
        y_sample,
        test_size=float(settings.EXPERIMENT_CONFIG.get("test_size", 0.2)),
        random_state=rs,
        stratify=y_sample if cfg.stratify else None,
        time_series=cfg.use_time_split,
    )
    return cfg, X_train, X_test, y_train, y_test, X_holdout, y_holdout


def run_one(
    dataset_name: str,
    sample_pct: float,
    model_type: str,
    use_distillation: bool,
    architecture: str = "simple",
    n_epochs: int = 200,
    distill_epochs: int = 300,
):
    cfg, X_train, X_test, y_train, y_test, X_val, y_val = prepare_data(
        dataset_name, sample_pct
    )
    runner = ExperimentRunner(logger=None)
    preprocessor = PreprocessorFactory.create(cfg, None)
    preprocessor.fit(X_train)

    mp = get_model_config(dataset_name, model_type)
    if model_type == "pytorch":
        arch_cfg = mp.get(architecture, mp.get("simple", {}))
        model_params = {
            "model_type": "pytorch",
            "task_type": cfg.task_type,
            "model_architecture": architecture,
            **arch_cfg,
            "device": settings.DEVICE,
            "use_distillation": False,
        }
        Xt = preprocessor.transform(X_train)
        if hasattr(Xt, "toarray"):
            Xt = Xt.toarray()
        model_params["input_size"] = Xt.shape[1]
    else:
        Xt = preprocessor.transform(X_train)
        if hasattr(Xt, "toarray"):
            Xt = Xt.toarray()
        model_params = {
            "model_type": model_type,
            "task_type": cfg.task_type,
            "use_distillation": use_distillation,
            "distillation_epochs": distill_epochs,
            "student_architecture": "improved" if use_distillation else "simple",
            "device": settings.DEVICE,
            "input_size": Xt.shape[1],
            **mp,
        }
        if cfg.task_type == "multiclass_classification":
            model_params["num_class"] = int(len(np.unique(np.asarray(y_train).ravel())))

    hist, _, _ = runner.train_and_evaluate(
        preprocessor,
        model_params,
        X_train,
        y_train,
        X_test,
        y_test,
        X_val,
        y_val,
        n_epochs=n_epochs if model_type == "pytorch" else 1,
    )
    return {
        "final_metric": hist["final_metric"],
        "best_val": hist.get("best_validation_metric", hist.get("best_val_metric")),
        "best_epoch": hist["best_epoch"],
        "metric": hist["metric_name"],
    }


def benchmark_dataset(dataset_name: str, sample_pct: float, n_epochs: int):
    print(f"\n{'='*60}\n{dataset_name.upper()} @ {sample_pct}% sample\n{'='*60}")
    variants = [
        ("lightgbm (native)", "lightgbm", False, "simple"),
        ("lightgbm + distill-improved", "lightgbm", True, "improved"),
        ("pytorch simple", "pytorch", False, "simple"),
        ("pytorch improved", "pytorch", False, "improved"),
    ]
    results = []
    for label, mt, ud, arch in variants:
        print(f"  Training: {label}...", flush=True)
        try:
            r = run_one(
                dataset_name,
                sample_pct,
                mt,
                ud,
                architecture=arch,
                n_epochs=n_epochs,
                distill_epochs=400,
            )
            results.append((label, r))
            print(
                f"    holdout {r['metric']}={r['final_metric']:.6g} "
                f"(best_val={r['best_val']:.6g} @ ep {r['best_epoch']})"
            )
        except Exception as exc:
            print(f"    FAILED: {exc}")
    if results:
        best = min(results, key=lambda x: x[1]["final_metric"]) if results[0][1]["metric"] == "mae" else max(
            results, key=lambda x: x[1]["final_metric"]
        )
        print(f"\n  Best variant: {best[0]} ({best[1]['metric']}={best[1]['final_metric']:.6g})")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sample", type=float, default=20.0)
    p.add_argument("--dataset", choices=["electric", "covertype", "both"], default="both")
    p.add_argument("--epochs", type=int, default=150)
    args = p.parse_args()
    if args.dataset in ("electric", "both"):
        benchmark_dataset("electric", args.sample, args.epochs)
    if args.dataset in ("covertype", "both"):
        benchmark_dataset("covertype", args.sample, args.epochs)


if __name__ == "__main__":
    main()
