"""Файловое хранилище результатов экспериментов и весов influence."""
import json
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import shutil


class InfluenceWeightsStorage:
    """Сохранение и загрузка артефактов эксперимента."""
    
    def __init__(self, base_path: str = "microservice_storage"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        self.experiments_dir = self.base_path / "experiments"
        self.experiments_dir.mkdir(exist_ok=True)
        
    def save_experiment(self, experiment_id: str, config: Dict[str, Any], 
                       results: Dict[str, Any], influence_weights: Dict[str, Any],
                       scores_raw: Dict[str, Any], metadata: Dict[str, Any] = None) -> str:
        """Сохраняет конфиг, результаты, веса и метаданные."""
        exp_dir = self.experiments_dir / experiment_id
        exp_dir.mkdir(exist_ok=True)

        config_path = exp_dir / "config.json"
        with open(config_path, 'w') as f:
            config_copy = self._prepare_for_json(config)
            json.dump(config_copy, f, indent=2, default=str)

        results_path = exp_dir / "results.json"
        with open(results_path, 'w') as f:
            results_copy = self._prepare_for_json(results)
            json.dump(results_copy, f, indent=2, default=str)

        weights_path = exp_dir / "influence_weights.pkl"
        with open(weights_path, 'wb') as f:
            pickle.dump(influence_weights, f)

        scores_path = exp_dir / "scores_raw.pkl"
        with open(scores_path, 'wb') as f:
            pickle.dump(scores_raw, f)

        if metadata is None:
            metadata = {}
        metadata['created_at'] = datetime.now().isoformat()
        
        metadata_path = exp_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        return str(exp_dir)
    
    def load_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Загружает сохранённый эксперимент или None."""
        exp_dir = self.experiments_dir / experiment_id
        if not exp_dir.exists():
            return None

        try:
            with open(exp_dir / "config.json", 'r') as f:
                config = json.load(f)

            with open(exp_dir / "results.json", 'r') as f:
                results = json.load(f)

            with open(exp_dir / "influence_weights.pkl", 'rb') as f:
                influence_weights = pickle.load(f)

            with open(exp_dir / "scores_raw.pkl", 'rb') as f:
                scores_raw = pickle.load(f)

            with open(exp_dir / "metadata.json", 'r') as f:
                metadata = json.load(f)
            
            return {
                'experiment_id': experiment_id,
                'config': config,
                'results': results,
                'influence_weights': influence_weights,
                'scores_raw': scores_raw,
                'metadata': metadata
            }
        except Exception as e:
            print(f"Error loading experiment {experiment_id}: {e}")
            return None
    
    def get_influence_weights(self, experiment_id: str, method: str = None) -> Optional[Dict[str, Any]]:
        """Get influence weights for specific method"""
        
        exp_dir = self.experiments_dir / experiment_id
        weights_path = exp_dir / "influence_weights.pkl"
        
        if not weights_path.exists():
            return None
        
        try:
            with open(weights_path, 'rb') as f:
                weights = pickle.load(f)
            
            if method:
                return weights.get(method)
            return weights
        except Exception as e:
            print(f"Error loading weights: {e}")
            return None
    
    def list_experiments(self) -> List[Dict[str, Any]]:
        """List all saved experiments"""
        
        experiments = []
        for exp_dir in self.experiments_dir.iterdir():
            if exp_dir.is_dir():
                metadata_path = exp_dir / "metadata.json"
                config_path = exp_dir / "config.json"
                
                if metadata_path.exists() and config_path.exists():
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        with open(config_path, 'r') as f:
                            config = json.load(f)

                        mr = config.get("model_run_config") or {}
                        if not isinstance(mr, dict):
                            mr = {}
                        rpc = mr.get("removal_per_class")
                        if rpc is None:
                            rpc = config.get("removal_per_class")
                        if rpc is None:
                            mrc = config.get("MODEL_RUN_CONFIG")
                            if isinstance(mrc, dict):
                                rpc = mrc.get("removal_per_class")
                        removal_per_class = bool(rpc) if rpc is not None else False
                        rst = mr.get("removal_stratify_target")
                        if rst is None:
                            rst = config.get("removal_stratify_target")
                        if rst is None:
                            _mrc_rst = config.get("MODEL_RUN_CONFIG")
                            if isinstance(_mrc_rst, dict):
                                rst = _mrc_rst.get("removal_stratify_target")
                        removal_stratify_target = bool(rst) if rst is not None else False
                        removal_adaptive_model = bool(
                            config.get("removal_adaptive_model", False)
                        )

                        experiments.append({
                            'experiment_id': exp_dir.name,
                            'created_at': metadata.get('created_at'),
                            'dataset': config.get('dataset_name'),
                            'model': config.get('model_type'),
                            'sample_size_percentage': config.get(
                                'sample_size_percentage'
                            ),
                            'status': metadata.get('status', 'unknown'),
                            'experiment_kind': config.get('experiment_kind'),
                            'parent_experiment_id': config.get('parent_experiment_id'),
                            'run_mode': config.get('run_mode'),
                            'removal_adaptive_model': removal_adaptive_model,
                            'removal_per_class': removal_per_class,
                            'removal_stratify_target': removal_stratify_target,
                        })
                    except Exception as e:
                        print(f"Error reading experiment {exp_dir.name}: {e}")
        
        return sorted(experiments, key=lambda x: x.get('created_at', ''), reverse=True)
    
    def delete_experiment(self, experiment_id: str) -> bool:
        """Delete experiment data"""
        
        exp_dir = self.experiments_dir / experiment_id
        if exp_dir.exists():
            try:
                shutil.rmtree(exp_dir)
                return True
            except Exception as e:
                print(f"Error deleting experiment: {e}")
                return False
        return False
    
    @staticmethod
    def _prepare_for_json(obj):
        """Convert numpy types and other objects to JSON-serializable format"""
        
        if isinstance(obj, dict):
            return {k: InfluenceWeightsStorage._prepare_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [InfluenceWeightsStorage._prepare_for_json(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj) if isinstance(obj, (np.floating, np.integer)) else obj
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif hasattr(obj, '__dict__'):
            return str(obj)
        return obj
