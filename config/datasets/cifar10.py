"""Конфигурация датасета CIFAR-10 (изображения → табличное представление)"""

from typing import List, Tuple
import pandas as pd
import numpy as np
import os
from .base import BaseDatasetConfig, PreprocessingConfig

try:
    from PIL import Image
except ImportError:
    Image = None


class Cifar10Config(BaseDatasetConfig):
    """Конфигурация для датасета CIFAR-10 (многоклассовая классификация, 3072 признака после flatten)."""

    name = 'cifar10'
    description = 'CIFAR-10 - Image Classification (10 classes)'
    data_type = 'tabular'
    task_type = 'multiclass_classification'

    data_path = 'datasets/cifar/cifar10/'
    required_files = []  # папка train с подпапками-классами
    train_dir = 'train'

    target_column = 'label'
    id_column = None
    columns_to_drop = []
    categorical_columns = []
    numeric_columns = [f'pixel_{i}' for i in range(32 * 32 * 3)]

    test_size = 0.2
    val_size = 0.1
    random_state = 39
    stratify = True

    metrics = ['accuracy', 'f1_weighted', 'confusion_matrix']

    max_samples = 15000  # ограничение для скорости (полный train ~50k)

    def __init__(self):
        super().__init__()
        self.preprocessing_config.handle_missing_values = False
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.encode_categorical = False

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Загрузить CIFAR-10 из папок train/class_name/*.png, сгладить в таблицу 3072 колонок."""
        if Image is None:
            raise ImportError("PIL (Pillow) is required for CIFAR-10. Install with: pip install Pillow")

        root = os.path.join(self.data_path, self.train_dir)
        if not os.path.isdir(root):
            raise FileNotFoundError(f"CIFAR-10 train directory not found: {root}")

        class_names = sorted([d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))])
        if not class_names:
            raise FileNotFoundError(f"No class folders in {root}")

        name_to_idx = {name: i for i, name in enumerate(class_names)}
        X_list, y_list = [], []
        n_per_class = (self.max_samples // len(class_names)) if self.max_samples else None

        for cls_name in class_names:
            cls_dir = os.path.join(root, cls_name)
            files = [f for f in os.listdir(cls_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            if n_per_class is not None:
                np.random.RandomState(self.random_state).shuffle(files)
                files = files[:n_per_class]
            for fname in files:
                path = os.path.join(cls_dir, fname)
                try:
                    img = Image.open(path).convert('RGB')
                    arr = np.array(img)
                    if arr.shape[:2] != (32, 32):
                        arr = np.array(Image.open(path).convert('RGB').resize((32, 32)))
                    X_list.append(arr.ravel())
                    y_list.append(name_to_idx[cls_name])
                except Exception:
                    continue

        if not X_list:
            raise ValueError(f"No images loaded from {root}")

        X = np.vstack(X_list)
        cols = [f'pixel_{i}' for i in range(X.shape[1])]
        df = pd.DataFrame(X, columns=cols)
        target = pd.Series(y_list, name=self.target_column)
        return df, target

    def validate_data(self, df: pd.DataFrame) -> bool:
        if df.shape[1] != 3072:
            print(f"Warning: Expected 3072 features, got {df.shape[1]}")
        return True
