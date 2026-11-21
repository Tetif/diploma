"""
Base class for dataset configurations.
Defines the interface for working with different datasets.
"""

from typing import List, Tuple, Optional, Dict, Any
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class PreprocessingConfig:
    """Preprocessing configuration for a dataset"""

    def __init__(self):
        self.handle_missing_values: bool = True
        self.missing_threshold: float = 0.7  # Drop columns with >70% missing
        self.encode_categorical: bool = True
        self.scale_numeric: bool = True
        self.remove_outliers: bool = False
        self.create_features: bool = False
        
        # Dataset-specific parameters (overridden in subclasses)
        self.custom_preprocessing_steps: List[str] = []


class BaseDatasetConfig(ABC):
    """Abstract base class of a dataset configuration"""

    # ===== IDENTIFICATION =====
    name: str  # Unique dataset name
    description: str  # Dataset description
    data_type: str  # 'tabular', 'text', 'image', 'sequence'
    task_type: str  # 'regression', 'binary_classification', 'multiclass_classification'

    # ===== PATHS =====
    data_path: str  # Base data path
    required_files: List[str]  # Required files

    # ===== DATA STRUCTURE =====
    target_column: str  # Target variable name
    id_column: Optional[str] = None  # Identifier column (if any)
    columns_to_drop: List[str]  # Columns to drop
    categorical_columns: List[str]  # Categorical features
    numeric_columns: List[str]  # Numeric features

    # ===== SPLIT PARAMETERS =====
    test_size: float = 0.2  # Test set size
    val_size: float = 0.1  # Validation set size
    random_state: int = 42
    stratify: bool = False  # Stratified split (classification)
    use_time_split: bool = False  # Use a chronological split for time series

    # ===== METRICS =====
    metrics: List[str]  # Evaluation metrics

    # ===== EXPERIMENT LOGS =====
    # None - use EXPERIMENT_CONFIG['show_top_bottom_influence']; 0 - disable (e.g. wide TF-IDF).
    show_top_bottom_influence: Optional[int] = None

    # ===== PREPROCESSING CONFIGURATION =====
    preprocessing_config: PreprocessingConfig

    def __init__(self):
        """Initialize the config"""
        if not hasattr(self, 'preprocessing_config') or self.preprocessing_config is None:
            self.preprocessing_config = PreprocessingConfig()

    @abstractmethod
    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load the dataset
        
        Returns:
            Tuple[pd.DataFrame, pd.Series]: (features, target)
        """
        pass

    @abstractmethod
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate the loaded data
        
        Args:
            df: DataFrame with the data
            
        Returns:
            bool: True if the data is valid
        """
        pass

    def get_preprocessing_config(self) -> PreprocessingConfig:
        """Get the preprocessing config"""
        return self.preprocessing_config

    def get_all_features(self) -> List[str]:
        """Get all features (categorical + numeric)"""
        return self.categorical_columns + self.numeric_columns

    def get_info(self) -> Dict[str, Any]:
        """Get information about the dataset"""
        return {
            'name': self.name,
            'description': self.description,
            'data_type': self.data_type,
            'task_type': self.task_type,
            'target_column': self.target_column,
            'n_categorical_features': len(self.categorical_columns),
            'n_numeric_features': len(self.numeric_columns),
            'test_size': self.test_size,
            'val_size': self.val_size,
            'stratify': self.stratify,
            'metrics': self.metrics
        }
