#!/usr/bin/env python3
"""Compare experiment baseline metrics vs naive mean/majority/random and simple linear models."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from config import DatasetRegistry  # noqa: E402
from data.loader import DataLoaderFactory  # noqa: E402
from utils.helpers import sample_data, split_data  # noqa: E402
import config.settings as settings  # noqa: E402

REPRESENTATIVE = {
    "wine": ("02-53-21", 100),
    "housing": ("03-12-15", 100),
    "adult": ("03-26-40", 100),
    "zillow_15": ("03-34-04", 15),
    "zillow_100": ("03-37-42", 100),
    "electric": ("08-07-06", 10),
    "imdb": ("08-19-17", 10),
    "covertype": ("07-59-16", 10),
    "mnist": ("08-24-11", 10),
    "cifar10": ("08-32-59", 10),
}


def parse_model_block(text: str) -> dict:
    m = {}
    for key in (
        "baseline_metric",
        "best_validation_metric",
        "best_epoch",
        "metric_name",
        "model_type",
        "total_training_epochs",
        "used_distillation",
    ):
        r = re.search(rf"{key}\s+(\S+)", text)
        if r:
            m[key] = r.group(1)
    return m


def _load_splits(dataset_name: str, sample_pct: float):
    """Same split logic as experiment_service (holdout val = metric set)."""
    rs = settings.RANDOM_STATE
    cfg = DatasetRegistry.get(dataset_name)
    X, y, cfg = DataLoaderFactory.load_dataset(cfg)

    val_sz = float(settings.EXPERIMENT_CONFIG.get("val_size", 0.1))
    X_temp, X_holdout, y_temp, y_holdout = split_data(
        X,
        y,
        test_size=val_sz,
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
    test_sz = float(settings.EXPERIMENT_CONFIG.get("test_size", 0.2))
    X_train, X_test, y_train, y_test = split_data(
        X_sample,
        y_sample,
        test_size=test_sz,
        random_state=rs,
        stratify=y_sample if cfg.stratify else None,
        time_series=cfg.use_time_split,
    )
    return cfg, X_train, X_test, y_train, y_test, X_holdout, y_holdout


def naive_baselines(dataset_name: str, sample_pct: float) -> dict:
    cfg, X_train, X_test, y_train, y_test, X_val, y_val = _load_splits(
        dataset_name, sample_pct
    )
    y_train = np.asarray(y_train).ravel()
    y_val = np.asarray(y_val).ravel()

    task = cfg.task_type
    out: dict = {
        "task": task,
        "n_train": len(y_train),
        "n_val": len(y_val),
    }

    if task == "regression":
        out["metric"] = "mae"
        mean_train = float(np.mean(y_train))
        out["naive_mean_mae"] = float(
            mean_absolute_error(y_val, np.full_like(y_val, mean_train))
        )
        Xt = X_train.toarray() if hasattr(X_train, "toarray") else np.asarray(X_train)
        Xv = X_val.toarray() if hasattr(X_val, "toarray") else np.asarray(X_val)
        if Xt.ndim == 2 and Xt.shape[1] <= 8000:
            sc = StandardScaler()
            ridge = Ridge(alpha=1.0)
            ridge.fit(sc.fit_transform(Xt), y_train)
            out["linear_mae"] = float(
                mean_absolute_error(y_val, ridge.predict(sc.transform(Xv)))
            )
    elif task == "binary_classification":
        out["metric"] = "f1"
        out["pos_rate"] = float(np.mean(y_train))
        maj = int(round(out["pos_rate"]))
        out["naive_majority_f1"] = float(
            f1_score(y_val, np.full_like(y_val, maj), zero_division=0)
        )
        rng = np.random.RandomState(42)
        out["naive_random_f1"] = float(
            f1_score(y_val, rng.randint(0, 2, len(y_val)), zero_division=0)
        )
        Xt = X_train.toarray() if hasattr(X_train, "toarray") else np.asarray(X_train)
        Xv = X_val.toarray() if hasattr(X_val, "toarray") else np.asarray(X_val)
        if Xt.ndim == 2:
            sc = StandardScaler(with_mean=False)
            lr = LogisticRegression(max_iter=500, n_jobs=1)
            lr.fit(sc.fit_transform(Xt), y_train)
            out["linear_f1"] = float(
                f1_score(y_val, lr.predict(sc.transform(Xv)), zero_division=0)
            )
    else:
        out["metric"] = "accuracy"
        classes, counts = np.unique(y_train, return_counts=True)
        maj = classes[counts.argmax()]
        out["n_classes"] = int(len(classes))
        out["naive_majority_acc"] = float(
            accuracy_score(y_val, np.full_like(y_val, maj))
        )
        out["naive_random_acc"] = 1.0 / out["n_classes"]
        rng = np.random.RandomState(42)
        out["naive_random_sample_acc"] = float(
            accuracy_score(y_val, rng.choice(classes, len(y_val)))
        )
        Xt = X_train.toarray() if hasattr(X_train, "toarray") else np.asarray(X_train)
        Xv = X_val.toarray() if hasattr(X_val, "toarray") else np.asarray(X_val)
        if Xt.ndim == 2 and Xt.shape[1] <= 8000:
            sc = StandardScaler(with_mean=False)
            lr = LogisticRegression(max_iter=500, n_jobs=1)
            lr.fit(sc.fit_transform(Xt), y_train)
            out["linear_acc"] = float(
                accuracy_score(y_val, lr.predict(sc.transform(Xv)))
            )

    return out


def judge(model: dict, naive: dict) -> list[str]:
    flags = []
    bm = float(model.get("baseline_metric", "nan"))
    task = naive["task"]

    if task == "regression":
        nm = naive.get("naive_mean_mae")
        if nm and bm > nm * 1.05:
            flags.append("хуже предсказания средним (naive mean)")
        lin = naive.get("linear_mae")
        if lin and bm > lin * 1.1:
            flags.append("хуже простой Ridge-регрессии")
        if bm > nm * 2:
            flags.append("сильно не обучилась (MAE >> mean)")
    elif task == "binary_classification":
        maj = naive.get("naive_majority_f1", 0)
        rnd = naive.get("naive_random_f1", 0)
        if bm < maj - 0.02:
            flags.append("хуже majority-class F1")
        if bm < rnd - 0.03:
            flags.append("хуже случайных меток F1")
        lin = naive.get("linear_f1")
        if lin and bm < lin - 0.05:
            flags.append("хуже LogisticRegression")
        if bm < 0.1 and naive.get("pos_rate", 0.5) > 0.2:
            flags.append("F1 почти ноль при обучаемом балансе")
    else:
        rnd = naive.get("naive_random_acc", 0)
        maj = naive.get("naive_majority_acc", 0)
        if bm < rnd + 0.01:
            flags.append("на уровне или ниже random accuracy")
        if bm < maj - 0.02:
            flags.append("хуже majority-class accuracy")
        lin = naive.get("linear_acc")
        if lin and bm < lin - 0.05:
            flags.append("хуже линейной многоклассовой модели")
        if naive.get("n_classes") == 10 and bm < 0.15:
            flags.append("accuracy <15% при 10 классах (близко к random 10%)")

    ep = model.get("best_epoch", "0")
    total = model.get("total_training_epochs", "?")
    if ep == "0" and str(total) not in ("0", "1", "?"):
        flags.append("best_epoch=0 — подозрение на сбой обучения")

    return flags


def main() -> None:
    log_dir = REPO / "experiment_logs" / "2026-05-19"
    print("BASELINE SANITY CHECK (test metric from experiment vs naive/linear)\n")

    for label, (subdir, sample_pct) in REPRESENTATIVE.items():
        ds_name = label.replace("_15", "").replace("_100", "")
        if label == "zillow_15":
            ds_name = "zillow"
        elif label == "zillow_100":
            ds_name = "zillow"

        summary_path = log_dir / subdir / "experiment_summary.txt"
        if not summary_path.is_file():
            print(f"[SKIP] {label}: no summary")
            continue

        model = parse_model_block(summary_path.read_text(encoding="utf-8", errors="replace"))
        try:
            naive = naive_baselines(ds_name, sample_pct)
        except Exception as exc:
            print(f"[ERR] {label}: {exc}")
            continue

        flags = judge(model, naive)
        status = "ПЛОХО" if flags else "OK"

        print(f"## {label} ({ds_name}, sample={sample_pct}%, {model.get('model_type', '?')})")
        print(f"   log: experiment_logs/2026-05-19/{subdir}")
        print(f"   test {model.get('metric_name')} = {model.get('baseline_metric')}")
        print(f"   val best = {model.get('best_validation_metric')} @ epoch {model.get('best_epoch')}/{model.get('total_training_epochs')}")
        print(f"   train n = {naive.get('n_train')} | holdout val n = {naive.get('n_val')}")

        if naive["task"] == "regression":
            print(f"   naive mean MAE = {naive.get('naive_mean_mae'):.6g}", end="")
            if "linear_mae" in naive:
                print(f" | Ridge MAE = {naive['linear_mae']:.6g}")
            else:
                print()
        elif naive["task"] == "binary_classification":
            print(
                f"   naive majority F1 = {naive.get('naive_majority_f1', 0):.4f} | "
                f"random F1 ~ {naive.get('naive_random_f1', 0):.4f} | pos_rate = {naive.get('pos_rate', 0):.3f}"
            )
            if "linear_f1" in naive:
                print(f"   LogReg F1 = {naive['linear_f1']:.4f}")
        else:
            print(
                f"   naive majority acc = {naive.get('naive_majority_acc', 0):.4f} | "
                f"random acc = {naive.get('naive_random_acc', 0):.4f} ({naive.get('n_classes')} classes)"
            )
            if "linear_acc" in naive:
                print(f"   LogReg acc = {naive['linear_acc']:.4f}")

        print(f"   >>> {status}: {', '.join(flags) if flags else 'модель лучше наивных порогов'}")
        print()


if __name__ == "__main__":
    main()
