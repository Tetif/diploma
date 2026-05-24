"""
Configuration for Covertype dataset
Multiclass classification, ~581K samples, 54 features
"""

RANDOM_STATE = 42

COVERTYPE_CONFIG = {
    'lightgbm': {
        'objective': 'multiclass',
        'num_class': 7,
        'metric': 'multi_logloss',
        'num_leaves': 127,
        'learning_rate': 0.05,
        'n_estimators': 800,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'min_data_in_leaf': 20,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'multi:softmax',
        'num_class': 7,
        'eval_metric': 'mlogloss',
        'max_depth': 10,
        'learning_rate': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 5,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 800,
        'learning_rate': 0.05,
        'depth': 8,
        'loss_function': 'MultiClass',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 20,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'pytorch': {
        'simple': {
            'layers': [128, 64],
            'dropout': 0.2,
            'learning_rate': 0.002
        },
        'improved': {
            'layers': [256, 128, 64],
            'batch_norm': True,
            'dropout': [0.25, 0.2, 0.15],
            'learning_rate': 0.001
        },
        'ft_transformer': {
            'd_model': 32,
            'nhead': 4,
            'num_layers': 2,
            'dim_feedforward': 128,
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

# ---------- UNDERFIT: слишком простая модель ----------
COVERTYPE_UNDERFIT_CONFIG = {
    'lightgbm': {
        'objective': 'multiclass',
        'num_class': 7,
        'metric': 'multi_logloss',
        'num_leaves': 4,
        'learning_rate': 0.5,
        'n_estimators': 5,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'min_data_in_leaf': 100,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'multi:softmax',
        'num_class': 7,
        'eval_metric': 'mlogloss',
        'max_depth': 1,
        'learning_rate': 0.5,
        'n_estimators': 5,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 50,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 5,
        'learning_rate': 0.5,
        'depth': 1,
        'loss_function': 'MultiClass',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 3,
        'max_depth': 1,
        'min_samples_split': 5,
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
COVERTYPE_OVERFIT_CONFIG = {
    'lightgbm': {
        'objective': 'multiclass',
        'num_class': 7,
        'metric': 'multi_logloss',
        'num_leaves': 1024,
        'learning_rate': 0.3,
        'n_estimators': 2000,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'min_data_in_leaf': 1,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'multi:softmax',
        'num_class': 7,
        'eval_metric': 'mlogloss',
        'max_depth': 30,
        'learning_rate': 0.3,
        'n_estimators': 2000,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 1,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 3000,
        'learning_rate': 0.3,
        'depth': 16,
        'loss_function': 'MultiClass',
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
