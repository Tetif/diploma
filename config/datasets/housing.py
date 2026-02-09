"""Конфигурация датасета Housing (California Housing)"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class HousingConfig(BaseDatasetConfig):
    """Конфигурация для датасета California Housing (регрессия)"""

    name = 'housing'
    description = 'California Housing Dataset - Median House Value Prediction (Regression)'
    data_type = 'tabular'
    task_type = 'regression'

    # Пути
    data_path = 'datasets/housing/'
    required_files = ['housing.csv']

    # Структура данных
    target_column = 'median_house_value'
    id_column = None
    columns_to_drop = []
    categorical_columns = ['ocean_proximity']
    numeric_columns = [
        'longitude', 'latitude', 'housing_median_age',
        'total_rooms', 'total_bedrooms', 'population',
        'households', 'median_income'
    ]

    # Параметры разделения
    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = False

    # Метрики
    metrics = ['mae', 'rmse', 'r2']

    def __init__(self):
        super().__init__()
        # Специфичные параметры предобработки для Housing
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.missing_threshold = 0.7
        self.preprocessing_config.encode_categorical = True
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.remove_outliers = False
        self.preprocessing_config.custom_preprocessing_steps = ['handle_missing_bedrooms']

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Загрузить данные Housing датасета"""
        df = pd.read_csv(self.data_path + 'housing.csv')

        # Проверка целевой переменной
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        target = df[self.target_column].copy()

        # Убрать целевую переменную из признаков
        df = df.drop(columns=[self.target_column])

        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Валидировать данные Housing датасета"""
        # Проверить наличие колонок
        all_cols = self.categorical_columns + self.numeric_columns

        for col in all_cols:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataset")

        # Проверить количество строк
        if len(df) < 100:
            print(f"Warning: Dataset has only {len(df)} rows")

        return True
