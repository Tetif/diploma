import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional
from tqdm import tqdm
from experiments.logger import debug_print


METHOD_LABEL_ORDER = [
    'LOO', 'Banzhaf', 'TMCShapley', 'DataShapley', 'BetaShapley', 'Influence',
    'ArnoldiInfluence', 'CgInfluence', 'LissaInfluence', 'NystroemSketchInfluence',
    'CatBoostInfluence', 'LossHigh', 'LossLow', 'random',
]


def _method_label_sort_key(m):
    """Порядок методов для легенд / столбчатых диаграмм (совпадает с get_methods_from_results)."""
    if m in METHOD_LABEL_ORDER:
        return (0, METHOD_LABEL_ORDER.index(m))
    if m.endswith('_lowest'):
        return (1, METHOD_LABEL_ORDER.index(m[:-7]) if m[:-7] in METHOD_LABEL_ORDER else 999)
    if m.endswith('_highest'):
        return (2, METHOD_LABEL_ORDER.index(m[:-8]) if m[:-8] in METHOD_LABEL_ORDER else 999)
    if m.endswith('_extremes'):
        return (3, METHOD_LABEL_ORDER.index(m[:-9]) if m[:-9] in METHOD_LABEL_ORDER else 999)
    if m.endswith('_median'):
        return (4, METHOD_LABEL_ORDER.index(m[:-7]) if m[:-7] in METHOD_LABEL_ORDER else 999)
    return (5, 0)


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
    return sorted(methods, key=_method_label_sort_key)


def _trend_colors_for_methods():
    """Те же цвета, что и для линий в plot_results_enhanced."""
    return {
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
        'CatBoostInfluence': '#17becf',
        'LossHigh': '#2e7d32',
        'LossLow': '#1565C0',
        'random': '#f39c12',
    }


def _resolve_method_color(method: str, color_map: dict, default: str = '#7f7f7f') -> str:
    """Цвет по имени метода; суффиксы стратегий (_lowest, …) → цвет базового метода (как в plot_results_enhanced)."""
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
            base = method[: -len(suffix)]
            return color_map.get(base, default)
    return default


def _pct_vs_left_neighbor(values):
    """
    Для каждого столбца: None (первый) или изменение относительно предыдущего, в %.
    (текущий − предыдущий) / |предыдущий| × 100; при |предыдущем|≈0 — None.
    """
    out = [None]
    for i in range(1, len(values)):
        prev = float(values[i - 1])
        cur = float(values[i])
        if not np.isfinite(prev) or not np.isfinite(cur) or abs(prev) < 1e-15:
            out.append(None)
        else:
            out.append(100.0 * (cur - prev) / prev)
    return out


def _pct_vs_best(values, higher_is_better: bool):
    """
    Отклонение каждого значения от лучшего в группе, в %.
    Лучший = max при higher_is_better, иначе min.
    Формула: 100 * (v - best) / |best| — у лучшего столбца 0%.
    """
    vals = [float(x) for x in values]
    n = len(vals)
    if n == 0:
        return []
    if higher_is_better:
        best = max(vals)
    else:
        best = min(vals)
    denom = abs(best)
    if denom < 1e-15 or not np.isfinite(best):
        return [None] * n
    out = []
    for v in vals:
        if not np.isfinite(v):
            out.append(None)
        else:
            out.append(100.0 * (v - best) / denom)
    return out


def _should_show_pct_vs_best(d: Optional[float]) -> bool:
    """У лучшего столбца отклонение 0% — вторую строку с процентом не показываем."""
    if d is None:
        return False
    return abs(float(d)) > 1e-3


def _removal_strategy_hatch(method: str) -> str:
    """Штриховка, чтобы отличать варианты одного базового метода на столбчатой диаграмме."""
    if method.endswith('_lowest'):
        return ''
    if method.endswith('_highest'):
        return '//'
    if method.endswith('_extremes'):
        return 'xx'
    if method.endswith('_median'):
        return '..'
    if method.endswith('_few_bad_rand'):
        return '\\'
    if method.endswith('_few_median_rand'):
        return '+'
    if method.endswith('_few_good_rand'):
        return 'o'
    return ''


