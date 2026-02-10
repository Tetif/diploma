"""Configuration settings"""
from .settings import (
    CURRENT_DATASET,
    DEBUG_MODE,
    EXPERIMENTS_BASE_DIR,
    DEVICE,
    N_JOBS,
    RANDOM_STATE,
    PYDVL_CONFIG,
    MODEL_CONFIGS,
    EXPERIMENT_CONFIG,
    SYNTHETIC_DATA_CONFIG,
    CACHE_DIR,
    USE_CACHE,
    DISTILLATION_CONFIG
)

# Датасеты и их конфиги
from .datasets import (
    BaseDatasetConfig,
    PreprocessingConfig,
    DatasetRegistry
)

__all__ = [
    'CURRENT_DATASET',
    'DEBUG_MODE',
    'EXPERIMENTS_BASE_DIR',
    'DEVICE',
    'N_JOBS',
    'RANDOM_STATE',
    'PYDVL_CONFIG',
    'MODEL_CONFIGS',
    'EXPERIMENT_CONFIG',
    'SYNTHETIC_DATA_CONFIG',
    'CACHE_DIR',
    'USE_CACHE',
    'DISTILLATION_CONFIG',
    # Датасеты
    'BaseDatasetConfig',
    'PreprocessingConfig',
    'DatasetRegistry'
]

