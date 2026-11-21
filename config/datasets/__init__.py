"""Registry of dataset configurations"""

from typing import Dict, Type, Optional
from .base import BaseDatasetConfig, PreprocessingConfig
from .adult import AdultConfig
from .housing import HousingConfig
from .wine import WineConfig
from .zillow import ZillowConfig
from .covertype import CovertypeConfig
from .electric import ElectricConfig
from .mnist import MnistConfig
from .imdb import ImdbConfig
from .cifar10 import Cifar10Config


class DatasetRegistry:
    """Registry that manages dataset configurations"""

    _registry: Dict[str, Type[BaseDatasetConfig]] = {}

    @classmethod
    def register(cls, name: str, config_class: Type[BaseDatasetConfig]) -> None:
        """
        Register a dataset configuration
        
        Args:
            name: Unique dataset name
            config_class: Configuration class
        """
        if name in cls._registry:
            print(f"Warning: Dataset '{name}' already registered. Overwriting...")
        cls._registry[name] = config_class

    @classmethod
    def get(cls, name: str) -> BaseDatasetConfig:
        """
        Get a dataset configuration
        
        Args:
            name: Dataset name
            
        Returns:
            Dataset configuration instance
            
        Raises:
            KeyError: If the dataset is not registered
        """
        if name not in cls._registry:
            available = ', '.join(cls._registry.keys())
            raise KeyError(f"Dataset '{name}' not found. Available datasets: {available}")

        config_class = cls._registry[name]
        return config_class()

    @classmethod
    def list(cls) -> list:
        """Get the list of all registered datasets"""
        return list(cls._registry.keys())

    @classmethod
    def get_all_info(cls) -> Dict[str, dict]:
        """Get information about all datasets"""
        info = {}
        for name in cls._registry:
            config = cls.get(name)
            info[name] = config.get_info()
        return info

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Check whether a dataset is registered"""
        return name in cls._registry


# ===== DATASET REGISTRATION =====
# Register all known datasets
DatasetRegistry.register('adult', AdultConfig)
DatasetRegistry.register('housing', HousingConfig)
DatasetRegistry.register('wine', WineConfig)
DatasetRegistry.register('zillow', ZillowConfig)
DatasetRegistry.register('covertype', CovertypeConfig)
DatasetRegistry.register('electric', ElectricConfig)
DatasetRegistry.register('mnist', MnistConfig)
DatasetRegistry.register('imdb', ImdbConfig)
DatasetRegistry.register('cifar10', Cifar10Config)


# Export for convenience
__all__ = [
    'DatasetRegistry',
    'BaseDatasetConfig',
    'PreprocessingConfig',
    'AdultConfig',
    'HousingConfig',
    'WineConfig',
    'ZillowConfig',
    'CovertypeConfig',
    'ElectricConfig',
    'MnistConfig',
    'ImdbConfig',
    'Cifar10Config',
]
