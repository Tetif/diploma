import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from experiments.logger import debug_print


class DataPreprocessor:
    """Класс для предобработки данных"""

    def __init__(self, logger=None):
        self.logger = logger
        self.preprocessor = None

    def comprehensive_preprocessing(self, df: pd.DataFrame, target: str = 'logerror'):
        """Комплексная предобработка данных"""
        if self.logger:
            self.logger.start_timing("preprocessing")
            self.logger.log_message("Starting simplified preprocessing...")
        else:
            debug_print("Starting simplified preprocessing...")

        original_shape = df.shape
        debug_print(f"Original shape: {original_shape}")

        # 1. Handling missing values
        debug_print("1. Handling missing values...")
        missing_frac = df.isna().mean()
        cols_to_drop = missing_frac[missing_frac >= 0.7].index.tolist()
        df = df.drop(columns=cols_to_drop)
        debug_print(f"Dropped {len(cols_to_drop)} columns with >70% missing values")

        # 2. Converting data types
        debug_print("2. Converting data types...")
        if 'transactiondate' in df.columns:
            df['transactiondate'] = pd.to_datetime(df['transactiondate'])
            df['tx_year'] = df['transactiondate'].dt.year
            df['tx_month'] = df['transactiondate'].dt.month

        # 3. Creating basic features
        debug_print("3. Creating basic features...")
        fin_cols = [c for c in df.columns if 'finishedsquarefeet' in c]
        if fin_cols:
            df['total_finished_sqft'] = df[fin_cols].sum(axis=1)

        # 4. Basic encoding
        debug_print("4. Basic encoding...")
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except:
                    df[col] = df[col].astype('category')

        # 5. Filling missing values
        debug_print("5. Filling missing values...")
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

        categorical_cols = df.select_dtypes(include=['category']).columns
        for col in categorical_cols:
            df[col] = df[col].fillna(df[col].mode()[0])

        # 6. Final cleanup
        debug_print("6. Final cleanup...")
        drop_cols = [
                        'parcelid', 'transactiondate', 'yearbuilt',
                        'bathroomcnt', 'bedroomcnt', 'roomcnt',
                        'fullbathcnt', 'threequarterbathnbr',
                        'propertyzoningdesc'
                    ] + fin_cols

        drop_cols = [col for col in drop_cols if col in df.columns]
        df = df.drop(columns=drop_cols)

        # Ensure target column exists
        if target in df.columns:
            y = df[target]
            X = df.drop(columns=[target])
        else:
            X = df
            y = None

        debug_print(f"Preprocessing completed! Final shape: {X.shape}")

        if self.logger:
            self.logger.end_timing("preprocessing")
            self.logger.log_message("Preprocessing completed!")

        return X, y

    def build_preprocessor(self, X: pd.DataFrame):
        """Построение пайплайна предобработки"""
        num_cols = X.select_dtypes(include=['number']).columns.tolist()
        cat_cols = X.select_dtypes(include=['category', 'object']).columns.tolist()

        numeric_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value=-1)),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        self.preprocessor = ColumnTransformer([
            ('num', numeric_transformer, num_cols),
            ('cat', categorical_transformer, cat_cols)
        ], remainder='drop')

        return self.preprocessor, num_cols, cat_cols

    def fit_preprocessor(self, X: pd.DataFrame):
        """Обучение предобработчика"""
        if self.preprocessor is None:
            self.build_preprocessor(X)

        self.preprocessor.fit(X)
        return self.preprocessor

    def transform_data(self, X: pd.DataFrame):
        """Трансформация данных"""
        if self.preprocessor is None:
            raise ValueError("Preprocessor not fitted. Call fit_preprocessor first.")

        return self.preprocessor.transform(X)