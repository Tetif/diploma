import importlib
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
    EXPERIMENT_CONFIG, DISTILLATION_CONFIG, RANDOM_STATE,
    CURRENT_DATASET, get_model_config, get_selected_metric, get_metric_metadata,
    MODEL_RUN_CONFIG, get_n_remove_list, get_selected_loss_removal_methods,
    REMOVAL_STRATEGIES,
    MODEL_FIT_MODE, FIT_MODE_EPOCHS,
)
from config import DatasetRegistry
from experiments.logger import ExperimentLogger
from data.loader import DataLoaderFactory
from data.preprocessing import PreprocessorFactory
from models.factory import ModelFactory
from experiments.runner import ExperimentRunner
from visualization.plots import (
    plot_influence_distribution,
    plot_results_enhanced,
    plot_combined_comparison,
    save_removal_metrics_csv,
    plot_method_comparison_bars,
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
        dataset_name: Имя датасета ('zillow', 'adult', 'housing', 'wine', 'covertype', 'electric', 'mnist', 'imdb', 'cifar10').
                     Если None, используется CURRENT_DATASET из settings
    """
    # Выбираем датасет: без --dataset строго из config/settings.py
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
    logger.log_message(f"FIT MODE: {MODEL_FIT_MODE}")
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
        'fit_mode': MODEL_FIT_MODE,
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
            'model_type': MODEL_RUN_CONFIG['model_type'],
            'model_architecture': MODEL_RUN_CONFIG['model_architecture'],
            'input_size': 'auto',
            'device': DEVICE,
            # Набор стратегий удаления для influence-методов (одна или несколько)
            'removal_strategies': MODEL_RUN_CONFIG.get('removal_strategies', REMOVAL_STRATEGIES),
            'removal_per_class': MODEL_RUN_CONFIG.get('removal_per_class', False),
            'removal_stratify_target': MODEL_RUN_CONFIG.get('removal_stratify_target', False),
            'removal_stratify_n_bins': MODEL_RUN_CONFIG.get('removal_stratify_n_bins', 10),
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
    X_temp, X_holdout_validation, y_temp, y_holdout_validation = split_data(
        X,
        y,
        test_size=cfg.val_size,
        random_state=RANDOM_STATE,
        stratify=y if cfg.stratify else None,
        time_series=cfg.use_time_split,
    )
    logger.log_message(f"Holdout validation set created: {len(X_holdout_validation)} rows (untouched)")

    # Теперь от оставшихся данных берем подвыборку для быстрых тестов (по умолчанию 100%)
    n = EXPERIMENT_CONFIG['sample_size_percentage'] / 100.0
    logger.log_message(f"Taking {n * 100}%")
    X_sample, y_sample = sample_data(
        X_temp,
        y_temp,
        sample_fraction=n,
        preserve_order=cfg.use_time_split,
    )

    logger.log_message(f"Training sample size: {X_sample.shape[0]} rows, {X_sample.shape[1]} features")

    # Разделяем подвыборку на train и test для обучения моделей
    logger.log_message("Splitting training sample into train/test sets...")
    X_train, X_test, y_train, y_test = split_data(
        X_sample,
        y_sample,
        test_size=EXPERIMENT_CONFIG['test_size'],
        random_state=RANDOM_STATE,
        time_series=cfg.use_time_split,
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
        logger.log_message(f"Warning: {e}. Using default parameters.")
        from config.settings import DATASET_MODEL_CONFIGS
        fit_configs = DATASET_MODEL_CONFIGS.get(dataset_name, {})
        normal_config = fit_configs.get(MODEL_FIT_MODE, fit_configs.get('normal', {}))
        dataset_model_config = normal_config.get(model_type, {}) if isinstance(normal_config, dict) else {}

    model_params = config['model_params'].copy()
    model_params['input_size'] = actual_input_size
    model_params['task_type'] = cfg.task_type
    model_params['available_metrics'] = list(getattr(cfg, 'metrics', []))

    # Добавляем оптимальные параметры в model_params (но не перезаписываем уже установленные)
    for key, value in dataset_model_config.items():
        if key not in model_params or key in [
            'learning_rate', 'num_leaves', 'max_depth', 'iterations', 'n_estimators',
            'layers', 'dropout', 'base_channels',
        ]:
            model_params[key] = value

    if cfg.task_type == 'multiclass_classification':
        model_params['num_class'] = int(len(np.unique(np.asarray(y_train).ravel())))

    # Для бинарной классификации (PyTorch): pos_weight для BCEWithLogitsLoss уменьшает эффект дисбаланса классов
    if cfg.task_type == 'binary_classification' and model_params.get('model_type') == 'pytorch':
        y_flat = np.asarray(y_train).ravel()
        n_pos = max(int((y_flat == 1).sum()), 1)
        n_neg = int((y_flat == 0).sum())
        model_params['pos_weight'] = n_neg / n_pos

    # n_epochs: из EXPERIMENT_CONFIG для PyTorch/дистилляции; для tree-моделей всегда 1 (игнорируется)
    if model_params['model_type'] == 'pytorch' or model_params.get('use_distillation', False):
        if MODEL_FIT_MODE != 'normal' and MODEL_FIT_MODE in FIT_MODE_EPOCHS:
            n_epochs = FIT_MODE_EPOCHS[MODEL_FIT_MODE]
            logger.log_message(f"FIT MODE '{MODEL_FIT_MODE}': n_epochs overridden to {n_epochs}")
        else:
            n_epochs = EXPERIMENT_CONFIG.get('n_epochs', 500)
    else:
        n_epochs = 1

    config['model_params'] = model_params
    config['training_params']['n_epochs'] = n_epochs
    selected_metric = get_selected_metric(cfg.task_type, getattr(cfg, 'metrics', []))
    config['evaluation_metric'] = {
        'name': selected_metric,
        **get_metric_metadata(selected_metric),
    }

    n_remove_list = get_n_remove_list()
    config['experiment_params'] = {
        'n_remove_percentages': n_remove_list,
        'removal_strategies': model_params.get('removal_strategies', REMOVAL_STRATEGIES),
        'removal_per_class': model_params.get('removal_per_class', False),
        'removal_stratify_target': model_params.get('removal_stratify_target', False),
        'removal_stratify_n_bins': model_params.get('removal_stratify_n_bins', 10),
        'loss_removal_methods': get_selected_loss_removal_methods(),
    }
    logger.save_config(config)
    logger.log_message("Starting experiments")

    experiment_runner = ExperimentRunner(logger)

    results, scores, scores_raw, random_run_results = experiment_runner.run_experiments(
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
    logger.save_results(results, scores, scores_raw, n_remove_list, random_run_results=random_run_results)

    # CSV с данными для графика removal в папку эксперимента
    removal_csv_path = logger.experiment_dir / "removal_metrics.csv"
    save_removal_metrics_csv(results, n_remove_list, removal_csv_path)
    logger.log_message(f"Removal metrics CSV saved: {removal_csv_path}")

    plot_influence_distribution(scores_raw, "influence_scores", logger)
    plt.show()

    plot_results_enhanced(results, n_remove_list, logger, random_run_results=random_run_results)
    plt.show()

    plot_method_comparison_bars(logger, results, n_remove_list)

    # plot_combined_comparison(results, n_remove_list, logger)
    # plt.show()

    # Генерация отчета
    model_metrics = {
        'baseline_metric': results['orig']['final_metric'],
        'best_validation_metric': results['orig']['best_val_metric'],
        'metric_name': results['orig'].get('metric_name'),
        'metric_label_ru': results['orig'].get('metric_label_ru'),
        'best_epoch': results['orig']['best_epoch'],
        'total_training_epochs': n_epochs,
        'model_type': model_params['model_type'],
        'used_distillation': model_params.get('use_distillation', False),
        'distillation_epochs': model_params.get('distillation_epochs', 0) if model_params.get('use_distillation', False) else 0,
        'student_architecture': model_params.get('student_architecture', 'none') if model_params.get('use_distillation', False) else 'none'
    }

    influence_stats = get_influence_statistics(scores_raw)
    logger.generate_summary(
        config,
        model_metrics,
        influence_stats,
        scores,
        scores_raw,
        removal_results=results,
        n_remove_list=n_remove_list,
    )

    logger.log_message("Program completed successfully!")
    logger.log_message(f"All results saved in: {logger.get_experiment_dir()}")


if __name__ == '__main__':
    # По умолчанию — значение из config/settings.py (без перезагрузки здесь, т.к. парсер создаётся до main)
    parser = argparse.ArgumentParser(description='Run experiments with different datasets')
    parser.add_argument('--dataset', type=str, default=None,
                        help=f"Dataset name. If not set, uses CURRENT_DATASET from config/settings.py (now: {CURRENT_DATASET})")
    args = parser.parse_args()
    # Явно: без --dataset используем только settings (в main при None подставится CURRENT_DATASET)
    main(args.dataset)