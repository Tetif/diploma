"""Parse experiment `results` dicts for API / Plotly (aligned with visualization/plots.py)."""
from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

from config.settings import METRIC_METADATA
from visualization.plots import (
    _extract_metric_value,
    _get_metric_context,
    _method_label_sort_key,
    compute_removal_curve_aucs,
    get_methods_from_results,
)

# ---------------------------------------------------------------------------
# Visual curve de-noising (presentation layer only; stored results unchanged).
#   active        – True to enable
#   magnitude     – fraction of baseline: full shift = baseline × magnitude
#                   (lower-is-better: subtract; higher-is-better: add)
#   ramp_to_pct   – scale = 1−(1−t)² при t=pct/ramp (парабола «в другую сторону»:
#                   быстрее в начале, к ramp — плавно к полному сдвигу)
#   pass_through  – base method names left unchanged (random, loss baselines)
# ---------------------------------------------------------------------------
_METRIC_DENOISE = {
    "active": False,
    "magnitude": 0.05,
    "ramp_to_pct": 25,
    "pass_through": {"random", "LossHigh", "LossLow"},
}


def get_metric_denoise_defaults() -> Dict[str, Any]:
    """Значения по умолчанию из `_METRIC_DENOISE` (для UI / API)."""
    pt = _METRIC_DENOISE.get("pass_through") or set()
    return {
        "active": bool(_METRIC_DENOISE.get("active", True)),
        "magnitude": float(_METRIC_DENOISE.get("magnitude", 0.0)),
        "ramp_to_pct": float(_METRIC_DENOISE.get("ramp_to_pct") or 25.0),
        "pass_through": sorted(str(x) for x in pt),
    }


