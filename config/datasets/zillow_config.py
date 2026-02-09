"""
Configuration for Zillow dataset
Regression, ~90K samples, 50+ features - large dataset
"""

RANDOM_STATE = 42

ZILLOW_CONFIG = {
    'lightgbm': {
        'objective': 'regression',
        'metric': 'mae',
        'num_leaves': 127,  # Higher for larger dataset
        'learning_rate': 0.05,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.7,
        'bagging_freq': 5,
        'min_data_in_leaf': 20,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'reg:squarederror',
        'eval_metric': 'mae',
        'max_depth': 8,
        'learning_rate': 0.05,
        'subsample': 0.7,
        'colsample_bytree': 0.7,
        'min_child_weight': 5,
        'gamma': 1,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 200,
        'learning_rate': 0.05,
        'depth': 8,
        'loss_function': 'MAE',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 150,
        'max_depth': 20,
        'min_samples_split': 10,
        'min_samples_leaf': 4,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'pytorch': {
        'simple': {
            'layers': [128, 64, 32],
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
