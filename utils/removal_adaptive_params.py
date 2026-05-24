"""Подбор model_params для шага removal при включённом removal_adaptive_model."""
from __future__ import annotations

import copy
import math
from typing import Any, Dict, Optional

import numpy as np


def _binary_pos_weight(y_sub: Any) -> float:
    y_arr = np.asarray(y_sub.values if hasattr(y_sub, "values") else y_sub).ravel()
    n_pos = max(int((y_arr == 1).sum()), 1)
    n_neg = int((y_arr == 0).sum())
    return float(n_neg / n_pos)


def _scale_int(val: Any, factor: float, minimum: int = 1) -> Any:
    if val is None:
        return None
    try:
        iv = int(val)
    except (TypeError, ValueError):
        return val
    if iv <= 0:
        return val
    return max(minimum, int(round(iv * factor)))


def _adjust_nhead_for_d_model(d_model: int, nhead: int) -> int:
    """MultiheadAttention требует d_model % nhead == 0."""
    d_model = int(d_model)
    nhead = max(1, min(int(nhead), d_model))
    while d_model % nhead != 0 and nhead > 1:
        nhead -= 1
    return nhead


def _scale_pytorch_capacity(out: Dict[str, Any], factor: float, min_layer_width: int) -> None:
    """
    Снижает ёмкость активной PyTorch-архитектуры при меньшем train.
    Раньше для regression + model_architecture=simple почти нечего было менять
    (переключение на simple только при keep_ratio < 0.5), из‑за чего кривые совпадали.
    """
    arch = out.get("model_architecture", "simple")
    acfg = out.get(arch)
    if not isinstance(acfg, dict):
        return

    if arch in ("simple", "improved"):
        layers = acfg.get("layers")
        if isinstance(layers, (list, tuple)) and layers:
            scaled = [_scale_int(w, factor, minimum=min_layer_width) for w in layers]
            acfg["layers"] = scaled

    elif arch in ("ft_transformer", "ft_transformer_simple"):
        if "d_model" in acfg:
            acfg["d_model"] = _scale_int(acfg["d_model"], factor, minimum=8)
        dm = int(acfg.get("d_model", 8))
        if "nhead" in acfg:
            acfg["nhead"] = _adjust_nhead_for_d_model(dm, acfg["nhead"])
        if "dim_feedforward" in acfg:
            acfg["dim_feedforward"] = _scale_int(acfg["dim_feedforward"], factor, minimum=16)
        if "num_layers" in acfg:
            acfg["num_layers"] = max(1, _scale_int(acfg["num_layers"], factor, minimum=1))


def model_params_for_removal_subset(
    base_params: Dict[str, Any],
    n_train_full: int,
    n_sub: int,
    y_sub: Any,
    adaptive: bool,
    cfg: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Возвращает model_params для обучения на подвыборке после removal.

    Если adaptive=False — возвращает тот же объект base_params (без копии).
    Если adaptive=True — deepcopy и правки ёмкости / pos_weight для подвыборки.
    """
    if not adaptive:
        return base_params

    if cfg is None:
        from config.settings import REMOVAL_ADAPTIVE_CONFIG

        cfg = REMOVAL_ADAPTIVE_CONFIG

    out = copy.deepcopy(base_params)
    if n_train_full <= 0:
        return out

    keep_ratio = float(n_sub) / float(n_train_full)
    keep_ratio = min(1.0, max(0.0, keep_ratio))

    thr = float(cfg.get("keep_ratio_threshold", 0.5))
    min_scale = float(cfg.get("min_scale", 0.3))
    factor = max(min_scale, math.sqrt(keep_ratio))

    model_type = out.get("model_type", "pytorch")

    if out.get("use_distillation") and keep_ratio < thr:
        out["student_architecture"] = "simple"

    if model_type == "pytorch":
        arch = out.get("model_architecture", "simple")
        if keep_ratio < thr and arch not in ("simple",):
            if "simple" in out and isinstance(out.get("simple"), dict):
                out["model_architecture"] = "simple"

        min_layer = int(cfg.get("pytorch_min_layer_width", 4))
        if keep_ratio < 1.0:
            _scale_pytorch_capacity(out, factor, min_layer_width=min_layer)

        task_type = out.get("task_type", "regression")
        if task_type == "binary_classification":
            out["pos_weight"] = _binary_pos_weight(y_sub)

    elif model_type in ("lightgbm", "xgboost", "catboost", "random_forest"):
        if "num_leaves" in out:
            out["num_leaves"] = _scale_int(out["num_leaves"], factor, minimum=8)
        if "max_depth" in out:
            md = out["max_depth"]
            if md is not None and md != -1:
                try:
                    if int(md) > 0:
                        out["max_depth"] = _scale_int(md, factor, minimum=2)
                except (TypeError, ValueError):
                    pass
        # CatBoost: глубина задаётся ключом depth, не max_depth
        if model_type == "catboost" and "depth" in out:
            try:
                d = int(out["depth"])
                if d > 0:
                    out["depth"] = _scale_int(d, factor, minimum=2)
            except (TypeError, ValueError):
                pass
        if "n_estimators" in out:
            out["n_estimators"] = _scale_int(out["n_estimators"], factor, minimum=10)
        if "iterations" in out:
            out["iterations"] = _scale_int(out["iterations"], factor, minimum=10)

    return out
