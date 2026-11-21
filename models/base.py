from abc import ABC, abstractmethod


class BaseModel(ABC):
    """Base class for all models"""

    @abstractmethod
    def fit(self, X, y, **kwargs):
        pass

    @abstractmethod
    def predict(self, X):
        pass

    def named_parameters(self):
        return []

    def get_params(self, deep=True):
        """Return the model parameters (sklearn compatibility)"""
        return {}

    def set_params(self, **params):
        return self