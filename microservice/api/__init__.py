"""FastAPI application"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import datetime
import json
import numpy as np

from microservice.api.models import (
    ExperimentConfig, ExperimentStartRequest, ExperimentStatusResponse,
    ExperimentStatus, InfluenceWeightsResponse, ExperimentResultsResponse,
    DatasetType, ModelType
)
from microservice.services.experiment_service import ExperimentService
from microservice.storage.influence_storage import InfluenceWeightsStorage
from config import DatasetRegistry

app = FastAPI(
    title="Influence Functions Microservice",
    description="API for running influence function experiments with custom configurations",
    version="1.0.0"
)

# Initialize services
experiment_service = ExperimentService()
storage = InfluenceWeightsStorage()


# ==================== Health & Info ====================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/info/datasets")
async def get_available_datasets():
    """Get list of available datasets"""
    return {
        "datasets": DatasetRegistry.list(),
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


# ==================== Experiments ====================

@app.post("/experiments/start", response_model=dict)
async def start_experiment(request: ExperimentStartRequest):
    """Start a new experiment"""
    
    try:
        # Validate dataset
        if request.config.dataset_name not in DatasetRegistry.list():
            raise HTTPException(
                status_code=400,
                detail=f"Unknown dataset: {request.config.dataset_name}"
            )
        
        # Convert enum values to strings
        config_dict = request.config.dict()
        config_dict['dataset_name'] = request.config.dataset_name
        config_dict['model_type'] = request.config.model_type
        config_dict['removal_strategy'] = request.config.removal_strategy
        # Convert InfluenceMethod enums to their string values
        config_dict['selected_influence_methods'] = [
            m if isinstance(m, str) else m.value 
            for m in request.config.selected_influence_methods
        ]
        
        # Start experiment
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


@app.get("/experiments/{experiment_id}/status", response_model=dict)
async def get_experiment_status(experiment_id: str):
    """Get experiment status"""
    
    status_info = experiment_service.get_experiment_status(experiment_id)
    
    if status_info is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    return {
        "experiment_id": experiment_id,
        "status": status_info['status'],
        "progress": status_info['progress'],
        "message": status_info['message']
    }


@app.get("/experiments/{experiment_id}/results", response_model=dict)
async def get_experiment_results(experiment_id: str):
    """Get experiment results"""
    
    # Try to get from active experiments first
    result = experiment_service.get_result(experiment_id)
    
    # If not in active experiments, try to load from storage
    if result is None:
        stored_exp = storage.load_experiment(experiment_id)
        if stored_exp:
            # Return stored results
            return {
                "experiment_id": experiment_id,
                "config": stored_exp.get('config', {}),
                "influence_methods": list(stored_exp.get('influence_weights', {}).keys()),
                "execution_time": 0,  # Not stored separately
                "samples_count": stored_exp.get('config', {}).get('sample_size', 0)
            }
        
        # Try to get error
        error = experiment_service.get_error(experiment_id)
        if error:
            raise HTTPException(status_code=500, detail=f"Experiment failed: {error}")
        raise HTTPException(status_code=404, detail="Results not found or experiment still running")
    
    # Save to storage (if not already saved, which is now done automatically)
    config = result.get('config', {})
    influence_weights = result.get('influence_weights', {})
    scores_raw = result.get('scores_raw', {})
    
    storage.save_experiment(
        experiment_id,
        config,
        result.get('results', {}),
        influence_weights,
        scores_raw,
        {'status': 'completed', 'saved_at': datetime.now().isoformat()}
    )
    
    return {
        "experiment_id": experiment_id,
        "config": config,
        "experiment_dir": config.get('experiment_dir') if isinstance(config, dict) else None,
        "influence_methods": list(influence_weights.keys()),
        "execution_time": result.get('execution_time', 0),
        "samples_count": config.get('sample_size', 0)
    }


@app.get("/experiments/{experiment_id}/influence-weights/{method}")
async def get_influence_weights(experiment_id: str, method: str):
    """Get influence weights for specific method"""
    
    # Try to get from active experiments first
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
    
    # Try to get from storage
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


@app.get("/experiments")
async def list_experiments():
    """List all saved experiments (including in-progress ones)"""
    # Get saved experiments from storage
    experiments = storage.list_experiments()
    
    # Add active experiments that haven't been saved yet
    for exp_id, exp_info in experiment_service.active_experiments.items():
        # Check if this experiment is already in the list
        if not any(e['experiment_id'] == exp_id for e in experiments):
            experiments.append({
                'experiment_id': exp_id,
                'created_at': datetime.now().isoformat(),
                'dataset': 'Unknown',  # Could be extracted from active experiment
                'model': 'Unknown',
                'status': exp_info.get('status', 'unknown')
            })
    
    return {
        "total": len(experiments),
        "experiments": sorted(experiments, key=lambda x: x.get('created_at', ''), reverse=True)
    }


@app.get("/experiments/{experiment_id}/graph-data")
async def get_experiment_graph_data(experiment_id: str):
    """Get experiment results data for plotting graphs"""
    
    # Try to get from active experiments first
    result = experiment_service.get_result(experiment_id)
    
    # If not in active experiments, try to load from storage
    if result is None:
        stored_exp = storage.load_experiment(experiment_id)
        if stored_exp:
            result = stored_exp
        else:
            raise HTTPException(status_code=404, detail="Experiment not found")
    
    # Extract relevant data for graphing
    results_dict = result.get('results', {}) if isinstance(result, dict) else {}
    config = result.get('config', {}) if isinstance(result, dict) else {}
    
    # Process results for Removal Impact plot
    removal_data = {}
    n_remove_percentages = config.get('n_remove_percentages', list(range(1, 100, 5)))
    
    for method_name in ['Influence', 'ArnoldiInfluence', 'CgInfluence', 'LissaInfluence', 'NystroemSketchInfluence', 
                        'PermutationImportance', 'Banzhaf', 'Shapley', 'BetaShapley']:
        method_data = []
        # Get baseline (0% removal)
        baseline_key = f'{method_name}_0'
        if baseline_key in results_dict:
            baseline_val = results_dict[baseline_key].get('final_mae', 0) if isinstance(results_dict[baseline_key], dict) else results_dict[baseline_key]
            method_data.append({'percent': 0, 'mae': baseline_val})
        
        # Get removal percentages
        for pct in n_remove_percentages:
            key = f'{method_name}_{pct}pct'
            if key in results_dict:
                val = results_dict[key].get('final_mae', 0) if isinstance(results_dict[key], dict) else results_dict[key]
                method_data.append({'percent': pct, 'mae': val})
        
        # Get random removal
        random_key = f'random_{pct}pct' if n_remove_percentages else None
        if random_key and random_key in results_dict:
            val = results_dict[random_key].get('final_mae', 0) if isinstance(results_dict[random_key], dict) else results_dict[random_key]
            method_data.append({'percent': pct, 'mae': val, 'method': 'random'})
        
        if method_data:
            removal_data[method_name] = method_data
    
    # Also add random removal baseline
    random_data = []
    for pct in n_remove_percentages:
        key = f'random_{pct}pct'
        if key in results_dict:
            val = results_dict[key].get('final_mae', 0) if isinstance(results_dict[key], dict) else results_dict[key]
            random_data.append({'percent': pct, 'mae': val})
    
    if random_data:
        removal_data['Random'] = random_data
    
    return {
        "experiment_id": experiment_id,
        "config": config,
        "removal_data": removal_data
    }


@app.delete("/experiments/{experiment_id}")
async def delete_experiment(experiment_id: str):
    """Delete experiment"""
    success = storage.delete_experiment(experiment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"message": "Experiment deleted successfully"}


# ==================== Custom Dataset (Stub) ====================

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
