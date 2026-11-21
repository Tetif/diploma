"""Removal strategies: how to order/select training points to remove (global, per class, per y-strata)."""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional

from config import settings as settings_module



CLASSIFICATION_TASKS = ('binary_classification', 'multiclass_classification')


def target_strata_labels(y_train, n_bins: int) -> Optional[np.ndarray]:
    """
    Quantile strata of the target (regression): ~equal frequencies over y, labels 0..k-1.
    None if it cannot be split (global removal without strata).
    """
    y_arr = np.asarray(
        y_train.values if hasattr(y_train, "values") else y_train,
        dtype=float,
    ).ravel()
    n = int(y_arr.size)
    if n < 4:
        return None
    nb = max(2, min(int(n_bins), n // 2))
    try:
        q = pd.qcut(
            pd.Series(y_arr),
            q=nb,
            labels=False,
            duplicates="drop",
        )
    except (ValueError, TypeError):
        return None
    arr = np.asarray(q, dtype=float)
    if np.isnan(arr).any():
        arr = np.nan_to_num(arr, nan=0.0)
    arr = arr.astype(int)
    if np.unique(arr).size < 2:
        return None
    return arr


def _allocate_proportional_n_per_class(y_arr: np.ndarray, n_to_remove: int) -> Dict[int, int]:
    """
    Distribute n_to_remove over the classes proportionally to their frequencies, capped at (count_c - 1) per class.
    """
    unique, counts = np.unique(y_arr, return_counts=True)
    n = len(y_arr)
    k = len(unique)
    if n_to_remove <= 0 or n == 0 or k == 0:
        return {}
    max_r = counts - 1
    raw = np.array([n_to_remove * int(c) / n for c in counts], dtype=float)
    floor = np.floor(raw).astype(int)
    floor = np.minimum(floor, max_r)
    short = int(n_to_remove - floor.sum())
    if short > 0:
        frac = raw - np.floor(raw)
        order = np.argsort(-frac)
        i = 0
        guard = 0
        while short > 0 and guard < k * (n + 5):
            j = int(order[i % k])
            if floor[j] < max_r[j]:
                floor[j] += 1
                short -= 1
            i += 1
            guard += 1
    elif short < 0:
        order = np.argsort(raw)
        i = 0
        guard = 0
        while short < 0 and guard < k * (n + 5):
            j = int(order[i % k])
            if floor[j] > 0:
                floor[j] -= 1
                short += 1
            i += 1
            guard += 1
    return {int(unique[i]): int(floor[i]) for i in range(k)}


def build_full_candidate_order_influence(
    asc_sorted: np.ndarray,
    strategy: str,
    n_train: int,
    n_to_remove: int,
    pct: int,
    fixed_frac: float = 0.1,
    seed_extra: int = 0,
    all_indices_scope: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    asc_sorted - global train indices sorted by ascending score.
    n_train = len(asc_sorted). For the few_* strategies all_indices_scope holds indices of the same set (global).
    """
    if all_indices_scope is None:
        all_indices_scope = np.arange(n_train)
    idx_sorted = asc_sorted
    if strategy == 'highest':
        idx_sorted = asc_sorted[::-1]
    elif strategy == 'few_good_then_random':
        idx_sorted = asc_sorted[::-1]

    if strategy in ('lowest', 'highest'):
        candidate_order_base = idx_sorted
    elif strategy == 'extremes':
        left, right = 0, len(idx_sorted) - 1
        order = []
        while left <= right:
            order.append(idx_sorted[left])
            left += 1
            if left <= right:
                order.append(idx_sorted[right])
                right -= 1
        candidate_order_base = np.asarray(order, dtype=int)
    elif strategy == 'median':
        n_sorted = len(idx_sorted)
        mid = n_sorted // 2
        positions = []
        left = mid
        right = mid + 1
        if 0 <= left < n_sorted:
            positions.append(left)
        while len(positions) < n_sorted:
            if right < n_sorted:
                positions.append(right)
                right += 1
            left -= 1
            if 0 <= left < n_sorted and len(positions) < n_sorted:
                positions.append(left)
        candidate_order_base = idx_sorted[positions]
    else:
        candidate_order_base = None

    if candidate_order_base is not None:
        return candidate_order_base

    n_total = n_to_remove
    if strategy == 'few_bad_then_random':
        n_fixed = min(int(fixed_frac * n_train), n_total)
        if n_fixed <= 0:
            n_fixed = min(1, n_total)
        det_idx = idx_sorted[:n_fixed]
        remaining = np.setdiff1d(all_indices_scope, det_idx, assume_unique=True)
        np.random.seed(settings_module.RANDOM_STATE + pct + seed_extra)
        rand_order = np.random.permutation(remaining)
        return np.concatenate([det_idx, rand_order])
    if strategy == 'few_median_then_random':
        n_fixed = min(int(fixed_frac * n_train), n_total)
        if n_fixed <= 0:
            n_fixed = min(1, n_total)
        n_train_sorted = len(idx_sorted)
        mid = n_train_sorted // 2
        half = n_fixed // 2
        start = max(0, mid - half)
        end = min(n_train_sorted, start + n_fixed)
        if end - start < n_fixed:
            if start == 0:
                end = n_fixed
            else:
                start = end - n_fixed
        det_idx = idx_sorted[start:end]
        remaining = np.setdiff1d(all_indices_scope, det_idx, assume_unique=True)
        np.random.seed(settings_module.RANDOM_STATE + pct + 1000 + seed_extra)
        rand_order = np.random.permutation(remaining)
        return np.concatenate([det_idx, rand_order])
    if strategy == 'few_good_then_random':
        n_fixed = min(int(fixed_frac * n_train), n_total)
        if n_fixed <= 0:
            n_fixed = min(1, n_total)
        det_idx = idx_sorted[:n_fixed]
        remaining = np.setdiff1d(all_indices_scope, det_idx, assume_unique=True)
        np.random.seed(settings_module.RANDOM_STATE + pct + 2000 + seed_extra)
        rand_order = np.random.permutation(remaining)
        return np.concatenate([det_idx, rand_order])
    return np.array([], dtype=int)


def removal_indices_per_class_influence(
    vals: np.ndarray,
    y_train,
    strategy: str,
    n_to_remove: int,
    pct: int,
    seed_extra: int = 0,
) -> np.ndarray:
    vals = np.asarray(vals).ravel()
    y_arr = np.asarray(y_train.values if hasattr(y_train, "values") else y_train).ravel()
    alloc = _allocate_proportional_n_per_class(y_arr, n_to_remove)
    removed: List[int] = []
    for cls in np.unique(y_arr):
        n_c = int(alloc.get(int(cls), 0))
        if n_c <= 0:
            continue
        idx_local = np.where(y_arr == cls)[0]
        m = len(idx_local)
        asc_c = idx_local[np.argsort(vals[idx_local])]
        co = build_full_candidate_order_influence(
            asc_c,
            strategy,
            m,
            n_c,
            pct,
            seed_extra=int(seed_extra) + int(cls) * 17,
            all_indices_scope=idx_local,
        )
        take = co[: min(n_c, len(co))]
        removed.extend(int(i) for i in take.tolist())
    return np.asarray(removed, dtype=int)


def removal_indices_per_class_random(y_train, n_to_remove: int, run_idx: int) -> np.ndarray:
    y_arr = np.asarray(y_train.values if hasattr(y_train, "values") else y_train).ravel()
    alloc = _allocate_proportional_n_per_class(y_arr, n_to_remove)
    removed: List[int] = []
    for cls in np.unique(y_arr):
        n_c = int(alloc.get(int(cls), 0))
        if n_c <= 0:
            continue
        idx_local = np.where(y_arr == cls)[0]
        np.random.seed(settings_module.RANDOM_STATE + run_idx + int(cls) * 31)
        perm = np.random.permutation(idx_local)
        take = perm[: min(n_c, len(perm))]
        removed.extend(int(i) for i in take.tolist())
    return np.asarray(removed, dtype=int)


def removal_indices_per_class_valuation(
    vals: np.ndarray,
    y_train,
    n_to_remove: int,
    scorer_higher_is_better: bool,
    *,
    remove_smallest_first: Optional[bool] = None,
) -> np.ndarray:
    """
    Removal by shares within groups (class / stratum). Order within a group:
    - remove_smallest_first is None: as for valuation - smallest values first
      if scorer_higher_is_better, otherwise largest.
    - remove_smallest_first True / False: explicit (for LossLow / LossHigh on the per-sample loss).
    """
    vals = np.asarray(vals).ravel()
    y_arr = np.asarray(y_train.values if hasattr(y_train, "values") else y_train).ravel()
    alloc = _allocate_proportional_n_per_class(y_arr, n_to_remove)
    removed: List[int] = []
    for cls in np.unique(y_arr):
        n_c = int(alloc.get(int(cls), 0))
        if n_c <= 0:
            continue
        idx_local = np.where(y_arr == cls)[0]
        sub = idx_local[np.argsort(vals[idx_local])]
        if remove_smallest_first is None:
            order = sub if scorer_higher_is_better else sub[::-1]
        else:
            order = sub if remove_smallest_first else sub[::-1]
        take = order[: min(n_c, len(order))]
        removed.extend(int(i) for i in take.tolist())
    return np.asarray(removed, dtype=int)
