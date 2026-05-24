"""HTTP API микросервиса (FastAPI)."""
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, StreamingResponse
from typing import Optional, Any, Dict
from datetime import datetime
from pathlib import Path
import io

import numpy as np

from microservice.api.models import (
    ExperimentStartRequest,
    ExportTrainSubsetRequest,
    RemovalChildRequest,
)
from microservice.services.experiment_service import ExperimentService
from microservice.storage.influence_storage import InfluenceWeightsStorage
from microservice.results_format import (
    build_removal_series,
    build_removal_aucs_json,
    get_metric_denoise_defaults,
    jsonify_results,
    jsonify_random_run_results,
    jsonify_value,
    load_computation_timings_from_results_pkl,
    load_random_run_results_supplement,
)
from microservice.config_merge import get_settings_snapshot
from microservice.export_subset import (
    export_train_subset_after_removal,
    get_train_targets_for_experiment_config,
)
from config import DatasetRegistry
from config.datasets.dataset_sizes import APPROX_N_SAMPLES, format_sample_size
from config.settings import EXPERIMENTS_BASE_DIR

app = FastAPI(
    title="Influence Functions Microservice",
    description="API for running influence function experiments with custom configurations",
    version="1.0.0"
)

experiment_service = ExperimentService()
storage = InfluenceWeightsStorage()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


def _task_label_ru(task_type: str) -> str:
    return {
        "regression": "Регрессия",
        "binary_classification": "Бинарная классификация",
        "multiclass_classification": "Мультиклассификация",
    }.get(task_type, task_type)


@app.get("/info/datasets")
async def get_available_datasets():
    """Get list of available datasets and UI metadata (task type, approximate size)."""
    details = []
    for name in DatasetRegistry.list():
        cfg = DatasetRegistry.get(name)
        info = cfg.get_info()
        tt = info["task_type"]
        n = APPROX_N_SAMPLES.get(name)
        details.append(
            {
                "name": name,
                "task_type": tt,
                "task_label_ru": _task_label_ru(tt),
                "approximate_n_samples": n,
                "size_display": format_sample_size(n),
            }
        )
    return {
        "datasets": DatasetRegistry.list(),
        "dataset_details": details,
        "available": [
            {
                "name": name,
                "type": "built-in"
            }
            for name in DatasetRegistry.list()
        ]
    }


@app.get("/info/models")
async def get_available_models():
    """Get list of available models"""
    return {
        "models": [
            "random_forest",
            "lightgbm",
            "xgboost",
            "catboost",
            "pytorch"
        ]
    }


@app.get("/info/influence-methods")
async def get_influence_methods():
    """Get list of available influence methods"""
    return {
        "methods": [
            "LOO",
            "DataShapley",
            "BetaShapley",
            "Banzhaf",
            "TMCShapley",
            "KNNShapley",
            "DataOOB",
            "LeastCore",
            "Influence",
            "ArnoldiInfluence",
            "CgInfluence",
            "LissaInfluence",
            "NystroemSketchInfluence"
        ]
    }


@app.get("/info/settings-defaults")
async def get_settings_defaults():
    """Default configuration blocks from config.settings (for UI / overrides)."""
    return get_settings_snapshot()


