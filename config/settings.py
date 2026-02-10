import torch

# ===== ВЫБОР ДАТАСЕТА =====
# Выбираемый датасет: 'zillow', 'adult', 'housing', 'wine'
CURRENT_DATASET = 'zillow'  # Можно менять для работы с разными датасетами

# Глобальные флаги для отладки
DEBUG_MODE = False
EXPERIMENTS_BASE_DIR = "experiment_logs"
CACHE_DIR = "data_cache"  # Папка для кэширования предобработанных данных
USE_CACHE = True  # Использовать ли кэш предобработанных данных

# Настройки вычислений
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
N_JOBS = 8
RANDOM_STATE = 39

# Настройки pyDVL
PYDVL_CONFIG = {
    'n_steps': 10,
    'rtol': 0.01,
    'max_updates': 1000,
    'beta_shapley_params': {'alpha': 0.1, 'beta': 0.1},
    # Настройки для новых методов
    'tmc_shapley_params': {'n_samples': 10},
    'knn_shapley_params': {'n_neighbors': 5},
    'banzhaf_params': {'n_samples': 10},
    'least_core_params': {'epsilon': 0.1, 'n_samples': 10},
    # Настройки для influence методов
    'influence_params': {
        'regularization': 1e-06,
        'batch_size': 16,  # Для DataLoader в influence методах
        'lissa_params': {'scale': 10, 'damping': 0.1},
        'cg_params': {'maxiter': 100, 'tolerance': 1e-2},
        'arnoldi_params': {'rank': 10},
        'nystroem_params': {'rank': 10}
    }
}

# Оптимальные параметры для каждого датасета и модели
# Подобраны на основе характеристик датасета и типа задачи
# Per-dataset configs are stored in separate modules under config/datasets
from .datasets.adult_config import ADULT_CONFIG
from .datasets.housing_config import HOUSING_CONFIG
from .datasets.wine_config import WINE_CONFIG
from .datasets.zillow_config import ZILLOW_CONFIG

DATASET_MODEL_CONFIGS = {
    'adult': ADULT_CONFIG,
    'housing': HOUSING_CONFIG,
    'wine': WINE_CONFIG,
    'zillow': ZILLOW_CONFIG
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
        raise ValueError(f"Unknown dataset: {dataset_name}. Available: {list(DATASET_MODEL_CONFIGS.keys())}")
    
    if model_type not in DATASET_MODEL_CONFIGS[dataset_name]:
        raise ValueError(f"Unknown model type: {model_type}. Available: {list(DATASET_MODEL_CONFIGS[dataset_name].keys())}")
    
    return DATASET_MODEL_CONFIGS[dataset_name][model_type].copy()

# Legacy MODEL_CONFIGS (для обратной совместимости) - использует конфиг для 'housing' по умолчанию
MODEL_CONFIGS = DATASET_MODEL_CONFIGS['housing']

# Настройки дистилляции
DISTILLATION_CONFIG = {
    'use_distillation': True,
    'distillation_epochs': 200,  # Количество эпох для дистилляции
    'temperature': 2.0,  # Температура для дистилляции (пока не используется)
    'student_architecture': 'simple'  # Архитектура студенческой модели: 'simple' или 'improved'
}

# Настройки экспериментов
EXPERIMENT_CONFIG = {
    'test_size': 0.2,
    'val_size': 0.1,
    'n_epochs': 500,
    'sample_size_percentage': 1,
    'n_remove_list': list(range(1, 100, 2)),
    'n_random_runs': 3,
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

# Экспортируем CURRENT_DATASET для удобства
__all__ = ['CURRENT_DATASET']