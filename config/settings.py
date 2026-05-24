import torch

# ===== ВЫБОР ДАТАСЕТА =====
# Выбираемый датасет: 'zillow', 'adult', 'housing', 'wine', 'covertype', 'electric', 'mnist', 'imdb', 'cifar10'
CURRENT_DATASET = 'zillow'

# ===== РЕЖИМ ОБУЧЕНИЯ (FIT MODE) =====
# 'normal'   — оптимальные гиперпараметры (по умолчанию)
# 'underfit' — намеренно слабая модель (мало ёмкости / мало эпох)
# 'overfit'  — намеренно переобученная модель (избыточная ёмкость / много эпох)
MODEL_FIT_MODE = 'normal'

# Переопределение числа эпох для PyTorch/дистилляции в режимах underfit/overfit.
# В режиме 'normal' используется EXPERIMENT_CONFIG['n_epochs'].
FIT_MODE_EPOCHS = {
    'underfit': 10,
    'overfit': 5000,
}

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
    'model_type': 'pytorch',  # lightgbm, xgboost, random_forest, pytorch, catboost
    'model_architecture': 'simple',  # pytorch: simple, improved, ft_transformer, ft_transformer_simple, cnn_small
    # Стратегии удаления для анализа influence-весов и вспомогательных скриптов.
    'removal_strategies': [
        # "lowest",
        # "highest",
        "random",
        "extremes",
        # "median",
        # "few_bad_then_random",
        # "few_median_then_random",
        # "few_good_then_random",
    ],
    # Классификация (binary / multiclass): True — доля удалений и ранжирование
    # influence (и loss-baseline) отдельно внутри каждого класса; False — глобально по всей train-выборке.
    'removal_per_class': False,
    # Регрессия: True — то же по квантильным стратам целевой переменной (равные частоты по y).
    'removal_stratify_target': False,
    'removal_stratify_n_bins': 10,
}

# Методы влияния/valuation: какие считаются при запуске (influence/methods.py)
# valuation_methods: LOO, DataShapley, BetaShapley, Banzhaf, TMCShapley, KNNShapley, DataOOB, LeastCore
# influence_methods: для PyTorch — Influence, ArnoldiInfluence, CgInfluence, LissaInfluence, NystroemSketchInfluence
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
    'n_remove_linspace': (1, 90, 10),
    'n_random_runs': 1,
    # Число переобучений PyTorch для каждой точки removal: берётся лучший из n запусков.
    # Устраняет нестабильность из-за плохой инициализации ("kill bad runs").
    # 1 = без повторов (старое поведение); 3 = хороший баланс качества и скорости.
    'n_retrain_runs': 3,
    # Дополнительные baselines по loss. Оставьте только нужные:
    # loss_high = удалять сначала объекты с наибольшим loss
    # loss_low = удалять сначала объекты с наименьшим loss
    'loss_removal_methods': [
        'loss_high',
        # 'loss_low'
    ],
    # CatBoost native object importance (LossFunctionChange).
    # Если model_type='catboost' — использует обученную модель напрямую (без mismatch).
    # Для других моделей — обучает proxy CatBoost для вычисления importance.
    'use_catboost_influence': False,
    # Показывать N примеров с наибольшими и наименьшими influence-весами в консоли и логах.
    # False или 0 — отключено.
    'show_top_bottom_influence': 10,
}

