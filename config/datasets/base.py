"""
Базовый класс для конфигурации датасетов.
Определяет интерфейс для работы с различными датасетами.
"""

from typing import List, Tuple, Optional, Dict, Any
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class PreprocessingConfig:
    """Конфигурация предобработки для датасета"""

    def __init__(self):
        self.handle_missing_values: bool = True
        self.missing_threshold: float = 0.7  # Drop columns with >70% missing
        self.encode_categorical: bool = True
        self.scale_numeric: bool = True
        self.remove_outliers: bool = False
        self.create_features: bool = False
        
        # Специфичные параметры для датасета (переопределяются в подклассах)
        self.custom_preprocessing_steps: List[str] = []


class BaseDatasetConfig(ABC):
    """Абстрактный базовый класс конфигурации датасета"""

    # ===== ИДЕНТИФИКАЦИЯ =====
    name: str  # Уникальное имя датасета
    description: str  # Описание датасета
    data_type: str  # 'tabular', 'text', 'image', 'sequence'
    task_type: str  # 'regression', 'binary_classification', 'multiclass_classification'

    # ===== ПУТИ =====
    data_path: str  # Базовый путь к данным
    required_files: List[str]  # Необходимые файлы

    # ===== СТРУКТУРА ДАННЫХ =====
    target_column: str  # Название целевой переменной
    id_column: Optional[str] = None  # Идентификатор (если есть)
    columns_to_drop: List[str]  # Колонки, которые нужно удалить
    categorical_columns: List[str]  # Категориальные признаки
    numeric_columns: List[str]  # Числовые признаки

    # ===== ПАРАМЕТРЫ РАЗДЕЛЕНИЯ =====
    test_size: float = 0.2  # Размер тестового множества
    val_size: float = 0.1  # Размер валидационного множества
    random_state: int = 39
    stratify: bool = False  # Стратифицированное разделение (для классификации)

    # ===== МЕТРИКИ =====
    metrics: List[str]  # Метрики для оценки

    # ===== КОНФИГУРАЦИЯ ПРЕДОБРАБОТКИ =====
    preprocessing_config: PreprocessingConfig

    def __init__(self):
        """Инициализация конфига"""
        if not hasattr(self, 'preprocessing_config') or self.preprocessing_config is None:
            self.preprocessing_config = PreprocessingConfig()

    @abstractmethod
    def load_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Загрузить данные датасета
        
        Returns:
            Tuple[pd.DataFrame, pd.Series]: (признаки, целевая переменная)
        """
        pass

    @abstractmethod
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Валидировать загруженные данные
        
        Args:
            df: DataFrame с данными
            
        Returns:
            bool: True если данные валидны
        """
        pass

    def get_preprocessing_config(self) -> PreprocessingConfig:
        """Получить конфиг предобработки"""
        return self.preprocessing_config

    def get_all_features(self) -> List[str]:
        """Получить все признаки (категориальные + числовые)"""
        return self.categorical_columns + self.numeric_columns

    def get_info(self) -> Dict[str, Any]:
        """Получить информацию о датасете"""
        return {
            'name': self.name,
            'description': self.description,
            'data_type': self.data_type,
            'task_type': self.task_type,
            'target_column': self.target_column,
            'n_categorical_features': len(self.categorical_columns),
            'n_numeric_features': len(self.numeric_columns),
            'test_size': self.test_size,
            'val_size': self.val_size,
            'stratify': self.stratify,
            'metrics': self.metrics
        }
