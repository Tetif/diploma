"""Adult dataset configuration"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class AdultConfig(BaseDatasetConfig):
    """Configuration for the Adult dataset (binary classification)"""

    name = 'adult'
    description = 'UCI Adult Dataset - Income Prediction (Binary Classification)'
    data_type = 'tabular'
    task_type = 'binary_classification'

    # Paths
    data_path = 'datasets/adult/'
    required_files = ['adult.csv']

    # Data structure
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

    # Split parameters
    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = True  # Important for class balancing

    # Metrics
    metrics = ['accuracy', 'f1', 'roc_auc', 'precision', 'recall']

    def __init__(self):
        super().__init__()
        # Adult-specific preprocessing parameters
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.missing_threshold = 0.5
        self.preprocessing_config.encode_categorical = True
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.custom_preprocessing_steps = ['replace_question_marks']

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Load the Adult dataset"""
        df = pd.read_csv(self.data_path + 'adult.csv')

        # Cleaning: replace '?' with NaN
        df = df.replace('?', np.nan)

        # Check the target variable
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        target = df[self.target_column].copy()

        # Drop the target variable from the features
        df = df.drop(columns=[self.target_column])

        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate the Adult dataset"""
        # Check that all numeric and categorical columns are present
        all_cols = self.categorical_columns + self.numeric_columns

        for col in all_cols:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataset")

        # Check data types
        for col in self.numeric_columns:
            if col in df.columns and df[col].dtype == 'object':
                print(f"Warning: Numeric column '{col}' has object dtype")

        return True
