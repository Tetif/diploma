import torch

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

# Настройки моделей
MODEL_CONFIGS = {
    'lightgbm': {
        'objective': 'regression',
        'metric': 'mae',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'reg:squarederror',
        'eval_metric': 'mae',
        'max_depth': 6,
        'learning_rate': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 100,
        'learning_rate': 0.05,
        'depth': 10,
        'loss_function': 'MAE',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'pytorch': {
        'simple': {
            'layers': [16, 8, 4],
            'dropout': 0.2,
            'learning_rate': 0.001
        },
    # 'pytorch': {
    #     'simple': {
    #         'layers': [128, 64, 32],
    #         'dropout': 0.2,
    #         'learning_rate': 0.001
    #     },
        'improved': {
            'layers': [32, 16, 8, 4],
            'batch_norm': True,
            'dropout': [0.3, 0.3, 0.2],
            'learning_rate': 0.001
        },
        'ft_transformer': {
            'd_model': 64,
            'nhead': 8,
            'num_layers': 3,
            'dim_feedforward': 256,
            'dropout': 0.1,
            'learning_rate': 0.001
        },
        'ft_transformer_simple': {
            'd_model': 16,
            'nhead': 4,
            'num_layers': 1,
            'dim_feedforward': 64,
            'dropout': 0.1,
            'learning_rate': 0.001
        }
    }
}

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
    'sample_size_percentage': 100.0,
    'n_remove_list': list(range(1, 100, 2)),
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