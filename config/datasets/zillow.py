"""Zillow dataset configuration"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class ZillowConfig(BaseDatasetConfig):
    """Configuration for the Zillow dataset (regression)"""

    name = 'zillow'
    description = 'Zillow Home Value Prediction - Log Error Regression'
    data_type = 'tabular'
    task_type = 'regression'

    # Paths
    data_path = 'datasets/'
    required_files = ['properties_2016.csv', 'train_2016_v2.csv', 'sample_submission.csv']

    # Data structure
    target_column = 'logerror'
    id_column = 'parcelid'
    
    # Zillow-specific columns to drop
    columns_to_drop = [
        'propertylandusetyp', 'fireplacecnt',
        'assessmentyear', 'taxamount', 'taxdelinquencyyear',
        'rawcensustractandblock', 'censustractandblock'
    ]

    # Main categorical features (columns actually present in the data)
    categorical_columns = [
        'propertycountylandusecode', 'propertylandusetypeid',
        'heatingorsystemtypeid', 'airconditioningtypeid'
    ]

    # Numeric features: geolocation, house properties, value, date, feature engineering
    numeric_columns = [
        'latitude', 'longitude', 'bathroomcnt', 'bedroomcnt',
        'buildingqualitytypeid', 'calculatedfinishedsquarefeet', 'finishedsquarefeet12',
        'fips', 'fullbathcnt', 'garagecarcnt', 'garagetotalsqft',
        'yearbuilt', 'numberofstories', 'poolcnt', 'roomcnt',
        'lotsizesquarefeet', 'structuretaxvaluedollarcnt', 'taxvaluedollarcnt',
        'landtaxvaluedollarcnt', 'tx_month', 'tx_year', 'tx_month_sin', 'tx_month_cos',
        'total_finished_sqft', 'age', 'price_per_sqft'
    ]

    # [AUDIT-FIX M7] logerror is now clipped AFTER the split, by quantiles of train only
    # (see main.py: train_target_clip_quantiles); holdout is not clipped and not used for the quantiles.
    train_target_clip_quantiles = (0.005, 0.995)

    # Split parameters
    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = False

    # Metrics
    metrics = ['mae', 'rmse', 'r2']

    def __init__(self):
        super().__init__()
        # Zillow-specific preprocessing parameters
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.missing_threshold = 0.7
        self.preprocessing_config.encode_categorical = True
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.remove_outliers = False
        self.preprocessing_config.create_features = True
        self.preprocessing_config.custom_preprocessing_steps = [
            'parse_transaction_date',
            'handle_zillow_missing_values',
            'create_aggregate_features'
        ]

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Load the Zillow dataset"""
        # Load properties and training data
        props_path = self.data_path + 'properties_2016.csv'
        train_path = self.data_path + 'train_2016_v2.csv'

        df_props = pd.read_csv(props_path, low_memory=False)
        df_train = pd.read_csv(train_path)

        # Merge on parcelid
        df = df_train.merge(df_props, on='parcelid', how='left')

        # Features from the transaction date (critical for logerror - seasonality)
        if 'transactiondate' in df.columns:
            df['transactiondate'] = pd.to_datetime(df['transactiondate'], errors='coerce')
            df['tx_month'] = df['transactiondate'].dt.month.fillna(6).astype(int)
            df['tx_year'] = df['transactiondate'].dt.year.fillna(2016).astype(int)
            df['tx_month_sin'] = np.sin(2 * np.pi * df['tx_month'] / 12)
            df['tx_month_cos'] = np.cos(2 * np.pi * df['tx_month'] / 12)

        # Feature engineering
        fin_cols = [c for c in df.columns if 'finishedsquarefeet' in c.lower()]
        if fin_cols:
            df['total_finished_sqft'] = df[fin_cols].sum(axis=1)
        if 'yearbuilt' in df.columns:
            df['age'] = (2016 - df['yearbuilt'].fillna(2010)).clip(lower=0)
        if 'structuretaxvaluedollarcnt' in df.columns and 'calculatedfinishedsquarefeet' in df.columns:
            sqft = df['calculatedfinishedsquarefeet'].replace(0, np.nan)
            df['price_per_sqft'] = df['structuretaxvaluedollarcnt'] / sqft

        # Check the target variable
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        target = df[self.target_column].copy()

        # [AUDIT-FIX M7] Previously the target was clipped here by quantiles of ALL data before the split
        # (leakage from holdout). Moved to main.py after the split.

        # Drop the target variable from the features
        df = df.drop(columns=[self.target_column])

        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate the Zillow dataset"""
        # Check the number of rows
        if len(df) < 1000:
            print(f"Warning: Dataset has only {len(df)} rows")
            return False

        # Check that the key column parcelid is present
        if 'parcelid' not in df.columns:
            print("Error: parcelid column not found")
            return False

        # Check that the main numeric columns are present
        critical_cols = ['latitude', 'longitude', 'finishedsquarefeet12']
        for col in critical_cols:
            if col not in df.columns:
                print(f"Warning: Critical column '{col}' not found")

        return True

    def get_info(self) -> dict:
        """Get information about the Zillow dataset"""
        info = super().get_info()
        info['special_notes'] = [
            'The data consists of two files: properties and training',
            'Merged on parcelid',
            'Many missing values (~50%)',
            'Dates need special handling'
        ]
        return info