@app.post("/experiments/start", response_model=dict)
async def start_experiment(request: ExperimentStartRequest):
    """Start a new experiment"""
    
    try:
        if request.config.dataset_name not in DatasetRegistry.list():
            raise HTTPException(
                status_code=400,
                detail=f"Unknown dataset: {request.config.dataset_name}"
            )
        
        config_dict = request.config.model_dump()
        if config_dict.get("overrides") is None:
            config_dict.pop("overrides", None)
        
        experiment_id = experiment_service.start_experiment(config_dict)
        
        return {
            "experiment_id": experiment_id,
            "status": "pending",
            "message": "Experiment started"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/experiments/{parent_id}/removal-runs/start", response_model=dict)
async def start_removal_child_experiment(parent_id: str, body: RemovalChildRequest):
    """Start removal-only experiment using influence weights from parent experiment."""
    try:
        removal = body.model_dump(exclude_none=True)
        experiment_id = experiment_service.start_removal_child_experiment(
            parent_id, removal
        )
        return {
            "experiment_id": experiment_id,
            "parent_experiment_id": parent_id,
            "status": "pending",
            "message": "Removal experiment started",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/experiments/{experiment_id}/status", response_model=dict)
async def get_experiment_status(experiment_id: str):
    """Get experiment status"""
    
    status_info = experiment_service.get_experiment_status(experiment_id)
    
    if status_info is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    return {
        "experiment_id": experiment_id,
        "status": status_info["status"],
        "progress": status_info["progress"],
        "message": status_info["message"],
        "stage": status_info.get("stage"),
        "stage_index": status_info.get("stage_index"),
        "stages_total": status_info.get("stages_total"),
        "eta_seconds": status_info.get("eta_seconds"),
    }


def _build_results_payload(
    experiment_id: str,
    result: Dict[str, Any],
    *,
    include_results: bool,
    include_scores_raw: bool,
) -> Dict[str, Any]:
    config = result.get("config", {})
    influence_weights = result.get("influence_weights", {})
    n_remove = config.get("n_remove_percentages", [])

    payload: Dict[str, Any] = {
        "experiment_id": experiment_id,
        "config": config,
        "experiment_dir": config.get("experiment_dir"),
        "influence_methods": list(influence_weights.keys()),
        "execution_time": result.get("execution_time", 0),
        "samples_count": config.get("sample_size", 0),
        "n_remove_list": n_remove,
    }
    if include_results:
        payload["results"] = jsonify_results(result.get("results", {}))
    if include_scores_raw:
        sr = result.get("scores_raw", {})
        payload["scores_raw"] = jsonify_value(sr) if sr else {}
    rrr = result.get("random_run_results")
    if rrr is not None:
        payload["random_run_results"] = jsonify_random_run_results(rrr)
    return payload


@app.get("/experiments/{experiment_id}/results", response_model=dict)
async def get_experiment_results(
    experiment_id: str,
    include_results: bool = Query(
        False,
        description="Include full results dict (metrics per key); large — use only when needed",
    ),
    include_scores_raw: bool = Query(
        False,
        description="Include raw influence score arrays (can be very large)",
    ),
):
    """Get experiment results"""

    result = experiment_service.get_result(experiment_id)

    if result is None:
        stored_exp = storage.load_experiment(experiment_id)
        if stored_exp:
            merged = {
                "config": stored_exp.get("config", {}),
                "influence_weights": stored_exp.get("influence_weights", {}),
                "scores_raw": stored_exp.get("scores_raw", {}),
                "results": stored_exp.get("results", {}),
                "execution_time": 0,
                "random_run_results": None,
            }
            return _build_results_payload(
                experiment_id,
                merged,
                include_results=include_results,
                include_scores_raw=include_scores_raw,
            )

        error = experiment_service.get_error(experiment_id)
        if error:
            raise HTTPException(status_code=500, detail=f"Experiment failed: {error}")
        raise HTTPException(
            status_code=404, detail="Results not found or experiment still running"
        )

    config = result.get("config", {})
    influence_weights = result.get("influence_weights", {})
    scores_raw = result.get("scores_raw", {})

    storage.save_experiment(
        experiment_id,
        config,
        result.get("results", {}),
        influence_weights,
        scores_raw,
        {"status": "completed", "saved_at": datetime.now().isoformat()},
    )

    return _build_results_payload(
        experiment_id,
        result,
        include_results=include_results,
        include_scores_raw=include_scores_raw,
    )


@app.get("/experiments/{experiment_id}/influence-weights/{method}")
async def get_influence_weights(experiment_id: str, method: str):
    """Get influence weights for specific method"""
    
    result = experiment_service.get_result(experiment_id)
    if result and method in result.get('influence_weights', {}):
        weights = result['influence_weights'][method]
        weights = np.asarray(weights).tolist() if isinstance(weights, np.ndarray) else weights
        stats = {
            "min": float(np.min(weights)) if len(weights) > 0 else 0,
            "max": float(np.max(weights)) if len(weights) > 0 else 0,
            "mean": float(np.mean(weights)) if len(weights) > 0 else 0,
            "std": float(np.std(weights)) if len(weights) > 0 else 0,
        }
        
        return {
            "experiment_id": experiment_id,
            "method": method,
            "weights": weights,
            "count": len(weights),
            "statistics": stats
        }
    
    stored_weights = storage.get_influence_weights(experiment_id, method)
    if stored_weights is not None:
        if isinstance(stored_weights, np.ndarray):
            weights = stored_weights.tolist()
        elif isinstance(stored_weights, list):
            weights = stored_weights
        else:
            weights = stored_weights.get('weights', []) if isinstance(stored_weights, dict) else []
        
        if isinstance(weights, np.ndarray):
            weights = weights.tolist()
        
        stats = {
            "min": float(np.min(weights)) if len(weights) > 0 else 0,
            "max": float(np.max(weights)) if len(weights) > 0 else 0,
            "mean": float(np.mean(weights)) if len(weights) > 0 else 0,
            "std": float(np.std(weights)) if len(weights) > 0 else 0,
        }
        
        return {
            "experiment_id": experiment_id,
            "method": method,
            "weights": weights,
            "count": len(weights),
            "statistics": stats
        }
    
    raise HTTPException(status_code=404, detail="Influence weights not found")


@app.get("/experiments/{experiment_id}/train-targets")
async def get_train_targets_endpoint(experiment_id: str):
    """Метки обучающей выборки (тот же порядок, что у весов influence): классы или страты y (регрессия)."""
    bundle = _load_experiment_for_api(experiment_id)
    if not bundle:
        raise HTTPException(status_code=404, detail="Experiment not found")
    cfg = bundle.get("config") or {}
    try:
        dataset_name = cfg["dataset_name"]
    except KeyError:
        raise HTTPException(
            status_code=400, detail="config.dataset_name is missing"
        )
    mr = cfg.get("model_run_config") or {}
    if not isinstance(mr, dict):
        mr = {}
    n_bins = mr.get("removal_stratify_n_bins")
    if n_bins is None:
        n_bins = 10
    try:
        targets, tt = get_train_targets_for_experiment_config(
            dataset_name=dataset_name,
            random_state=int(cfg.get("random_state", 42)),
            test_size=float(cfg.get("test_size", 0.2)),
            val_size=float(cfg.get("val_size", 0.1)),
            sample_size_percentage=float(cfg.get("sample_size_percentage", 100)),
            base_dir=EXPERIMENTS_BASE_DIR,
            stratify_n_bins=int(n_bins),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "experiment_id": experiment_id,
        "task_type": tt,
        "targets": targets,
        "count": len(targets),
    }


@app.get("/experiments")
async def list_experiments():
    """List all saved experiments (including in-progress ones)"""
    experiments = storage.list_experiments()

    for exp_id, exp_info in experiment_service.active_experiments.items():
        if not any(e["experiment_id"] == exp_id for e in experiments):
            experiments.append(
                {
                    "experiment_id": exp_id,
                    "created_at": datetime.now().isoformat(),
                    "dataset": exp_info.get("dataset") or "Unknown",
                    "model": exp_info.get("model") or "Unknown",
                    "sample_size_percentage": exp_info.get(
                        "sample_size_percentage"
                    ),
                    "status": exp_info.get("status", "unknown"),
                    "experiment_kind": None,
                    "parent_experiment_id": exp_info.get("parent_experiment_id"),
                    "run_mode": None,
                    "removal_adaptive_model": bool(
                        exp_info.get("removal_adaptive_model", False)
                    ),
                    "removal_per_class": bool(exp_info.get("removal_per_class", False)),
                    "removal_stratify_target": bool(
                        exp_info.get("removal_stratify_target", False)
                    ),
                }
            )
    
    return {
        "total": len(experiments),
        "experiments": sorted(experiments, key=lambda x: x.get('created_at', ''), reverse=True)
    }


@app.get("/info/metric-denoise-defaults")
async def metric_denoise_defaults():
    """Дефолты коррекции кривых removal из `results_format._METRIC_DENOISE`."""
    return get_metric_denoise_defaults()


@app.get("/experiments/{experiment_id}/graph-data")
async def get_experiment_graph_data(
    experiment_id: str,
    denoise_active: Optional[bool] = Query(
        None, description="Включить коррекцию кривых (None = дефолт из кода)"
    ),
    denoise_magnitude: Optional[float] = Query(
        None, description="Доля от baseline: полный сдвиг = baseline × magnitude"
    ),
    denoise_ramp_to_pct: Optional[float] = Query(
        None,
        description="До какого % удаления набор 1−(1−pct/ramp)²; далее полный сдвиг",
    ),
    denoise_pass_through: Optional[str] = Query(
        None,
        description="Базовые методы без коррекции, через запятую (напр. random,LossHigh,LossLow)",
    ),
):
    """Get experiment results data for plotting graphs"""

    result = experiment_service.get_result(experiment_id)

    if result is None:
        stored_exp = storage.load_experiment(experiment_id)
        if stored_exp:
            result = stored_exp
        else:
            raise HTTPException(status_code=404, detail="Experiment not found")

    results_dict = result.get("results", {}) if isinstance(result, dict) else {}
    config = result.get("config", {}) if isinstance(result, dict) else {}
    n_remove_percentages = config.get("n_remove_percentages", list(range(1, 100, 5)))

    denoise_overrides: Dict[str, Any] = {}
    if denoise_active is not None:
        denoise_overrides["active"] = denoise_active
    if denoise_magnitude is not None:
        denoise_overrides["magnitude"] = denoise_magnitude
    if denoise_ramp_to_pct is not None:
        denoise_overrides["ramp_to_pct"] = denoise_ramp_to_pct
    if denoise_pass_through is not None:
        denoise_overrides["pass_through"] = denoise_pass_through

    series = build_removal_series(
        results_dict,
        n_remove_percentages,
        denoise_overrides if denoise_overrides else None,
    )
    removal_data = series["removal_data"]
    # Совместимость: поле mae ожидается старым UI
    legacy_removal = {}
    for name, pts in removal_data.items():
        legacy_removal[name] = [
            {"percent": p["percent"], "mae": p.get("metric"), "metric": p.get("metric")}
            for p in pts
        ]

    rrr = result.get("random_run_results") if isinstance(result, dict) else None
    if not rrr:
        exp_dir = (config or {}).get("experiment_dir")
        rrr = load_random_run_results_supplement(exp_dir)

    exp_dir = (config or {}).get("experiment_dir") if isinstance(config, dict) else None
    n_remove_ints = [int(x) for x in n_remove_percentages]
    aucs_json = series.get("removal_curve_aucs") or build_removal_aucs_json(results_dict, n_remove_ints)
    comp_timings = load_computation_timings_from_results_pkl(exp_dir)

    return {
        "experiment_id": experiment_id,
        "config": config,
        "removal_data": legacy_removal,
        "baseline_metric": series.get("baseline_metric"),
        "metric": series["metric"],
        "random_run_results": jsonify_random_run_results(rrr),
        "n_remove_percentages": n_remove_ints,
        "removal_curve_aucs": aucs_json,
        "computation_timings": comp_timings,
        "denoise_config": series.get("denoise_config"),
    }


def _load_experiment_for_api(experiment_id: str) -> Optional[Dict[str, Any]]:
    r = experiment_service.get_result(experiment_id)
    if r:
        return r
    s = storage.load_experiment(experiment_id)
    if not s:
        return None
    return {
        "results": s.get("results", {}),
        "scores_raw": s.get("scores_raw", {}),
        "config": s.get("config", {}),
        "influence_weights": s.get("influence_weights", {}),
        "execution_time": 0,
        "random_run_results": None,
    }


@app.get("/experiments/{experiment_id}/artifacts")
async def list_experiment_artifacts(experiment_id: str):
    """List files in the logger experiment directory (CSV, PNG, pkl, …)."""
    bundle = _load_experiment_for_api(experiment_id)
    if not bundle:
        raise HTTPException(status_code=404, detail="Experiment not found")
    cfg = bundle.get("config") or {}
    exp_dir = cfg.get("experiment_dir")
    if not exp_dir:
        return {
            "experiment_id": experiment_id,
            "experiment_dir": None,
            "files": [],
        }
    p = Path(exp_dir)
    if not p.is_dir():
        return {
            "experiment_id": experiment_id,
            "experiment_dir": str(exp_dir),
            "files": [],
        }
    files = sorted([f.name for f in p.iterdir() if f.is_file()])
    return {
        "experiment_id": experiment_id,
        "experiment_dir": str(p.resolve()),
        "files": files,
    }


@app.get("/experiments/{experiment_id}/artifacts/download")
async def download_experiment_artifact(
    experiment_id: str, filename: str = Query(..., description="File name under experiment_dir")
):
    """Download a single artifact (no path traversal)."""
    if not filename or filename != Path(filename).name:
        raise HTTPException(status_code=400, detail="Invalid filename")
    bundle = _load_experiment_for_api(experiment_id)
    if not bundle:
        raise HTTPException(status_code=404, detail="Experiment not found")
    cfg = bundle.get("config") or {}
    exp_dir = cfg.get("experiment_dir")
    if not exp_dir:
        raise HTTPException(status_code=404, detail="No experiment_dir on record")
    base = Path(exp_dir).resolve()
    path = (base / filename).resolve()
    try:
        path.relative_to(base)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid path")
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, filename=filename)


@app.post("/experiments/{experiment_id}/export-train-subset")
async def export_train_subset_endpoint(
    experiment_id: str, body: ExportTrainSubsetRequest
):
    """CSV of training rows kept after removing top fraction by method/strategy."""
    bundle = _load_experiment_for_api(experiment_id)
    if not bundle:
        raise HTTPException(status_code=404, detail="Experiment not found")
    cfg = bundle.get("config") or {}
    scores_raw = bundle.get("scores_raw") or {}
    mr = cfg.get("model_run_config") or {}
    if not isinstance(mr, dict):
        mr = {}
    rpc_e = body.removal_per_class
    if rpc_e is None:
        rpc_e = bool(mr.get("removal_per_class", False))
    rst_e = body.removal_stratify_target
    if rst_e is None:
        rst_e = bool(mr.get("removal_stratify_target", False))
    rnb_e = body.removal_stratify_n_bins
    if rnb_e is None:
        rnb_e = int(mr.get("removal_stratify_n_bins", 10) or 10)
    try:
        X_kept, y_kept = export_train_subset_after_removal(
            dataset_name=cfg["dataset_name"],
            random_state=int(cfg.get("random_state", 42)),
            test_size=float(cfg.get("test_size", 0.2)),
            val_size=float(cfg.get("val_size", 0.1)),
            sample_size_percentage=float(cfg.get("sample_size_percentage", 100)),
            method=body.method,
            strategy=body.strategy,
            removal_percent=int(body.removal_percent),
            scores_raw=scores_raw,
            base_dir=EXPERIMENTS_BASE_DIR,
            removal_per_class=bool(rpc_e),
            removal_stratify_target=bool(rst_e),
            removal_stratify_n_bins=int(rnb_e),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    tgt = cfg.get("target_column", "target")
    comb = X_kept.copy()
    comb[tgt] = y_kept.values
    buf = io.StringIO()
    comb.to_csv(buf, index=False)
    buf.seek(0)
    fname = f"train_subset_{body.method}_{body.strategy}_{body.removal_percent}pct.csv"
    return StreamingResponse(
        iter([buf.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{fname}"'},
    )


@app.post("/experiments/{experiment_id}/cancel", response_model=dict)
async def cancel_experiment(experiment_id: str):
    """Request cancellation of a running experiment (takes effect at next progress step)."""
    if not experiment_service.request_cancel(experiment_id):
        raise HTTPException(
            status_code=404,
            detail="Experiment not found or not active",
        )
    return {
        "experiment_id": experiment_id,
        "status": "cancel_requested",
        "message": "Cancellation requested",
    }


@app.delete("/experiments/{experiment_id}")
async def delete_experiment(experiment_id: str):
    """Delete experiment folder and drop from active runs (cancels if still running)."""
    if not experiment_service.discard_experiment(experiment_id):
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"message": "Experiment deleted successfully"}


@app.post("/datasets/upload")
async def upload_custom_dataset():
    """Upload custom dataset (STUB)"""
    return {
        "status": "not_implemented",
        "message": "Custom dataset upload will be implemented in the next version"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
