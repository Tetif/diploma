import lightgbm as lgb
import xgboost as xgb
import catboost as cb
from sklearn.ensemble import RandomForestRegressor
from .base import BaseModel
from config.settings import MODEL_CONFIGS, RANDOM_STATE


class LightGBMModel(BaseModel):
    def __init__(self, **params):
        super().__init__()
        self.model = None
        self.params = MODEL_CONFIGS['lightgbm'].copy()
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
        self.params = MODEL_CONFIGS['xgboost'].copy()
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
        self.params = MODEL_CONFIGS['random_forest'].copy()
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
        self.params = MODEL_CONFIGS['catboost'].copy()
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