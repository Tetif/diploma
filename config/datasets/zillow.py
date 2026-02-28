"""Конфигурация датасета Zillow"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class ZillowConfig(BaseDatasetConfig):
    """Конфигурация для датасета Zillow (регрессия)"""

    name = 'zillow'
    description = 'Zillow Home Value Prediction - Log Error Regression'
    data_type = 'tabular'
    task_type = 'regression'

    # Пути
    data_path = 'datasets/'
    required_files = ['properties_2016.csv', 'train_2016_v2.csv', 'sample_submission.csv']

    # Структура данных
    target_column = 'logerror'
    id_column = 'parcelid'
    
    # Специфичные для Zillow колонки для удаления
    columns_to_drop = [
        'propertylandusetyp', 'fireplacecnt',
        'assessmentyear', 'taxamount', 'taxdelinquencyyear',
        'rawcensustractandblock', 'censustractandblock'
    ]

    # Основные категориальные признаки (колонки, реально присутствующие в данных)
    categorical_columns = [
        'propertycountylandusecode', 'propertylandusetypeid',
        'heatingorsystemtypeid', 'airconditioningtypeid'
    ]

    # Числовые признаки: геолокация, характеристики дома, стоимость, дата, feature engineering
    numeric_columns = [
        'latitude', 'longitude', 'bathroomcnt', 'bedroomcnt',
        'buildingqualitytypeid', 'calculatedfinishedsquarefeet', 'finishedsquarefeet12',
        'fips', 'fullbathcnt', 'garagecarcnt', 'garagetotalsqft',
        'yearbuilt', 'numberofstories', 'poolcnt', 'roomcnt',
        'lotsizesquarefeet', 'structuretaxvaluedollarcnt', 'taxvaluedollarcnt',
        'landtaxvaluedollarcnt', 'tx_month', 'tx_year', 'tx_month_sin', 'tx_month_cos',
        'total_finished_sqft', 'age', 'price_per_sqft'
    ]

    # Параметры разделения
    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = False

    # Метрики
    metrics = ['mae', 'rmse', 'r2']

    def __init__(self):
        super().__init__()
        # Специфичные параметры предобработки для Zillow
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
        """Загрузить данные Zillow датасета"""
        # Загружаем properties и training data
        props_path = self.data_path + 'properties_2016.csv'
        train_path = self.data_path + 'train_2016_v2.csv'

        df_props = pd.read_csv(props_path, low_memory=False)
        df_train = pd.read_csv(train_path)

        # Merge по parcelid
        df = df_train.merge(df_props, on='parcelid', how='left')

        # Признаки из даты транзакции (критично для logerror — сезонность)
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

        # Проверка целевой переменной
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        target = df[self.target_column].copy()

        # Клиппинг выбросов logerror (min -4.6, max 4.7 при std 0.16)
        low, high = target.quantile([0.005, 0.995])
        target = target.clip(low, high)

        # Убрать целевую переменную из признаков
        df = df.drop(columns=[self.target_column])

        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        """Валидировать данные Zillow датасета"""
        # Проверить количество строк
        if len(df) < 1000:
            print(f"Warning: Dataset has only {len(df)} rows")
            return False

        # Проверить наличие ключевой колонки parcelid
        if 'parcelid' not in df.columns:
            print("Error: parcelid column not found")
            return False

        # Проверить наличие основных числовых колонок
        critical_cols = ['latitude', 'longitude', 'finishedsquarefeet12']
        for col in critical_cols:
            if col not in df.columns:
                print(f"Warning: Critical column '{col}' not found")

        return True

    def get_info(self) -> dict:
        """Получить информацию о Zillow датасете"""
        info = super().get_info()
        info['special_notes'] = [
            'Данные содержат два файла: properties и training',
            'Merge происходит по parcelid',
            'Много пропущенных значений (~50%)',
            'Требует специальной обработки дат'
        ]
        return info
