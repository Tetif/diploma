import numpy as np
import pandas as pd
import pydvl
import torch
import matplotlib.pyplot as plt
import argparse
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm

from sklearn.model_selection import train_test_split

from config.settings import (
    DEBUG_MODE, EXPERIMENTS_BASE_DIR, DEVICE,
    EXPERIMENT_CONFIG, MODEL_CONFIGS, CACHE_DIR, USE_CACHE, DISTILLATION_CONFIG, RANDOM_STATE,
    CURRENT_DATASET, get_model_config
)
from config import DatasetRegistry
from experiments.logger import ExperimentLogger
from data.loader import DataLoaderFactory
from data.preprocessing import PreprocessorFactory
from data.cache import DataCache
from models.factory import ModelFactory
from experiments.runner import ExperimentRunner
from visualization.plots import (
    plot_influence_distribution,
    plot_results_enhanced,
    plot_combined_comparison
)
from utils.helpers import (
    set_random_seeds, sample_data, split_data,
    check_gpu_availability, print_data_info
)
from influence.utils import get_influence_statistics


def main(dataset_name=None):
    """
    Основная функция для запуска экспериментов с любым датасетом
    
    Args:
        dataset_name: Имя датасета ('zillow', 'adult', 'housing', 'wine')
                     Если None, используется CURRENT_DATASET из settings
    """
    # Выбираем датасет
    if dataset_name is None:
        dataset_name = CURRENT_DATASET
    
    # Получаем конфиг датасета
    try:
        dataset_config = DatasetRegistry.get(dataset_name)
    except KeyError as e:
        print(f"Error: {e}")
        print(f"Available datasets: {', '.join(DatasetRegistry.list())}")
        return
    
    set_random_seeds(RANDOM_STATE)
    logger = ExperimentLogger(base_dir=EXPERIMENTS_BASE_DIR)

    logger.log_message(f"\n{'='*60}")
    logger.log_message(f"DATASET: {dataset_config.name.upper()}")
    logger.log_message(f"TASK TYPE: {dataset_config.task_type}")
    logger.log_message(f"TARGET COLUMN: {dataset_config.target_column}")
    logger.log_message(f"{'='*60}")

    gpu_available = check_gpu_availability()
    if gpu_available:
        logger.log_message(f"GPU detected: {torch.cuda.get_device_name(0)}")
        logger.log_message(f"   CUDA version: {torch.version.cuda}")
    else:
        logger.log_message("GPU not available, using CPU")

    # Конфигурация эксперимента
    config = {
        'debug_mode': DEBUG_MODE,
        'pyDVL_version': pydvl.__version__,
        'torch_version': torch.__version__,
        'dataset': {
            'name': dataset_config.name,
            'task_type': dataset_config.task_type,
            'target_column': dataset_config.target_column,
            'data_type': dataset_config.data_type,
            'metrics': dataset_config.metrics
        },
        'model_params': {
            'model_type': 'random_forest',  # Можно менять: lightgbm, xgboost, random_forest, pytorch, catboost
            'model_architecture': 'simple',  # Для pytorch: simple, improved или ft_transformer
            'input_size': 'auto',
            'device': DEVICE,
            'removal_strategy': 'remove_lowest_influence',
            # Параметры дистилляции
            'use_distillation': DISTILLATION_CONFIG['use_distillation'],
            'distillation_epochs': DISTILLATION_CONFIG['distillation_epochs'],
            'temperature': DISTILLATION_CONFIG['temperature'],
            'student_architecture': DISTILLATION_CONFIG['student_architecture']
        },
        'training_params': EXPERIMENT_CONFIG.copy(),
        'distillation_config': DISTILLATION_CONFIG.copy()
    }

    logger.log_message("Loading and preparing data...")

    # Загружаем данные используя фабрику
    X, y, cfg = DataLoaderFactory.load_dataset(dataset_config, logger)
    
    logger.log_message(f"Data loaded: {X.shape[0]} rows, {X.shape[1]} columns")
    logger.log_message(f"Target shape: {y.shape}")

    # Кодируем целевую переменную если это классификация
    if cfg.task_type in ['binary_classification', 'multiclass_classification']:
        if y.dtype == 'object' or y.dtype.name == 'object':
            logger.log_message("Encoding target variable for classification...")
            le = LabelEncoder()
            y = pd.Series(le.fit_transform(y), index=y.index)
            logger.log_message(f"  Classes: {le.classes_}")

    # Отделяем данные для holdout validation
    X_temp, X_holdout_validation, y_temp, y_holdout_validation = train_test_split(
        X, y,
        test_size=cfg.val_size,
        random_state=RANDOM_STATE,
        stratify=y if cfg.stratify else None
    )
    logger.log_message(f"Holdout validation set created: {len(X_holdout_validation)} rows (untouched)")

    # Теперь от оставшихся данных берем подвыборку для быстрых тестов (по умолчанию 100%)
    n = EXPERIMENT_CONFIG['sample_size_percentage'] / 100.0
    logger.log_message(f"Taking {n * 100}%")
    X_sample, y_sample = sample_data(X_temp, y_temp, sample_fraction=n)

    logger.log_message(f"Training sample size: {X_sample.shape[0]} rows, {X_sample.shape[1]} features")

    # Разделяем подвыборку на train и test для обучения моделей
    logger.log_message("Splitting training sample into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_sample, y_sample, test_size=EXPERIMENT_CONFIG['test_size'], random_state=RANDOM_STATE
    )

    logger.log_message(f"Final data split:")
    logger.log_message(f"   Train: {len(X_train)} rows")
    logger.log_message(f"   Test: {len(X_test)} rows")
    logger.log_message(f"   Holdout Validation: {len(X_holdout_validation)} rows")

    # Создаем предобработчик используя фабрику
    logger.log_message("Creating preprocessor...")
    preprocessor = PreprocessorFactory.create(dataset_config, logger)

    # Подгоняем предобработчик на train данных
    logger.log_message("Fitting preprocessor on training data...")
    preprocessor.fit(X_train)

    # Трансформируем все данные для baseline
    logger.log_message("Transforming data...")
    X_train_processed = preprocessor.transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    X_validation_processed = preprocessor.transform(X_holdout_validation)

    # Конвертируем в numpy если нужно
    if hasattr(X_train_processed, 'toarray'):
        X_train_processed = X_train_processed.toarray()
        X_test_processed = X_test_processed.toarray()
        X_validation_processed = X_validation_processed.toarray()

    actual_input_size = X_train_processed.shape[1]

    config['training_params']['sample_size_percentage'] = n * 100
    config['training_params']['final_sample_size'] = len(X_train_processed) + len(X_test_processed)
    config['data_info'] = {
        'original_rows': len(X),
        'remaining_after_holdout': len(X_temp),
        'training_sample_rows': len(X_sample),
        'final_training_rows': len(X_train_processed),
        'final_test_rows': len(X_test_processed),
        'holdout_validation_rows': len(X_validation_processed),
        'total_features': X_train_processed.shape[1],
        'preprocessed_features': actual_input_size
    }

    # Получаем оптимальные параметры модели для этого датасета
    model_type = config['model_params']['model_type']
    logger.log_message(f"\nLoading optimal model configuration for {dataset_name} + {model_type}...")
    
    try:
        # Получаем параметры модели для конкретного датасета
        dataset_model_config = get_model_config(dataset_name, model_type)
        logger.log_message(f"Using optimized parameters for {dataset_name} dataset")
        logger.log_message(f"Model config: {dataset_model_config}")
    except ValueError as e:
        logger.log_message(f"Warning: {e}. Using default parameters from MODEL_CONFIGS")
        dataset_model_config = MODEL_CONFIGS.get(model_type, {})

    model_params = config['model_params'].copy()
    model_params['input_size'] = actual_input_size
    model_params['task_type'] = cfg.task_type
    
    # Добавляем оптимальные параметры в model_params (но не перезаписываем уже установленные)
    for key, value in dataset_model_config.items():
        if key not in model_params or key in ['learning_rate', 'num_leaves', 'max_depth', 'iterations', 'n_estimators', 'layers', 'dropout']:
            model_params[key] = value

    if model_params['model_type'] == 'pytorch' or model_params.get('use_distillation', False):
        n_epochs = 500
    else:
        n_epochs = 1

    config['model_params'] = model_params
    config['training_params']['n_epochs'] = n_epochs


    n_remove_list = np.linspace(1, 99, 33, dtype=int).tolist()

    config['experiment_params'] = {
        'n_remove_percentages': n_remove_list,
        'removal_strategy': model_params['removal_strategy']
    }
    logger.save_config(config)
    logger.log_message("Starting experiments")

    experiment_runner = ExperimentRunner(logger)

    results, scores, scores_raw = experiment_runner.run_experiments(
        X_train, 
        y_train, 
        X_test, 
        y_test, 
        X_holdout_validation, 
        y_holdout_validation,
        preprocessor, 
        model_params,
        n_remove_list, 
        n_epochs,
        dataset_config=dataset_config
    )

    # Визуализация
    logger.log_message("Plotting results...")
    logger.save_results(results, scores, scores_raw, n_remove_list)

    plot_influence_distribution(scores_raw, "influence_scores", logger)
    plt.show()

    # Получаем random_run_results из experiment_runner если они доступны
    random_run_results = getattr(experiment_runner, 'random_run_results', None)
    plot_results_enhanced(results, n_remove_list, logger, random_run_results=random_run_results)
    plt.show()

    # plot_combined_comparison(results, n_remove_list, logger)
    # plt.show()

    # Генерация отчета
    model_metrics = {
        'baseline_mae': results['orig']['final_mae'],
        'best_validation_mae': results['orig']['best_val_mae'],
        'best_epoch': results['orig']['best_epoch'],
        'total_training_epochs': n_epochs,
        'model_type': model_params['model_type'],
        'used_distillation': model_params.get('use_distillation', False),
        'distillation_epochs': model_params.get('distillation_epochs', 0) if model_params.get('use_distillation', False) else 0,
        'student_architecture': model_params.get('student_architecture', 'none') if model_params.get('use_distillation', False) else 'none'
    }

    influence_stats = get_influence_statistics(scores_raw)
    logger.generate_summary(config, model_metrics, influence_stats, scores, scores_raw)

    logger.log_message("Program completed successfully!")
    logger.log_message(f"All results saved in: {logger.get_experiment_dir()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run experiments with different datasets')
    parser.add_argument('--dataset', type=str, default=None,
                       help=f'Dataset name: {', '.join(DatasetRegistry.list())}. Default: {CURRENT_DATASET}')
    args = parser.parse_args()
    
    main(args.dataset)