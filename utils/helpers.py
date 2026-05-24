import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from config.settings import RANDOM_STATE, EXPERIMENT_CONFIG


def set_random_seeds(seed=42):
    """Установка случайных seed для воспроизводимости"""
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def sample_data(X, y, sample_fraction=None, random_state=None, preserve_order=False):
    """Выборка данных"""
    if sample_fraction is None:
        sample_fraction = EXPERIMENT_CONFIG.get('default_sample_fraction', 0.01)
    if random_state is None:
        random_state = RANDOM_STATE

    if sample_fraction >= 1.0:
        return X, y

    sample_size = max(0, int(len(X) * sample_fraction))

    if preserve_order:
        if isinstance(X, pd.DataFrame):
            X_sample = X.iloc[:sample_size]
        else:
            X_sample = X[:sample_size]

        if isinstance(y, pd.Series):
            y_sample = y.iloc[:sample_size]
        else:
            y_sample = y[:sample_size]

        return X_sample, y_sample

    np.random.seed(random_state)
    sample_indices = np.random.choice(len(X), size=sample_size, replace=False)

    if isinstance(X, pd.DataFrame):
        X_sample = X.iloc[sample_indices]
    else:
        X_sample = X[sample_indices]

    if isinstance(y, pd.Series):
        y_sample = y.iloc[sample_indices]
    else:
        y_sample = y[sample_indices]

    return X_sample, y_sample


def time_series_split(X, y, test_size):
    """Последовательное разбиение временного ряда без перемешивания."""
    n = len(X)
    if isinstance(test_size, float):
        test_size = int(np.ceil(n * test_size))
    else:
        test_size = int(test_size)

    if test_size < 0 or test_size > n:
        raise ValueError(f"Invalid test_size={test_size} for length {n}")

    split_idx = n - test_size
    if isinstance(X, pd.DataFrame):
        X_train = X.iloc[:split_idx]
        X_test = X.iloc[split_idx:]
    else:
        X_train = X[:split_idx]
        X_test = X[split_idx:]

    if isinstance(y, pd.Series):
        y_train = y.iloc[:split_idx]
        y_test = y.iloc[split_idx:]
    else:
        y_train = y[:split_idx]
        y_test = y[split_idx:]

    return X_train, X_test, y_train, y_test


def split_data(X, y, test_size=None, random_state=None, stratify=None, time_series=False):
    """Разделение данных на train/validation."""
    if test_size is None:
        test_size = EXPERIMENT_CONFIG.get('test_size', 0.2)
    if time_series:
        return time_series_split(X, y, test_size)
    if random_state is None:
        random_state = RANDOM_STATE
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=stratify)


def check_gpu_availability():
    """Проверка доступности GPU с детальной диагностикой"""
    gpu_available = torch.cuda.is_available()

    if gpu_available:
        device_count = torch.cuda.device_count()
        device_name = torch.cuda.get_device_name(0)
        cuda_version = torch.version.cuda
        print(f"[OK] GPU available: {device_count} device(s)")
        print(f"   Device name: {device_name}")
        print(f"   CUDA version: {cuda_version}")
        
        # Проверяем память GPU
        if device_count > 0:
            memory_total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"   GPU memory: {memory_total:.2f} GB")
    else:
        print("GPU not available, using CPU")
        print("   To enable GPU:")
        print("   1. Install PyTorch with CUDA support: pip install torch --index-url https://download.pytorch.org/whl/cu118")
        print("   2. Ensure you have NVIDIA GPU with CUDA support")
        print("   3. Install NVIDIA CUDA Toolkit")

    return gpu_available


def print_data_info(df, name="Dataset"):
    """Вывод информации о данных"""
    print(f"\n{name} — сводка:")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB")

    # Типы данных
    dtypes = df.dtypes.value_counts()
    print(f"   Data types:")
    for dtype, count in dtypes.items():
        print(f"     {dtype}: {count}")

    # Пропущенные значения
    missing = df.isnull().sum().sum()
    if missing > 0:
        missing_pct = missing / (df.shape[0] * df.shape[1]) * 100
        print(f"   Missing values: {missing} ({missing_pct:.2f}%)")
    else:
        print(f"   Missing values: None")

    # Уникальные значения
    print(f"   Unique values per column (top 5):")
    for col in df.columns[:5]:
        unique_count = df[col].nunique()
        print(f"     {col}: {unique_count}")