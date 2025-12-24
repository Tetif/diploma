import pickle
import matplotlib.pyplot as plt
import numpy as np

def load_results_pickle(filename="results_test.pkl"):
    """Загружает результаты из pickle файла"""
    with open(filename, 'rb') as f:
        data = pickle.load(f)

    print(f"Results loaded from {filename}")
    return data['results'], data['scores'], data['n_remove_list']

def plot_results_enhanced(results: dict, n_remove_list: list):
    print("Available keys in results:", list(results.keys()))

    print("\nCreating enhanced visualization...")

    plt.figure(figsize=(14, 8))

    base_colors = {
        'Baseline': '#000000B3',
        'LOO': '#2ecc7199',
        'DataShapley': '#3498db99',
        'BetaShapley': '#e74c3c99',
        'Influence': '#9b59b699',
        'random': '#f39c1299'
    }


    trend_colors = {
        'Baseline': '#000000',
        'LOO': '#2ecc71',
        'DataShapley': '#3498db',
        'BetaShapley': '#e74c3c',
        'Influence': '#9b59b6',
        'random': '#f39c12'
    }


    x_points = [0] + n_remove_list


    if 'orig' in results:
        baseline_mae = results['orig']['final_mae']
        plt.plot([0], [baseline_mae], 'o-', color=base_colors['Baseline'],
                 alpha=0.3, linewidth=1, markersize=6)

    methods = ['LOO', 'DataShapley', 'BetaShapley', 'Influence', 'random']

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
                         color=base_colors[method], alpha=0.3, linewidth=1,
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
                     color=trend_colors[method], alpha=0.9, linewidth=3,
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
    plt.show()

results, scores, n_remove_list = load_results_pickle("experiment_logs/2025-12-24/02-31-40/results.pkl")
plot_results_enhanced(results, n_remove_list)