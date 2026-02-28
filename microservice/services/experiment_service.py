"""Experiment service wrapper"""
import sys
import os
import json
import time
import uuid
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import threading
from queue import Queue
from copy import deepcopy
from datetime import datetime

# Add parent directory to path to import main project modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import (
    RANDOM_STATE, DEVICE, EXPERIMENTS_BASE_DIR
)
from config import DatasetRegistry
from data.loader import DataLoaderFactory
from data.preprocessing import PreprocessorFactory
from data.cache import DataCache
from models.factory import ModelFactory
from experiments.runner import ExperimentRunner
from experiments.logger import ExperimentLogger
from influence.methods import InfluenceMethods
from utils.helpers import set_random_seeds
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from visualization.plots import plot_influence_distribution, plot_results_enhanced
from microservice.storage.influence_storage import InfluenceWeightsStorage


class ExperimentService:
    """Service for running experiments with custom configuration"""

    def __init__(self):
        self.active_experiments = {}  # experiment_id -> status and progress
        self.tasks_queue = Queue()
        self.storage = InfluenceWeightsStorage()

    def start_experiment(self, config: Dict[str, Any], experiment_id: Optional[str] = None) -> str:
        """Start experiment in background thread"""
        if experiment_id is None:
            experiment_id = str(uuid.uuid4())

        self.active_experiments[experiment_id] = {
            'status': 'running',
            'progress': 0.0,
            'message': 'Initializing...',
            'start_time': time.time(),
            'result': None,
            'error': None
        }

        # Start background thread
        thread = threading.Thread(
            target=self._run_experiment_thread,
            args=(experiment_id, config),
            daemon=True
        )
        thread.start()

        return experiment_id
    
    def get_experiment_status(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Get experiment status"""
        return self.active_experiments.get(experiment_id)
    
    def _run_experiment_thread(self, experiment_id: str, config: Dict[str, Any]):
        """Run experiment in thread"""
        
        try:
            set_random_seeds(config.get('random_state', RANDOM_STATE))
            
            # Update status
            self._update_status(experiment_id, 'running', 5, 'Loading dataset...')
            
            # Load dataset
            dataset_name = config['dataset_name']
            try:
                dataset_config = DatasetRegistry.get(dataset_name)
            except KeyError:
                raise ValueError(f"Unknown dataset: {dataset_name}")
            
            logger = ExperimentLogger(base_dir=EXPERIMENTS_BASE_DIR)
            
            # Load and prepare data
            X, y, cfg = DataLoaderFactory.load_dataset(dataset_config, logger)
            
            # Encode target if classification
            if cfg.task_type in ['binary_classification', 'multiclass_classification']:
                if y.dtype == 'object':
                    le = LabelEncoder()
                    y = pd.Series(le.fit_transform(y), index=y.index)
            
            self._update_status(experiment_id, 'running', 10, 'Splitting data...')
            
            # Split data
            X_temp, X_holdout_validation, y_temp, y_holdout_validation = train_test_split(
                X, y,
                test_size=config.get('val_size', 0.1),
                random_state=config.get('random_state', RANDOM_STATE),
                stratify=y if cfg.stratify else None
            )
            
            # Sample data
            sample_pct = config.get('sample_size_percentage', 100) / 100.0
            n_samples = max(10, int(len(X_temp) * sample_pct))
            indices = np.random.choice(len(X_temp), size=n_samples, replace=False)
            X_sample = X_temp.iloc[indices]
            y_sample = y_temp.iloc[indices]
            
            # Split into train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X_sample, y_sample,
                test_size=config.get('test_size', 0.2),
                random_state=config.get('random_state', RANDOM_STATE)
            )
            
            self._update_status(experiment_id, 'running', 15, 'Creating preprocessor...')
            
            # Create and fit preprocessor
            preprocessor = PreprocessorFactory.create(dataset_config, logger)
            preprocessor.fit(X_train)
            
            X_train_processed = preprocessor.transform(X_train)
            X_test_processed = preprocessor.transform(X_test)
            X_val_processed = preprocessor.transform(X_holdout_validation)
            
            if hasattr(X_train_processed, 'toarray'):
                X_train_processed = X_train_processed.toarray()
                X_test_processed = X_test_processed.toarray()
                X_val_processed = X_val_processed.toarray()
            
            input_size = X_train_processed.shape[1]
            
            self._update_status(experiment_id, 'running', 20, 'Building model configuration...')
            
            # Prepare model parameters
            model_params = {
                'model_type': config.get('model_type', 'random_forest'),
                'task_type': cfg.task_type,
                'input_size': input_size,
                'device': DEVICE,
                'removal_strategy': config.get('removal_strategy', 'remove_lowest_influence'),
                'use_distillation': config.get('use_distillation', False),
                'distillation_epochs': config.get('distillation_epochs', 200)
            }
            
            # Merge with provided model_params
            if 'model_params' in config:
                model_params.update(config['model_params'])
            
            self._update_status(experiment_id, 'running', 25, 'Training baseline model...')
            
            # Run experiments
            n_epochs = config.get('n_epochs', 500)
            n_remove_list = config.get('n_remove_percentages', list(range(1, 100, 5)))
            
            experiment_runner = ExperimentRunner(logger)
            
            results, scores, scores_raw, random_run_results = experiment_runner.run_experiments(
                X_train, y_train, X_test, y_test,
                X_holdout_validation, y_holdout_validation,
                preprocessor, model_params,
                n_remove_list, n_epochs,
                dataset_config=dataset_config
            )
            
            self._update_status(experiment_id, 'running', 90, 'Finalizing results...')
            
            # Store results
            # Include logger experiment directory in config so UI can load PNGs
            saved_config = {
                'dataset_name': dataset_name,
                'model_type': config.get('model_type'),
                'sample_size': len(X_train),
                'features': input_size,
                'n_remove_percentages': n_remove_list,
                'removal_strategy': config.get('removal_strategy'),
                'n_epochs': n_epochs,
                'experiment_dir': str(logger.get_experiment_dir())
            }

            self.active_experiments[experiment_id]['result'] = {
                'results': results,
                'influence_weights': scores,
                'scores_raw': scores_raw,
                'random_run_results': random_run_results,
                'config': saved_config,
                'execution_time': time.time() - self.active_experiments[experiment_id]['start_time']
            }
            
            self._update_status(experiment_id, 'completed', 100, 'Saving results to storage...')
            
            # Save results to persistent storage
            result = self.active_experiments[experiment_id]['result']
            try:
                config = result.get('config', {})
                influence_weights = result.get('influence_weights', {})
                scores_raw = result.get('scores_raw', {})

                # Save plots and results via logger (same behavior as main.py)
                try:
                    # Save aggregated results pickle and metadata
                    logger.save_results(result.get('results', {}), influence_weights, scores_raw, n_remove_list)
                except Exception:
                    pass

                try:
                    # Save influence distribution PNGs
                    plot_influence_distribution(scores_raw, "influence_scores", logger)
                except Exception as e_plot:
                    print(f"Warning: failed to save influence distribution plot: {e_plot}")

                try:
                    # Save results comparison PNG
                    plot_results_enhanced(result.get('results', {}), n_remove_list, logger, random_run_results=getattr(experiment_runner, 'random_run_results', None))
                except Exception as e_plot:
                    print(f"Warning: failed to save results comparison plot: {e_plot}")

                # Persist core experiment data to storage
                self.storage.save_experiment(
                    experiment_id,
                    config,
                    result.get('results', {}),
                    influence_weights,
                    scores_raw,
                    {'status': 'completed', 'saved_at': datetime.now().isoformat()}
                )

                self._update_status(experiment_id, 'completed', 100, 'Experiment completed successfully!')
            except Exception as save_err:
                print(f"Warning: Failed to save results to storage: {save_err}")
                self._update_status(experiment_id, 'completed', 100, 'Experiment completed (storage save failed)')
            
        except Exception as e:
            import traceback
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            self._update_status(experiment_id, 'failed', 0, error_msg)
            self.active_experiments[experiment_id]['error'] = error_msg
    
    def _update_status(self, experiment_id: str, status: str, progress: float, message: str):
        """Update experiment status"""
        if experiment_id in self.active_experiments:
            self.active_experiments[experiment_id].update({
                'status': status,
                'progress': progress,
                'message': message
            })
    
    def get_result(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Get experiment result"""
        exp_info = self.active_experiments.get(experiment_id)
        if exp_info:
            return exp_info.get('result')
        return None
    
    def get_error(self, experiment_id: str) -> Optional[str]:
        """Get experiment error"""
        exp_info = self.active_experiments.get(experiment_id)
        if exp_info:
            return exp_info.get('error')
        return None
