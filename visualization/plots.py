import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from experiments.logger import debug_print


def plot_influence_distribution(scores, plot_name_suffix="", logger=None):
    """Визуализация распределения influence scores"""
    methods = list(scores.keys())
    n_methods = len(methods)

    fig, axes = plt.subplots(n_methods, 1, figsize=(12, 4 * n_methods))
    if n_methods == 1:
        axes = [axes]

    colors = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6', '#f1c40f']

    for idx, (method, color) in enumerate(tqdm(zip(methods, colors), total=n_methods, desc="Plotting distributions", unit="method", leave=False)):
        ax = axes[idx]
        method_scores = scores[method]

        if len(method_scores.shape) > 1:
            method_scores = method_scores.flatten()

        ax.hist(method_scores, bins=50, color=color, alpha=0.7, edgecolor='black')

        mean_score = np.mean(method_scores)
        ax.axvline(x=mean_score, color='black', linestyle='--', alpha=0.5,
                   label=f'Mean: {mean_score:.4f}')

        ax.set_title(f'{method} Influence Distribution {plot_name_suffix}', pad=20)
        ax.set_xlabel('Influence Score')
        ax.set_ylabel('Frequency')
        ax.grid(True, alpha=0.3)

        std_score = np.std(method_scores)
        ax.text(0.02, 0.98,
                f'Mean: {mean_score:.4f}\nStd: {std_score:.4f}\nMin: {np.min(method_scores):.4f}\nMax: {np.max(method_scores):.4f}\nNon-zero: {np.sum(method_scores > 0)}/{len(method_scores)}',
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        ax.legend()

    plt.tight_layout()

    if logger:
        plot_name = f"influence_distribution{'_' + plot_name_suffix if plot_name_suffix else ''}"
        logger.save_plot(plt, plot_name)

    return plt


def plot_results_enhanced(results, n_remove_list, logger=None, random_run_results=None):
    """Улучшенная визуализация результатов экспериментов
    
    Args:
        results: Основные результаты экспериментов
        n_remove_list: Список процентов удаляемых образцов
        logger: Логгер для вывода информации
        random_run_results: Результаты от нескольких случайных запусков для отображения вариативности
                           Должен быть список результатов от разных запусков с аналогичной структурой
    """
    if logger:
        logger.log_message("Creating enhanced visualization...")
    else:
        debug_print("Creating enhanced visualization...")

    plt.figure(figsize=(14, 8))

    # Расширенные базовые цвета (приглушенные)
    base_colors = {
        'Baseline': '#000000B3',
        'LOO': '#2ecc7199',
        'Banzhaf': '#1f77b499',
        'TMCShapley': '#ff7f0e99',
        'DataShapley': '#3498db99',
        'BetaShapley': '#e74c3c99',
        'Influence': '#9b59b699',
        'ArnoldiInfluence': '#d6272899',
        'CgInfluence': '#9467bd99',
        'LissaInfluence': '#8c564b99',
        'NystroemSketchInfluence': '#e377c299',
        'random': '#f39c1299'
    }

    # Расширенные яркие цвета для трендовых линий
    trend_colors = {
        'Baseline': '#000000',
        'LOO': '#2ecc71',
        'Banzhaf': '#1f77b4',
        'TMCShapley': '#ff7f0e',
        'DataShapley': '#3498db',
        'BetaShapley': '#e74c3c',
        'Influence': '#9b59b6',
        'ArnoldiInfluence': '#d62728',
        'CgInfluence': '#9467bd',
        'LissaInfluence': '#8c564b',
        'NystroemSketchInfluence': '#e377c2',
        'random': '#f39c12'
    }

    x_points = [0] + n_remove_list

    if 'orig' in results:
        baseline_mae = results['orig']['final_mae']
        plt.plot([0], [baseline_mae], 'o-', color=base_colors['Baseline'],
                 alpha=0.3, linewidth=1, markersize=6)

    # Автоматически определяем все доступные методы из результатов
    all_keys = set(results.keys())
    methods = []

    # Извлекаем названия методов из ключей результатов
    for key in all_keys:
        if key.startswith(('LOO_', 'DataShapley_', 'BetaShapley_', 'Influence_', 'Banzhaf_', 'TMCShapley_', 'ArnoldiInfluence_', 'CgInfluence_', 'LissaInfluence_', 'NystroemSketchInfluence_')):
            method_name = key.split('_')[0]
            if method_name not in methods:
                methods.append(method_name)
        elif key == 'random' or key.startswith('random_'):
            if 'random' not in methods:
                methods.append('random')

    # Сортируем методы для консистентности
    method_order = ['LOO', 'Banzhaf', 'TMCShapley', 'DataShapley', 'BetaShapley', 'Influence', 'ArnoldiInfluence', 'CgInfluence', 'LissaInfluence', 'NystroemSketchInfluence', 'random']
    methods = sorted(methods, key=lambda x: method_order.index(x) if x in method_order else len(method_order))

    if logger:
        logger.log_message(f"Detected methods for plotting: {methods}")
    else:
        debug_print(f"Detected methods for plotting: {methods}")

    for method in tqdm(methods, desc="Plotting raw results", unit="method", leave=False):
        # Пропускаем random если выводятся несколько запусков random
        if method == 'random' and random_run_results is not None and isinstance(random_run_results, dict) and len(random_run_results) > 0:
            continue
            
        mae_values = []

        if 'orig' in results:
            mae_values.append(results['orig']['final_mae'])

        for pct in n_remove_list:
            key = f'{method}_{pct}pct'
            if key in results:
                mae_values.append(results[key]['final_mae'])
            else:
                mae_values.append(float('nan'))

        if len(mae_values) > 0:
            valid_indices = [i for i, val in enumerate(mae_values) if not np.isnan(val)]
            if len(valid_indices) > 0:
                x_valid = [x_points[i] for i in valid_indices]
                y_valid = [mae_values[i] for i in valid_indices]
                plt.plot(x_valid, y_valid, 'o-',
                         color=base_colors.get(method, '#99999999'), alpha=0.3, linewidth=1,
                         markersize=4, label=f'{method} (raw)')

    for method in tqdm(methods, desc="Plotting smoothed trends", unit="method", leave=False):
        # Пропускаем random если выводятся несколько запусков random
        if method == 'random' and random_run_results is not None and isinstance(random_run_results, dict) and len(random_run_results) > 0:
            continue
            
        mae_values = []

        if 'orig' in results:
            mae_values.append(results['orig']['final_mae'])

        for pct in n_remove_list:
            key = f'{method}_{pct}pct'
            if key in results:
                mae_values.append(results[key]['final_mae'])
            else:
                mae_values.append(float('nan'))

        clean_mae = [val for val in mae_values if not np.isnan(val)]
        clean_indices = [i for i, val in enumerate(mae_values) if not np.isnan(val)]

        if len(clean_mae) > 1:
            window_size = min(3, len(clean_mae))
            if window_size > 1:
                smoothed = np.convolve(clean_mae, np.ones(window_size) / window_size, mode='same')
                # Заменяем крайние точки на оригинальные значения для точности
                smoothed[0] = clean_mae[0]
                smoothed[-1] = clean_mae[-1]
            else:
                smoothed = clean_mae

            x_smooth = [x_points[i] for i in clean_indices[:len(smoothed)]]
            plt.plot(x_smooth, smoothed, '-',
                     color=trend_colors.get(method, '#999999'), alpha=0.9, linewidth=3,
                     label=f'{method} (trend)')

    # Добавляем результаты от нескольких случайных запусков
    if random_run_results is not None and isinstance(random_run_results, dict) and len(random_run_results) > 0:
        if logger:
            logger.log_message(f"Plotting uncertainty bounds from random runs...")
        else:
            debug_print(f"Plotting uncertainty bounds from random runs...")
        
        # random_run_results это словарь {pct: [mae_values]}
        x_random = [0] + n_remove_list
        worst_values = []
        best_values = []
        mean_values = []
        
        # Для каждой точки (0%, 10%, 20% и т.д.)
        for pct_value in tqdm(x_random, desc="Processing random run percentages", unit="pct", leave=False):
            if pct_value == 0:
                # Для базовой точки (0%) нет данных в random_run_results
                worst_values.append(np.nan)
                best_values.append(np.nan)
                mean_values.append(np.nan)
            else:
                # Для других процентов берем данные из словаря
                if pct_value in random_run_results and len(random_run_results[pct_value]) > 0:
                    mae_at_point = random_run_results[pct_value]
                    worst_values.append(max(mae_at_point))
                    best_values.append(min(mae_at_point))
                    mean_values.append(np.mean(mae_at_point))
                else:
                    worst_values.append(np.nan)
                    best_values.append(np.nan)
                    mean_values.append(np.nan)
        
        # Используем индексы с валидными данными
        valid_indices = [i for i in range(len(mean_values)) if not np.isnan(mean_values[i])]
        if len(valid_indices) > 0:
            x_valid = [x_random[i] for i in valid_indices]
            worst_valid = [worst_values[i] for i in valid_indices]
            best_valid = [best_values[i] for i in valid_indices]
            mean_valid = [mean_values[i] for i in valid_indices]
            
            # Показываем доверительный интервал (худший-лучший диапазон) - полупрозрачная полоса
            plt.fill_between(x_valid, best_valid, worst_valid, 
                            color='#f39c12', alpha=0.15, label='Random Runs Range')
            
            # Линия среднего значения - яркая (без маркеров)
            plt.plot(x_valid, mean_valid, '-', color='#f39c12', alpha=0.9,
                    linewidth=2.5, label='Random Mean')

    if 'orig' in results:
        baseline_mae = results['orig']['final_mae']
        plt.axhline(y=baseline_mae, color=trend_colors['Baseline'],
                    linestyle='--', alpha=0.7, linewidth=2, label='Baseline')

    plt.xlabel('Percentage of Samples Removed')
    plt.ylabel('Validation MAE')
    plt.title('Validation MAE vs Percentage of Samples Removed\n(With Trend Lines)', fontsize=14, pad=20)
    plt.xticks(x_points, ['0%'] + [f'{pct}%' for pct in n_remove_list])
    plt.grid(True, alpha=0.2)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    if logger:
        logger.save_plot(plt, "results_comparison")

    return plt


def plot_training_history(history, model_name="Model", logger=None):
    """Визуализация истории обучения"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # График потерь
    if 'train' in history and len(history['train']) > 0:
        ax1.plot(history['train'], label='Train Loss', color='blue')
    if 'val' in history and len(history['val']) > 0:
        ax1.plot(history['val'], label='Validation Loss', color='red')

    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title(f'{model_name} Training History')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # График MAE
    if 'final_mae' in history:
        ax2.bar(['Final MAE'], [history['final_mae']], color='green')
        ax2.text(0, history['final_mae'], f'{history["final_mae"]:.4f}',
                 ha='center', va='bottom')
        ax2.set_ylabel('MAE')
        ax2.set_title('Final Validation MAE')
        ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    if logger:
        logger.save_plot(plt, f"{model_name.lower()}_training_history")

    return plt


def plot_combined_comparison(results, n_remove_list, logger=None):
    """Комбинированный график с двумя метриками на одной оси"""
    if logger:
        logger.log_message("Creating combined comparison visualization...")

    plt.figure(figsize=(12, 7))

    colors = plt.cm.Set2.colors

    x_points = [0] + n_remove_list

    # Определяем методы
    methods = []
    for key in results.keys():
        if '_' in key and key != 'orig':
            method = key.split('_')[0]
            if method not in methods and not method.startswith('random'):
                methods.append(method)

    # Для каждого метода строим две линии
    for idx, method in enumerate(methods):
        color = colors[idx % len(colors)]

        # Данные для final_mae (holdout validation)
        final_mae_values = []
        if 'orig' in results:
            final_mae_values.append(results['orig']['final_mae'])
        for pct in n_remove_list:
            key = f'{method}_{pct}pct'
            if key in results:
                final_mae_values.append(results[key]['final_mae'])
            else:
                final_mae_values.append(np.nan)

        # Данные для best_val_mae (test during training)
        test_mae_values = []
        if 'orig' in results:
            test_mae_values.append(results['orig']['best_val_mae'])
        for pct in n_remove_list:
            key = f'{method}_{pct}pct'
            if key in results:
                test_mae_values.append(results[key]['best_val_mae'])
            else:
                test_mae_values.append(np.nan)

        # Отображаем линии
        plt.plot(x_points, final_mae_values, 'o-', color=color, alpha=0.7,
                 linewidth=2, markersize=6, label=f'{method} (Holdout)')
        plt.plot(x_points, test_mae_values, 's--', color=color, alpha=0.5,
                 linewidth=1.5, markersize=4, label=f'{method} (Test)')

    # Добавляем случайное удаление
    if 'random_10pct' in results:
        final_random = [results['orig']['final_mae']]
        test_random = [results['orig']['best_val_mae']]
        for pct in n_remove_list:
            key = f'random_{pct}pct'
            if key in results:
                final_random.append(results[key]['final_mae'])
                test_random.append(results[key]['best_val_mae'])
            else:
                final_random.append(np.nan)
                test_random.append(np.nan)

        plt.plot(x_points, final_random, 'o-', color='gray', alpha=0.7,
                 linewidth=2, markersize=6, label='Random (Holdout)')
        plt.plot(x_points, test_random, 's--', color='gray', alpha=0.5,
                 linewidth=1.5, markersize=4, label='Random (Test)')

    plt.xlabel('Percentage of Samples Removed')
    plt.ylabel('MAE')
    plt.title('Comparison of Holdout vs Test MAE for Different Removal Methods',
              fontsize=14, pad=20)
    plt.xticks(x_points, ['0%'] + [f'{pct}%' for pct in n_remove_list])
    plt.grid(True, alpha=0.2)

    # Добавляем легенду
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2)

    # Добавляем информационный текст
    plt.figtext(0.5, 0.01,
                'Solid lines with circles: Holdout Validation (unbiased estimate)\n'
                'Dashed lines with squares: Test during training (used for model selection)',
                ha='center', fontsize=10, style='italic', alpha=0.7)

    plt.tight_layout()

    if logger:
        logger.save_plot(plt, "combined_holdout_vs_test")

    return plt