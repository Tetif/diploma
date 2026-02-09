"""
Базовый класс для предобработки данных.
Определяет интерфейс для работы с различными типами данных.
"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


class BasePreprocessor(ABC):
    """Абстрактный базовый класс для предобработки"""

    def __init__(self, logger=None):
        """
        Инициализация предобработчика
        
        Args:
            logger: Логгер для вывода информации
        """
        self.logger = logger
        self.preprocessor: Pipeline = None
        self.is_fitted = False

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'BasePreprocessor':
        """
        Подогнать предобработчик на данные
        
        Args:
            X: Признаки
            y: Целевая переменная (опционально)
            
        Returns:
            self
        """
        pass

    @abstractmethod
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Преобразовать данные
        
        Args:
            X: Признаки
            
        Returns:
            Преобразованные признаки
        """
        pass

    def fit_transform(self, X: pd.DataFrame, y: pd.Series = None) -> np.ndarray:
        """
        Подогнать и преобразовать данные
        
        Args:
            X: Признаки
            y: Целевая переменная (опционально)
            
        Returns:
            Преобразованные признаки
        """
        self.fit(X, y)
        return self.transform(X)

    def get_preprocessor(self) -> Pipeline:
        """Получить sklearn Pipeline"""
        if not self.is_fitted:
            raise RuntimeError("Preprocessor is not fitted. Call fit() first.")
        return self.preprocessor

    def log_message(self, msg: str):
        """Логировать сообщение"""
        if self.logger:
            self.logger.log_message(msg)
        else:
            print(msg)
