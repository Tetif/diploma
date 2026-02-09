"""Конфигурация датасета Adult"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class AdultConfig(BaseDatasetConfig):
    """Конфигурация для датасета Adult (двоичная классификация)"""

    name = 'adult'
    description = 'UCI Adult Dataset - Income Prediction (Binary Classification)'
    data_type = 'tabular'
    task_type = 'binary_classification'

    # Пути
    data_path = 'datasets/adult/'
    required_files = ['adult.csv']

    # Структура данных
    target_column = 'income'
    id_column = None
    columns_to_drop = ['fnlwgt']  # Weight column
    categorical_columns = [
        'workclass', 'education', 'marital.status', 'occupation',
        'relationship', 'race', 'sex', 'native.country'
    ]
    numeric_columns = [
        'age', 'education.num', 'capital.gain', 'capital.loss', 'hours.per.week'
    ]

    # Параметры разделения
    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = True  # Важно для балансировки классов

    # Метрики
    metrics = ['accuracy', 'f1', 'roc_auc', 'precision', 'recall']

    def __init__(self):
        super().__init__()
        # Специфичные параметры предобработки для Adult
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.missing_threshold = 0.5
        self.preprocessing_config.encode_categorical = True
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.custom_preprocessing_steps = ['replace_question_marks']

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Загрузить данные Adult датасета"""
        df = pd.read_csv(self.data_path + 'adult.csv')

        # Очистка: заменить '?' на NaN
        df = df.replace('?', np.nan)

        # Проверка целевой переменной
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        target = df[self.target_column].copy()

        # Убрать целевую переменную из признаков
        df = df.drop(columns=[self.target_column])

        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Валидировать данные Adult датасета"""
        # Проверить наличие всех числовых и категориальных колонок
        all_cols = self.categorical_columns + self.numeric_columns

        for col in all_cols:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataset")

        # Проверить типы данных
        for col in self.numeric_columns:
            if col in df.columns and df[col].dtype == 'object':
                print(f"Warning: Numeric column '{col}' has object dtype")

        return True
