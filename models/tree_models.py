import threading

import lightgbm as lgb
import xgboost as xgb
import catboost as cb
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from .base import BaseModel
from config.settings import RANDOM_STATE

# [AUDIT-FIX B12] LightGBM fits started concurrently from joblib threads (pyDVL LOO with the threading
# backend) deadlocked on Windows (all threads idle in Dataset construction / Booster.update). LightGBM fits are
# serialised with this lock; they are cheap, other models keep the parallel refits.
_LGB_LOCK = threading.Lock()

# Default configurations for models when no explicit params provided
DEFAULT_MODEL_PARAMS = {
    'lightgbm': {
        'objective': 'regression', 'metric': 'mae', 'num_leaves': 31,
        'learning_rate': 0.1, 'feature_fraction': 0.9, 'bagging_fraction': 0.8,
        'bagging_freq': 5, 'min_data_in_leaf': 5, 'verbose': -1,
        'n_jobs': -1, 'random_state': RANDOM_STATE
    },
    'xgboost': {
        'objective': 'reg:squarederror', 'eval_metric': 'mae', 'max_depth': 5,
        'learning_rate': 0.1, 'subsample': 0.8, 'colsample_bytree': 0.8,
        'min_child_weight': 1, 'random_state': RANDOM_STATE, 'n_jobs': -1
    },
    'random_forest': {
        'n_estimators': 100, 'max_depth': 12, 'min_samples_split': 5,
        'min_samples_leaf': 2, 'random_state': RANDOM_STATE, 'n_jobs': -1
    },
    'catboost': {
        'iterations': 100, 'learning_rate': 0.1, 'depth': 6,
        'loss_function': 'MAE', 'verbose': False, 'random_state': RANDOM_STATE,
        'thread_count': -1
    }
}

CLASSIFICATION_TASKS = ('binary_classification', 'multiclass_classification')


def _sklearn_style_proba(model, X):
    """[AUDIT-FIX D1] predict_proba with one column per class 0..max(classes_) (a class absent from a
    small training subset gets probability 0 instead of shifting the columns)."""
    p = np.asarray(model.predict_proba(X), dtype=np.float64)
    classes = np.asarray(getattr(model, 'classes_', np.arange(p.shape[1]))).astype(int)
    if p.ndim == 2 and len(classes) == p.shape[1] and np.array_equal(classes, np.arange(len(classes))):
        return p
    out = np.zeros((p.shape[0], int(classes.max()) + 1))
    out[:, classes] = p
    return out

def _class_weighting(params: dict, y, task_type: str, lib: str):
    """[AUDIT-FIX P8] params['class_weight'] == 'balanced' -> native class weighting of each library, computed on
    the labels of THIS fit (LOO / removal refits use their own subset), like the MLP's pos_weight = neg/pos.

    binary:      LightGBM / XGBoost scale_pos_weight = neg/pos; CatBoost auto_class_weights='Balanced';
                 RandomForest class_weight='balanced'.
    multiclass:  LightGBM / XGBoost have no class_weight in this API -> per-sample weights n / (K * n_c)
                 (= sklearn 'balanced'); CatBoost / RF as above.
    Returns (params for the library without the key, sample_weight or None, info dict)."""
    p = dict(params)
    cw = p.pop('class_weight', None)
    if cw in (None, 'none') or task_type not in CLASSIFICATION_TASKS:
        return p, None, {}
    if cw != 'balanced':
        raise ValueError(f"class_weight must be 'balanced' or None, got {cw!r}")
    y = np.asarray(y).astype(int).ravel()
    if lib == 'catboost':
        p['auto_class_weights'] = 'Balanced'
        return p, None, {'auto_class_weights': 'Balanced'}
    if lib == 'random_forest':
        p['class_weight'] = 'balanced'
        return p, None, {'class_weight': 'balanced'}
    if task_type == 'binary_classification':
        pos = int((y == 1).sum())
        spw = float((y == 0).sum()) / max(pos, 1)
        p['scale_pos_weight'] = spw
        return p, None, {'scale_pos_weight': spw}
    classes, counts = np.unique(y, return_counts=True)
    w_c = len(y) / (len(classes) * counts.astype(float))
    w = w_c[np.searchsorted(classes, y)]
    return p, w, {'sample_weight': 'balanced', 'class_weights': {int(c): float(v) for c, v in zip(classes, w_c)}}


