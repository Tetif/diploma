"""
Configuration for Zillow dataset
Regression, ~90K samples, 50+ features - large dataset.
Усиленные гиперпараметры для сложной задачи logerror.
"""

RANDOM_STATE = 42

ZILLOW_CONFIG = {
    'lightgbm': {
        'objective': 'regression',
        'metric': 'mae',
        'num_leaves': 255,
        'learning_rate': 0.03,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.7,
        'bagging_freq': 5,
        'min_data_in_leaf': 15,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'reg:squarederror',
        'eval_metric': 'mae',
        'max_depth': 10,
        'learning_rate': 0.03,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'min_child_weight': 5,
        'gamma': 1,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 300,
        'learning_rate': 0.05,
        'depth': 8,
        'loss_function': 'MAE',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 200,
        'max_depth': 25,
        'min_samples_split': 8,
        'min_samples_leaf': 3,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'pytorch': {
        'simple': {
            'layers': [256, 128, 64, 32],
            'dropout': 0.3,
            'learning_rate': 0.001
        },
        'improved': {
            'layers': [256, 128, 64, 32],
            'batch_norm': True,
            'dropout': [0.3, 0.25, 0.2],
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
            'd_model': 32,
            'nhead': 4,
            'num_layers': 2,
            'dim_feedforward': 128,
            'dropout': 0.1,
            'learning_rate': 0.001
        }
    }
}

# ---------- UNDERFIT: слишком простая модель ----------
ZILLOW_UNDERFIT_CONFIG = {
    'lightgbm': {
        'objective': 'regression',
        'metric': 'mae',
        'num_leaves': 4,
        'learning_rate': 0.5,
        'n_estimators': 5,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.7,
        'bagging_freq': 5,
        'min_data_in_leaf': 100,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'reg:squarederror',
        'eval_metric': 'mae',
        'max_depth': 1,
        'learning_rate': 0.5,
        'n_estimators': 5,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'min_child_weight': 50,
        'gamma': 1,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 5,
        'learning_rate': 0.5,
        'depth': 1,
        'loss_function': 'MAE',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 3,
        'max_depth': 1,
        'min_samples_split': 8,
        'min_samples_leaf': 50,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'pytorch': {
        'simple': {
            'layers': [4],
            'dropout': 0.8,
            'learning_rate': 0.0001
        },
        'improved': {
            'layers': [8, 4],
            'batch_norm': True,
            'dropout': [0.8, 0.7],
            'learning_rate': 0.0001
        },
        'ft_transformer': {
            'd_model': 4,
            'nhead': 1,
            'num_layers': 1,
            'dim_feedforward': 8,
            'dropout': 0.5,
            'learning_rate': 0.0001
        },
        'ft_transformer_simple': {
            'd_model': 4,
            'nhead': 1,
            'num_layers': 1,
            'dim_feedforward': 8,
            'dropout': 0.5,
            'learning_rate': 0.0001
        }
    }
}

# ---------- OVERFIT: избыточно сложная модель ----------
ZILLOW_OVERFIT_CONFIG = {
    'lightgbm': {
        'objective': 'regression',
        'metric': 'mae',
        'num_leaves': 1024,
        'learning_rate': 0.3,
        'n_estimators': 2000,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.7,
        'bagging_freq': 5,
        'min_data_in_leaf': 1,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'reg:squarederror',
        'eval_metric': 'mae',
        'max_depth': 30,
        'learning_rate': 0.3,
        'n_estimators': 2000,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'min_child_weight': 1,
        'gamma': 0,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 3000,
        'learning_rate': 0.3,
        'depth': 16,
        'loss_function': 'MAE',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 2000,
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'pytorch': {
        'simple': {
            'layers': [1024, 512, 256, 128],
            'dropout': 0.0,
            'learning_rate': 0.01
        },
        'improved': {
            'layers': [1024, 512, 256, 128],
            'batch_norm': True,
            'dropout': [0.0, 0.0, 0.0],
            'learning_rate': 0.01
        },
        'ft_transformer': {
            'd_model': 128,
            'nhead': 8,
            'num_layers': 6,
            'dim_feedforward': 512,
            'dropout': 0.0,
            'learning_rate': 0.01
        },
        'ft_transformer_simple': {
            'd_model': 128,
            'nhead': 8,
            'num_layers': 6,
            'dim_feedforward': 512,
            'dropout': 0.0,
            'learning_rate': 0.01
        }
    }
}
