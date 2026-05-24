"""Конфигурация датасета IMDB Reviews (текст → табличное представление через TF-IDF)"""

from typing import List, Tuple
import pandas as pd
import numpy as np
from .base import BaseDatasetConfig, PreprocessingConfig


class ImdbConfig(BaseDatasetConfig):
    """Конфигурация для датасета IMDB (бинарная классификация, признаки — TF-IDF по отзывам)."""

    name = 'imdb'
    description = 'IMDB Movie Reviews - Sentiment Classification (Binary)'
    data_type = 'tabular'
    task_type = 'binary_classification'

    data_path = 'datasets/imdb/'
    required_files = ['IMDB Dataset.csv']

    target_column = 'sentiment'
    id_column = None
    columns_to_drop = []
    categorical_columns = []
    # Имена колонок задаём после векторизации
    numeric_columns = []  # заполняется в load_data

    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = True

    metrics = ['accuracy', 'f1', 'roc_auc', 'precision', 'recall']

    # Широкая разреженная матрица TF-IDF: log_top_bottom_influence непомерно тяжёлый
    show_top_bottom_influence = 0

    # Ограничение выборки и размер словаря TF-IDF
    max_samples = 25000
    tfidf_max_features = 2000
    use_tfidf_lsa = False
    lsa_n_components = 200

    def __init__(self):
        super().__init__()
        self.preprocessing_config.handle_missing_values = True
        self.preprocessing_config.encode_categorical = False
        self.preprocessing_config.scale_numeric = True

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Загрузить IMDB, векторизовать отзывы через TF-IDF в таблицу признаков."""
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer

        df = pd.read_csv(self.data_path + 'IMDB Dataset.csv')
        if self.max_samples is not None:
            df = df.sample(n=min(len(df), self.max_samples), random_state=self.random_state)

        texts = df['review'].astype(str)
        y_raw = df[self.target_column].map({'positive': 1, 'negative': 0})
        if y_raw.isna().any():
            y_raw = y_raw.fillna(0).astype(int)

        vectorizer = TfidfVectorizer(max_features=self.tfidf_max_features, stop_words='english', sublinear_tf=True)
        X = vectorizer.fit_transform(texts)

        if self.use_tfidf_lsa:
            n_components = min(self.lsa_n_components, X.shape[1])
            if n_components <= 0:
                raise ValueError('lsa_n_components must be positive')
            X = TruncatedSVD(n_components=n_components, random_state=self.random_state).fit_transform(X)
            feature_names = [f'lsa_{i}' for i in range(X.shape[1])]
            X_df = pd.DataFrame(X, columns=feature_names)
        else:
            feature_names = [f'tfidf_{i}' for i in range(X.shape[1])]
            X_df = pd.DataFrame.sparse.from_spmatrix(X, columns=feature_names)

        self.numeric_columns = feature_names
        target = pd.Series(y_raw.values, name=self.target_column, index=X_df.index)
        return X_df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        if len(df) < 100:
            print(f"Warning: Dataset has only {len(df)} rows")
        return True
