"""
Скрипт для создания графика сравнения Influence_lowest при разных параметрах регуляризации.

Использование:
    python scripts/plot_influence_by_regularization.py --results-dir <path> --dataset electric

Результаты сохраняются в каталоге результатов экспериментов.
"""

import argparse
import pickle
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
import sys

from config.settings import (
    DATASET_INFLUENCE_PARAMS, 
    EXPERIMENTS_BASE_DIR, 
    DEBUG_MODE,
    get_n_remove_list
)
from experiments.logger import ExperimentLogger, debug_print
from visualization.plots import plot_influence_lowest_by_regularization


def load_results_from_pickle(pkl_path: Path) -> Dict:
    """Загружает результаты из pickle файла."""
    try:
        with open(pkl_path, 'rb') as f:
            results = pickle.load(f)
        debug_print(f"Loaded results from {pkl_path}")
        return results if isinstance(results, dict) else {}
    except Exception as e:
        debug_print(f"Error loading {pkl_path}: {e}")
        return {}


def find_experiment_dirs_with_regularization(
    base_dir: Path,
    dataset_name: str,
    model_type: str = "pytorch",
) -> Dict[str, Path]:
    """
    Ищет директории экспериментов по датасету и различным регуляризациям.
    
    Returns:
        Dict {regularization_value: experiment_dir_path}
    """
    results_dirs = {}
    
    if not base_dir.exists():
        debug_print(f"Base directory not found: {base_dir}")
        return results_dirs
    
    # Ищем во всех поддиректориях
    for date_dir in sorted(base_dir.iterdir()):
        if not date_dir.is_dir() or date_dir.name == 'large_study':
            continue
        
        for time_dir in sorted(date_dir.iterdir()):
            if not time_dir.is_dir():
                continue
            
            config_file = time_dir / 'config.json'
            results_file = time_dir / 'results.pkl'
            
            if not config_file.exists() or not results_file.exists():
                continue
            
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                # Проверяем датасет
                cfg_dataset = config.get('dataset', {}).get('name', '')
                if cfg_dataset.lower() != dataset_name.lower():
                    continue
                
                # Проверяем модель
                cfg_model = config.get('model', {}).get('type', '')
                if model_type.lower() not in cfg_model.lower() and cfg_model:
                    continue
                
                # Ищем параметр регуляризации в конфиге
                # Может быть в разных местах: settings_snapshot или напрямую
                reg_value = None
                
                # Проверяем в settings_snapshot
                settings = config.get('settings_snapshot', {})
                influence_cfg = settings.get('INFLUENCE_METHODS_CONFIG', {})
                if influence_cfg:
                    # Для каждого параметра попробуем найти регуляризацию
                    for key, val in settings.items():
                        if 'regularization' in str(key).lower():
                            reg_value = str(val)
                            break
                
                # Если не нашли, проверяем значение по умолчанию для датасета
                if not reg_value:
                    reg_value = str(DATASET_INFLUENCE_PARAMS.get(
                        dataset_name, {}
                    ).get('regularization', '1e-06'))
                
                # Нормализуем значение регуляризации для использования в качестве ключа
                reg_key = _normalize_regularization_value(reg_value)
                
                if reg_key not in results_dirs:
                    results_dirs[reg_key] = results_file
                    debug_print(f"Found: {dataset_name} with reg={reg_key} at {time_dir}")
                
            except Exception as e:
                debug_print(f"Error processing {time_dir}: {e}")
                continue
    
    return results_dirs


def _normalize_regularization_value(value) -> str:
    """Нормализует значение регуляризации для использования как ключ."""
    s = str(value).strip().lower()
    # Преобразуем научную нотацию
    if 'e-' in s:
        return s
    # Преобразуем десятичные значения в научную нотацию
    try:
        f = float(s)
        if f < 0.0001:
            return f"{f:.0e}".replace('+', '')
        return s
    except:
        return s


