import numpy as np
import pandas as pd
import pydvl
import torch
import matplotlib.pyplot as plt

from config.settings import (
    DEBUG_MODE, EXPERIMENTS_BASE_DIR, DEVICE,
    EXPERIMENT_CONFIG, MODEL_CONFIGS, CACHE_DIR, USE_CACHE
)
from experiments.logger import ExperimentLogger
from data.loader import DataLoader as DataLoaderClass
from data.preprocessor import DataPreprocessor
from data.cache import DataCache
from models.factory import ModelFactory
from experiments.runner import ExperimentRunner
from visualization.plots import (
    plot_influence_distribution,
    plot_results_enhanced
)
from utils.helpers import (
    set_random_seeds, sample_data, split_data,
    check_gpu_availability, print_data_info
)
from influence.utils import get_influence_statistics


def main():
    # Инициализация
    set_random_seeds(42)

    # Создание логгера
    logger = ExperimentLogger(base_dir=EXPERIMENTS_BASE_DIR)

    # Проверка GPU
    gpu_available = check_gpu_availability()
    if gpu_available:
        logger.log_message(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
        logger.log_message(f"   CUDA version: {torch.version.cuda}")
    else:
        logger.log_message("⚠️ GPU not available, using CPU")
        logger.log_message("   To use GPU, ensure CUDA-compatible GPU and PyTorch with CUDA support are installed")

    # Конфигурация эксперимента
    config = {
        'debug_mode': DEBUG_MODE,
        'pyDVL_version': pydvl.__version__,
        'torch_version': torch.__version__,
        'data_files': {
            'properties': 'properties_2016.csv',
            'train': 'train_2016_v2.csv',
            'submission': 'sample_submission.csv'
        },
        'model_params': {
            'model_type': 'catboost',  # Можно менять: lightgbm, xgboost, random_forest, pytorch, catboost
            'model_architecture': 'simple',  # Для pytorch: simple, improved или ft_transformer
            'input_size': 'auto',
            'device': DEVICE
        },
        'training_params': EXPERIMENT_CONFIG.copy()
    }

    # Загрузка данных
    logger.log_message("Starting the program...")
    # Пути к файлам (проверяем наличие в разных местах)
    import os
    if os.path.exists('datasets/properties_2016.csv'):
        PROP_PATH = 'datasets/properties_2016.csv'
        TRAIN_PATH = 'datasets/train_2016_v2.csv'
        SUB_PATH = 'datasets/sample_submission.csv'
    elif os.path.exists('properties_2016.csv'):
        PROP_PATH = 'properties_2016.csv'
        TRAIN_PATH = 'train_2016_v2.csv'
        SUB_PATH = 'sample_submission.csv'
    else:
        raise FileNotFoundError("Не найдены файлы данных. Проверьте наличие файлов в папке datasets/ или в корне проекта")

    logger.log_message("Loading and preparing data...")

    data_loader = DataLoaderClass(logger)
    df, df_subs = data_loader.load_and_merge_data(PROP_PATH, TRAIN_PATH, SUB_PATH)

    # Информация о данных
    logger.log_message(f"📁 File sizes:")
    if os.path.exists(PROP_PATH):
        logger.log_message(f"   {PROP_PATH}: {os.path.getsize(PROP_PATH) / (1024 * 1024):.1f} MB")
    if os.path.exists(TRAIN_PATH):
        logger.log_message(f"   {TRAIN_PATH}: {os.path.getsize(TRAIN_PATH) / (1024 * 1024):.1f} MB")
    if SUB_PATH and os.path.exists(SUB_PATH):
        logger.log_message(f"   {SUB_PATH}: {os.path.getsize(SUB_PATH) / (1024 * 1024):.1f} MB")

    logger.log_message(f"\n📊 DATA SIZE DIAGNOSTICS:")
    logger.log_message(f"   Original dataset size: {len(df)} rows, {len(df.columns)} columns")
    
    # Проверка потери данных при merge
    df_train_check = pd.read_csv(TRAIN_PATH)
    if len(df) < len(df_train_check):
        logger.log_message(f"⚠️ Lost {len(df_train_check) - len(df):,} rows in merge (no matching properties)")

    # Предобработка с кэшированием
    cache = DataCache(cache_dir=CACHE_DIR, logger=logger) if USE_CACHE else None
    cache_key = None
    preprocessor = DataPreprocessor(logger)  # Всегда создаем preprocessor
    
    if cache and USE_CACHE:
        cache_key = cache.get_cache_key([PROP_PATH, TRAIN_PATH], {'target': 'logerror'})
        X, y, metadata = cache.load(cache_key)
        
        if X is not None:
            logger.log_message("✅ Using cached preprocessed data")
        else:
            logger.log_message("📝 Cache not found, preprocessing data...")
            X, y = preprocessor.comprehensive_preprocessing(df, target='logerror')
            
            # Сохраняем в кэш
            metadata = {
                'shape': X.shape,
                'target': 'logerror',
                'preprocessing_time': logger.timings.get('preprocessing', {}).get('duration', 0)
            }
            cache.save(X, y, cache_key, metadata)
    else:
        logger.log_message("📝 Preprocessing data (cache disabled)...")
        X, y = preprocessor.comprehensive_preprocessing(df, target='logerror')

    logger.log_message(f"   After preprocessing: {X.shape[0]} rows, {X.shape[1]} features")

    # Построение предобработчика
    preproc_pipeline, num_cols, cat_cols = preprocessor.build_preprocessor(X)

    # Выборка данных
    n = 0.001  # 0.1% от данных
    logger.log_message(f"\nTaking {n * 100}% sample of the data...")
    X_sample, y_sample = sample_data(X, y, sample_fraction=n)

    config['training_params']['sample_size_percentage'] = n * 100
    config['training_params']['final_sample_size'] = X_sample.shape[0]
    config['data_info'] = {
        'original_rows': len(df),
        'final_training_rows': X_sample.shape[0],
        'numeric_columns': len(num_cols),
        'categorical_columns': len(cat_cols),
        'total_features': len(num_cols) + len(cat_cols)
    }

    # Разделение данных
    logger.log_message("Splitting data...")
    X_train, X_val, y_train, y_val = split_data(X_sample, y_sample)
    logger.log_message(f"Training set size: {len(X_train)}, Validation set size: {len(X_val)}")

    # Параметры модели
    model_params = {
        'model_type': 'lightgbm',  # Можно менять
        'model_architecture': 'ft_transformer_simple',
        'input_size': X_sample.shape[1],
        'device': DEVICE,
        'removal_strategy': 'remove_lowest_influence'
    }

    n_epochs = 50 if model_params['model_type'] == 'pytorch' else 1
    config['model_params'] = model_params
    config['training_params']['n_epochs'] = n_epochs

    logger.log_message(f"cuda available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.log_message(f"device count: {torch.cuda.device_count()}")
        logger.log_message(f"device name: {torch.cuda.get_device_name(0)}")
    
    logger.log_message(f"Using device: {DEVICE}")
    logger.log_message(f"Using model: {model_params['model_type']}")
    logger.log_message(f"Training epochs: {n_epochs}")

    # Список процентов удаления
    n_remove_list = np.linspace(2, 100, 50, dtype=int).tolist()
    config['experiment_params'] = {
        'n_remove_percentages': n_remove_list,
        'removal_strategy': model_params['removal_strategy']
    }

    # Сохранение конфигурации
    logger.save_config(config)

    # Запуск экспериментов
    logger.log_message("Starting experiments...")

    experiment_runner = ExperimentRunner(logger)
    results, scores, scores_raw = experiment_runner.run_experiments(
        X_train, y_train, X_val, y_val,
        preproc_pipeline, model_params,
        n_remove_list, n_epochs
    )

    # Визуализация
    logger.log_message("Plotting results...")
    logger.save_results(results, scores, scores_raw, n_remove_list)

    # Визуализация распределения influence scores
    plot_influence_distribution(scores, "normalized", logger)
    plt.show()

    plot_influence_distribution(scores_raw, "raw", logger)
    plt.show()

    # Визуализация результатов экспериментов
    plot_results_enhanced(results, n_remove_list, logger)
    plt.show()

    # Генерация отчета
    model_metrics = {
        'baseline_mae': results['orig']['final_mae'],
        'best_validation_mae': results['orig']['best_val_mae'],
        'best_epoch': results['orig']['best_epoch'],
        'total_training_epochs': n_epochs,
        'model_type': model_params['model_type']
    }

    influence_stats = get_influence_statistics(scores)
    logger.generate_summary(config, model_metrics, influence_stats, scores, scores_raw)

    logger.log_message("Program completed successfully!")
    logger.log_message(f"All results saved in: {logger.get_experiment_dir()}")


if __name__ == '__main__':
    main()