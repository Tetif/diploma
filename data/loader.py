import pandas as pd
from typing import Tuple
from experiments.logger import debug_print
from config.datasets.base import BaseDatasetConfig
import time


class DataLoaderFactory:
    """Фабрика для загрузки данных из различных датасетов"""

    @staticmethod
    def load_dataset(dataset_config: BaseDatasetConfig, logger=None) -> Tuple[pd.DataFrame, pd.Series, BaseDatasetConfig]:
        """
        Загрузить датасет используя его конфигурацию
        
        Args:
            dataset_config: Конфигурация датасета
            logger: Логгер для вывода информации
            
        Returns:
            Tuple[pd.DataFrame, pd.Series, BaseDatasetConfig]: (признаки, целевая переменная, конфиг)
        """
        if logger:
            logger.start_timing("data_loading")
            logger.log_message(f"Loading dataset: {dataset_config.name}")

        try:
            # Загружаем данные используя конфиг
            X, y = dataset_config.load_data()

            # Валидируем данные
            is_valid = dataset_config.validate_data(X)
            if not is_valid:
                if logger:
                    logger.log_message("Warning: Dataset validation failed")

            if logger:
                logger.log_message(f"Loaded {len(X)} rows, {len(X.columns)} columns")
                logger.end_timing("data_loading")

            return X, y, dataset_config

        except Exception as e:
            if logger:
                logger.log_message(f"Error loading dataset: {str(e)}")
            raise


class DataLoader:
    """Класс для загрузки и объединения данных (для обратной совместимости)"""

    def __init__(self, logger=None):
        self.logger = logger

    def load_and_merge_data(self, props_path: str, train_path: str, subs_path: str = None):
        """Загрузка и объединение данных из CSV файлов"""
        if self.logger:
            self.logger.start_timing("data_loading")

        debug_print(f"Loading properties from {props_path}")
        df_props = pd.read_csv(props_path, low_memory=False)

        debug_print(f"Loading training data from {train_path}")
        df_train = pd.read_csv(train_path)

        if subs_path:
            debug_print(f"Loading submission data from {subs_path}")
            df_subs = pd.read_csv(subs_path)
        else:
            df_subs = None

        debug_print("Merging dataframes...")
        df = df_train.merge(df_props, on='parcelid', how='left')

        if self.logger:
            self.logger.end_timing("data_loading")

        return df, df_subs

    def load_single_dataset(self, filepath: str, **kwargs):
        """Загрузка одиночного датасета"""
        return pd.read_csv(filepath, **kwargs)

    def validate_data(self, df: pd.DataFrame, target_column: str = None):
        """Валидация данных"""
        if df.empty:
            raise ValueError("DataFrame is empty")

        if target_column and target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame")

        debug_print(f"Data shape: {df.shape}")
        debug_print(f"Columns: {df.columns.tolist()}")

        return True