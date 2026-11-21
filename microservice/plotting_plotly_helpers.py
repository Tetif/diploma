"""Pure helpers for Plotly bars without importing matplotlib (Streamlit must not pull in pyplot)."""
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


def _trend_colors_for_methods():
    """Same colors as the lines in plot_results_enhanced."""
    return {
        "Baseline": "#000000",
        "LOO": "#2ecc71",
        "Banzhaf": "#1f77b4",
        "TMCShapley": "#ff7f0e",
        "DataShapley": "#3498db",
        "BetaShapley": "#e74c3c",
        "Influence": "#9b59b6",
        "ArnoldiInfluence": "#d62728",
        "CgInfluence": "#9467bd",
        "LissaInfluence": "#8c564b",
        "NystroemSketchInfluence": "#e377c2",
        "CatBoostInfluence": "#17becf",
        "LossHigh": "#2e7d32",
        "LossLow": "#1565C0",
        "random": "#f39c12",
    }


def _resolve_method_color(method: str, color_map: dict, default: str = "#7f7f7f") -> str:
    """Color by method name; strategy suffixes (_lowest, ...) -> color of the base method."""
    if method in color_map:
        return color_map[method]
    suffixes = (
        "_lowest",
        "_highest",
        "_extremes",
        "_median",
        "_few_bad_rand",
        "_few_median_rand",
        "_few_good_rand",
    )
    for suffix in suffixes:
        if method.endswith(suffix):
            base = method[: -len(suffix)]
            return color_map.get(base, default)
    return default


def _pct_vs_best(values, higher_is_better: bool):
    """Deviation of each value from the best in the group, in %."""
    vals = [float(x) for x in values]
    n = len(vals)
    if n == 0:
        return []
    if higher_is_better:
        best = max(vals)
    else:
        best = min(vals)
    denom = abs(best)
    if denom < 1e-15 or not np.isfinite(best):
        return [None] * n
    out = []
    for v in vals:
        if not np.isfinite(v):
            out.append(None)
        else:
            out.append(100.0 * (v - best) / denom)
    return out


def _should_show_pct_vs_best(d: Optional[float]) -> bool:
    """The best bar has a 0% deviation, so the second line with the percentage is not shown."""
    if d is None:
        return False
    return abs(float(d)) > 1e-3


def _percent_to_metric_map(pts: Any) -> Dict[int, Optional[float]]:
    d: Dict[int, Optional[float]] = {}
    for pt in pts or []:
        pct = int(pt.get("percent", 0))
        v = pt.get("metric")
        if v is None:
            v = pt.get("mae")
        try:
            if v is None:
                fv = None
            else:
                fv = float(v)
                if not np.isfinite(fv):
                    fv = None
        except (TypeError, ValueError):
            fv = None
        d[pct] = fv
    return d


def mean_pct_abs_diff_from_pointwise_best(
    removal_data: Dict[str, Any],
    methods: List[str],
    higher_is_better: bool,
) -> Tuple[Dict[str, float], int]:
    """
    At each removal percentage where all selected curves have a value:
    the reference is the best among them (max if higher is better, min if lower is better).
    For each curve: |v-ref|/|ref|*100%, then the mean over those points.
    """
    if not methods:
        return {}, 0

    per_m = {m: _percent_to_metric_map(removal_data.get(m)) for m in methods}

    common: Optional[set] = None
    for m in methods:
        s = {
            p
            for p, val in per_m[m].items()
            if val is not None and np.isfinite(float(val))
        }
        common = s if common is None else common & s
    if not common:
        return {}, 0

    sums = {m: 0.0 for m in methods}
    n_pts = 0

    for p in sorted(common):
        vals: List[float] = []
        skip = False
        for m in methods:
            v = per_m[m].get(p)
            if v is None or not np.isfinite(float(v)):
                skip = True
                break
            vals.append(float(v))
        if skip:
            continue
        ref = float(max(vals)) if higher_is_better else float(min(vals))
        denom = abs(ref) + max(1e-12, 1e-9 * max(abs(ref), 1.0))
        n_pts += 1
        for i, m in enumerate(methods):
            sums[m] += 100.0 * abs(vals[i] - ref) / denom

    if n_pts == 0:
        return {}, 0
    return {m: sums[m] / n_pts for m in methods}, n_pts


def removal_curve_rank_scores(aucs, metric_name, metric_metadata):
    """
    A common scale for comparison: higher rank_score = better curve.
    For higher-is-better metrics rank_score = AUC; for MAE/RMSE rank_score = -AUC.
    """
    meta = (metric_metadata or {}).get(metric_name) or {}
    higher = meta.get("higher_is_better", True)
    ranked = {}
    for m, auc in aucs.items():
        if auc is None or (isinstance(auc, float) and not np.isfinite(auc)):
            ranked[m] = float("nan")
        elif higher:
            ranked[m] = float(auc)
        else:
            ranked[m] = float(-auc)
    return ranked