class LightGBMModel(BaseModel):
    def __init__(self, params=None, task_type='regression', **kwargs):
        super().__init__()
        self.model = None
        self.task_type = task_type
        self._params_arg = params  # [AUDIT-FIX B1] for get_params()/clone()
        # Use provided params, fall back to defaults
        if params is None:
            self.params = DEFAULT_MODEL_PARAMS['lightgbm'].copy()
        else:
            self.params = params.copy() if isinstance(params, dict) else DEFAULT_MODEL_PARAMS['lightgbm'].copy()
        # Only update with a whitelist of valid LightGBM parameters
        lightgbm_keys = {
            'objective', 'metric', 'num_leaves', 'learning_rate', 'feature_fraction',
            'bagging_fraction', 'bagging_freq', 'min_data_in_leaf', 'verbose', 'n_jobs',
            'random_state', 'max_depth', 'subsample', 'colsample_bytree', 'num_class',
            'n_estimators',
        }
        for key in lightgbm_keys:
            if key in kwargs:
                self.params[key] = kwargs[key]

    def fit(self, X, y, X_val=None, y_val=None, **kwargs):
        with _LGB_LOCK:     # [AUDIT-FIX B12]
            return self._fit(X, y, X_val, y_val, **kwargs)

    def _fit(self, X, y, X_val=None, y_val=None, **kwargs):
        # [AUDIT-FIX P8] optional class weighting (scale_pos_weight / balanced sample weights)
        params, weight, self.class_weighting_ = _class_weighting(self.params, y, self.task_type, 'lightgbm')
        train_data = lgb.Dataset(X, label=y, weight=weight)

        # n_estimators from config overrides the default num_boost_round
        num_boost_round = params.get('n_estimators') or kwargs.get('epochs', 1000)
        # Exclude n_estimators from native lgb.train params to avoid conflict
        train_params = {k: v for k, v in params.items() if k != 'n_estimators'}

        if X_val is not None and y_val is not None:
            valid_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
            self.model = lgb.train(
                train_params,
                train_data,
                num_boost_round=num_boost_round,
                valid_sets=[valid_data],
                callbacks=[lgb.early_stopping(50, verbose=False)]
            )
        else:
            self.model = lgb.train(
                train_params,
                train_data,
                num_boost_round=num_boost_round,
                callbacks=None
            )
        return 0.0

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        """Class probabilities (as in sklearn); needed for distillation and metrics."""
        if self.task_type not in CLASSIFICATION_TASKS:
            raise AttributeError("predict_proba is only defined for classification tasks")
        p = np.asarray(self.model.predict(X), dtype=np.float64)
        if self.task_type == 'binary_classification':
            p1 = np.clip(p.reshape(-1), 0.0, 1.0)
            return np.column_stack([1.0 - p1, p1])
        if p.ndim != 2:
            raise ValueError(
                f"LightGBM multiclass predict_proba expected shape (N, C), got {p.shape}"
            )
        return p

    def get_params(self, deep=True):
        """[AUDIT-FIX B1] Constructor arguments (the same objects); sklearn.clone() keeps task_type."""
        return {'params': self._params_arg, 'task_type': self.task_type}

    def set_params(self, **params):
        if 'task_type' in params:
            self.task_type = params.pop('task_type')
        if 'params' in params:
            new = params.pop('params')
            self._params_arg = new
            self.params = dict(new) if isinstance(new, dict) else self.params
        self.params.update(params)
        return self


class XGBoostModel(BaseModel):
    def __init__(self, params=None, task_type='regression', **kwargs):
        super().__init__()
        self.model = None
        self.task_type = task_type
        self._params_arg = params  # [AUDIT-FIX B1] for get_params()/clone()
        if params is None:
            self.params = DEFAULT_MODEL_PARAMS['xgboost'].copy()
        else:
            self.params = params.copy() if isinstance(params, dict) else DEFAULT_MODEL_PARAMS['xgboost'].copy()
        # Only update with valid XGBoost parameters (num_class needed for multiclass, clone-safe)
        xgboost_keys = {
            'objective', 'eval_metric', 'max_depth', 'learning_rate', 'subsample',
            'colsample_bytree', 'min_child_weight', 'gamma', 'random_state', 'n_jobs',
            'num_class', 'n_estimators',
        }
        for key in xgboost_keys:
            if key in kwargs:
                self.params[key] = kwargs[key]

    def fit(self, X, y, **kwargs):
        params, weight, self.class_weighting_ = _class_weighting(self.params, y, self.task_type, 'xgboost')  # [P8]
        if self.task_type in CLASSIFICATION_TASKS:
            # [AUDIT-FIX D1] multi:softmax has no probabilities; softprob gives the same predict() labels
            if params.get('objective') == 'multi:softmax':
                params['objective'] = 'multi:softprob'
            self.model = xgb.XGBClassifier(**params)
        else:
            self.model = xgb.XGBRegressor(**params)
        self.model.fit(X, y, sample_weight=weight)
        return 0.0

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        """[AUDIT-FIX D1] Was missing: distillation used hard 0/1 teacher labels, LossHigh used 0/1 loss."""
        if self.task_type not in CLASSIFICATION_TASKS:
            raise AttributeError("predict_proba is only defined for classification tasks")
        return _sklearn_style_proba(self.model, X)

    def get_params(self, deep=True):
        """[AUDIT-FIX B1] Constructor arguments (the same objects); sklearn.clone() keeps task_type."""
        return {'params': self._params_arg, 'task_type': self.task_type}

    def set_params(self, **params):
        if 'task_type' in params:
            self.task_type = params.pop('task_type')
        if 'params' in params:
            new = params.pop('params')
            self._params_arg = new
            self.params = dict(new) if isinstance(new, dict) else self.params
        self.params.update(params)
        return self


