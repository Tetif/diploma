"""
Preprocessor for tabular data.
"""

import pandas as pd
import numpy as np
from scipy.sparse import issparse
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

from .base import BasePreprocessor
from config.datasets.base import BaseDatasetConfig
from experiments.logger import debug_print


class TabularPreprocessor(BasePreprocessor):
    """Preprocessor for tabular data"""

    def __init__(self, dataset_config: BaseDatasetConfig, logger=None):
        """
        Initialize the tabular preprocessor
        
        Args:
            dataset_config: Dataset configuration
            logger: Logger for output
        """
        super().__init__(logger)
        self.dataset_config = dataset_config
        self.numeric_cols = dataset_config.numeric_columns
        self.categorical_cols = dataset_config.categorical_columns
        self.preprocessor = None
        self.stats_dict = None

    def fit(self, X: pd.DataFrame, y: pd.Series = None) -> 'TabularPreprocessor':
        """
        Fit the preprocessor on the data
        
        Args:
            X: Features
            y: Target (optional)
            
        Returns:
            self
        """
        debug_print("Building preprocessing pipeline...")

        # X being a numpy array is an error
        if isinstance(X, np.ndarray):
            raise ValueError("fit() requires a pandas DataFrame, got numpy array")

        # Keep the original columns for use in transform
        self._original_columns = X.columns.tolist()

        # Keep only the columns present in the data
        numeric_cols = [c for c in self.numeric_cols if c in X.columns]
        categorical_cols = [c for c in self.categorical_cols if c in X.columns]

        debug_print(f"  Numeric columns: {len(numeric_cols)}")
        debug_print(f"  Categorical columns: {len(categorical_cols)}")

        # Convert categorical columns to strings and fill NaN
        X_copy = X.copy()
        for col in categorical_cols:
            if col in X_copy.columns:
                # Fill NaN values before the type conversion
                X_copy[col] = X_copy[col].fillna('missing')
                # Convert to string
                X_copy[col] = X_copy[col].astype(str)

        # StandardScaler cannot center sparse matrices; use with_mean=False when data is sparse
        numeric_is_sparse = False
        if numeric_cols:
            X_num = X_copy[numeric_cols]
            if issparse(X_num):
                numeric_is_sparse = True
            elif hasattr(X_num, 'values') and issparse(X_num.values):
                numeric_is_sparse = True
            elif isinstance(X_num.dtypes.iloc[0], pd.SparseDtype):
                numeric_is_sparse = True

        scaler = StandardScaler(with_mean=not numeric_is_sparse)

        # Pipeline for numeric columns
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', scaler)
        ])

        # Pipeline for categorical columns
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])

        # Combine the transformers
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_cols),
                ('cat', categorical_transformer, categorical_cols)
            ],
            remainder='drop'
        )

        # Fit on the data
        preprocessor.fit(X_copy)

        self.preprocessor = preprocessor
        self.is_fitted = True
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols

        debug_print("Preprocessing pipeline built and fitted successfully")

        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        """
        Transform the data
        
        Args:
            X: Features (DataFrame or numpy array)
            
        Returns:
            Transformed features (numpy array)
        """
        if not self.is_fitted:
            raise RuntimeError("Preprocessor is not fitted. Call fit() first.")

        # X is a numpy array
        if isinstance(X, np.ndarray):
            # If original_columns are saved and the column count matches, convert
            if hasattr(self, '_original_columns') and X.shape[1] == len(self._original_columns):
                X = pd.DataFrame(X, columns=self._original_columns)
            else:
                # If the column count does not match, X is already transformed
                # Pass it through as is
                return X
        
        # Convert categorical columns to strings and fill NaN
        X_copy = X.copy()
        for col in self.categorical_cols:
            if col in X_copy.columns:
                # Fill NaN values before the type conversion
                X_copy[col] = X_copy[col].fillna('missing')
                # Convert to string
                X_copy[col] = X_copy[col].astype(str)

        return self.preprocessor.transform(X_copy)