def plot_method_comparison_bars(logger, results, n_remove_list, metric_metadata=None):
    """
    Сохраняет в каталог эксперимента четыре столбчатые диаграммы по методам:
    max_wanted_MB и RAM_MB (этапы *_computation), время в секундах, AUC кривых removal.
    """
    if logger is None:
        return

    from config.settings import METRIC_METADATA as _DEFAULT_MM

    mm = metric_metadata if metric_metadata is not None else _DEFAULT_MM
    colors = _trend_colors_for_methods()

    timings = getattr(logger, 'timings', None) or {}
    comp_rows = []
    for stage_name, tinfo in timings.items():
        sn = str(stage_name)
        if not sn.endswith('_computation'):
            continue
        dur = tinfo.get('duration')
        if dur is None:
            continue
        method = sn[: -len('_computation')]
        ram = tinfo.get('ram_peak_mb')
        vram = tinfo.get('gpu_peak_mb')
        max_w = tinfo.get('gpu_memory_max_wanted_mb')
        if max_w is None:
            max_w = vram
        if max_w is None:
            max_w = 0.0
        if ram is None:
            ram = 0.0
        comp_rows.append(
            {
                'method': method,
                'duration': float(dur),
                'ram_mb': float(ram),
                'max_wanted_mb': float(max_w),
            }
        )

    comp_rows.sort(key=lambda r: _method_label_sort_key(r['method']))

    def _save_bar(
        methods,
        values,
        title,
        ylabel,
        plot_base_name,
        value_fmt='%.4f',
        *,
        higher_is_better: bool = False,
    ):
        """higher_is_better: для ресурсов (память, время) — False (чем меньше тем лучше)."""
        if not methods:
            return
        w = max(10.0, 0.55 * len(methods))
        fig = plt.figure(figsize=(w, 6.4))
        ax = fig.add_subplot(111)
        x = np.arange(len(methods))
        vals_f = [float(v) for v in values]
        deltas = _pct_vs_best(vals_f, higher_is_better)
        bars = ax.bar(
            x,
            vals_f,
            color=[_resolve_method_color(m, colors) for m in methods],
            edgecolor='black',
            linewidth=0.4,
            alpha=0.92,
        )
        lbls = []
        for i, v in enumerate(vals_f):
            main = value_fmt % v
            d = deltas[i]
            if d is not None and _should_show_pct_vs_best(d):
                lbls.append(f'{main}\nк лучш.: {d:+.1f}%')
            else:
                lbls.append(main)
        ax.bar_label(bars, labels=lbls, fontsize=6.5, padding=2)
        ax.set_xticks(x)
        ax.set_xticklabels(methods, rotation=38, ha='right')
        ax.set_ylabel(ylabel)
        ax.set_title(
            title + '\n(к лучшему в группе — отклонение в %; '
            + ('больше' if higher_is_better else 'меньше')
            + ' значение лучше)',
            fontsize=10,
        )
        ax.grid(True, axis='y', alpha=0.28)
        ymax = max(vals_f) if vals_f else 1.0
        ymin = min(vals_f) if vals_f else 0.0
        span = ymax - ymin if ymax > ymin else max(abs(ymax), 1e-9)
        ax.set_ylim(ymin - 0.06 * span, ymax + 0.22 * span)
        fig.tight_layout()
        logger.save_plot(plt, plot_base_name)
        plt.close(fig)

    if comp_rows:
        methods = [r['method'] for r in comp_rows]
        _save_bar(
            methods,
            [r['max_wanted_mb'] for r in comp_rows],
            'GPU: max_wanted_MB по методам (этапы *_computation)',
            'max_wanted_MB',
            'methods_bar_max_wanted_MB',
            value_fmt='%.2f',
            higher_is_better=False,
        )
        _save_bar(
            methods,
            [r['ram_mb'] for r in comp_rows],
            'RAM: RSS peak (MB) по методам (этапы *_computation)',
            'RAM_MB',
            'methods_bar_RAM_MB',
            value_fmt='%.2f',
            higher_is_better=False,
        )
        _save_bar(
            methods,
            [r['duration'] for r in comp_rows],
            'Время вычисления влияния по методам (этапы *_computation)',
            's (seconds)',
            'methods_bar_seconds',
            value_fmt='%.2f',
            higher_is_better=False,
        )
    else:
        logger.log_message(
            "Skipping methods_bar (max_wanted / RAM / s): no *_computation timings in logger."
        )

    aucs = compute_removal_curve_aucs(results, n_remove_list) if results and n_remove_list else {}
    auc_methods = [m for m, v in aucs.items() if v is not None and np.isfinite(v)]
    if auc_methods:
        metric_ctx = _get_metric_context(results)
        mn = metric_ctx.get('name') or 'metric'
        meta = (mm or {}).get(mn) or {}
        higher = meta.get('higher_is_better', True)
        direction = 'выше лучше' if higher else 'ниже лучше'
        rank_scores = removal_curve_rank_scores(aucs, mn, mm)

        def _rank_key(m):
            rs = rank_scores.get(m, float('-inf'))
            if not np.isfinite(rs):
                return float('-inf')
            return float(rs)

        auc_order = sorted(auc_methods, key=_rank_key, reverse=True)
        vals = [float(aucs[m]) for m in auc_order]
        w = max(12.0, 0.52 * len(auc_order))
        fig = plt.figure(figsize=(w, 7.2))
        ax = fig.add_subplot(111)
        x = np.arange(len(auc_order))
        bar_colors = [_resolve_method_color(m, colors) for m in auc_order]
        hatches = [_removal_strategy_hatch(m) for m in auc_order]
        bars = ax.bar(
            x,
            vals,
            color=bar_colors,
            edgecolor='#333333',
            linewidth=0.5,
            alpha=0.9,
        )
        for bar, h in zip(bars, hatches):
            if h:
                bar.set_hatch(h)
        ax.set_xticks(x)
        ax.set_xticklabels(auc_order, rotation=40, ha='right', fontsize=8)
        ax.set_ylabel('AUC')
        ax.set_title(
            f'Removal curves: ∫ metric d(доля удалённых), AUC ({mn}, {direction})\n'
            f'Слева — лучше по rank_score; цвет = базовый метод, штрих = стратегия удаления\n'
            f'к лучш. — отклонение от лучшего AUC в группе (в %)',
            fontsize=11,
        )
        auc_deltas = _pct_vs_best(vals, higher)
        auc_lbls = []
        for i, v in enumerate(vals):
            main = f'{v:.4f}'
            d = auc_deltas[i]
            if d is not None and _should_show_pct_vs_best(d):
                auc_lbls.append(f'{main}\nк лучш.: {d:+.1f}%')
            else:
                auc_lbls.append(main)
        ymin, ymax = min(vals), max(vals)
        span = ymax - ymin if ymax > ymin else max(abs(ymax), 1e-9)
        pad = max(0.015 * span, 0.008)
        ax.set_ylim(ymin - pad * 0.15, ymax + pad * 1.55)
        ax.bar_label(bars, labels=auc_lbls, fontsize=6.5, padding=2)
        ax.grid(True, axis='y', alpha=0.28)
        best_m, best_v = auc_order[0], vals[0]
        ax.text(
            0.02,
            0.98,
            f'Лучший: {best_m}  AUC={best_v:.4f}',
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
        )
        if any(hatches):
            from matplotlib.patches import Patch

            present = set(hatches)
            handles = []
            if '' in present:
                handles.append(
                    Patch(
                        facecolor='#e0e0e0',
                        edgecolor='black',
                        linewidth=0.6,
                        label='_lowest / без суффикса',
                    )
                )
            if '//' in present:
                handles.append(
                    Patch(
                        facecolor='#e0e0e0',
                        edgecolor='black',
                        hatch='//',
                        label='_highest',
                    )
                )
            if 'xx' in present:
                handles.append(
                    Patch(
                        facecolor='#e0e0e0',
                        edgecolor='black',
                        hatch='xx',
                        label='_extremes',
                    )
                )
            if '..' in present:
                handles.append(
                    Patch(
                        facecolor='#e0e0e0',
                        edgecolor='black',
                        hatch='..',
                        label='_median',
                    )
                )
            extra = {'\\': 'few_bad_rand', '+': 'few_median_rand', 'o': 'few_good_rand'}
            for hch, lab in extra.items():
                if hch in present:
                    handles.append(
                        Patch(
                            facecolor='#e0e0e0',
                            edgecolor='black',
                            hatch=hch,
                            label=lab,
                        )
                    )
            if handles:
                ax.legend(
                    handles=handles,
                    title='Штрих = суффикс стратегии',
                    fontsize=8,
                    title_fontsize=9,
                    loc='lower right',
                )
        fig.tight_layout()
        logger.save_plot(plt, 'methods_bar_removal_AUC')
        plt.close(fig)
    else:
        logger.log_message(
            "Skipping methods_bar_removal_AUC: no removal curve AUC (need results + n_remove_list)."
        )


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