# Эвристика для removal_adaptive_model: снижение ёмкости модели на меньшем train.
REMOVAL_ADAPTIVE_CONFIG = {
    # Доля оставшихся примеров (len(X_sub) / len(X_train_full)): ниже порога PyTorch
    # переключается на архитектуру simple (если в model_params есть ключ 'simple').
    'keep_ratio_threshold': 0.5,
    # Множитель ёмкости деревьев и ширины слоёв PyTorch MLP: max(min_scale, sqrt(keep_ratio)).
    'min_scale': 0.3,
    # Нижняя граница ширины скрытого слоя при adaptive (PyTorch simple/improved).
    'pytorch_min_layer_width': 4,
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
from .datasets.adult_config import ADULT_CONFIG, ADULT_UNDERFIT_CONFIG, ADULT_OVERFIT_CONFIG
from .datasets.housing_config import HOUSING_CONFIG, HOUSING_UNDERFIT_CONFIG, HOUSING_OVERFIT_CONFIG
from .datasets.wine_config import WINE_CONFIG, WINE_UNDERFIT_CONFIG, WINE_OVERFIT_CONFIG
from .datasets.zillow_config import ZILLOW_CONFIG, ZILLOW_UNDERFIT_CONFIG, ZILLOW_OVERFIT_CONFIG
from .datasets.covertype_config import COVERTYPE_CONFIG, COVERTYPE_UNDERFIT_CONFIG, COVERTYPE_OVERFIT_CONFIG
from .datasets.electric_config import ELECTRIC_CONFIG, ELECTRIC_UNDERFIT_CONFIG, ELECTRIC_OVERFIT_CONFIG
from .datasets.mnist_config import MNIST_CONFIG, MNIST_UNDERFIT_CONFIG, MNIST_OVERFIT_CONFIG
from .datasets.imdb_config import IMDB_CONFIG, IMDB_UNDERFIT_CONFIG, IMDB_OVERFIT_CONFIG
from .datasets.cifar10_config import CIFAR10_CONFIG, CIFAR10_UNDERFIT_CONFIG, CIFAR10_OVERFIT_CONFIG

DATASET_MODEL_CONFIGS = {
    'adult': {
        'normal': ADULT_CONFIG,
        'underfit': ADULT_UNDERFIT_CONFIG,
        'overfit': ADULT_OVERFIT_CONFIG,
    },
    'housing': {
        'normal': HOUSING_CONFIG,
        'underfit': HOUSING_UNDERFIT_CONFIG,
        'overfit': HOUSING_OVERFIT_CONFIG,
    },
    'wine': {
        'normal': WINE_CONFIG,
        'underfit': WINE_UNDERFIT_CONFIG,
        'overfit': WINE_OVERFIT_CONFIG,
    },
    'zillow': {
        'normal': ZILLOW_CONFIG,
        'underfit': ZILLOW_UNDERFIT_CONFIG,
        'overfit': ZILLOW_OVERFIT_CONFIG,
    },
    'covertype': {
        'normal': COVERTYPE_CONFIG,
        'underfit': COVERTYPE_UNDERFIT_CONFIG,
        'overfit': COVERTYPE_OVERFIT_CONFIG,
    },
    'electric': {
        'normal': ELECTRIC_CONFIG,
        'underfit': ELECTRIC_UNDERFIT_CONFIG,
        'overfit': ELECTRIC_OVERFIT_CONFIG,
    },
    'mnist': {
        'normal': MNIST_CONFIG,
        'underfit': MNIST_UNDERFIT_CONFIG,
        'overfit': MNIST_OVERFIT_CONFIG,
    },
    'imdb': {
        'normal': IMDB_CONFIG,
        'underfit': IMDB_UNDERFIT_CONFIG,
        'overfit': IMDB_OVERFIT_CONFIG,
    },
    'cifar10': {
        'normal': CIFAR10_CONFIG,
        'underfit': CIFAR10_UNDERFIT_CONFIG,
        'overfit': CIFAR10_OVERFIT_CONFIG,
    },
}

# Функция для получения конфигов модели для конкретного датасета
def get_model_config(dataset_name, model_type):
    """
    Получить конфигурацию модели для конкретного датасета с учётом MODEL_FIT_MODE.

    Args:
        dataset_name (str): Имя датасета ('adult', 'housing', 'wine', 'zillow', ...)
        model_type (str): Тип модели ('lightgbm', 'xgboost', 'catboost', 'random_forest', 'pytorch')

    Returns:
        dict: Конфигурация модели для данного датасета и текущего fit-режима
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

# Настройки дистилляции
DISTILLATION_CONFIG = {
    'use_distillation': False,
    'distillation_epochs': 500,  # Количество эпох для дистилляции
    'temperature': 2.0,  # Температура для дистилляции
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