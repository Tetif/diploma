"""Forest Covertype dataset configuration"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class CovertypeConfig(BaseDatasetConfig):
    """Configuration for the Forest Covertype dataset (multiclass classification)"""

    name = 'covertype'
    description = 'Forest Covertype Dataset - Forest Cover Type Prediction (Multiclass Classification)'
    data_type = 'tabular'
    task_type = 'multiclass_classification'

    # Paths (EDA: datasets/covertype/covtype.data)
    data_path = 'datasets/covertype/'
    required_files = ['covtype.data']

    # Data structure: 54 features + target (1-7)
    target_column = 'target'
    id_column = None
    columns_to_drop = []
    categorical_columns = []
    numeric_columns = [f'feature_{i}' for i in range(54)]

    # Split parameters
    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = True

    # Metrics
    metrics = ['accuracy', 'f1_weighted', 'confusion_matrix']

    def __init__(self):
        super().__init__()
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.missing_threshold = 0.7
        self.preprocessing_config.encode_categorical = False
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.remove_outliers = False

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Load the Covertype data (covtype.data without a header)."""
        col_names = [f'feature_{i}' for i in range(54)] + ['target']
        df = pd.read_csv(self.data_path + 'covtype.data', header=None, names=col_names)

        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        target = df[self.target_column].copy()
        # Classes in the data are 1-7; sklearn/xgboost need 0-6
        target = target.astype(int) - 1
        df = df.drop(columns=[self.target_column])
        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate the Covertype data."""
        for col in self.numeric_columns:
            if col not in df.columns:
                print(f"Warning: Column '{col}' not found in dataset")
        if len(df) < 1000:
            print(f"Warning: Dataset has only {len(df)} rows")
        return True
