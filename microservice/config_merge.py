"""Merge API request with defaults from config.settings (same fields as ExperimentLogger snapshot)."""
from __future__ import annotations

import copy
import threading
from contextlib import contextmanager
from typing import Any, Dict, Optional

import config.settings as settings_module

VALUATION_METHOD_NAMES = frozenset(
    {
        "LOO",
        "DataShapley",
        "BetaShapley",
        "Banzhaf",
        "TMCShapley",
        "KNNShapley",
        "DataOOB",
        "LeastCore",
    }
)
INFLUENCE_METHOD_NAMES = frozenset(
    {
        "Influence",
        "ArnoldiInfluence",
        "CgInfluence",
        "LissaInfluence",
        "NystroemSketchInfluence",
    }
)

_EXPERIMENT_LOCK = threading.Lock()


def get_settings_snapshot() -> Dict[str, Any]:
    """JSON-serializable defaults aligned with experiments/logger.py _get_settings_snapshot."""
    return {
        "CURRENT_DATASET": settings_module.CURRENT_DATASET,
        "DEBUG_MODE": settings_module.DEBUG_MODE,
        "EXPERIMENTS_BASE_DIR": settings_module.EXPERIMENTS_BASE_DIR,
        "CACHE_DIR": settings_module.CACHE_DIR,
        "USE_CACHE": settings_module.USE_CACHE,
        "DEVICE": settings_module.DEVICE,
        "N_JOBS": settings_module.N_JOBS,
        "RANDOM_STATE": settings_module.RANDOM_STATE,
        "MODEL_FIT_MODE": settings_module.MODEL_FIT_MODE,
        "FIT_MODE_EPOCHS": copy.deepcopy(settings_module.FIT_MODE_EPOCHS),
        "MODEL_RUN_CONFIG": copy.deepcopy(settings_module.MODEL_RUN_CONFIG),
        "INFLUENCE_METHODS_CONFIG": copy.deepcopy(
            settings_module.INFLUENCE_METHODS_CONFIG
        ),
        "EXPERIMENT_CONFIG": copy.deepcopy(settings_module.EXPERIMENT_CONFIG),
        "REMOVAL_STRATEGIES": copy.deepcopy(settings_module.REMOVAL_STRATEGIES),
        "METRIC_CONFIG": copy.deepcopy(settings_module.METRIC_CONFIG),
        "METRIC_METADATA": copy.deepcopy(settings_module.METRIC_METADATA),
        "PYDVL_CONFIG": copy.deepcopy(settings_module.PYDVL_CONFIG),
        "DATASET_INFLUENCE_PARAMS": copy.deepcopy(
            settings_module.DATASET_INFLUENCE_PARAMS
        ),
        "DISTILLATION_CONFIG": copy.deepcopy(settings_module.DISTILLATION_CONFIG),
        "SYNTHETIC_DATA_CONFIG": copy.deepcopy(settings_module.SYNTHETIC_DATA_CONFIG),
    }


def _deep_merge_influence_params(
    base: Dict[str, Any], overlay: Dict[str, Any]
) -> Dict[str, Any]:
    """Слияние influence_params с вложенными dict (lissa_params, cg_params, …)."""
    out = copy.deepcopy(base)
    for k, v in overlay.items():
        if (
            k in out
            and isinstance(out[k], dict)
            and isinstance(v, dict)
            and k
            in (
                "lissa_params",
                "cg_params",
                "arnoldi_params",
                "nystroem_params",
            )
        ):
            merged_sub = copy.deepcopy(out[k])
            merged_sub.update(copy.deepcopy(v))
            out[k] = merged_sub
        else:
            out[k] = copy.deepcopy(v)
    return out


