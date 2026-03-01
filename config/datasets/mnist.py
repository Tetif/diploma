"""Конфигурация датасета MNIST (изображения → табличное представление)"""

from typing import List, Tuple
import pandas as pd
import numpy as np
import os
from .base import BaseDatasetConfig, PreprocessingConfig


def _load_mnist_images(path: str, max_samples: int = None) -> np.ndarray:
    """Загрузить изображения MNIST из IDX формата."""
    with open(path, 'rb') as f:
        magic, num, rows, cols = np.frombuffer(f.read(16), dtype='>i4')
        assert magic == 2051
        if max_samples is not None:
            num = min(num, max_samples)
        buf = f.read(rows * cols * num)
        data = np.frombuffer(buf, dtype=np.uint8)
        data = data.reshape(num, rows * cols)
    return data


def _load_mnist_labels(path: str, max_samples: int = None) -> np.ndarray:
    """Загрузить метки MNIST из IDX формата."""
    with open(path, 'rb') as f:
        magic, num = np.frombuffer(f.read(8), dtype='>i4')
        assert magic == 2049
        if max_samples is not None:
            num = min(num, max_samples)
        buf = f.read(num)
        labels = np.frombuffer(buf, dtype=np.uint8)
    return labels


class MnistConfig(BaseDatasetConfig):
    """Конфигурация для датасета MNIST (многоклассовая классификация, 784 признака после flatten)."""

    name = 'mnist'
    description = 'MNIST Handwritten Digits - Digit Classification (Multiclass)'
    data_type = 'tabular'
    task_type = 'multiclass_classification'

    data_path = 'datasets/mnist/'
    required_files = ['train-images-idx3-ubyte', 'train-labels-idx1-ubyte']

    target_column = 'label'
    id_column = None
    columns_to_drop = []
    categorical_columns = []
    numeric_columns = [f'pixel_{i}' for i in range(28 * 28)]

    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = True

    metrics = ['accuracy', 'f1_weighted', 'confusion_matrix']

    # Ограничение выборки для быстрых экспериментов (None = все данные)
    max_train_samples = 20000

    def __init__(self):
        super().__init__()
        self.preprocessing_config.handle_missing_values = False
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.encode_categorical = False

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Загрузить MNIST, сгладить изображения в таблицу 784 колонок."""
        img_path = os.path.join(self.data_path, 'train-images-idx3-ubyte')
        lbl_path = os.path.join(self.data_path, 'train-labels-idx1-ubyte')
        if not os.path.isfile(img_path) or not os.path.isfile(lbl_path):
            raise FileNotFoundError(f"MNIST files not found in {self.data_path}")

        X = _load_mnist_images(img_path, self.max_train_samples)
        y = _load_mnist_labels(lbl_path, self.max_train_samples)

        cols = [f'pixel_{i}' for i in range(X.shape[1])]
        df = pd.DataFrame(X, columns=cols)
        target = pd.Series(y, name=self.target_column)
        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        if df.shape[1] != 784:
            print(f"Warning: Expected 784 features, got {df.shape[1]}")
        return True
