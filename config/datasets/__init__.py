"""Реестр конфигураций датасетов"""

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
    """Реестр для управления конфигурациями датасетов"""

    _registry: Dict[str, Type[BaseDatasetConfig]] = {}

    @classmethod
    def register(cls, name: str, config_class: Type[BaseDatasetConfig]) -> None:
        """
        Регистрировать конфигурацию датасета
        
        Args:
            name: Уникальное имя датасета
            config_class: Класс конфигурации
        """
        if name in cls._registry:
            print(f"Warning: Dataset '{name}' already registered. Overwriting...")
        cls._registry[name] = config_class

    @classmethod
    def get(cls, name: str) -> BaseDatasetConfig:
        """
        Получить конфигурацию датасета
        
        Args:
            name: Имя датасета
            
        Returns:
            Экземпляр конфигурации датасета
            
        Raises:
            KeyError: Если датасет не зарегистрирован
        """
        if name not in cls._registry:
            available = ', '.join(cls._registry.keys())
            raise KeyError(f"Dataset '{name}' not found. Available datasets: {available}")

        config_class = cls._registry[name]
        return config_class()

    @classmethod
    def list(cls) -> list:
        """Получить список всех зарегистрированных датасетов"""
        return list(cls._registry.keys())

    @classmethod
    def get_all_info(cls) -> Dict[str, dict]:
        """Получить информацию по всем датасетам"""
        info = {}
        for name in cls._registry:
            config = cls.get(name)
            info[name] = config.get_info()
        return info

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Проверить, зарегистрирован ли датасет"""
        return name in cls._registry


# ===== РЕГИСТРАЦИЯ ДАТАСЕТОВ =====
# Регистрируем все известные датасеты
DatasetRegistry.register('adult', AdultConfig)
DatasetRegistry.register('housing', HousingConfig)
DatasetRegistry.register('wine', WineConfig)
DatasetRegistry.register('zillow', ZillowConfig)
DatasetRegistry.register('covertype', CovertypeConfig)
DatasetRegistry.register('electric', ElectricConfig)
DatasetRegistry.register('mnist', MnistConfig)
DatasetRegistry.register('imdb', ImdbConfig)
DatasetRegistry.register('cifar10', Cifar10Config)


# Экспортируем для удобства
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
