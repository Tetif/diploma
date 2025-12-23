import matplotlib.pyplot as plt
import numpy as np
from experiments.logger import debug_print


def plot_influence_distribution(scores, plot_name_suffix="", logger=None):
    """Визуализация распределения influence scores"""
    methods = list(scores.keys())
    n_methods = len(methods)

    fig, axes = plt.subplots(n_methods, 1, figsize=(12, 4 * n_methods))
    if n_methods == 1:
        axes = [axes]

    colors = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6', '#f1c40f']

    for idx, (method, color) in enumerate(zip(methods, colors)):
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


def plot_results_enhanced(results, n_remove_list, logger=None):
    """Улучшенная визуализация результатов экспериментов"""
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

    for method in methods:
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

    for method in methods:
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
                smoothed = np.convolve(clean_mae, np.ones(window_size) / window_size, mode='valid')

                pad_size = len(clean_mae) - len(smoothed)
                smoothed = np.concatenate([clean_mae[:pad_size], smoothed])
            else:
                smoothed = clean_mae

            x_smooth = [x_points[i] for i in clean_indices[:len(smoothed)]]
            plt.plot(x_smooth, smoothed, '-',
                     color=trend_colors.get(method, '#999999'), alpha=0.9, linewidth=3,
                     label=f'{method} (trend)')

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