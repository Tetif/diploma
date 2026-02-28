"""
Configuration for Adult dataset
Binary Classification, ~32K samples, 14 features after preprocessing
"""

RANDOM_STATE = 42

ADULT_CONFIG = {
    'lightgbm': {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'num_leaves': 63,
        'learning_rate': 0.05,
        'feature_fraction': 0.85,
        'bagging_fraction': 0.75,
        'bagging_freq': 5,
        'min_data_in_leaf': 10,
        'verbose': -1,
        'n_jobs': -1,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'binary:logistic',
        'eval_metric': 'logloss',
        'max_depth': 7,
        'learning_rate': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 1,
        'gamma': 0,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'catboost': {
        'iterations': 150,
        'learning_rate': 0.05,
        'depth': 7,
        'loss_function': 'Logloss',
        'verbose': False,
        'random_state': RANDOM_STATE,
        'thread_count': -1
    },
    'random_forest': {
        'n_estimators': 200,
        'max_depth': 15,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': RANDOM_STATE,
        'n_jobs': -1
    },
    'pytorch': {
        'simple': {
            'layers': [64, 32, 16],
            'dropout': 0.3,
            'learning_rate': 0.001
        },
        'improved': {
            'layers': [128, 64, 32, 16],
            'batch_norm': True,
            'dropout': [0.3, 0.25, 0.2],
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
