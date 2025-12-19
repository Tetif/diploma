import pickle
import os
import hashlib
import pandas as pd
from pathlib import Path
from experiments.logger import debug_print


class DataCache:
    """Класс для кэширования предобработанных данных"""

    def __init__(self, cache_dir="data_cache", logger=None):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.logger = logger

    def get_cache_key(self, file_paths, preprocessing_params=None):
        """Генерирует ключ кэша на основе путей к файлам и параметров"""
        if preprocessing_params is None:
            preprocessing_params = {}
        
        # Создаем строку из путей и параметров
        key_string = str(sorted(file_paths)) + str(preprocessing_params)
        
        # Используем хеш для создания короткого ключа
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        return key_hash
    
    def _get_cache_key(self, file_paths, preprocessing_params=None):
        """Приватный метод для обратной совместимости"""
        return self.get_cache_key(file_paths, preprocessing_params)

    def _get_cache_path(self, cache_key, suffix=""):
        """Возвращает путь к файлу кэша"""
        filename = f"preprocessed_{cache_key}{suffix}.pkl"
        return self.cache_dir / filename

    def save(self, X, y, cache_key, metadata=None):
        """Сохраняет предобработанные данные в кэш"""
        try:
            cache_path_X = self._get_cache_path(cache_key, "_X")
            cache_path_y = self._get_cache_path(cache_key, "_y")
            cache_path_meta = self._get_cache_path(cache_key, "_meta")

            # Сохраняем данные
            X.to_pickle(cache_path_X)
            if y is not None:
                y.to_pickle(cache_path_y)
            
            # Сохраняем метаданные
            if metadata:
                with open(cache_path_meta, 'wb') as f:
                    pickle.dump(metadata, f)

            if self.logger:
                self.logger.log_message(f"💾 Data cached: {cache_key[:8]}...")
            else:
                debug_print(f"Data cached: {cache_key[:8]}...")

            return True
        except Exception as e:
            if self.logger:
                self.logger.log_message(f"⚠️ Failed to save cache: {e}")
            else:
                debug_print(f"Failed to save cache: {e}")
            return False

    def load(self, cache_key):
        """Загружает предобработанные данные из кэша"""
        try:
            cache_path_X = self._get_cache_path(cache_key, "_X")
            cache_path_y = self._get_cache_path(cache_key, "_y")
            cache_path_meta = self._get_cache_path(cache_key, "_meta")

            # Проверяем существование файлов
            if not cache_path_X.exists():
                return None, None, None

            # Загружаем данные
            X = pd.read_pickle(cache_path_X)
            y = None
            if cache_path_y.exists():
                y = pd.read_pickle(cache_path_y)

            # Загружаем метаданные
            metadata = None
            if cache_path_meta.exists():
                with open(cache_path_meta, 'rb') as f:
                    metadata = pickle.load(f)

            if self.logger:
                self.logger.log_message(f"📂 Data loaded from cache: {cache_key[:8]}...")
            else:
                debug_print(f"Data loaded from cache: {cache_key[:8]}...")

            return X, y, metadata
        except Exception as e:
            if self.logger:
                self.logger.log_message(f"⚠️ Failed to load cache: {e}")
            else:
                debug_print(f"Failed to load cache: {e}")
            return None, None, None

    def exists(self, cache_key):
        """Проверяет существование кэша"""
        cache_path_X = self._get_cache_path(cache_key, "_X")
        return cache_path_X.exists()

    def clear_cache(self):
        """Очищает весь кэш"""
        try:
            for file in self.cache_dir.glob("preprocessed_*.pkl"):
                file.unlink()
            if self.logger:
                self.logger.log_message("🗑️ Cache cleared")
            else:
                debug_print("Cache cleared")
            return True
        except Exception as e:
            if self.logger:
                self.logger.log_message(f"⚠️ Failed to clear cache: {e}")
            else:
                debug_print(f"Failed to clear cache: {e}")
            return False