def _trapezoid_np(y, x):
    """Трапеции ∫ y dx; numpy 2+: trapezoid, иначе trapz."""
    fn = getattr(np, "trapezoid", None)
    if fn is not None:
        return float(fn(y, x))
    return float(np.trapz(y, x))


def compute_removal_curve_aucs(results, n_remove_list):
    """
    Площадь под кривой «метрика vs. доля удалённых»: ∫ y dx, где x ∈ [0,1] — доля удалённых
    от train (0 = baseline, без удаления). Совпадает с тем, что в removal_metrics.csv / графике.
    Возвращает dict method_name -> AUC (сырое интегральное значение).
    """
    if not n_remove_list:
        return {}
    methods = get_methods_from_results(results)
    if not methods:
        return {}
    metric_ctx = _get_metric_context(results)
    final_key = metric_ctx["final_key"]
    baseline = _extract_metric_value(results.get("orig", {}), final_key)
    x = np.asarray([0.0] + [float(p) for p in n_remove_list], dtype=float) / 100.0
    out = {}
    for method in methods:
        ys = []
        for pct in [0] + list(n_remove_list):
            if pct == 0:
                ys.append(baseline)
            else:
                key = f"{method}_{pct}pct"
                ys.append(_extract_metric_value(results.get(key, {}), final_key))
        y = np.asarray(ys, dtype=float)
        if np.any(~np.isfinite(y)):
            out[method] = float("nan")
        else:
            out[method] = _trapezoid_np(y, x)
    return out


