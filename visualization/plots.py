import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from experiments.logger import debug_print


def get_methods_from_results(results):
    """Извлекает список имён методов из ключей results (для графика и CSV)."""
    all_keys = set(results.keys())
    methods = []
    for key in all_keys:
        if key == 'orig':
            continue
        if key == 'random' or key.startswith('random_'):
            if 'random' not in methods:
                methods.append('random')
            continue
        if '_' in key and key.endswith('pct'):
            suffix = key.rsplit('_', 1)[-1]
            if suffix[:-3].isdigit() and suffix.endswith('pct'):
                method_name = key.rsplit('_', 1)[0]
                if method_name not in methods:
                    methods.append(method_name)
    method_order = ['LOO', 'Banzhaf', 'TMCShapley', 'DataShapley', 'BetaShapley', 'Influence', 'ArnoldiInfluence', 'CgInfluence', 'LissaInfluence', 'NystroemSketchInfluence', 'LossHigh', 'LossLow', 'random']
    def _sort_key(m):
        if m in method_order:
            return (0, method_order.index(m))
        if m.endswith('_lowest'):
            return (1, method_order.index(m[:-7]) if m[:-7] in method_order else 999)
        if m.endswith('_highest'):
            return (2, method_order.index(m[:-8]) if m[:-8] in method_order else 999)
        if m.endswith('_extremes'):
            return (3, method_order.index(m[:-9]) if m[:-9] in method_order else 999)
        if m.endswith('_median'):
            return (4, method_order.index(m[:-7]) if m[:-7] in method_order else 999)
        return (5, 0)
    return sorted(methods, key=_sort_key)


def _get_metric_context(data):
    """Достать метаданные выбранной метрики из history/results."""
    metric_source = data.get('orig', data) if isinstance(data, dict) else {}
    metric_name = metric_source.get('metric_name', 'mae')
    metric_short_label = metric_source.get('metric_short_label_ru', 'MAE')
    metric_label_ru = metric_source.get('metric_label_ru', 'Средняя абсолютная ошибка')
    final_metric_key = 'final_metric' if 'final_metric' in metric_source else 'final_mae'
    best_metric_key = 'best_val_metric' if 'best_val_metric' in metric_source else 'best_val_mae'
    return {
        'name': metric_name,
        'short_label_ru': metric_short_label,
        'label_ru': metric_label_ru,
        'final_key': final_metric_key,
        'best_key': best_metric_key,
    }


def _extract_metric_value(metrics_dict, metric_key):
    """Безопасно достать значение метрики из словаря history/results."""
    if not isinstance(metrics_dict, dict):
        return np.nan
    if metric_key in metrics_dict:
        return metrics_dict.get(metric_key, np.nan)
    if metric_key == 'final_metric':
        return metrics_dict.get('final_mae', np.nan)
    if metric_key == 'best_val_metric':
        return metrics_dict.get('best_val_mae', np.nan)
    return np.nan


