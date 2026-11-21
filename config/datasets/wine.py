"""Wine Quality dataset configuration"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class WineConfig(BaseDatasetConfig):
    """Configuration for the Wine Quality dataset (regression or multiclass classification)"""

    name = 'wine'
    description = 'Wine Quality Dataset - Wine Quality Prediction (Regression)'
    data_type = 'tabular'
    task_type = 'regression'  # Can be switched to 'multiclass_classification'

    # Paths
    data_path = 'datasets/wine/'
    required_files = ['WineQT.csv']

    # Data structure
    target_column = 'quality'
    id_column = 'Id'
    columns_to_drop = ['Id']  # The ID column is not needed by the model
    categorical_columns = []  # No categorical features
    numeric_columns = [
        'fixed acidity', 'volatile acidity', 'citric acid',
        'residual sugar', 'chlorides', 'free sulfur dioxide',
        'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol'
    ]

    # Split parameters
    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = False  # Can be switched to True for multiclass classification

    # Metrics
    metrics = ['mae', 'rmse', 'r2']  # For regression
    # metrics = ['accuracy', 'f1_weighted', 'confusion_matrix']  # For classification

    def __init__(self):
        super().__init__()
        # Wine-specific preprocessing parameters
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.missing_threshold = 0.9
        self.preprocessing_config.encode_categorical = False  # No categorical features
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.remove_outliers = False

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Load the Wine dataset"""
        df = pd.read_csv(self.data_path + 'WineQT.csv')

        # Check the target variable
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        target = df[self.target_column].copy()

        # Drop the target variable and the ID column from the features
        df = df.drop(columns=self.columns_to_drop + [self.target_column])

        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate the Wine dataset"""
        # Check that all numeric columns are present
        for col in self.numeric_columns:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataset")

        # Check data types
        for col in self.numeric_columns:
            if col in df.columns and df[col].dtype != 'float64' and df[col].dtype != 'int64':
                print(f"Warning: Numeric column '{col}' has dtype {df[col].dtype}")

        return True
