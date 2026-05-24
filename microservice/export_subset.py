"""Replay train split and export remaining rows after removal (aligned with ExperimentRunner)."""
from __future__ import annotations

from typing import Any, List, Optional, Tuple

import numpy as np
import pandas as pd

from config import DatasetRegistry
from data.loader import DataLoaderFactory
from experiments.logger import ExperimentLogger
from experiments.runner import (
    ExperimentRunner,
    removal_indices_per_class_influence,
    target_strata_labels,
)
from sklearn.preprocessing import LabelEncoder
from utils.helpers import sample_data, set_random_seeds, split_data


def _build_candidate_order_influence(
    strategy: str, vals: np.ndarray
) -> Optional[np.ndarray]:
    vals = np.asarray(vals).ravel()
    n_train = len(vals)
    all_indices = np.arange(n_train)
    idx_sorted = np.argsort(vals)

    if strategy == "lowest":
        return idx_sorted
    if strategy == "highest":
        return idx_sorted[::-1]
    if strategy == "extremes":
        left, right = 0, len(idx_sorted) - 1
        order = []
        while left <= right:
            order.append(idx_sorted[left])
            left += 1
            if left <= right:
                order.append(idx_sorted[right])
                right -= 1
        return np.asarray(order, dtype=int)
    if strategy == "median":
        n_sorted = len(idx_sorted)
        mid = n_sorted // 2
        positions = []
        left, right = mid, mid + 1
        if 0 <= left < n_sorted:
            positions.append(left)
        while len(positions) < n_sorted:
            if right < n_sorted:
                positions.append(right)
                right += 1
            left -= 1
            if 0 <= left < n_sorted and len(positions) < n_sorted:
                positions.append(left)
        return idx_sorted[positions]
    return None


def replay_train_split(
    *,
    dataset_name: str,
    random_state: int,
    test_size: float,
    val_size: float,
    sample_size_percentage: float,
    base_dir: str = "experiment_logs",
) -> Tuple[pd.DataFrame, pd.Series, Any]:
    """Тот же train-сплит, что в ExperimentRunner / export (порядок строк = порядок весов influence)."""
    set_random_seeds(random_state)

    dataset_config = DatasetRegistry.get(dataset_name)
    logger = ExperimentLogger(base_dir=base_dir)
    X, y, cfg = DataLoaderFactory.load_dataset(dataset_config, logger)

    if cfg.task_type in ("binary_classification", "multiclass_classification"):
        if y.dtype == "object":
            le = LabelEncoder()
            y = pd.Series(le.fit_transform(y), index=y.index)

    X_temp, _, y_temp, _ = split_data(
        X,
        y,
        test_size=val_size,
        random_state=random_state,
        stratify=y if cfg.stratify else None,
        time_series=cfg.use_time_split,
    )

    sample_pct = float(sample_size_percentage) / 100.0
    X_sample, y_sample = sample_data(
        X_temp,
        y_temp,
        sample_fraction=sample_pct,
        random_state=random_state,
        preserve_order=cfg.use_time_split,
    )

    X_train, _, y_train, _ = split_data(
        X_sample,
        y_sample,
        test_size=test_size,
        random_state=random_state,
        time_series=cfg.use_time_split,
    )
    return X_train, y_train, cfg


def get_train_targets_for_experiment_config(
    *,
    dataset_name: str,
    random_state: int,
    test_size: float,
    val_size: float,
    sample_size_percentage: float,
    base_dir: str = "experiment_logs",
    stratify_n_bins: Optional[int] = None,
) -> Tuple[List[int], str]:
    """
    Метки train в порядке строк, согласованном с весами influence.
    Классификация — метки классов; регрессия — квантильные страты по y (как removal_stratify_target).
    """
    _, y_train, cfg = replay_train_split(
        dataset_name=dataset_name,
        random_state=random_state,
        test_size=test_size,
        val_size=val_size,
        sample_size_percentage=sample_size_percentage,
        base_dir=base_dir,
    )
    if cfg.task_type in ("binary_classification", "multiclass_classification"):
        t = np.asarray(y_train).ravel()
        return [int(x) for x in t.tolist()], str(cfg.task_type)
    if cfg.task_type == "regression":
        nb = int(stratify_n_bins if stratify_n_bins is not None else 10)
        strata = target_strata_labels(y_train, nb)
        if strata is None:
            raise ValueError(
                "Для регрессии не удалось построить квантильные страты по y (мало данных?)."
            )
        return [int(x) for x in strata.tolist()], "regression"
    raise ValueError(
        f"Раскраска по таргету не поддерживается для task_type={cfg.task_type!r}."
    )


def export_train_subset_after_removal(
    *,
    dataset_name: str,
    random_state: int,
    test_size: float,
    val_size: float,
    sample_size_percentage: float,
    method: str,
    strategy: str,
    removal_percent: int,
    scores_raw: dict,
    base_dir: str = "experiment_logs",
    removal_per_class: bool = False,
    removal_stratify_target: bool = False,
    removal_stratify_n_bins: int = 10,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Reload data, reproduce splits, apply removal policy for one influence method.
    Supported strategies: lowest, highest, extremes, median (same as runner for PyTorch influence).
    """
    X_train, y_train, cfg = replay_train_split(
        dataset_name=dataset_name,
        random_state=random_state,
        test_size=test_size,
        val_size=val_size,
        sample_size_percentage=sample_size_percentage,
        base_dir=base_dir,
    )

    if method not in scores_raw:
        raise KeyError(f"No scores for method {method!r} in stored experiment")

    vals = np.asarray(scores_raw[method]).ravel()
    if len(vals) != len(X_train):
        raise ValueError(
            f"Score length {len(vals)} != train rows {len(X_train)}; cannot export."
        )

    n_train = len(X_train)
    n_to_remove = int(n_train * removal_percent / 100)
    n_to_remove = max(0, n_to_remove)
    n_to_remove = min(n_to_remove, max(0, n_train - 10))

    n_classes_expected = None
    if cfg.task_type in ("binary_classification", "multiclass_classification"):
        n_classes_expected = int(y_train.nunique())

    strata_labels = None
    if cfg.task_type == "regression" and bool(removal_stratify_target):
        strata_labels = target_strata_labels(y_train, int(removal_stratify_n_bins or 10))
        if strata_labels is not None and np.unique(strata_labels).size < 2:
            strata_labels = None

    rpc = bool(removal_per_class) and bool(n_classes_expected)
    if rpc:
        remove_idx = removal_indices_per_class_influence(
            vals,
            y_train,
            strategy,
            n_to_remove,
            int(removal_percent),
        )
    elif strata_labels is not None:
        remove_idx = removal_indices_per_class_influence(
            vals,
            strata_labels,
            strategy,
            n_to_remove,
            int(removal_percent),
        )
    else:
        candidate_order = _build_candidate_order_influence(strategy, vals)
        if candidate_order is None:
            raise ValueError(
                f"Strategy {strategy!r} is not supported for export (try lowest, highest, extremes, median)."
            )

        remove_idx = ExperimentRunner._select_indices_keep_one_per_class(
            candidate_order,
            y_train,
            n_to_remove,
            n_classes_expected=n_classes_expected,
            logger=None,
            context=f"export {method} {strategy} {removal_percent}%",
        )

    keep_mask = np.ones(n_train, dtype=bool)
    keep_mask[remove_idx] = False

    X_kept = X_train.loc[keep_mask].copy()
    y_kept = y_train.loc[keep_mask].copy()
    return X_kept, y_kept