def save_removal_metrics_csv(results, n_remove_list, csv_path):
    """Сохраняет данные графика removal в CSV: pct_removed, baseline, method1, method2, ..."""
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    methods = get_methods_from_results(results)
    metric_ctx = _get_metric_context(results)
    baseline_metric = _extract_metric_value(results.get('orig', {}), metric_ctx['final_key'])
    rows = []
    for pct in [0] + n_remove_list:
        row = {'pct_removed': pct}
        row['baseline'] = baseline_metric
        for method in methods:
            if pct == 0:
                val = baseline_metric
            else:
                key = f'{method}_{pct}pct'
                val = _extract_metric_value(results.get(key, {}), metric_ctx['final_key'])
            row[method] = val
        rows.append(row)
    pd.DataFrame(rows).to_csv(csv_path, index=False)


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
    metric_ctx = _get_metric_context(results)
    metric_short_label = metric_ctx['short_label_ru']
    metric_label_ru = metric_ctx['label_ru']

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
        'LossHigh': '#e74c3c99',
        'LossLow': '#1abc9c99',
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
        'LossHigh': '#e74c3c',
        'LossLow': '#1abc9c',
        'random': '#f39c12'
    }

    x_points = [0] + n_remove_list

    if 'orig' in results:
        baseline_metric = _extract_metric_value(results['orig'], metric_ctx['final_key'])
        plt.plot([0], [baseline_metric], 'o-', color=base_colors['Baseline'],
                 alpha=0.3, linewidth=1, markersize=6)

    methods = get_methods_from_results(results)

    def _color_for_method(method, color_map, default='#999999'):
        """Resolve color for method; суффиксы используют цвет базового метода."""
        if method in color_map:
            return color_map[method]
        suffixes = (
            '_lowest',
            '_highest',
            '_extremes',
            '_median',
            '_few_bad_rand',
            '_few_median_rand',
            '_few_good_rand',
        )
        for suffix in suffixes:
            if method.endswith(suffix):
                base = method[:-len(suffix)]
                return color_map.get(base, default)
        return default

    def _linestyle_for_method(method):
        """
        lowest  — сплошная,
        highest — пунктир,
        extremes — штрих-пунктир,
        median — точками,
        few_*_rand — комбинированные стили (отличаются от базовых).
        """
        if method.endswith('_lowest'):
            return '-'
        if method.endswith('_highest'):
            return '--'
        if method.endswith('_extremes'):
            return '-.'
        if method.endswith('_median'):
            return ':'
        if method.endswith('_few_bad_rand'):
            return '--'
        if method.endswith('_few_median_rand'):
            return '-.'
        if method.endswith('_few_good_rand'):
            return ':'
        return '-'

    def _marker_for_method(method):
        """Маркер для стратегий, чтобы few_* были визуально отличимы."""
        if method.endswith('_few_bad_rand'):
            return 's'   # квадрат
        if method.endswith('_few_median_rand'):
            return 'D'   # ромб
        if method.endswith('_few_good_rand'):
            return '^'   # треугольник
        return 'o'

    if logger:
        logger.log_message(f"Detected methods for plotting: {methods}")
    else:
        debug_print(f"Detected methods for plotting: {methods}")

    for method in tqdm(methods, desc="Plotting raw results", unit="method", leave=False):
        # Пропускаем random если выводятся несколько запусков random
        if method == 'random' and random_run_results is not None and isinstance(random_run_results, dict) and len(random_run_results) > 0:
            continue
            
        metric_values = []

        if 'orig' in results:
            metric_values.append(_extract_metric_value(results['orig'], metric_ctx['final_key']))

        for pct in n_remove_list:
            key = f'{method}_{pct}pct'
            if key in results:
                metric_values.append(_extract_metric_value(results[key], metric_ctx['final_key']))
            else:
                metric_values.append(float('nan'))

        if len(metric_values) > 0:
            valid_indices = [i for i, val in enumerate(metric_values) if not np.isnan(val)]
            if len(valid_indices) > 0:
                x_valid = [x_points[i] for i in valid_indices]
                y_valid = [metric_values[i] for i in valid_indices]
                ls = _linestyle_for_method(method)
                marker = _marker_for_method(method)
                # Все "сырые" линии делаем одинаковой прозрачности
                alpha_raw = 0.25
                plt.plot(
                    x_valid,
                    y_valid,
                    marker + ls,
                    color=_color_for_method(method, base_colors, '#99999999'),
                    alpha=alpha_raw,
                    linewidth=1,
                    markersize=4,
                    label=f'{method} (raw)',
                )

    for method in tqdm(methods, desc="Plotting smoothed trends", unit="method", leave=False):
        # Пропускаем random если выводятся несколько запусков random
        if method == 'random' and random_run_results is not None and isinstance(random_run_results, dict) and len(random_run_results) > 0:
            continue
            
        metric_values = []

        if 'orig' in results:
            metric_values.append(_extract_metric_value(results['orig'], metric_ctx['final_key']))

        for pct in n_remove_list:
            key = f'{method}_{pct}pct'
            if key in results:
                metric_values.append(_extract_metric_value(results[key], metric_ctx['final_key']))
            else:
                metric_values.append(float('nan'))

        clean_values = [val for val in metric_values if not np.isnan(val)]
        clean_indices = [i for i, val in enumerate(metric_values) if not np.isnan(val)]

        if len(clean_values) > 1:
            window_size = min(3, len(clean_values))
            if window_size > 1:
                smoothed = np.convolve(clean_values, np.ones(window_size) / window_size, mode='same')
                # Заменяем крайние точки на оригинальные значения для точности
                smoothed[0] = clean_values[0]
                smoothed[-1] = clean_values[-1]
            else:
                smoothed = clean_values

            x_smooth = [x_points[i] for i in clean_indices[:len(smoothed)]]
            ls = _linestyle_for_method(method)
            # Все трендовые линии одинаковой яркости, различаются только стилем
            alpha_trend = 0.8
            plt.plot(
                x_smooth,
                smoothed,
                ls,
                color=_color_for_method(method, trend_colors, '#999999'),
                alpha=alpha_trend,
                linewidth=3,
                label=f'{method} (trend)',
            )

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
                    metric_at_point = random_run_results[pct_value]
                    worst_values.append(max(metric_at_point))
                    best_values.append(min(metric_at_point))
                    mean_values.append(np.mean(metric_at_point))
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
                            color='#f39c12', alpha=0.15, label='Диапазон случайных запусков')
            
            # Линия среднего значения - яркая (без маркеров)
            plt.plot(x_valid, mean_valid, '-', color='#f39c12', alpha=0.9,
                    linewidth=2.5, label='Среднее по случайным запускам')

    if 'orig' in results:
        baseline_metric = _extract_metric_value(results['orig'], metric_ctx['final_key'])
        plt.axhline(y=baseline_metric, color=trend_colors['Baseline'],
                    linestyle='--', alpha=0.7, linewidth=2, label='Базовая модель')

    plt.xlabel('Доля удалённых объектов, %')
    plt.ylabel(f'{metric_label_ru} на валидации')
    plt.title(
        f'{metric_short_label} на валидации в зависимости от доли удалённых объектов\n(со сглаженными трендами)',
        fontsize=14,
        pad=20,
    )
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
    metric_ctx = _get_metric_context(history)

    # График потерь
    if 'train' in history and len(history['train']) > 0:
        ax1.plot(history['train'], label='Ошибка на обучении', color='blue')
    if 'val' in history and len(history['val']) > 0:
        ax1.plot(history['val'], label='Метрика на валидации', color='red')

    ax1.set_xlabel('Эпоха')
    ax1.set_ylabel('Значение')
    ax1.set_title(f'История обучения: {model_name}')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # График основной метрики
    final_metric = _extract_metric_value(history, metric_ctx['final_key'])
    if not np.isnan(final_metric):
        ax2.bar([metric_ctx['short_label_ru']], [final_metric], color='green')
        ax2.text(0, final_metric, f'{final_metric:.4f}',
                 ha='center', va='bottom')
        ax2.set_ylabel(metric_ctx['label_ru'])
        ax2.set_title(f'Финальная метрика на валидации: {metric_ctx["short_label_ru"]}')
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
    metric_ctx = _get_metric_context(results)

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

        # Данные для финальной метрики на holdout validation
        final_metric_values = []
        if 'orig' in results:
            final_metric_values.append(_extract_metric_value(results['orig'], metric_ctx['final_key']))
        for pct in n_remove_list:
            key = f'{method}_{pct}pct'
            if key in results:
                final_metric_values.append(_extract_metric_value(results[key], metric_ctx['final_key']))
            else:
                final_metric_values.append(np.nan)

        # Данные для лучшей метрики во время обучения
        test_metric_values = []
        if 'orig' in results:
            test_metric_values.append(_extract_metric_value(results['orig'], metric_ctx['best_key']))
        for pct in n_remove_list:
            key = f'{method}_{pct}pct'
            if key in results:
                test_metric_values.append(_extract_metric_value(results[key], metric_ctx['best_key']))
            else:
                test_metric_values.append(np.nan)

        # Отображаем линии
        plt.plot(x_points, final_metric_values, 'o-', color=color, alpha=0.7,
                 linewidth=2, markersize=6, label=f'{method} (holdout)')
        plt.plot(x_points, test_metric_values, 's--', color=color, alpha=0.5,
                 linewidth=1.5, markersize=4, label=f'{method} (лучшая на test)')

    # Добавляем случайное удаление
    if 'random_10pct' in results:
        final_random = [_extract_metric_value(results['orig'], metric_ctx['final_key'])]
        test_random = [_extract_metric_value(results['orig'], metric_ctx['best_key'])]
        for pct in n_remove_list:
            key = f'random_{pct}pct'
            if key in results:
                final_random.append(_extract_metric_value(results[key], metric_ctx['final_key']))
                test_random.append(_extract_metric_value(results[key], metric_ctx['best_key']))
            else:
                final_random.append(np.nan)
                test_random.append(np.nan)

        plt.plot(x_points, final_random, 'o-', color='gray', alpha=0.7,
                 linewidth=2, markersize=6, label='Случайное удаление (holdout)')
        plt.plot(x_points, test_random, 's--', color='gray', alpha=0.5,
                 linewidth=1.5, markersize=4, label='Случайное удаление (лучшая на test)')

    plt.xlabel('Доля удалённых объектов, %')
    plt.ylabel(metric_ctx['label_ru'])
    plt.title('Сравнение holdout и test-метрики для разных методов удаления',
              fontsize=14, pad=20)
    plt.xticks(x_points, ['0%'] + [f'{pct}%' for pct in n_remove_list])
    plt.grid(True, alpha=0.2)

    # Добавляем легенду
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2)

    # Добавляем информационный текст
    plt.figtext(0.5, 0.01,
                'Сплошные линии с кружками: holdout validation\n'
                'Пунктирные линии с квадратами: лучшая метрика на test во время обучения',
                ha='center', fontsize=10, style='italic', alpha=0.7)

    plt.tight_layout()

    if logger:
        logger.save_plot(plt, "combined_holdout_vs_test")

    return plt