def removal_curve_rank_scores(aucs, metric_name, metric_metadata):
    """
    Единая шкала для сравнения: больше rank_score = лучше кривая.
    Для метрик «чем выше тем лучше» rank_score = AUC; для MAE/RMSE — rank_score = -AUC.
    """
    meta = (metric_metadata or {}).get(metric_name) or {}
    higher = meta.get("higher_is_better", True)
    ranked = {}
    for m, auc in aucs.items():
        if auc is None or (isinstance(auc, float) and not np.isfinite(auc)):
            ranked[m] = float("nan")
        elif higher:
            ranked[m] = float(auc)
        else:
            ranked[m] = float(-auc)
    return ranked


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
        'CatBoostInfluence': '#17becf',
        'LossHigh': '#2e7d32',
        'LossLow': '#1565C0',
        'random': '#f39c12'
    }

    x_points = [0] + n_remove_list

    if 'orig' in results:
        baseline_metric = _extract_metric_value(results['orig'], metric_ctx['final_key'])
        plt.plot(
            [0],
            [baseline_metric],
            'o-',
            color=trend_colors['Baseline'],
            alpha=0.55,
            linewidth=1.2,
            markersize=5,
        )

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
        highest — штрих-пунктир,
        extremes — пунктир,
        median — точками,
        few_*_rand — комбинированные стили (отличаются от базовых).
        """
        if method.endswith('_lowest'):
            return '-'
        if method.endswith('_highest'):
            return '-.'
        if method.endswith('_extremes'):
            return '--'
        if method.endswith('_median'):
            return ':'
        if method.endswith('_few_bad_rand'):
            return '--'
        if method.endswith('_few_median_rand'):
            return (0, (6, 2))
        if method.endswith('_few_good_rand'):
            return ':'
        return '-'

    def _marker_for_method(method):
        """Маркер для стратегий: lowest/highest/extremes и few_* отличаются."""
        if method.endswith('_lowest'):
            return 'o'
        if method.endswith('_highest'):
            return 'D'
        if method.endswith('_extremes'):
            return 's'
        if method.endswith('_few_bad_rand'):
            return 's'
        if method.endswith('_few_median_rand'):
            return 'D'
        if method.endswith('_few_good_rand'):
            return '^'
        return 'o'

    if logger:
        logger.log_message(f"Detected methods for plotting: {methods}")
    else:
        debug_print(f"Detected methods for plotting: {methods}")

    for method in tqdm(methods, desc="Plotting removal curves", unit="method", leave=False):
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
                plt.plot(
                    x_valid,
                    y_valid,
                    marker + ls,
                    color=_color_for_method(method, trend_colors, '#666666'),
                    alpha=0.95,
                    linewidth=2,
                    markersize=5,
                    label=f'{method}',
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
        f'{metric_short_label} на валидации в зависимости от доли удалённых объектов',
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


def plot_influence_lowest_by_regularization(
    results_dict,
    n_remove_list,
    logger=None,
    title_suffix="",
    regularization_values=None
):
    """
    График MAE на валидации в зависимости от доли удалённых объектов.
    Сравнивает только метод Influence_lowest при разных параметрах регуляризации.
    
    Args:
        results_dict: Словарь {regularization_param: results_dict}
                     Например: {'1e-05': results1, '1e-04': results2, ...}
                     ИЛИ список результатов (тогда используется regularization_values)
        n_remove_list: Список процентов удаляемых образцов [10, 20, 30, ...]
        logger: Логгер для сохранения графика
        title_suffix: Дополнительный текст к заголовку
        regularization_values: Список названий параметров регуляризации для легенды
                              (используется если results_dict — список)
    """
    # Параметры стиля в точном соответствии с на plot_results_enhanced
    regularization_colors = {
        '1e-05': '#9b59b6',    # Фиолетовый (базовый цвет Influence)
        '1e-04': '#8e44ad',    # Более тёмный фиолетовый
        '1e-03': '#6c3483',    # Ещё более тёмный фиолетовый
        '1e-02': '#4a235a',    # Тёмный фиолетовый
        '0.0001': '#8e44ad',
        '0.001': '#6c3483',
        '0.01': '#4a235a',
    }
    
    regularization_linestyles = {
        '1e-05': '-',      # Сплошная
        '1e-04': '--',     # Пунктир
        '1e-03': '-.',     # Штрих-пунктир
        '1e-02': ':',      # Точки
        '0.0001': '--',
        '0.001': '-.',
        '0.01': ':',
    }
    
    regularization_markers = {
        '1e-05': 'o',      # Круг
        '1e-04': 's',      # Квадрат
        '1e-03': '^',      # Треугольник
        '1e-02': 'D',      # Ромб
        '0.0001': 's',
        '0.001': '^',
        '0.01': 'D',
    }
    
    # Инициализация
    if logger:
        logger.log_message("Creating Influence_lowest comparison by regularization...")
    else:
        debug_print("Creating Influence_lowest comparison by regularization...")
    
    # Преобразуем список в словарь, если нужно
    if isinstance(results_dict, (list, tuple)) and regularization_values:
        results_dict = {str(reg): res for reg, res in zip(regularization_values, results_dict)}
    
    if not results_dict:
        if logger:
            logger.log_message("ERROR: results_dict is empty!")
        else:
            debug_print("ERROR: results_dict is empty!")
        return None
    
    # Создаём фигуру
    fig = plt.figure(figsize=(14, 8))
    plt.rcParams['agg.path.chunksize'] = 10000
    
    # Получаем метрики из первого результата
    first_results = list(results_dict.values())[0]
    metric_ctx = _get_metric_context(first_results)
    metric_short_label = metric_ctx['short_label_ru']
    metric_label_ru = metric_ctx['label_ru']
    
    x_points = [0] + n_remove_list
    
    # Рисуем базовую модель (в первом результате)
    if 'orig' in first_results:
        baseline_metric = _extract_metric_value(first_results['orig'], metric_ctx['final_key'])
        plt.plot(
            [0],
            [baseline_metric],
            'o-',
            color='#000000',
            alpha=0.55,
            linewidth=1.2,
            markersize=5,
        )
    
    # Для каждого параметра регуляризации рисуем Influence_lowest
    for reg_param, results in sorted(results_dict.items()):
        # Получаем цвет, стиль линии и маркер
        color = regularization_colors.get(reg_param, '#9b59b6')
        linestyle = regularization_linestyles.get(reg_param, '-')
        marker = regularization_markers.get(reg_param, 'o')
        
        # Извлекаем значения Influence_lowest
        metric_values = []
        
        if 'orig' in results:
            metric_values.append(_extract_metric_value(results['orig'], metric_ctx['final_key']))
        
        for pct in n_remove_list:
            key = f'Influence_lowest_{pct}pct'
            if key in results:
                metric_values.append(_extract_metric_value(results[key], metric_ctx['final_key']))
            else:
                metric_values.append(float('nan'))
        
        # Рисуем линию только для валидных точек
        if len(metric_values) > 0:
            valid_indices = [i for i, val in enumerate(metric_values) if not np.isnan(val)]
            if len(valid_indices) > 0:
                x_valid = [x_points[i] for i in valid_indices]
                y_valid = [metric_values[i] for i in valid_indices]
                
                plt.plot(
                    x_valid,
                    y_valid,
                    marker + linestyle,
                    color=color,
                    alpha=0.85,
                    linewidth=2.5,
                    markersize=6,
                    label=f'Regularization = {reg_param}',
                )
    
    # Базовая линия модели
    if 'orig' in first_results:
        baseline_metric = _extract_metric_value(first_results['orig'], metric_ctx['final_key'])
        plt.axhline(
            y=baseline_metric,
            color='#000000',
            linestyle='--',
            alpha=0.7,
            linewidth=2,
            label='Базовая модель'
        )
    
    # Оформление графика
    plt.xlabel('Доля удалённых объектов, %', fontsize=12)
    plt.ylabel(f'{metric_label_ru} на валидации', fontsize=12)
    plt.title(
        f'{metric_short_label} на валидации в зависимости от доли удалённых объектов\n'
        f'(метод Influence_lowest при разных параметрах регуляризации{" " + title_suffix if title_suffix else ""})',
        fontsize=14,
        pad=20,
    )
    plt.xticks(x_points, ['0%'] + [f'{pct}%' for pct in n_remove_list])
    plt.grid(True, alpha=0.2)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=11)
    plt.tight_layout()
    
    if logger:
        logger.save_plot(plt, "influence_lowest_by_regularization")
    
    return plt