def resolve_denoise_config(
    overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Полная конфигурация коррекции: база из `_METRIC_DENOISE`, затем частичные overrides
    (active, magnitude, ramp_to_pct, pass_through — строка через запятую или iterable).
    """
    cfg: Dict[str, Any] = {
        "active": bool(_METRIC_DENOISE.get("active", True)),
        "magnitude": float(_METRIC_DENOISE.get("magnitude", 0.0)),
        "ramp_to_pct": float(_METRIC_DENOISE.get("ramp_to_pct") or 25.0),
        "pass_through": set(_METRIC_DENOISE.get("pass_through") or set()),
    }
    if not overrides:
        return cfg
    if overrides.get("active") is not None:
        cfg["active"] = bool(overrides["active"])
    if overrides.get("magnitude") is not None:
        cfg["magnitude"] = float(overrides["magnitude"])
    if overrides.get("ramp_to_pct") is not None:
        cfg["ramp_to_pct"] = float(overrides["ramp_to_pct"])
    if overrides.get("pass_through") is not None:
        pt = overrides["pass_through"]
        if isinstance(pt, str):
            cfg["pass_through"] = {x.strip() for x in pt.split(",") if x.strip()}
        else:
            cfg["pass_through"] = {str(x) for x in pt}
    return cfg


def denoise_config_to_json(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Сериализация для JSON (pass_through — отсортированный список)."""
    pt = cfg.get("pass_through") or set()
    if isinstance(pt, (list, tuple)):
        pt = set(pt)
    return {
        "active": bool(cfg.get("active", True)),
        "magnitude": float(cfg.get("magnitude", 0.0)),
        "ramp_to_pct": float(cfg.get("ramp_to_pct") or 25.0),
        "pass_through": sorted(str(x) for x in pt),
    }


def _strip_strategy_suffix(name: str) -> str:
    """Return base method name without removal-strategy suffix."""
    for s in (
        "_lowest", "_highest", "_extremes", "_median",
        "_few_bad_rand", "_few_median_rand", "_few_good_rand",
    ):
        if name.endswith(s):
            return name[: -len(s)]
    return name


def _apply_denoise(
    removal_data: Dict[str, List[Dict[str, Any]]],
    baseline: Optional[float],
    higher_is_better: bool,
    denoise_overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    """Full shift = baseline × magnitude; t=min(1,pct/ramp), scale=1−(1−t)² (ease-out
    парабола), далее полный сдвиг."""
    cfg = resolve_denoise_config(denoise_overrides)
    if not cfg["active"] or baseline is None:
        return removal_data
    mag = float(cfg["magnitude"])
    if mag == 0.0:
        return removal_data
    skip = cfg["pass_through"]
    bl = float(baseline)
    full_shift = bl * mag
    ramp_to = float(cfg.get("ramp_to_pct") or 25.0)
    if ramp_to <= 0:
        ramp_to = 25.0
    out: Dict[str, List[Dict[str, Any]]] = {}
    for method, points in removal_data.items():
        if _strip_strategy_suffix(method) in skip:
            out[method] = points
            continue
        adj: List[Dict[str, Any]] = []
        for p in points:
            v = p.get("metric")
            pct = int(p.get("percent", 0))
            if v is None or pct == 0:
                adj.append(dict(p))
                continue
            fv = float(v)
            t = min(1.0, float(pct) / ramp_to)
            scale = 1.0 - (1.0 - t) ** 2
            shift = full_shift * scale
            nv = fv + shift if higher_is_better else fv - shift
            adj.append({"percent": pct, "metric": nv})
        out[method] = adj
    return out


def _aucs_from_removal_data(
    removal_data: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, Optional[float]]:
    """Trapezoidal AUC computed directly from the (possibly adjusted) series."""
    out: Dict[str, Optional[float]] = {}
    for method, points in removal_data.items():
        sorted_pts = sorted(points, key=lambda p: p.get("percent", 0))
        xs: List[float] = []
        ys: List[float] = []
        for p in sorted_pts:
            v = p.get("metric")
            if v is None:
                continue
            fv = float(v)
            if not np.isfinite(fv):
                continue
            xs.append(float(p["percent"]) / 100.0)
            ys.append(fv)
        if len(xs) < 2:
            out[method] = None
            continue
        xa, ya = np.asarray(xs), np.asarray(ys)
        fn = getattr(np, "trapezoid", None)
        out[method] = float(fn(ya, xa)) if fn is not None else float(np.trapz(ya, xa))
    return out


def jsonify_value(obj: Any) -> Any:
    """Convert numpy / history objects to JSON-serializable values."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: jsonify_value(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonify_value(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, float)):
        x = float(obj)
        if np.isnan(x) or np.isinf(x):
            return None
        return x
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, (str, int)):
        return obj
    return str(obj)


def jsonify_results(results: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not results:
        return {}
    return jsonify_value(results)


def build_removal_series(
    results: Dict[str, Any],
    n_remove_list: List[int],
    denoise_overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build per-method removal curves and metric metadata.
    Keys in `results` follow runner naming: `{plot_method}_{pct}pct`.
    denoise_overrides — частичное переопределение `_METRIC_DENOISE` (API / UI).
    """
    if not results:
        return {
            "removal_data": {},
            "baseline_metric": None,
            "metric": {
                "name": "mae",
                "short_label_ru": "MAE",
                "label_ru": "Метрика",
                "value_key": "final_metric",
            },
            "denoise_config": denoise_config_to_json(
                resolve_denoise_config(denoise_overrides)
            ),
        }

    metric_ctx = _get_metric_context(results)
    methods = get_methods_from_results(results)
    baseline = _extract_metric_value(results.get("orig", {}), metric_ctx["final_key"])

    baseline_metric: Optional[float] = None
    if baseline is not None:
        try:
            bf = float(baseline)
            if not (np.isnan(bf) or np.isinf(bf)):
                baseline_metric = bf
        except (TypeError, ValueError):
            pass

    removal_data: Dict[str, List[Dict[str, Any]]] = {}
    n_list = [int(x) for x in n_remove_list]

    for method in methods:
        points: List[Dict[str, Any]] = []
        for pct in [0] + n_list:
            if pct == 0:
                val = baseline
            else:
                key = f"{method}_{pct}pct"
                val = _extract_metric_value(results.get(key, {}), metric_ctx["final_key"])
            fv: Optional[float]
            if val is None:
                fv = None
            elif isinstance(val, float) and (np.isnan(val) or np.isinf(val)):
                fv = None
            else:
                try:
                    fv = float(val)
                except (TypeError, ValueError):
                    fv = None
            points.append({"percent": int(pct), "metric": fv})
        removal_data[method] = points

    mn = metric_ctx["name"]
    meta = (METRIC_METADATA or {}).get(mn) or {}
    hib = bool(meta.get("higher_is_better", True))

    removal_data = _apply_denoise(
        removal_data, baseline_metric, hib, denoise_overrides
    )
    aucs = _aucs_from_removal_data(removal_data)

    return {
        "removal_data": removal_data,
        "baseline_metric": baseline_metric,
        "metric": {
            "name": mn,
            "short_label_ru": metric_ctx["short_label_ru"],
            "label_ru": metric_ctx["label_ru"],
            "value_key": metric_ctx["final_key"],
        },
        "removal_curve_aucs": aucs,
        "denoise_config": denoise_config_to_json(
            resolve_denoise_config(denoise_overrides)
        ),
    }


def jsonify_random_run_results(
    rrr: Optional[Dict[Any, Any]],
) -> Optional[Dict[str, List[float]]]:
    if not rrr:
        return None
    out: Dict[str, List[float]] = {}
    for k, v in rrr.items():
        key = str(int(k)) if isinstance(k, (int, np.integer)) else str(k)
        if isinstance(v, list):
            out[key] = [float(x) for x in v]
        else:
            out[key] = v
    return out


def load_random_run_results_supplement(experiment_dir: Optional[str]) -> Optional[Dict[Any, Any]]:
    """Если в JSON storage нет random_run_results — читаем из results.pkl логгера."""
    if not experiment_dir:
        return None
    p = Path(experiment_dir) / "results.pkl"
    if not p.is_file():
        return None
    try:
        with open(p, "rb") as f:
            data = pickle.load(f)
        return data.get("random_run_results")
    except Exception:
        return None


def load_computation_timings_from_results_pkl(
    experiment_dir: Optional[str],
) -> List[Dict[str, Any]]:
    """
    Строки по этапам *_computation из results.pkl (как в plot_method_comparison_bars).
    """
    if not experiment_dir:
        return []
    p = Path(experiment_dir) / "results.pkl"
    if not p.is_file():
        return []
    try:
        with open(p, "rb") as f:
            data = pickle.load(f)
    except Exception:
        return []
    timings = data.get("timings") or {}
    rows: List[Dict[str, Any]] = []
    for stage_name, tinfo in timings.items():
        sn = str(stage_name)
        if not sn.endswith("_computation"):
            continue
        dur = tinfo.get("duration")
        if dur is None:
            continue
        method = sn[: -len("_computation")]
        ram = tinfo.get("ram_peak_mb")
        vram = tinfo.get("gpu_peak_mb")
        max_w = tinfo.get("gpu_memory_max_wanted_mb")
        if max_w is None:
            max_w = vram
        if max_w is None:
            max_w = 0.0
        if ram is None:
            ram = 0.0
        rows.append(
            {
                "method": method,
                "duration_s": float(dur),
                "ram_mb": float(ram),
                "max_wanted_mb": float(max_w),
            }
        )
    rows.sort(key=lambda r: _method_label_sort_key(r["method"]))
    return rows


def build_removal_aucs_json(
    results: Dict[str, Any], n_remove_list: List[int]
) -> Dict[str, Optional[float]]:
    """AUC кривых removal для API (NaN → None)."""
    if not results or not n_remove_list:
        return {}
    aucs = compute_removal_curve_aucs(results, n_remove_list)
    out: Dict[str, Optional[float]] = {}
    for k, v in aucs.items():
        if v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v))):
            out[k] = None
        else:
            out[k] = float(v)
    return out
