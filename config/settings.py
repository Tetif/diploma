import torch

# ===== ВЫБОР ДАТАСЕТА =====
# Выбираемый датасет: 'zillow', 'adult', 'housing', 'wine', 'covertype', 'electric', 'mnist', 'imdb', 'cifar10'
CURRENT_DATASET = 'electric'

# Глобальные флаги для отладки
DEBUG_MODE = False
EXPERIMENTS_BASE_DIR = "experiment_logs"
CACHE_DIR = "data_cache"
USE_CACHE = True

# Настройки вычислений
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
N_JOBS = 8
RANDOM_STATE = 42

# Модель и стратегии удаления для main/экспериментов (единая точка настройки)
MODEL_RUN_CONFIG = {
    'model_type': 'xgboost',  # lightgbm, xgboost, random_forest, pytorch, catboost
    'model_architecture': 'simple',  # для pytorch: simple, improved, ft_transformer
    # Стратегии удаления для анализа influence-весов и вспомогательных скриптов.
    'removal_strategies': [
        "lowest",
        # "highest",
        "random",
        # "extremes",
        # "median",
        # "few_bad_then_random",
        # "few_median_then_random",
        # "few_good_then_random",
    ],
}

# Методы влияния/valuation: какие считаются при запуске (influence/methods.py)
# valuation_methods: LOO, DataShapley, BetaShapley, Banzhaf, TMCShapley, KNNShapley, DataOOB, LeastCore
# influence_methods: для PyTorch — Influence, ArnoldiInfluence, CgInfluence, LissaInfluence, NystroemSketchInfluence
INFLUENCE_METHODS_CONFIG = {
    'valuation_methods': [
        # 'LOO',
        # 'DataShapley',
        # 'BetaShapley',
        # 'Banzhaf',
        # 'TMCShapley',
        # 'KNNShapley',
        # 'DataOOB',
        # 'LeastCore'
                          ],
    'influence_methods': [
        'Influence',
        # 'ArnoldiInfluence',
        # 'CgInfluence', # не использовать!!! ОЧЕНЬ ДОЛГО РАБОТАЕТ
        'LissaInfluence',
        'NystroemSketchInfluence'
        ],
}

# Настройки экспериментов
EXPERIMENT_CONFIG = {
    'test_size': 0.2,
    'val_size': 0.1,
    'n_epochs': 500,
    'sample_size_percentage': 10,
    # Проценты удаления: (start, stop, num) для np.linspace — единый источник для main и вспомогательных скриптов
    'n_remove_linspace': (1, 80, 9),
    'n_random_runs': 3,
    # Дополнительные baselines по loss. Оставьте только нужные:
    # loss_high = удалять сначала объекты с наибольшим loss
    # loss_low = удалять сначала объекты с наименьшим loss
    'loss_removal_methods': [
        'loss_high',
        'loss_low'
    ],
}

# Стратегии удаления для анализа сохранённых influence-весов (scripts/plot_removal_from_weights.py)
# Единственный источник — список в MODEL_RUN_CONFIG.
REMOVAL_STRATEGIES = MODEL_RUN_CONFIG['removal_strategies']

# Метрики качества по типу задачи.
# Меняйте значения здесь, чтобы переключать основную метрику эксперимента и графиков.
# Поддерживаемые варианты:
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


def get_selected_metric(task_type, available_metrics=None):
    """Вернуть выбранную метрику для типа задачи с валидацией по датасету."""
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
    """Метаданные метрики для подписей графиков и логики сравнения."""
    if metric_name not in METRIC_METADATA:
        raise ValueError(
            f"Unknown metric: {metric_name}. Available: {list(METRIC_METADATA.keys())}"
        )
    return METRIC_METADATA[metric_name].copy()


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



def get_n_remove_list():
    """Список процентов удаления из EXPERIMENT_CONFIG['n_remove_linspace'] (start, stop, num)."""
    import numpy as np
    params = EXPERIMENT_CONFIG.get('n_remove_linspace', (1, 99, 33))
    return np.linspace(params[0], params[1], params[2], dtype=int).tolist()


def get_selected_loss_removal_methods():
    """Вернуть включённые loss-стратегии удаления в формате имён методов эксперимента."""
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

# Настройки для synthetic_data экспериментов
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
    'MODEL_RUN_CONFIG',
    'INFLUENCE_METHODS_CONFIG',
    'METRIC_CONFIG',
    'METRIC_METADATA',
    'get_selected_metric',
    'get_metric_metadata',
    'get_n_remove_list',
    'get_selected_loss_removal_methods',
]