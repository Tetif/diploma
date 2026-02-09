"""
Фабрика для создания предобработчиков для разных типов данных.
"""

from .base import BasePreprocessor
from .tabular import TabularPreprocessor
from config.datasets.base import BaseDatasetConfig


class PreprocessorFactory:
    """Фабрика для создания предобработчиков"""

    @staticmethod
    def create(dataset_config: BaseDatasetConfig, logger=None) -> BasePreprocessor:
        """
        Создать предобработчик для датасета
        
        Args:
            dataset_config: Конфигурация датасета
            logger: Логгер для вывода информации
            
        Returns:
            Предобработчик подходящего типа
            
        Raises:
            ValueError: Если тип данных не поддерживается
        """
        data_type = dataset_config.data_type

        if data_type == 'tabular':
            return TabularPreprocessor(dataset_config, logger)
        elif data_type == 'text':
            raise NotImplementedError("Text preprocessing not yet implemented")
        elif data_type == 'image':
            raise NotImplementedError("Image preprocessing not yet implemented")
        else:
            raise ValueError(f"Unknown data type: {data_type}")
