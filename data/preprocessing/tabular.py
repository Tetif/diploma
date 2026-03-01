"""
Предобработчик для табличных данных.
"""

import pandas as pd
import numpy as np
from scipy.sparse import issparse
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

from .base import BasePreprocessor
from config.datasets.base import BaseDatasetConfig
from experiments.logger import debug_print


class TabularPreprocessor(BasePreprocessor):
    """Предобработчик для табличных данных"""

    def __init__(self, dataset_config: BaseDatasetConfig, logger=None):
        """
        Инициализация табличного предобработчика
        
        Args:
            dataset_config: Конфигурация датасета
            logger: Логгер для вывода информации
        """
        super().__init__(logger)
        self.dataset_config = dataset_config
        self.numeric_cols = dataset_config.numeric_columns
        self.categorical_cols = dataset_config.categorical_columns
        self.preprocessor = None
        self.stats_dict = None

    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'TabularPreprocessor':
        """
        Подогнать предобработчик на данные
        
        Args:
            X: Признаки
            y: Целевая переменная (опционально)
            
        Returns:
            self
        """
        debug_print("Building preprocessing pipeline...")

        # Если X это numpy array, это ошибка
        if isinstance(X, np.ndarray):
            raise ValueError("fit() requires a pandas DataFrame, got numpy array")

        # Сохраняем исходные колонки для использования в transform
        self._original_columns = X.columns.tolist()

        # Фильтруем только те колонки, которые есть в данных
        numeric_cols = [c for c in self.numeric_cols if c in X.columns]
        categorical_cols = [c for c in self.categorical_cols if c in X.columns]

        debug_print(f"  Numeric columns: {len(numeric_cols)}")
        debug_print(f"  Categorical columns: {len(categorical_cols)}")

        # Преобразуем категориальные колонки в строки и заполняем NaN
        X_copy = X.copy()
        for col in categorical_cols:
            if col in X_copy.columns:
                # Заполняем NaN значения перед конвертацией типа
                X_copy[col] = X_copy[col].fillna('missing')
                # Конвертируем в string
                X_copy[col] = X_copy[col].astype(str)

        # StandardScaler cannot center sparse matrices; use with_mean=False when data is sparse
        numeric_is_sparse = False
        if numeric_cols:
            X_num = X_copy[numeric_cols]
            if issparse(X_num):
                numeric_is_sparse = True
            elif hasattr(X_num, 'values') and issparse(X_num.values):
                numeric_is_sparse = True
            elif isinstance(X_num.dtypes.iloc[0], pd.SparseDtype):
                numeric_is_sparse = True

        scaler = StandardScaler(with_mean=not numeric_is_sparse)

        # Создаем пайплайн для числовых колонок
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', scaler)
        ])

        # Создаем пайплайн для категориальных колонок
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])

        # Комбинируем трансформеры
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_cols),
                ('cat', categorical_transformer, categorical_cols)
            ],
            remainder='drop'
        )

        # Подгоняем на данных
        preprocessor.fit(X_copy)

        self.preprocessor = preprocessor
        self.is_fitted = True
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols

        debug_print("Preprocessing pipeline built and fitted successfully")

        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Преобразовать данные
        
        Args:
            X: Признаки (DataFrame или numpy array)
            
        Returns:
            Преобразованные признаки (numpy array)
        """
        if not self.is_fitted:
            raise RuntimeError("Preprocessor is not fitted. Call fit() first.")

        # Если X это numpy array
        if isinstance(X, np.ndarray):
            # Если у нас есть сохраненные original_columns и количество совпадает, конвертируем
            if hasattr(self, '_original_columns') and X.shape[1] == len(self._original_columns):
                X = pd.DataFrame(X, columns=self._original_columns)
            else:
                # Если количество колонок не совпадает, это значит что X уже трансформирован
                # Просто передаем его как есть
                return X
        
        # Преобразуем категориальные колонки в строки и заполняем NaN
        X_copy = X.copy()
        for col in self.categorical_cols:
            if col in X_copy.columns:
                # Заполняем NaN значения перед конвертацией типа
                X_copy[col] = X_copy[col].fillna('missing')
                # Конвертируем в string
                X_copy[col] = X_copy[col].astype(str)

        return self.preprocessor.transform(X_copy)
