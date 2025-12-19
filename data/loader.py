import pandas as pd
from experiments.logger import debug_print
import time


class DataLoader:
    """Класс для загрузки и объединения данных"""

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