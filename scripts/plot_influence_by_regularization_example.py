"""
Пример использования plot_influence_lowest_by_regularization с синтетическими данными.

Этот скрипт создает фиктивные результаты экспериментов для разных параметров регуляризации
и демонстрирует как рисовать граф
"""

import sys
from pathlib import Path

# Добавляем родительскую директорию в path
sys.path.insert(0, str(Path(__file__).parents[1]))

import numpy as np
import matplotlib.pyplot as plt

from visualization.plots import plot_influence_lowest_by_regularization
from experiments.logger import ExperimentLogger


def create_synthetic_results(
    n_remove_list,
    regularization_value,
    seed=42
):
    """
    Создает синтетические результаты экспериментов для одного параметра регуляризации.
    
    Args:
        n_remove_list: Список процентов удаления [10, 20, ...]
        regularization_value: Значение параметра регуляризации
        seed: Seed для воспроизводимости
    
    Returns:
        results: Словарь результатов в формате как из реальных экспериментов
    """
    np.random.seed(seed)
    
    # Базовое значение MAE
    baseline_mae = 0.0173
    
    # Параметр регуляризации влияет на скорость роста ошибки при удалении данных
    # Меньшее значение регуляризации → более быстрый рост ошибки
    reg_effect = float(regularization_value.replace('1e-', '1e-')) if '1e-' in str(regularization_value) else 1e-4
    
    # Фактор роста ошибки: меньшая регуляризация → больший рост
    growth_factor = 1.0 + (5e-5 / (reg_effect + 1e-6))
    
    results = {
        'orig': {
            'final_mae': baseline_mae,
            'best_val_mae': baseline_mae,
            'final_metric': baseline_mae,
            'best_val_metric': baseline_mae,
            'metric_name': 'mae',
            'metric_short_label_ru': 'MAE',
            'metric_label_ru': 'Средняя абсолютная ошибка',
        }
    }
    
    # Для каждого процента удаления создаем меtrики
    for pct in n_remove_list:
        # Синтетическая кривая: экспоненциальный рост ошибки
        fraction_removed = pct / 100.0
        
        # Базовый рост
        mae_value = baseline_mae * (1.0 + growth_factor * np.power(fraction_removed, 1.8))
        
        # Добавляем небольшой noise
        mae_value += np.random.normal(0, baseline_mae * 0.001)
        
        # Сохраняем результат для Influence_lowest
        key = f'Influence_lowest_{pct}pct'
        results[key] = {
            'final_mae': mae_value,
            'best_val_mae': mae_value * 0.99,
            'final_metric': mae_value,
            'best_val_metric': mae_value * 0.99,
        }
    
    return results


def create_synthetic_dataset_for_all_regularizations(
    n_remove_list,
    regularization_values,
    seed=42
):
    """
    Создает синтетический датасет с результатами для всех параметров регуляризации.
    
    Args:
        n_remove_list: Список процентов удаления
        regularization_values: Список параметров регуляризации ['1e-05', '1e-04', ...]
        seed: Seed для воспроизводимости
    
    Returns:
        results_dict: {regularization: results}
    """
    results_dict = {}
    
    for idx, reg_value in enumerate(regularization_values):
        results_dict[reg_value] = create_synthetic_results(
            n_remove_list,
            reg_value,
            seed=seed + idx
        )
    
    return results_dict


def main():
    """Основная функция для демонстрации."""
    
    print("\n" + "="*60)
    print("EXAMPLE: Influence_lowest by Regularization")
    print("="*60 + "\n")
    
    # Параметры
    n_remove_list = [10, 20, 30, 40, 50, 60, 70, 80]
    regularization_values = ['1e-05', '1e-04', '1e-03', '1e-02']
    
    print(f"Creating synthetic data for:")
    print(f"  - Removal percentages: {n_remove_list}")
    print(f"  - Regularization values: {regularization_values}\n")
    
    # Создаём синтетические данные
    results_dict = create_synthetic_dataset_for_all_regularizations(
        n_remove_list,
        regularization_values,
        seed=42
    )
    
    print(f"✓ Created {len(results_dict)} synthetic result dictionaries\n")
    
    # Печатаем небольшую статистику
    for reg_val, results in results_dict.items():
        baseline = results['orig']['final_mae']
        final_80 = results.get('Influence_lowest_80pct', {}).get('final_mae', np.nan)
        print(f"  Regularization {reg_val:6s}: baseline={baseline:.6f}, MAE@80%={final_80:.6f}")
    
    print()
    
    # Создаём логгер для сохранения результатов
    output_dir = Path("visualization_results")
    output_dir.mkdir(exist_ok=True)
    
    logger = ExperimentLogger(base_dir=str(output_dir))
    logger.log_message("Creating plot for synthetic data example...")
    
    # Создаём график
    print("Creating plot...")
    plt_obj = plot_influence_lowest_by_regularization(
        results_dict,
        n_remove_list,
        logger=logger,
        title_suffix="(синтетические данные для примера)",
        regularization_values=regularization_values
    )
    
    if plt_obj:
        print("✓ Plot created successfully!")
        print(f"✓ Saved to: {output_dir}")
    else:
        print("✗ Failed to create plot")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()
