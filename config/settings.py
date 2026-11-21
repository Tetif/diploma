import os

import torch

# ===== DATASET SELECTION =====
# Selected dataset: 'zillow', 'adult', 'housing', 'wine', 'covertype', 'electric', 'mnist', 'imdb', 'cifar10'
CURRENT_DATASET = 'adult'  # zillow has almost no signal (see AUDIT.md section 4)

# ===== FIT MODE =====
# 'normal'   - optimal hyperparameters (default)
# 'underfit' - deliberately weak model (low capacity / few epochs)
# 'overfit'  - deliberately overfitted model (excess capacity / many epochs)
MODEL_FIT_MODE = 'normal'

# Epoch override for PyTorch/distillation in the underfit/overfit modes.
# The 'normal' mode uses EXPERIMENT_CONFIG['n_epochs'].
FIT_MODE_EPOCHS = {
    'underfit': 10,
    'overfit': 5000,
}

# Global debug flags
DEBUG_MODE = False
EXPERIMENTS_BASE_DIR = "experiment_logs"
CACHE_DIR = "data_cache"
USE_CACHE = True

# Compute settings
# Overridden by the environment variables DIPLOMA_DEVICE / DIPLOMA_N_JOBS (run_study.py, run_overnight.ps1).
DEVICE = os.environ.get('DIPLOMA_DEVICE') or ('cuda' if torch.cuda.is_available() else 'cpu')
N_JOBS = int(os.environ.get('DIPLOMA_N_JOBS', 8))
RANDOM_STATE = 42

# Model and removal strategies for main/experiments (single place to configure)
MODEL_RUN_CONFIG = {
    'model_type': 'pytorch',  # lightgbm, xgboost, random_forest, pytorch, catboost
    'model_architecture': 'simple',  # pytorch: simple, improved, ft_transformer, ft_transformer_simple, cnn_small
    # Removal strategies for the analysis of influence weights and helper scripts.
    'removal_strategies': [
        # [AUDIT-FIX M3] lowest/highest are enabled: they are what tests the hypothesis.
        # 'extremes' mixes harmful and helpful points (the effects cancel out) - disabled.
        "lowest",
        "highest",
        "random",
        # "extremes",
        # "median",
        # "few_bad_then_random",
        # "few_median_then_random",
        # "few_good_then_random",
    ],
    # Classification (binary / multiclass): True - the removal share and the ranking of
    # influence (and the loss baseline) are done separately within each class; False - globally over the whole train set.
    'removal_per_class': False,
    # Regression: True - the same over quantile strata of the target (equal frequencies over y).
    'removal_stratify_target': False,
    'removal_stratify_n_bins': 10,
}

# Influence/valuation methods computed in a run (influence/methods.py)
# valuation_methods: LOO, DataShapley, BetaShapley, Banzhaf, TMCShapley, KNNShapley, DataOOB, LeastCore
# influence_methods: for PyTorch - Influence, ArnoldiInfluence, CgInfluence, LissaInfluence, NystroemSketchInfluence
INFLUENCE_METHODS_CONFIG = {
    'valuation_methods': [
        'LOO',
        # 'DataShapley',
        # 'BetaShapley',
        # 'Banzhaf',
        'TMCShapley',
        # 'KNNShapley',
        # 'DataOOB',
        # 'LeastCore'
                          ],
    'influence_methods': [
        'Influence',
        # 'ArnoldiInfluence',
        # 'CgInfluence', # do not use!!! VERY SLOW
        'LissaInfluence',
        'NystroemSketchInfluence'
        ],
}

