import numpy as np
import pandas as pd
import pydvl
import torch
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from config.settings import (
    DEBUG_MODE, EXPERIMENTS_BASE_DIR, DEVICE,
    EXPERIMENT_CONFIG, MODEL_CONFIGS, CACHE_DIR, USE_CACHE, DISTILLATION_CONFIG
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
        logger.log_message(f"GPU detected: {torch.cuda.get_device_name(0)}")
        logger.log_message(f"   CUDA version: {torch.version.cuda}")
    else:
        logger.log_message("GPU not available, using CPU")
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
            'model_type': 'random_forest',  # Можно менять: lightgbm, xgboost, random_forest, pytorch, catboost
            'model_architecture': 'simple',  # Для pytorch: simple, improved или ft_transformer
            'input_size': 'auto',
            'device': DEVICE,
            'removal_strategy': 'remove_highest_influence',
            # Параметры дистилляции
            'use_distillation': DISTILLATION_CONFIG['use_distillation'],
            'distillation_epochs': DISTILLATION_CONFIG['distillation_epochs'],
            'temperature': DISTILLATION_CONFIG['temperature'],
            'student_architecture': DISTILLATION_CONFIG['student_architecture']
        },
        'training_params': EXPERIMENT_CONFIG.copy(),
        'distillation_config': DISTILLATION_CONFIG.copy()
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
    logger.log_message(f"File sizes:")
    if os.path.exists(PROP_PATH):
        logger.log_message(f"   {PROP_PATH}: {os.path.getsize(PROP_PATH) / (1024 * 1024):.1f} MB")
    if os.path.exists(TRAIN_PATH):
        logger.log_message(f"   {TRAIN_PATH}: {os.path.getsize(TRAIN_PATH) / (1024 * 1024):.1f} MB")
    if SUB_PATH and os.path.exists(SUB_PATH):
        logger.log_message(f"   {SUB_PATH}: {os.path.getsize(SUB_PATH) / (1024 * 1024):.1f} MB")

    logger.log_message(f"\nDATA SIZE DIAGNOSTICS:")
    logger.log_message(f"   Original dataset size: {len(df)} rows, {len(df.columns)} columns")
    
    # Проверка потери данных при merge
    df_train_check = pd.read_csv(TRAIN_PATH)
    if len(df) < len(df_train_check):
        logger.log_message(f"Lost {len(df_train_check) - len(df):,} rows in merge (no matching properties)")

    # СНАЧАЛА ОТДЕЛЯЕМ HOLDOUT VALIDATION ОТ ПОЛНОГО ДАТАСЕТА
    logger.log_message("Creating holdout validation set from full dataset...")
    X_full = df.drop(columns=['logerror'])
    y_full = df['logerror']

    # Отделяем 20% данных для holdout validation - эти данные БОЛЬШЕ НИКОГДА НЕ ИСПОЛЬЗУЮТСЯ
    X_temp, X_holdout_validation, y_temp, y_holdout_validation = train_test_split(
        X_full, y_full, test_size=0.2, random_state=42
    )

    logger.log_message(f"Holdout validation set created: {len(X_holdout_validation)} rows (untouched)")

    # Теперь от оставшихся 80% данных берем подвыборку для эффективного обучения
    n = 1
    logger.log_message(f"Taking {n * 100}% sample from remaining {len(X_temp)} rows for training...")
    X_sample, y_sample = sample_data(X_temp, y_temp, sample_fraction=n)

    logger.log_message(f"Training sample size: {X_sample.shape[0]} rows, {X_sample.shape[1]} features")

    # Разделяем подвыборку на train и test для обучения моделей
    logger.log_message("Splitting training sample into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_sample, y_sample, test_size=0.25, random_state=42
    )

    logger.log_message(f"Final data split:")
    logger.log_message(f"   Train: {len(X_train)} rows (for training models)")
    logger.log_message(f"   Test: {len(X_test)} rows (for validation during training)")
    logger.log_message(f"   Holdout Validation: {len(X_holdout_validation)} rows (NEVER USED until final evaluation)")

    # Сначала определяем колонки для удаления на объединенном train+test датасете
    preprocessor = DataPreprocessor(logger)
    logger.log_message("Determining columns to drop from combined train+test data...")
    X_train_test_combined = pd.concat([pd.concat([X_train, y_train], axis=1),
                                       pd.concat([X_test, y_test], axis=1)])
    _, _, _, cols_to_drop = preprocessor.comprehensive_preprocessing(
        X_train_test_combined, target='logerror', fit=True
    )

    # Предобработка: рассчитываем статистики ТОЛЬКО на train
    logger.log_message("Preprocessing training data (computing statistics)...")
    X_train_processed, y_train_processed, stats_dict, _ = preprocessor.comprehensive_preprocessing(
        pd.concat([X_train, y_train], axis=1),
        target='logerror', fit=True, cols_to_drop=cols_to_drop
    )

    # Применяем те же статистики и колонки к test данным
    logger.log_message("Preprocessing test data (using train statistics)...")
    X_test_processed, y_test_processed = preprocessor.comprehensive_preprocessing(
        pd.concat([X_test, y_test], axis=1),
        target='logerror', fit=False, stats_dict=stats_dict, cols_to_drop=cols_to_drop
    )

    # VALIDATION ДАННЫЕ ОСТАЮТСЯ НЕТРОНУТЫМИ ДО КОНЦА!

    logger.log_message(f"Training set size: {len(X_train_processed)}, Test set size: {len(X_test_processed)}")
    logger.log_message(f"Holdout validation set size: {len(X_holdout_validation)} (untouched)")

    # Построение предобработчика на тренировочных данных
    preproc_pipeline, num_cols, cat_cols = preprocessor.build_preprocessor(X_train_processed)

    # Временно обучаем предобработчик на небольшой выборке для определения размерности выхода
    sample_size = min(1000, len(X_train_processed))
    X_sample_for_fitting = X_train_processed.head(sample_size)
    preproc_pipeline.fit(X_sample_for_fitting)
    X_transformed_sample = preproc_pipeline.transform(X_sample_for_fitting)
    if hasattr(X_transformed_sample, 'toarray'):
        X_transformed_sample = X_transformed_sample.toarray()
    actual_input_size = X_transformed_sample.shape[1]

    config['training_params']['sample_size_percentage'] = n * 100
    config['training_params']['final_sample_size'] = len(X_train_processed) + len(X_test_processed)
    config['data_info'] = {
        'original_rows': len(df),
        'remaining_after_holdout': len(X_temp),
        'training_sample_rows': len(X_sample),
        'final_training_rows': len(X_train_processed),
        'final_test_rows': len(X_test_processed),
        'holdout_validation_rows': len(X_holdout_validation),
        'numeric_columns': len(num_cols),
        'categorical_columns': len(cat_cols),
        'total_features': len(num_cols) + len(cat_cols),
        'preprocessed_features': actual_input_size
    }

    # num_cols = X_sample.select_dtypes(include=['number']).columns.tolist()
    # cat_cols = X_sample.select_dtypes(include=['category']).columns.tolist()

    # Параметры модели
    model_params = config['model_params'].copy()  # Создаем копию
    model_params['input_size'] = actual_input_size  # Используем размерность после предобработки
    model_params['device'] = DEVICE
    model_params['removal_strategy'] = 'remove_lowest_influence'
    # Добавляем параметры дистилляции
    model_params.update({
        'use_distillation': config['distillation_config']['use_distillation'],
        'distillation_epochs': config['distillation_config']['distillation_epochs'],
        'temperature': config['distillation_config']['temperature'],
        'student_architecture': config['distillation_config']['student_architecture']
    })
    # model_params = {
    #     'model_type': 'pytorch',  # Можно менять: lightgbm, xgboost, random_forest, pytorch, catboost
    #     'model_architecture': 'simple',
    #     # 'input_size': X_sample.shape[1],
    #     'input_size': len(num_cols) + len(cat_cols),
    #     'device': DEVICE,
    #     'removal_strategy': 'remove_lowest_influence'
    # }
    # model_params = config['model_params']

    # Определяем количество эпох в зависимости от типа модели и использования дистилляции
    if model_params['model_type'] == 'pytorch' or model_params.get('use_distillation', False):
        n_epochs = 500  # Меньше эпох для PyTorch и дистиллированных моделей
    else:
        n_epochs = 1  # 1 эпоха для tree-based моделей

    config['model_params'] = model_params
    config['training_params']['n_epochs'] = n_epochs

    logger.log_message(f"cuda available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.log_message(f"device count: {torch.cuda.device_count()}")
        logger.log_message(f"device name: {torch.cuda.get_device_name(0)}")
    
    logger.log_message(f"Using device: {DEVICE}")
    logger.log_message(f"Using model: {model_params['model_type']}")
    logger.log_message(f"Using distillation: {model_params.get('use_distillation', False)}")
    if model_params.get('use_distillation', False):
        logger.log_message(f"Distillation epochs: {model_params.get('distillation_epochs', 50)}")
        logger.log_message(f"Student architecture: {model_params.get('student_architecture', 'simple')}")
    logger.log_message(f"Training epochs: {n_epochs}")

    # Список процентов удаления
    n_remove_list = np.linspace(2, 100, 33, dtype=int).tolist()
    config['experiment_params'] = {
        'n_remove_percentages': n_remove_list,
        'removal_strategy': model_params['removal_strategy']
    }

    # Сохранение конфигурации
    logger.save_config(config)

    # Предобрабатываем holdout validation данные с использованием статистик из train
    X_validation_processed, y_validation_processed = preprocessor.comprehensive_preprocessing(
        pd.concat([X_holdout_validation, y_holdout_validation], axis=1),
        target='logerror', fit=False, stats_dict=stats_dict
    )

    # Запуск экспериментов (используем train+test для обучения, validation оставляем для финальной оценки)
    logger.log_message("Starting experiments (train+test for training, validation held out)...")

    experiment_runner = ExperimentRunner(logger)
    # results, scores, scores_raw = experiment_runner.run_experiments(
    #     X_train_processed, y_train_processed, X_test_processed, y_test_processed,
    #     preproc_pipeline, model_params,
    #     n_remove_list, n_epochs
    # )

    results, scores, scores_raw = experiment_runner.run_experiments(
        X_train_processed, y_train_processed, X_validation_processed, y_validation_processed,
        preproc_pipeline, model_params,
        n_remove_list, n_epochs
    )

    # Финальная оценка на holdout validation
    logger.log_message("Final evaluation on holdout validation set...")



    # Получаем лучшую модель из экспериментов (baseline модель)
    from models.factory import ModelFactory
    model = ModelFactory.create_model(model_params)

    # Обучаем модель на всех train+test данных
    X_train_test = pd.concat([X_train_processed, X_test_processed])
    y_train_test = pd.concat([y_train_processed, y_test_processed])

    preproc_pipeline, _, _ = preprocessor.build_preprocessor(X_train_test)
    preproc_pipeline.fit(X_train_test)
    X_train_test_transformed = preproc_pipeline.transform(X_train_test)
    X_holdout_validation_transformed = preproc_pipeline.transform(X_validation_processed)

    model.fit(X_train_test_transformed, y_train_test.values if hasattr(y_train_test, 'values') else y_train_test)

    # Предсказания на holdout validation
    y_pred_validation = model.predict(X_holdout_validation_transformed)
    validation_mae = np.mean(np.abs(y_pred_validation - y_validation_processed.values))

    logger.log_message(f"Final validation MAE: {validation_mae:.4f}")
    logger.log_message(f"   (This is the true unbiased estimate of model performance)")

    # Добавляем финальную метрику в результаты
    results['final_holdout_validation'] = {
        'mae': validation_mae,
        'n_samples': len(X_validation_processed)
    }

    # Визуализация
    logger.log_message("Plotting results...")
    logger.save_results(results, scores, scores_raw, n_remove_list)

    # Визуализация распределения influence scores
    plot_influence_distribution(scores_raw, "influence_scores", logger)
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
        'model_type': model_params['model_type'],
        'used_distillation': model_params.get('use_distillation', False),
        'distillation_epochs': model_params.get('distillation_epochs', 0) if model_params.get('use_distillation', False) else 0,
        'student_architecture': model_params.get('student_architecture', 'none') if model_params.get('use_distillation', False) else 'none',
        'final_holdout_validation_mae': results['final_holdout_validation']['mae'],
        'holdout_validation_samples': results['final_holdout_validation']['n_samples']
    }

    influence_stats = get_influence_statistics(scores_raw)
    logger.generate_summary(config, model_metrics, influence_stats, scores, scores_raw)

    logger.log_message("Program completed successfully!")
    logger.log_message(f"All results saved in: {logger.get_experiment_dir()}")


if __name__ == '__main__':
    main()