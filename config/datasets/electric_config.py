"""
Configuration for Electric (Household Power Consumption) dataset
Regression, ~2M rows (sampled in pipeline), 9 features after datetime encoding
"""

RANDOM_STATE = 42

ELECTRIC_CONFIG = {
    'lightgbm': {
        'objective': 'regression',
        'metric': 'mae',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'min_data_in_leaf': 20,
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
        'min_child_weight': 5,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 100,
        'learning_rate': 0.05,
        'depth': 6,
        'loss_function': 'MAE',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 15,
        'min_samples_split': 5,
        'min_samples_leaf': 5,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'pytorch': {
        'simple': {
            'layers': [64, 32, 16],
            'dropout': 0.2,
            'learning_rate': 0.001
        },
        'improved': {
            'layers': [64, 32, 16, 8],
            'batch_norm': True,
            'dropout': [0.2, 0.15, 0.1],
            'learning_rate': 0.001
        },
        'ft_transformer': {
            'd_model': 16,
            'nhead': 4,
            'num_layers': 2,
            'dim_feedforward': 64,
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
