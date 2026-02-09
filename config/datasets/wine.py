"""Конфигурация датасета Wine Quality"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class WineConfig(BaseDatasetConfig):
    """Конфигурация для датасета Wine Quality (регрессия или многоклассовая классификация)"""

    name = 'wine'
    description = 'Wine Quality Dataset - Wine Quality Prediction (Regression)'
    data_type = 'tabular'
    task_type = 'regression'  # Можно менять на 'multiclass_classification'

    # Пути
    data_path = 'datasets/wine/'
    required_files = ['WineQT.csv']

    # Структура данных
    target_column = 'quality'
    id_column = 'Id'
    columns_to_drop = ['Id']  # ID колонка не нужна для модели
    categorical_columns = []  # Нет категориальных признаков
    numeric_columns = [
        'fixed acidity', 'volatile acidity', 'citric acid',
        'residual sugar', 'chlorides', 'free sulfur dioxide',
        'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol'
    ]

    # Параметры разделения
    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = False  # Можно менять на True для многоклассовой классификации

    # Метрики
    metrics = ['mae', 'rmse', 'r2']  # Для регрессии
    # metrics = ['accuracy', 'f1_weighted', 'confusion_matrix']  # Для классификации

    def __init__(self):
        super().__init__()
        # Специфичные параметры предобработки для Wine
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.missing_threshold = 0.9
        self.preprocessing_config.encode_categorical = False  # Нет категориальных
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.remove_outliers = False

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Загрузить данные Wine датасета"""
        df = pd.read_csv(self.data_path + 'WineQT.csv')

        # Проверка целевой переменной
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        target = df[self.target_column].copy()

        # Убрать целевую переменную и ID колонки из признаков
        df = df.drop(columns=self.columns_to_drop + [self.target_column])

        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Валидировать данные Wine датасета"""
        # Проверить наличие всех числовых колонок
        for col in self.numeric_columns:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataset")

        # Проверить типы данных
        for col in self.numeric_columns:
            if col in df.columns and df[col].dtype != 'float64' and df[col].dtype != 'int64':
                print(f"Warning: Numeric column '{col}' has dtype {df[col].dtype}")

        return True
