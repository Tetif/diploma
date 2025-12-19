import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split


def set_random_seeds(seed=42):
    """Установка случайных seed для воспроизводимости"""
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def sample_data(X, y, sample_fraction=0.01, random_state=42):
    """Выборка данных"""
    if sample_fraction >= 1.0:
        return X, y

    sample_size = int(len(X) * sample_fraction)
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


def split_data(X, y, test_size=0.2, random_state=42):
    """Разделение данных на train/validation"""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def check_gpu_availability():
    """Проверка доступности GPU с детальной диагностикой"""
    gpu_available = torch.cuda.is_available()

    if gpu_available:
        device_count = torch.cuda.device_count()
        device_name = torch.cuda.get_device_name(0)
        cuda_version = torch.version.cuda
        print(f"✅ GPU available: {device_count} device(s)")
        print(f"   Device name: {device_name}")
        print(f"   CUDA version: {cuda_version}")
        
        # Проверяем память GPU
        if device_count > 0:
            memory_total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            print(f"   GPU memory: {memory_total:.2f} GB")
    else:
        print("⚠️ GPU not available, using CPU")
        print("   To enable GPU:")
        print("   1. Install PyTorch with CUDA support: pip install torch --index-url https://download.pytorch.org/whl/cu118")
        print("   2. Ensure you have NVIDIA GPU with CUDA support")
        print("   3. Install NVIDIA CUDA Toolkit")

    return gpu_available


def print_data_info(df, name="Dataset"):
    """Вывод информации о данных"""
    print(f"\n📊 {name} INFORMATION:")
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