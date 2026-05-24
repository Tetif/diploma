"""Конфигурация датасета Household Power Consumption (Electric)"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class ElectricConfig(BaseDatasetConfig):
    """Конфигурация для датасета потребления электроэнергии (регрессия)"""

    name = 'electric'
    description = 'Household Power Consumption - Global Active Power Prediction (Regression)'
    data_type = 'tabular'
    task_type = 'regression'

    # Пути (EDA: datasets/electric/household_power_consumption.txt)
    data_path = 'datasets/electric/'
    required_files = ['household_power_consumption.txt']

    # После загрузки: признаки из datetime + числовые колонки
    target_column = 'Global_active_power'
    id_column = None
    columns_to_drop = ['datetime']
    categorical_columns = []
    numeric_columns = [
        'hour', 'day_of_week', 'month',
        'Global_reactive_power', 'Voltage', 'Global_intensity',
        'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'
    ]

    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = False
    use_time_split = True

    metrics = ['mae', 'rmse', 'r2']

    def __init__(self):
        super().__init__()
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.missing_threshold = 0.5
        self.preprocessing_config.encode_categorical = False
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.remove_outliers = False

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Загрузить данные Electric (разделитель ;, пропуски ?)."""
        df = pd.read_csv(
            self.data_path + 'household_power_consumption.txt',
            sep=';',
            na_values='?',
            low_memory=False
        )
        df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        df = df.dropna(subset=['datetime'])
        df = df.sort_values('datetime', ignore_index=True)
        df['hour'] = df['datetime'].dt.hour
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['month'] = df['datetime'].dt.month
        df = df.drop(columns=['Date', 'Time'])

        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        # Удаляем строки с пропусками в целевой переменной
        df = df.dropna(subset=[self.target_column])
        target = df[self.target_column].copy().astype(float)
        df = df.drop(columns=[self.target_column, 'datetime'])

        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Валидировать данные Electric."""
        for col in self.numeric_columns:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataset")
        return True