# Experiment settings
EXPERIMENT_CONFIG = {
    'test_size': 0.2,
    'val_size': 0.1,
    'n_epochs': 500,
    'sample_size_percentage': 10,
    # Removal percentages: (start, stop, num) for np.linspace - single source for main and helper scripts
    'n_remove_linspace': (1, 90, 10),
    'n_random_runs': 5,  # [AUDIT-FIX M2] was 1 - the spread of random removal could not be estimated
    # Number of PyTorch retrains for each removal point: the best of n runs is taken.
    # Removes instability caused by a bad initialization ("kill bad runs").
    # 1 = no repeats (old behaviour); 3 = a good quality/speed trade-off.
    'n_retrain_runs': 3,
    # [AUDIT-FIX M1] How to combine n_retrain_runs runs:
    #   'mean'         - mean over seeds (+ final_metric_std), holdout is not used for selection;
    #   'best_holdout' - old behaviour: best of n on holdout (optimistically biased).
    'retrain_aggregate': 'mean',
    # [AUDIT-FIX B1] How many full-batch epochs the PyTorch model trains on each subset
    # inside the pyDVL valuation methods (LOO/TMC/...). Previously it was effectively 5.
    'valuation_epochs': 200,
    # Additional loss baselines. Keep only the ones you need:
    # loss_high = remove the samples with the highest loss first
    # loss_low = remove the samples with the lowest loss first
    'loss_removal_methods': [
        'loss_high',
        # 'loss_low'
    ],
    # CatBoost native object importance (LossFunctionChange).
    # If model_type='catboost' - uses the trained model directly (no mismatch).
    # For other models - trains a proxy CatBoost to compute the importance.
    'use_catboost_influence': False,
    # Show N samples with the highest and lowest influence weights in the console and logs.
    # False or 0 - disabled.
    'show_top_bottom_influence': 10,
}

# Heuristic for removal_adaptive_model: reduce model capacity on a smaller train set.
REMOVAL_ADAPTIVE_CONFIG = {
    # Share of the remaining samples (len(X_sub) / len(X_train_full)): below the threshold PyTorch
    # switches to the simple architecture (if model_params has a 'simple' key).
    'keep_ratio_threshold': 0.5,
    # Multiplier of tree capacity and PyTorch MLP layer width: max(min_scale, sqrt(keep_ratio)).
    'min_scale': 0.3,
    # Lower bound of the hidden layer width in adaptive mode (PyTorch simple/improved).
    'pytorch_min_layer_width': 4,
}

# Removal strategies for the analysis of saved influence weights (archive/scripts/plot_removal_from_weights.py)
# The only source is the list in MODEL_RUN_CONFIG.
REMOVAL_STRATEGIES = MODEL_RUN_CONFIG['removal_strategies']

# Quality metrics per task type.
# Change the values here to switch the main metric of the experiment and the plots.
# Supported options:
# regression: mae | rmse | r2
# binary_classification: accuracy | f1 | precision | recall
# multiclass_classification: accuracy | f1_weighted | f1_macro
METRIC_CONFIG = {
    'regression': 'mae',
    'binary_classification': 'f1',
    'multiclass_classification': 'accuracy',
}

METRIC_METADATA = {
    'mae': {
        'short_label_ru': 'MAE',
        'label_ru': 'Средняя абсолютная ошибка',
        'higher_is_better': False,
    },
    'rmse': {
        'short_label_ru': 'RMSE',
        'label_ru': 'Корень из среднеквадратичной ошибки',
        'higher_is_better': False,
    },
    'r2': {
        'short_label_ru': 'R²',
        'label_ru': 'Коэффициент детерминации',
        'higher_is_better': True,
    },
    'accuracy': {
        'short_label_ru': 'Accuracy',
        'label_ru': 'Точность классификации',
        'higher_is_better': True,
    },
    'f1': {
        'short_label_ru': 'F1',
        'label_ru': 'F1-мера',
        'higher_is_better': True,
    },
    'f1_weighted': {
        'short_label_ru': 'Weighted F1',
        'label_ru': 'Взвешенная F1-мера',
        'higher_is_better': True,
    },
    'f1_macro': {
        'short_label_ru': 'Macro F1',
        'label_ru': 'Макро F1-мера',
        'higher_is_better': True,
    },
    'precision': {
        'short_label_ru': 'Precision',
        'label_ru': 'Точность (precision)',
        'higher_is_better': True,
    },
    'recall': {
        'short_label_ru': 'Recall',
        'label_ru': 'Полнота (recall)',
        'higher_is_better': True,
    },
}

