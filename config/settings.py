import torch

# ===== ВЫБОР ДАТАСЕТА =====
# Выбираемый датасет: 'zillow', 'adult', 'housing', 'wine', 'covertype', 'electric', 'mnist', 'imdb', 'cifar10'
CURRENT_DATASET = 'imdb'

# Глобальные флаги для отладки
DEBUG_MODE = False
EXPERIMENTS_BASE_DIR = "experiment_logs"
CACHE_DIR = "data_cache"
USE_CACHE = True

# Настройки вычислений
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
N_JOBS = 8
RANDOM_STATE = 42

# Настройки pyDVL
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
        'batch_size': 16,  # Для DataLoader в influence методах
        'influence_val_batch_size': 500,  # Батч по валидации при influences_from_factors (чтобы не создавать матрицу n_val×n_train в GPU)
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
        'influence_val_batch_size': 256,  # меньше из-за большого n_train/n_val и ограниченной GPU
        'lissa_params': {'scale': 15, 'damping': 0.2},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 15},
        'nystroem_params': {'rank': 15}
    },
    'electric': {
        'regularization': 1e-05,
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


# Оптимальные параметры для каждого датасета и модели
from .datasets.adult_config import ADULT_CONFIG
from .datasets.housing_config import HOUSING_CONFIG
from .datasets.wine_config import WINE_CONFIG
from .datasets.zillow_config import ZILLOW_CONFIG
from .datasets.covertype_config import COVERTYPE_CONFIG
from .datasets.electric_config import ELECTRIC_CONFIG
from .datasets.mnist_config import MNIST_CONFIG
from .datasets.imdb_config import IMDB_CONFIG
from .datasets.cifar10_config import CIFAR10_CONFIG

DATASET_MODEL_CONFIGS = {
    'adult': ADULT_CONFIG,
    'housing': HOUSING_CONFIG,
    'wine': WINE_CONFIG,
    'zillow': ZILLOW_CONFIG,
    'covertype': COVERTYPE_CONFIG,
    'electric': ELECTRIC_CONFIG,
    'mnist': MNIST_CONFIG,
    'imdb': IMDB_CONFIG,
    'cifar10': CIFAR10_CONFIG,
}

# Функция для получения конфигов модели для конкретного датасета
def get_model_config(dataset_name, model_type):
    """
    Получить конфигурацию модели для конкретного датасета.

    Args:
        dataset_name (str): Имя датасета ('adult', 'housing', 'wine', 'zillow')
        model_type (str): Тип модели ('lightgbm', 'xgboost', 'catboost', 'random_forest', 'pytorch')

    Returns:
        dict: Конфигурация модели для данного датасета
    """
    if dataset_name not in DATASET_MODEL_CONFIGS:
        raise ValueError(
            f"Unknown dataset: {dataset_name}. Available: {list(DATASET_MODEL_CONFIGS.keys())}"
        )

    if model_type not in DATASET_MODEL_CONFIGS[dataset_name]:
        raise ValueError(f"Unknown model type: {model_type}. Available: {list(DATASET_MODEL_CONFIGS[dataset_name].keys())}")

    return DATASET_MODEL_CONFIGS[dataset_name][model_type].copy()


MODEL_CONFIGS = DATASET_MODEL_CONFIGS

# Настройки дистилляции
DISTILLATION_CONFIG = {
    'use_distillation': True,
    'distillation_epochs': 500,  # Количество эпох для дистилляции
    'temperature': 2.0,  # Температура для дистилляции (пока не используется)
    'student_architecture': 'simple'  # Архитектура студенческой модели: 'simple' или 'improved'
}

# Настройки экспериментов
EXPERIMENT_CONFIG = {
    'test_size': 0.2,
    'val_size': 0.1,
    'n_epochs': 500,
    'sample_size_percentage': 10,
    'n_remove_list': list(range(1, 100, 2)),
    'n_random_runs': 1,
    'removal_strategies': ['remove_lowest_influence', 'remove_highest_influence']
}

# Настройки для synthetic_data экспериментов
SYNTHETIC_DATA_CONFIG = {
    'batch_size': 32,
    'learning_rate': 1e-3,
    'n_epochs': 10,
    'hidden_size': 50,
    'n_estimators': 50,
    'n_jobs': 1
}

__all__ = ['CURRENT_DATASET']