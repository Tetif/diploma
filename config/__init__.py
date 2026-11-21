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

# Datasets and their configs
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
    # Datasets
    'BaseDatasetConfig',
    'PreprocessingConfig',
    'DatasetRegistry'
]

