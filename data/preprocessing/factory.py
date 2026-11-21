"""
Factory that creates preprocessors for different data types.
"""

from .base import BasePreprocessor
from .tabular import TabularPreprocessor
from config.datasets.base import BaseDatasetConfig


class PreprocessorFactory:
    """Factory that creates preprocessors"""

    @staticmethod
    def create(dataset_config: BaseDatasetConfig, logger=None) -> BasePreprocessor:
        """
        Create a preprocessor for a dataset
        
        Args:
            dataset_config: Dataset configuration
            logger: Logger for output
            
        Returns:
            Preprocessor of the matching type
            
        Raises:
            ValueError: If the data type is not supported
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
