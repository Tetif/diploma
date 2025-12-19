from abc import ABC, abstractmethod


class BaseModel(ABC):
    """Базовый класс для всех моделей"""

    @abstractmethod
    def fit(self, X, y, **kwargs):
        pass

    @abstractmethod
    def predict(self, X):
        pass

    def named_parameters(self):
        return []

    def get_params(self, deep=True):
        """Возвращает параметры модели (совместимость с sklearn)"""
        return {}

    def set_params(self, **params):
        return self