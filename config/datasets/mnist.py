"""MNIST dataset configuration (images -> tabular representation)"""

from typing import List, Optional, Tuple
import gzip
import os
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

from .base import BaseDatasetConfig, PreprocessingConfig

# Official archives (gzip); the same mirrors as torchvision.datasets.MNIST uses
_MNIST_MIRRORS = (
    "http://yann.lecun.com/exdb/mnist/",
    "https://ossci-datasets.s3.amazonaws.com/mnist/",
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _download_mnist_ubyte(data_dir: Path, basename: str) -> None:
    """Download {basename}.gz from one of the mirrors and save the unpacked IDX into data_dir."""
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
        f"Failed to download MNIST ({gz_name}). Check the network or put the files into {data_dir} manually."
    ) from last_err


def _ensure_mnist_file(data_dir: Path, basename: str) -> None:
    if _local_mnist_path(data_dir, basename) is not None:
        return
    _download_mnist_ubyte(data_dir, basename)


def _local_mnist_path(data_dir: Path, basename: str) -> Optional[Path]:
    """Path to the local IDX file: the standard name or the variant with a dot instead of «-idx»."""
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
    """Load MNIST images from the IDX format."""
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
    """Load MNIST labels from the IDX format."""
    with open(path, 'rb') as f:
        magic, num = np.frombuffer(f.read(8), dtype='>i4')
        assert magic == 2049
        if max_samples is not None:
            num = min(num, max_samples)
        buf = f.read(num)
        labels = np.frombuffer(buf, dtype=np.uint8)
    return labels


class MnistConfig(BaseDatasetConfig):
    """Configuration for the MNIST dataset (multiclass classification, 784 features after flatten)."""

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

    # Sample limit for quick experiments (None = all data)
    max_train_samples = 20000

    def __init__(self):
        super().__init__()
        self.preprocessing_config.handle_missing_values = False
        self.preprocessing_config.scale_numeric = True
        self.preprocessing_config.encode_categorical = False

    def _resolved_data_dir(self) -> Path:
        """Path to the data directory relative to the repository root (independent of CWD)."""
        p = Path(self.data_path)
        if p.is_absolute():
            return p
        return _project_root() / p

    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Load MNIST and flatten the images into a 784-column table."""
        data_dir = self._resolved_data_dir()
        train_img, train_lbl = "train-images-idx3-ubyte", "train-labels-idx1-ubyte"
        t10k_img, t10k_lbl = "t10k-images-idx3-ubyte", "t10k-labels-idx1-ubyte"

        # Try the training set first; if the files are missing, download them from the mirrors.
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
            # Only t10k is available locally (a common case) - download the labels or both files
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
                    f"MNIST: neither a full train-* pair nor a t10k-* pair in {data_dir}. "
                    f"Expected {train_img}, {train_lbl} (or {t10k_img}, {t10k_lbl})."
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
