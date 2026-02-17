"""
Configuration for Wine dataset
Regression, ~6K samples, 11 features - small dataset
"""

RANDOM_STATE = 42

WINE_CONFIG = {
    'lightgbm': {
        'objective': 'regression',
        'metric': 'mae',
        'num_leaves': 15,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'min_data_in_leaf': 5,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'reg:squarederror',
        'eval_metric': 'mae',
        'max_depth': 16,
        'learning_rate': 0.01,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 1,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 50,
        'learning_rate': 0.05,
        'depth': 4,
        'loss_function': 'MAE',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 50,
        'max_depth': 8,
        'min_samples_split': 3,
        'min_samples_leaf': 1,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'pytorch': {
        'simple': {
            'layers': [16, 8],
            'dropout': 0.2,
            'learning_rate': 0.001
        },
        'improved': {
            'layers': [32, 16, 8],
            'batch_norm': True,
            'dropout': [0.2, 0.15],
            'learning_rate': 0.001
        },
        'ft_transformer': {
            'd_model': 8,
            'nhead': 2,
            'num_layers': 1,
            'dim_feedforward': 32,
            'dropout': 0.1,
            'learning_rate': 0.001
        },
        'ft_transformer_simple': {
            'd_model': 8,
            'nhead': 2,
            'num_layers': 1,
            'dim_feedforward': 32,
            'dropout': 0.1,
            'learning_rate': 0.001
        }
    }
}
