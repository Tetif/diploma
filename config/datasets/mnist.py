"""Конфигурация датасета MNIST (изображения → табличное представление)"""

from typing import List, Optional, Tuple
import gzip
import os
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

from .base import BaseDatasetConfig, PreprocessingConfig

# Официальные архивы (gzip); те же зеркала, что использует torchvision.datasets.MNIST
_MNIST_MIRRORS = (
    "http://yann.lecun.com/exdb/mnist/",
    "https://ossci-datasets.s3.amazonaws.com/mnist/",
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _download_mnist_ubyte(data_dir: Path, basename: str) -> None:
    """Скачать {basename}.gz с одного из зеркал и сохранить распакованный IDX в data_dir."""
    gz_name = f"{basename}.gz"
    dest = data_dir / basename
    last_err: Optional[Exception] = None
    for base in _MNIST_MIRRORS:
        url = base + gz_name
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "diploma-mnist-loader/1.0"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                compressed = resp.read()
            raw = gzip.decompress(compressed)
            data_dir.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
            return
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(
        f"Не удалось скачать MNIST ({gz_name}). Проверьте сеть или положите файлы в {data_dir} вручную."
    ) from last_err


def _ensure_mnist_file(data_dir: Path, basename: str) -> None:
    if _local_mnist_path(data_dir, basename) is not None:
        return
    _download_mnist_ubyte(data_dir, basename)


def _local_mnist_path(data_dir: Path, basename: str) -> Optional[Path]:
    """Путь к локальному IDX-файлу: стандартное имя или вариант с точкой вместо «-idx»."""
    p = data_dir / basename
    if p.is_file():
        return p
    if "-idx" in basename:
        alt = basename.replace("-idx", ".idx")
        p2 = data_dir / alt
        if p2.is_file():
            return p2
    return None


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

    def _resolved_data_dir(self) -> Path:
        """Путь к каталогу данных относительно корня репозитория (не зависит от CWD)."""
        p = Path(self.data_path)
        if p.is_absolute():
            return p
        return _project_root() / p

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Загрузить MNIST, сгладить изображения в таблицу 784 колонок."""
        data_dir = self._resolved_data_dir()
        train_img, train_lbl = "train-images-idx3-ubyte", "train-labels-idx1-ubyte"
        t10k_img, t10k_lbl = "t10k-images-idx3-ubyte", "t10k-labels-idx1-ubyte"

        # Сначала пытаемся обучающую выборку; при отсутствии файлов — докачиваем с зеркал.
        use_train = (
            _local_mnist_path(data_dir, train_img) is not None
            and _local_mnist_path(data_dir, train_lbl) is not None
        )
        if not use_train:
            try:
                _ensure_mnist_file(data_dir, train_img)
                _ensure_mnist_file(data_dir, train_lbl)
                use_train = True
            except Exception:
                use_train = False

        if use_train:
            img_path = str(_local_mnist_path(data_dir, train_img))
            lbl_path = str(_local_mnist_path(data_dir, train_lbl))
        else:
            # Локально только t10k (частый случай) — докачиваем метки или оба файла
            if _local_mnist_path(data_dir, t10k_lbl) is None:
                try:
                    _ensure_mnist_file(data_dir, t10k_lbl)
                except Exception:
                    pass
            p_img = _local_mnist_path(data_dir, t10k_img)
            p_lbl = _local_mnist_path(data_dir, t10k_lbl)
            if p_img is not None and p_lbl is not None:
                img_path = str(p_img)
                lbl_path = str(p_lbl)
            else:
                raise FileNotFoundError(
                    f"MNIST: нет ни полной пары train-*, ни пары t10k-* в {data_dir}. "
                    f"Ожидаются {train_img}, {train_lbl} (или {t10k_img}, {t10k_lbl})."
                )

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