class RandomForestModel(BaseModel):
    def __init__(self, params=None, task_type='regression', **kwargs):
        super().__init__()
        self.model = None
        self.task_type = task_type
        self._params_arg = params  # [AUDIT-FIX B1] for get_params()/clone()
        if params is None:
            self.params = DEFAULT_MODEL_PARAMS['random_forest'].copy()
        else:
            self.params = params.copy() if isinstance(params, dict) else DEFAULT_MODEL_PARAMS['random_forest'].copy()
        # Only update with valid RandomForest parameters
        rf_keys = {
            'n_estimators', 'max_depth', 'min_samples_split', 'min_samples_leaf',
            'random_state', 'n_jobs', 'criterion', 'max_features', 'min_weight_fraction_leaf'
        }
        for key in rf_keys:
            if key in kwargs:
                self.params[key] = kwargs[key]

    def fit(self, X, y, **kwargs):
        params, _, self.class_weighting_ = _class_weighting(self.params, y, self.task_type, 'random_forest')  # [P8]
        if self.task_type in CLASSIFICATION_TASKS:
            self.model = RandomForestClassifier(**params)
        else:
            self.model = RandomForestRegressor(**params)
        self.model.fit(X, y)
        return 0.0

    def predict(self, X):
        return np.asarray(self.model.predict(X))

    def predict_proba(self, X):
        """[AUDIT-FIX D1] Was missing (see XGBoostModel.predict_proba)."""
        if self.task_type not in CLASSIFICATION_TASKS:
            raise AttributeError("predict_proba is only defined for classification tasks")
        return _sklearn_style_proba(self.model, X)

    def get_params(self, deep=True):
        """[AUDIT-FIX B1] Constructor arguments (the same objects); sklearn.clone() keeps task_type."""
        return {'params': self._params_arg, 'task_type': self.task_type}

    def set_params(self, **params):
        if 'task_type' in params:
            self.task_type = params.pop('task_type')
        if 'params' in params:
            new = params.pop('params')
            self._params_arg = new
            self.params = dict(new) if isinstance(new, dict) else self.params
        self.params.update(params)
        return self


class CatBoostModel(BaseModel):
    def __init__(self, params=None, task_type='regression', **kwargs):
        super().__init__()
        self.model = None
        self.task_type = task_type
        self._params_arg = params  # [AUDIT-FIX B1] for get_params()/clone()
        if params is None:
            self.params = DEFAULT_MODEL_PARAMS['catboost'].copy()
        else:
            self.params = params.copy() if isinstance(params, dict) else DEFAULT_MODEL_PARAMS['catboost'].copy()
        # Only update with valid CatBoost parameters
        catboost_keys = {
            'iterations', 'learning_rate', 'depth', 'loss_function', 'verbose',
            'random_state', 'thread_count', 'objective', 'metric', 'eval_metric'
        }
        for key in catboost_keys:
            if key in kwargs:
                self.params[key] = kwargs[key]

    def fit(self, X, y, **kwargs):
        params, _, self.class_weighting_ = _class_weighting(self.params, y, self.task_type, 'catboost')  # [P8]
        if self.task_type in CLASSIFICATION_TASKS:
            self.model = cb.CatBoostClassifier(**params)
        else:
            self.model = cb.CatBoostRegressor(**params)
        self.model.fit(X, y, verbose=False)
        return 0.0

    def predict(self, X):
        p = np.asarray(self.model.predict(X))
        return p.ravel() if p.ndim == 2 and p.shape[1] == 1 else p

    def predict_proba(self, X):
        """[AUDIT-FIX D1] Was missing (see XGBoostModel.predict_proba)."""
        if self.task_type not in CLASSIFICATION_TASKS:
            raise AttributeError("predict_proba is only defined for classification tasks")
        return _sklearn_style_proba(self.model, X)

    def get_params(self, deep=True):
        """[AUDIT-FIX B1] Constructor arguments (the same objects); sklearn.clone() keeps task_type."""
        return {'params': self._params_arg, 'task_type': self.task_type}

    def set_params(self, **params):
        if 'task_type' in params:
            self.task_type = params.pop('task_type')
        if 'params' in params:
            new = params.pop('params')
            self._params_arg = new
            self.params = dict(new) if isinstance(new, dict) else self.params
        self.params.update(params)
        return self
