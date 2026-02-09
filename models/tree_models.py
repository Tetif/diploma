import lightgbm as lgb
import xgboost as xgb
import catboost as cb
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from .base import BaseModel
from config.settings import get_model_config, CURRENT_DATASET, RANDOM_STATE


class LightGBMModel(BaseModel):
    def __init__(self, **params):
        super().__init__()
        self.model = None
        # Если params содержит полную конфигурацию, используем её. Иначе берём из конфига для текущего датасета
        if any(key in params for key in ['objective', 'metric', 'num_leaves']):
            self.params = params.copy()
        else:
            self.params = get_model_config(CURRENT_DATASET, 'lightgbm').copy()
            self.params.update(params)

    def fit(self, X, y, X_val=None, y_val=None, **kwargs):
        train_data = lgb.Dataset(X, label=y)

        if X_val is not None and y_val is not None:
            valid_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
            self.model = lgb.train(
                self.params,
                train_data,
                num_boost_round=kwargs.get('epochs', 1000),
                valid_sets=[valid_data],
                callbacks=[lgb.early_stopping(50, verbose=False)]
            )
        else:
            self.model = lgb.train(
                self.params,
                train_data,
                num_boost_round=kwargs.get('epochs', 1000),
                callbacks=None
            )
        return 0.0

    def predict(self, X):
        return self.model.predict(X)

    def get_params(self, deep=True):
        """Возвращает параметры модели (совместимость с sklearn)"""
        return self.params.copy() if deep else self.params

    def set_params(self, **params):
        self.params.update(params)
        return self


class XGBoostModel(BaseModel):
    def __init__(self, **params):
        super().__init__()
        self.model = None
        # Если params содержит полную конфигурацию, используем её. Иначе берём из конфига для текущего датасета
        if any(key in params for key in ['objective', 'eval_metric', 'max_depth']):
            self.params = params.copy()
        else:
            self.params = get_model_config(CURRENT_DATASET, 'xgboost').copy()
            self.params.update(params)

    def fit(self, X, y, **kwargs):
        self.model = xgb.XGBRegressor(**self.params)
        self.model.fit(X, y)
        return 0.0

    def predict(self, X):
        return self.model.predict(X)

    def get_params(self, deep=True):
        """Возвращает параметры модели (совместимость с sklearn)"""
        return self.params.copy() if deep else self.params

    def set_params(self, **params):
        self.params.update(params)
        return self


class RandomForestModel(BaseModel):
    def __init__(self, **params):
        super().__init__()
        self.model = None
        # Если params содержит полную конфигурацию, используем её. Иначе берём из конфига для текущего датасета
        if any(key in params for key in ['n_estimators', 'max_depth', 'min_samples_split']):
            self.params = params.copy()
        else:
            self.params = get_model_config(CURRENT_DATASET, 'random_forest').copy()
            self.params.update(params)

    def fit(self, X, y, **kwargs):
        self.model = RandomForestRegressor(**self.params)
        self.model.fit(X, y)
        return 0.0

    def predict(self, X):
        return self.model.predict(X)

    def get_params(self, deep=True):
        """Возвращает параметры модели (совместимость с sklearn)"""
        return self.params.copy() if deep else self.params

    def set_params(self, **params):
        self.params.update(params)
        return self


class CatBoostModel(BaseModel):
    def __init__(self, **params):
        super().__init__()
        self.model = None
        # Если params содержит полную конфигурацию, используем её. Иначе берём из конфига для текущего датасета
        if any(key in params for key in ['iterations', 'learning_rate', 'depth', 'loss_function']):
            self.params = params.copy()
        else:
            self.params = get_model_config(CURRENT_DATASET, 'catboost').copy()
            self.params.update(params)

    def fit(self, X, y, **kwargs):
        self.model = cb.CatBoostRegressor(**self.params)
        self.model.fit(X, y, verbose=False)
        return 0.0

    def predict(self, X):
        return self.model.predict(X)

    def get_params(self, deep=True):
        """Возвращает параметры модели (совместимость с sklearn)"""
        return self.params.copy() if deep else self.params

    def set_params(self, **params):
        self.params.update(params)
        return self