def deep_merge(base: Dict[str, Any], overlay: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not overlay:
        return copy.deepcopy(base)
    out = copy.deepcopy(base)
    for k, v in overlay.items():
        if (
            k in out
            and isinstance(out[k], dict)
            and isinstance(v, dict)
            and k
            not in (
                "METRIC_METADATA",
                "DATASET_INFLUENCE_PARAMS",
            )
        ):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def build_merged_config(api_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Flat API fields + optional `overrides` nested dict merged onto settings snapshot.
    """
    snap = get_settings_snapshot()
    overrides = api_config.get("overrides")
    overrides = overrides if isinstance(overrides, dict) else None
    merged = deep_merge(snap, overrides)

    merged["CURRENT_DATASET"] = api_config["dataset_name"]
    merged["RANDOM_STATE"] = int(api_config.get("random_state", merged["RANDOM_STATE"]))

    mr = dict(merged["MODEL_RUN_CONFIG"])
    mr["model_type"] = api_config["model_type"]
    mp_extra = api_config.get("model_params") or {}
    if "model_architecture" in mp_extra:
        mr["model_architecture"] = mp_extra["model_architecture"]
    merged["MODEL_RUN_CONFIG"] = mr

    ex = dict(merged["EXPERIMENT_CONFIG"])
    ex["test_size"] = float(api_config.get("test_size", ex.get("test_size", 0.2)))
    ex["sample_size_percentage"] = float(
        api_config.get("sample_size_percentage", ex.get("sample_size_percentage", 100))
    )
    ex["n_random_runs"] = int(
        api_config.get("n_random_runs", ex.get("n_random_runs", 3))
    )
    ex["n_epochs"] = int(api_config.get("n_epochs", ex.get("n_epochs", 500)))
    ex["val_size"] = float(api_config.get("val_size", ex.get("val_size", 0.1)))
    merged["EXPERIMENT_CONFIG"] = ex

    dist = dict(merged["DISTILLATION_CONFIG"])
    dist["use_distillation"] = bool(
        api_config.get("use_distillation", dist.get("use_distillation", False))
    )
    dist["distillation_epochs"] = int(
        api_config.get("distillation_epochs", dist.get("distillation_epochs", 200))
    )
    if api_config.get("distillation_temperature") is not None:
        dist["temperature"] = float(api_config["distillation_temperature"])
    if api_config.get("student_architecture"):
        dist["student_architecture"] = str(api_config["student_architecture"])
    merged["DISTILLATION_CONFIG"] = dist

    mfm = api_config.get("model_fit_mode")
    if mfm:
        merged["MODEL_FIT_MODE"] = str(mfm)

    fme = api_config.get("fit_mode_epochs")
    if isinstance(fme, dict) and fme:
        fe = dict(merged.get("FIT_MODE_EPOCHS") or {})
        if "underfit" in fme:
            fe["underfit"] = int(fme["underfit"])
        if "overfit" in fme:
            fe["overfit"] = int(fme["overfit"])
        merged["FIT_MODE_EPOCHS"] = fe

    mc = api_config.get("metric_config")
    if isinstance(mc, dict) and mc:
        mcfg = dict(merged.get("METRIC_CONFIG") or {})
        for k in ("regression", "binary_classification", "multiclass_classification"):
            if k in mc and mc[k]:
                mcfg[k] = str(mc[k])
        merged["METRIC_CONFIG"] = mcfg

    if api_config.get("device"):
        merged["DEVICE"] = str(api_config["device"])
    if api_config.get("use_cache") is not None:
        merged["USE_CACHE"] = bool(api_config["use_cache"])
    if api_config.get("n_jobs") is not None:
        merged["N_JOBS"] = int(api_config["n_jobs"])
    if api_config.get("debug_mode") is not None:
        merged["DEBUG_MODE"] = bool(api_config["debug_mode"])

    ex_extra = merged["EXPERIMENT_CONFIG"]
    if api_config.get("n_retrain_runs") is not None:
        ex_extra["n_retrain_runs"] = int(api_config["n_retrain_runs"])
    if api_config.get("loss_removal_methods") is not None:
        ex_extra["loss_removal_methods"] = list(api_config["loss_removal_methods"])
    if api_config.get("use_catboost_influence") is not None:
        ex_extra["use_catboost_influence"] = bool(api_config["use_catboost_influence"])
    if api_config.get("show_top_bottom_influence") is not None:
        ex_extra["show_top_bottom_influence"] = int(
            api_config["show_top_bottom_influence"]
        )
    merged["EXPERIMENT_CONFIG"] = ex_extra

    inf_overlay = api_config.get("influence_params")
    if isinstance(inf_overlay, dict) and inf_overlay:
        ds_name = api_config["dataset_name"]
        pydvl = dict(merged["PYDVL_CONFIG"])
        base_ip = copy.deepcopy(pydvl.get("influence_params") or {})
        pydvl["influence_params"] = _deep_merge_influence_params(base_ip, inf_overlay)
        merged["PYDVL_CONFIG"] = pydvl

        dip_all = copy.deepcopy(merged.get("DATASET_INFLUENCE_PARAMS") or {})
        ds_base = copy.deepcopy(
            dip_all.get(ds_name) or pydvl["influence_params"]
        )
        dip_all[ds_name] = _deep_merge_influence_params(ds_base, inf_overlay)
        merged["DATASET_INFLUENCE_PARAMS"] = dip_all

    selected = api_config.get("selected_influence_methods") or []
    if selected:
        merged["INFLUENCE_METHODS_CONFIG"] = {
            "valuation_methods": [m for m in selected if m in VALUATION_METHOD_NAMES],
            "influence_methods": [m for m in selected if m in INFLUENCE_METHOD_NAMES],
        }

    # Список стратегий удаления: явный API → legacy removal_strategy → overrides
    ovr_mr = (overrides or {}).get("MODEL_RUN_CONFIG") if isinstance(overrides, dict) else None
    api_rs = api_config.get("removal_strategies")
    if isinstance(api_rs, list) and len(api_rs) > 0:
        merged["MODEL_RUN_CONFIG"]["removal_strategies"] = list(api_rs)
        merged["REMOVAL_STRATEGIES"] = list(api_rs)
    elif not (isinstance(ovr_mr, dict) and ovr_mr.get("removal_strategies") is not None):
        rs = api_config.get("removal_strategy")
        if rs == "remove_lowest_influence":
            merged["MODEL_RUN_CONFIG"]["removal_strategies"] = ["lowest"]
            merged["REMOVAL_STRATEGIES"] = ["lowest"]
        elif rs == "remove_highest_influence":
            merged["MODEL_RUN_CONFIG"]["removal_strategies"] = ["highest"]
            merged["REMOVAL_STRATEGIES"] = ["highest"]

    if api_config.get("removal_per_class") is not None:
        merged["MODEL_RUN_CONFIG"]["removal_per_class"] = bool(
            api_config["removal_per_class"]
        )

    if api_config.get("removal_stratify_target") is not None:
        merged["MODEL_RUN_CONFIG"]["removal_stratify_target"] = bool(
            api_config["removal_stratify_target"]
        )
    if api_config.get("removal_stratify_n_bins") is not None:
        merged["MODEL_RUN_CONFIG"]["removal_stratify_n_bins"] = int(
            api_config["removal_stratify_n_bins"]
        )

    return merged


_PATCH_KEYS = (
    "CURRENT_DATASET",
    "DEBUG_MODE",
    "RANDOM_STATE",
    "MODEL_FIT_MODE",
    "FIT_MODE_EPOCHS",
    "MODEL_RUN_CONFIG",
    "INFLUENCE_METHODS_CONFIG",
    "EXPERIMENT_CONFIG",
    "REMOVAL_STRATEGIES",
    "METRIC_CONFIG",
    "METRIC_METADATA",
    "PYDVL_CONFIG",
    "DATASET_INFLUENCE_PARAMS",
    "DISTILLATION_CONFIG",
    "DEVICE",
    "N_JOBS",
)


@contextmanager
def runtime_settings_patch(merged: Dict[str, Any]):
    """
    Apply merged dict to config.settings for the duration of one experiment run.
    Uses a global lock so parallel experiments do not clobber each other.
    """
    backup: Dict[str, Any] = {}
    with _EXPERIMENT_LOCK:
        try:
            for k in _PATCH_KEYS:
                if k in merged:
                    backup[k] = copy.deepcopy(getattr(settings_module, k, None))
                    setattr(settings_module, k, copy.deepcopy(merged[k]))
            yield
        finally:
            for k, v in backup.items():
                setattr(settings_module, k, v)
