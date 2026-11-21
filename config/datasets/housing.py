"""Housing (California Housing) dataset configuration"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class HousingConfig(BaseDatasetConfig):
    """Configuration for the California Housing dataset (regression)"""

    name = 'housing'
    description = 'California Housing Dataset - Median House Value Prediction (Regression)'
    data_type = 'tabular'
    task_type = 'regression'

    # Paths
    data_path = 'datasets/housing/'
    required_files = ['housing.csv']

    # Data structure
    target_column = 'median_house_value'
    id_column = None
    columns_to_drop = []
    categorical_columns = ['ocean_proximity']
    numeric_columns = [
        'longitude', 'latitude', 'housing_median_age',
        'total_rooms', 'total_bedrooms', 'population',
        'households', 'median_income'
    ]

    # Split parameters
    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = False

    # Metrics
    metrics = ['mae', 'rmse', 'r2']

    def __init__(self):
        super().__init__()
        # Housing-specific preprocessing parameters
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.missing_threshold = 0.7
        self.preprocessing_config.encode_categorical = True
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.remove_outliers = False
        self.preprocessing_config.custom_preprocessing_steps = ['handle_missing_bedrooms']

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Load the Housing dataset"""
        df = pd.read_csv(self.data_path + 'housing.csv')

        # Check the target variable
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        target = df[self.target_column].copy()

        # Drop the target variable from the features
        df = df.drop(columns=[self.target_column])

        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate the Housing dataset"""
        # Check that the columns are present
        all_cols = self.categorical_columns + self.numeric_columns

        for col in all_cols:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataset")

        # Check the number of rows
        if len(df) < 100:
            print(f"Warning: Dataset has only {len(df)} rows")

        return True