# pyDVL settings
PYDVL_CONFIG = {
    'n_steps': 10,
    'rtol': 0.01,
    'max_updates': 1000,
    'beta_shapley_params': {'alpha': 0.1, 'beta': 0.1},

    'tmc_shapley_params': {'n_samples': 10},
    'knn_shapley_params': {'n_neighbors': 5},
    'banzhaf_params': {'n_samples': 10},
    'least_core_params': {'epsilon': 0.1, 'n_samples': 10},

    'influence_params': {
        'regularization': 1e-06,
        'batch_size': 16,  # For the DataLoader in the influence methods
        'influence_val_batch_size': 500,  # Validation batch for influences_from_factors (so as not to build an n_val x n_train matrix on the GPU)
        'lissa_params': {'scale': 10, 'damping': 0.1},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 10},
        'nystroem_params': {'rank': 10}
    }
}

# ===== DATASET-SPECIFIC INFLUENCE PARAMETERS =====
DATASET_INFLUENCE_PARAMS = {
    'housing': {
        'regularization': 1e-04,
        'batch_size': 16,
        'lissa_params': {'scale': 25, 'damping': 0.3},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 10},
        'nystroem_params': {'rank': 10}
    },
    'adult': {
        'regularization': 1e-05,
        'batch_size': 16,
        'lissa_params': {'scale': 15, 'damping': 0.2},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 10},
        'nystroem_params': {'rank': 10}
    },
    'wine': {
        'regularization': 1e-04,
        'batch_size': 8,
        'lissa_params': {'scale': 30, 'damping': 0.4},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 8},
        'nystroem_params': {'rank': 8}
    },
    'zillow': {
        'regularization': 1e-06,
        'batch_size': 32,
        'lissa_params': {'scale': 10, 'damping': 0.1},
        'cg_params': {'maxiter': 150, 'tolerance': 1e-3},
        'arnoldi_params': {'rank': 20},
        'nystroem_params': {'rank': 20}
    },
    'covertype': {
        'regularization': 1e-05,
        'batch_size': 32,
        'influence_val_batch_size': 256,  # smaller because of the large n_train/n_val and limited GPU
        'lissa_params': {'scale': 15, 'damping': 0.2},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 15},
        'nystroem_params': {'rank': 15}
    },
    'electric': {
        'regularization': 1e-06,
        'batch_size': 32,
        'influence_val_batch_size': 256,
        'lissa_params': {'scale': 15, 'damping': 0.2},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 10},
        'nystroem_params': {'rank': 10}
    },
    'mnist': {
        'regularization': 1e-05,
        'batch_size': 64,
        'lissa_params': {'scale': 10, 'damping': 0.1},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 20},
        'nystroem_params': {'rank': 20}
    },
    'imdb': {
        'regularization': 1e-05,
        'batch_size': 32,
        'lissa_params': {'scale': 15, 'damping': 0.2},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 15},
        'nystroem_params': {'rank': 15}
    },
    'cifar10': {
        'regularization': 1e-05,
        'batch_size': 32,
        'influence_val_batch_size': 256,
        'lissa_params': {'scale': 10, 'damping': 0.1},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 15},
        'nystroem_params': {'rank': 15}
    }
}

def get_influence_params(dataset_name):
    from copy import deepcopy
    if dataset_name not in DATASET_INFLUENCE_PARAMS:
        return deepcopy(PYDVL_CONFIG['influence_params'])
    return deepcopy(DATASET_INFLUENCE_PARAMS[dataset_name])


def get_selected_metric(task_type, available_metrics=None):
    """Return the selected metric for the task type, validated against the dataset."""
    selected_metric = METRIC_CONFIG.get(task_type)
    if selected_metric is None:
        raise ValueError(
            f"Unknown task type for metric selection: {task_type}. "
            f"Available: {list(METRIC_CONFIG.keys())}"
        )

    if available_metrics and selected_metric not in available_metrics:
        raise ValueError(
            f"Metric '{selected_metric}' is not available for task '{task_type}'. "
            f"Available metrics: {available_metrics}"
        )

    return selected_metric


