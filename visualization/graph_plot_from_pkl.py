import pickle
import matplotlib.pyplot as plt
import numpy as np
import os

def load_results_pickle(filename="results_test.pkl"):
    """Загружает результаты из pickle файла"""
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    print(f"Results loaded from {filename}")
    return data['results'], data['scores'], data['n_remove_list']

def plot_results_enhanced(results, n_remove_list, logger=None):
    """Улучшенная визуализация результатов экспериментов"""
    print("Creating enhanced visualization...")

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

    print(f"Detected methods for plotting: {methods}")

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

    return plt

# Получаем путь к директории скрипта и строим абсолютный путь к файлу
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)  # поднимаемся на уровень выше от experiments/
results_path = os.path.join(project_root, "experiment_logs", "2025-12-29", "03-41-33", "results.pkl")

results, scores, n_remove_list = load_results_pickle(results_path)
plot_results_enhanced(results, n_remove_list)
plt.show()