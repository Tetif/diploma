"""
Base class for data preprocessing.
Defines the interface for working with different data types.
"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


class BasePreprocessor(ABC):
    """Abstract base class for preprocessing"""

    def __init__(self, logger=None):
        """
        Initialize the preprocessor
        
        Args:
            logger: Logger for output
        """
        self.logger = logger
        self.preprocessor: Pipeline = None
        self.is_fitted = False

    @abstractmethod
    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'BasePreprocessor':
        """
        Fit the preprocessor on the data
        
        Args:
            X: Features
            y: Target (optional)
            
        Returns:
            self
        """
        pass

    @abstractmethod
    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Transform the data
        
        Args:
            X: Features
            
        Returns:
            Transformed features
        """
        pass

    def fit_transform(self, X: pd.DataFrame, y: pd.Series = None) -> np.ndarray:
        """
        Fit and transform the data
        
        Args:
            X: Features
            y: Target (optional)
            
        Returns:
            Transformed features
        """
        self.fit(X, y)
        return self.transform(X)

    def get_preprocessor(self) -> Pipeline:
        """Get the sklearn Pipeline"""
        if not self.is_fitted:
            raise RuntimeError("Preprocessor is not fitted. Call fit() first.")
        return self.preprocessor

    def log_message(self, msg: str):
        """Log a message"""
        if self.logger:
            self.logger.log_message(msg)
        else:
            print(msg)