def get_metric_metadata(metric_name):
    """Metric metadata for plot labels and comparison logic."""
    if metric_name not in METRIC_METADATA:
        raise ValueError(
            f"Unknown metric: {metric_name}. Available: {list(METRIC_METADATA.keys())}"
        )
    return METRIC_METADATA[metric_name].copy()


# Model hyperparameters for each dataset and fit mode (normal/underfit/overfit)
# live in config/model_params/<dataset>.json (previously 9 files config/datasets/*_config.py).
from .model_params import load_all_model_params

DATASET_MODEL_CONFIGS = load_all_model_params()

# Function that returns the model config for a given dataset
def get_model_config(dataset_name, model_type):
    """
    Get the model configuration for a given dataset, taking MODEL_FIT_MODE into account.

    Args:
        dataset_name (str): Dataset name ('adult', 'housing', 'wine', 'zillow', ...)
        model_type (str): Model type ('lightgbm', 'xgboost', 'catboost', 'random_forest', 'pytorch')

    Returns:
        dict: Model configuration for this dataset and the current fit mode
    """
    if dataset_name not in DATASET_MODEL_CONFIGS:
        raise ValueError(
            f"Unknown dataset: {dataset_name}. Available: {list(DATASET_MODEL_CONFIGS.keys())}"
        )

    dataset_configs = DATASET_MODEL_CONFIGS[dataset_name]
    fit_config = dataset_configs.get(MODEL_FIT_MODE, dataset_configs['normal'])

    if model_type not in fit_config:
        raise ValueError(
            f"Unknown model type: {model_type}. "
            f"Available: {list(fit_config.keys())}"
        )

    return fit_config[model_type].copy()


MODEL_CONFIGS = DATASET_MODEL_CONFIGS

# Distillation settings
DISTILLATION_CONFIG = {
    'use_distillation': False,
    'distillation_epochs': 500,  # Number of distillation epochs
    'temperature': 2.0,  # Distillation temperature
    'student_architecture': 'simple'  # Student model architecture: 'simple' or 'improved'
}



def get_n_remove_list():
    """List of removal percentages from EXPERIMENT_CONFIG['n_remove_linspace'] (start, stop, num)."""
    import numpy as np
    params = EXPERIMENT_CONFIG.get('n_remove_linspace', (1, 99, 33))
    return np.linspace(params[0], params[1], params[2], dtype=int).tolist()


def get_selected_loss_removal_methods():
    """Return the enabled loss removal strategies as experiment method names."""
    configured_methods = EXPERIMENT_CONFIG.get('loss_removal_methods', ['loss_high', 'loss_low']) or []
    method_mapping = {
        'loss_high': 'LossHigh',
        'loss_low': 'LossLow',
    }
    invalid_methods = [method for method in configured_methods if method not in method_mapping]
    if invalid_methods:
        raise ValueError(
            f"Unknown loss removal methods: {invalid_methods}. "
            f"Available: {list(method_mapping.keys())}"
        )

    selected_methods = []
    for method in configured_methods:
        mapped_name = method_mapping[method]
        if mapped_name not in selected_methods:
            selected_methods.append(mapped_name)
    return selected_methods

# Settings for the synthetic_data experiments (code in archive/synthetic_data)
SYNTHETIC_DATA_CONFIG = {
    'batch_size': 32,
    'learning_rate': 1e-3,
    'n_epochs': 10,
    'hidden_size': 50,
    'n_estimators': 50,
    'n_jobs': 1
}

__all__ = [
    'CURRENT_DATASET',
    'MODEL_FIT_MODE',
    'FIT_MODE_EPOCHS',
    'MODEL_RUN_CONFIG',
    'INFLUENCE_METHODS_CONFIG',
    'METRIC_CONFIG',
    'METRIC_METADATA',
    'get_selected_metric',
    'get_metric_metadata',
    'get_n_remove_list',
    'get_selected_loss_removal_methods',
]