def load_results_by_regularization(
    base_dir: Path,
    dataset_name: str,
    model_type: str = "pytorch",
) -> Tuple[Dict[str, Dict], List[int]]:
    """
    Загружает результаты для разных параметров регуляризации.
    
    Returns:
        (results_dict, n_remove_list)
        results_dict: {regularization: results}
        n_remove_list: [10, 20, 30, ...]
    """
    experiment_dirs = find_experiment_dirs_with_regularization(
        base_dir,
        dataset_name,
        model_type
    )
    
    results_dict = {}
    n_remove_list = None
    
    for reg_value, results_file in sorted(experiment_dirs.items()):
        results = load_results_from_pickle(results_file)
        
        if results:
            results_dict[reg_value] = results
            
            # Попытаемся получить n_remove_list из первого найденного результата
            if n_remove_list is None and results:
                # Ищем ключи вида method_Xpct
                for key in results.keys():
                    if '_pct' in key and key != 'orig':
                        parts = key.split('_')
                        if parts[-1].endswith('pct') and parts[-1][:-3].isdigit():
                            pct = int(parts[-1][:-3])
                            if n_remove_list is None:
                                n_remove_list = []
                            if pct not in n_remove_list:
                                n_remove_list.append(pct)
                
                if n_remove_list:
                    n_remove_list = sorted(n_remove_list)
                    debug_print(f"Detected n_remove_list: {n_remove_list}")
    
    if not n_remove_list:
        n_remove_list = list(get_n_remove_list())
        debug_print(f"Using default n_remove_list: {n_remove_list}")
    
    return results_dict, n_remove_list


def main():
    parser = argparse.ArgumentParser(
        description="Create plot comparing Influence_lowest at different regularization values"
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="electric",
        help="Dataset name (default: electric)"
    )
    parser.add_argument(
        "--model-type",
        type=str,
        default="pytorch",
        help="Model type (default: pytorch)"
    )
    parser.add_argument(
        "--base-dir",
        type=str,
        default=EXPERIMENTS_BASE_DIR,
        help=f"Base directory with experiments (default: {EXPERIMENTS_BASE_DIR})"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory for plot (default: same as results)"
    )
    parser.add_argument(
        "--title-suffix",
        type=str,
        default="",
        help="Additional text to append to plot title"
    )
    
    args = parser.parse_args()
    
    base_dir = Path(args.base_dir)
    output_dir = Path(args.output_dir) if args.output_dir else base_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Инициализируем логгер
    logger = ExperimentLogger(base_dir=str(output_dir))
    logger.log_message(f"\n{'='*60}")
    logger.log_message(f"Plotting Influence_lowest by Regularization")
    logger.log_message(f"Dataset: {args.dataset}")
    logger.log_message(f"Model type: {args.model_type}")
    logger.log_message(f"Base directory: {base_dir}")
    logger.log_message(f"{'='*60}\n")
    
    # Загружаем результаты
    logger.log_message("Loading experiment results...")
    results_dict, n_remove_list = load_results_by_regularization(
        base_dir,
        args.dataset,
        args.model_type
    )
    
    if not results_dict:
        logger.log_message("ERROR: No results found!")
        logger.log_message(f"Searched in: {base_dir}")
        logger.log_message(f"Dataset: {args.dataset}, Model: {args.model_type}")
        return
    
    logger.log_message(f"Found {len(results_dict)} experiment(s):")
    for reg_val in sorted(results_dict.keys()):
        logger.log_message(f"  - regularization = {reg_val}")
    logger.log_message(f"Removal percentages: {n_remove_list}\n")
    
    # Создаём график
    logger.log_message("Creating plot...")
    try:
        plt = plot_influence_lowest_by_regularization(
            results_dict,
            n_remove_list,
            logger=logger,
            title_suffix=args.title_suffix,
            regularization_values=sorted(results_dict.keys())
        )
        
        if plt:
            logger.log_message("✓ Plot created successfully!")
        else:
            logger.log_message("ERROR: Failed to create plot")
    
    except Exception as e:
        logger.log_message(f"ERROR during plot creation: {e}")
        import traceback
        logger.log_message(traceback.format_exc())
        return
    
    logger.log_message(f"Results saved to: {output_dir}")


if __name__ == "__main__":
    main()
