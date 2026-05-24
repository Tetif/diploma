"""Plotting utilities for Streamlit interface"""
import sys
from pathlib import Path

# Add project root to sys.path so top-level modules (visualization, config, etc.)
# can be imported when this module is used from the microservice folder.
sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from config.settings import METRIC_METADATA
from microservice.plotting_plotly_helpers import (
    _pct_vs_best,
    _resolve_method_color,
    _should_show_pct_vs_best,
    _trend_colors_for_methods,
    mean_pct_abs_diff_from_pointwise_best,
    removal_curve_rank_scores,
)
from typing import Dict, List, Any, Optional, Tuple


def _load_viz_matplotlib():
    """Ленивый импорт matplotlib-визуализации с Agg (только при вызове ExperimentPlotter)."""
    import matplotlib

    matplotlib.use("Agg")
    from visualization.plots import (
        plot_influence_distribution as viz_plot_influence_distribution,
        plot_results_enhanced as viz_plot_results_enhanced,
    )

    return viz_plot_influence_distribution, viz_plot_results_enhanced


class ExperimentPlotter:
    """Utility class for plotting experiment results"""
    
    @staticmethod
    def plot_influence_distribution(weights: List[float], method: str, 
                                   bins: int = 50) -> go.Figure:
        """Plot distribution of influence weights"""
        try:
            # Use shared matplotlib-based visualization when available
            viz_dist, _ = _load_viz_matplotlib()
            scores = {method: np.array(weights)}
            plt_obj = viz_dist(scores, plot_name_suffix=method)
            return plt_obj
        except Exception:
            # Fallback to local Plotly implementation
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=weights,
                nbinsx=bins,
                name='Influence Score',
                marker=dict(
                    color='rgba(55, 128, 191, 0.7)',
                    line=dict(color='rgba(55, 128, 191, 1)', width=1)
                ),
                hovertemplate="<b>Score Range</b><br>%{x}<br>Frequency: %{y}<extra></extra>"
            ))

            fig.update_layout(
                title=f"<b>Influence Weights Distribution - {method}</b>",
                xaxis_title="Influence Score",
                yaxis_title="Frequency",
                hovermode='x unified',
                template='plotly_white',
                showlegend=True,
                height=500
            )

            return fig
    
    @staticmethod
    def plot_weights_comparison(weights_dict: Dict[str, List[float]], 
                               top_n: int = 10) -> go.Figure:
        """Compare top influences across multiple methods"""
        fig = go.Figure()
        
        for method, weights in weights_dict.items():
            sorted_indices = np.argsort(weights)[::-1][:top_n]
            sorted_weights = np.array(weights)[sorted_indices]
            
            fig.add_trace(go.Bar(
                x=list(range(1, len(sorted_weights) + 1)),
                y=sorted_weights,
                name=method,
                hovertemplate=f"<b>{method}</b><br>Rank: %{{x}}<br>Score: %{{y:.4f}}<extra></extra>"
            ))
        
        fig.update_layout(
            title=f"<b>Top {top_n} Influential Samples Comparison</b>",
            xaxis_title="Rank",
            yaxis_title="Influence Score",
            barmode='group',
            template='plotly_white',
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def plot_removal_impact(results: Dict[str, Any], removal_percentages: List[int],
                           methods: List[str] = None) -> go.Figure:
        """Plot impact of data removal on model performance"""
        try:
            # Prefer shared matplotlib visualization for results comparison
            _, viz_enh = _load_viz_matplotlib()
            plt_obj = viz_enh(results, removal_percentages)
            return plt_obj
        except Exception:
            fig = go.Figure()
            for method in (methods or []):
                values = []
                for pct in removal_percentages:
                    key = f"{method}_{pct}pct"
                    if key in results:
                        mae = results[key].get('final_mae', np.nan)
                        values.append(mae)
                    else:
                        values.append(np.nan)

                if any(~np.isnan(values)):
                    fig.add_trace(go.Scatter(
                        x=removal_percentages,
                        y=values,
                        mode='lines+markers',
                        name=method,
                        hovertemplate="<b>%{fullData.name}</b><br>Removal: %{x}%<br>MAE: %{y:.4f}<extra></extra>",
                        line=dict(width=2),
                        marker=dict(size=6)
                    ))

            # Add baseline
            if 'orig' in results:
                baseline_mae = results['orig'].get('final_mae', 0)
                fig.add_hline(
                    y=baseline_mae,
                    line_dash="dash",
                    line_color="red",
                    name="Baseline",
                    annotation_text="Baseline",
                    annotation_position="right"
                )

            fig.update_layout(
                title="<b>Model Performance vs Data Removal</b>",
                xaxis_title="Data Removal Percentage (%)",
                yaxis_title="Mean Absolute Error",
                hovermode='x unified',
                template='plotly_white',
                height=500,
                showlegend=True
            )

            return fig
    
    @staticmethod
    def plot_random_baseline_comparison(results: Dict[str, Any], 
                                       removal_percentages: List[int],
                                       random_run_results: Optional[Dict] = None) -> go.Figure:
        """Compare influence-based removal vs random removal"""
        try:
            # Use shared matplotlib-enhanced visualization to show random runs and trends
            _, viz_enh = _load_viz_matplotlib()
            plt_obj = viz_enh(
                results, removal_percentages, random_run_results=random_run_results
            )
            return plt_obj
        except Exception:
            fig = go.Figure()

            # Plot random removal baseline with confidence interval
            if random_run_results:
                means = []
                stds = []

                for pct in removal_percentages:
                    if pct in random_run_results:
                        values = random_run_results[pct]
                        means.append(np.mean(values))
                        stds.append(np.std(values))
                    else:
                        means.append(np.nan)
                        stds.append(np.nan)

                # Add confidence band
                means = np.array(means)
                stds = np.array(stds)

                fig.add_trace(go.Scatter(
                    x=removal_percentages + removal_percentages[::-1],
                    y=list(means + stds) + list((means - stds)[::-1]),
                    fill='toself',
                    name='Random (±1σ)',
                    fillcolor='rgba(100, 100, 100, 0.2)',
                    line=dict(color='rgba(100, 100, 100, 0)'),
                    hoverinfo='skip'
                ))

                # Add mean line
                fig.add_trace(go.Scatter(
                    x=removal_percentages,
                    y=means,
                    mode='lines+markers',
                    name='Random Baseline',
                    line=dict(color='gray', width=2, dash='dash'),
                    marker=dict(size=6),
                    hovertemplate="<b>Random Removal</b><br>Removal: %{x}%<br>MAE: %{y:.4f}<extra></extra>"
                ))

            # Plot influence-based methods
            methods_to_plot = [k.split('_')[0] for k in results.keys() 
                              if isinstance(k, str) and '_pct' in k]
            methods_to_plot = list(set(methods_to_plot))

            for method in methods_to_plot[:3]:  # Plot top 3 methods
                values = []
                for pct in removal_percentages:
                    key = f"{method}_{pct}pct"
                    if key in results:
                        mae = results[key].get('final_mae', np.nan)
                        values.append(mae)

                if any(~np.isnan(values)):
                    fig.add_trace(go.Scatter(
                        x=removal_percentages,
                        y=values,
                        mode='lines+markers',
                        name=f"{method} (Influence)",
                        line=dict(width=2),
                        marker=dict(size=6),
                        hovertemplate=f"<b>{method}</b><br>Removal: %{{x}}%<br>MAE: %{{y:.4f}}<extra></extra>"
                    ))

            fig.update_layout(
                title="<b>Influence-Based vs Random Data Removal</b>",
                xaxis_title="Data Removal Percentage (%)",
                yaxis_title="Mean Absolute Error",
                hovermode='x unified',
                template='plotly_white',
                height=500,
                showlegend=True
            )

            return fig
    
    @staticmethod
    def plot_influence_statistics(weights: List[float], method: str) -> go.Figure:
        """Plot detailed statistics of influence weights"""
        fig = go.Figure()
        
        weights_array = np.array(weights)
        
        # Box plot
        fig.add_trace(go.Box(
            y=weights,
            name='Influence Scores',
            boxmean='sd',
            marker_color='rgba(55, 128, 191, 0.7)',
            hovertemplate="<b>Influence Score</b><br>Value: %{y:.4f}<extra></extra>"
        ))
        
        fig.update_layout(
            title=f"<b>Influence Scores Statistics - {method}</b>",
            yaxis_title="Score Value",
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def plot_sample_ranking(weights: List[float], top_n: int = 20) -> pd.DataFrame:
        """Create dataframe of ranked samples by influence"""
        weights_array = np.array(weights)
        sorted_indices = np.argsort(weights_array)[::-1]
        
        df = pd.DataFrame({
            'Rank': range(1, len(sorted_indices) + 1),
            'Sample Index': sorted_indices,
            'Influence Score': weights_array[sorted_indices],
            'Percentile': (100 * (len(sorted_indices) - np.arange(len(sorted_indices))) 
                          / len(sorted_indices)).astype(int)
        })
        
        return df.head(top_n)
    
    @staticmethod
    def plot_method_comparison_heatmap(weights_dict: Dict[str, List[float]], 
                                       top_n: int = 30) -> go.Figure:
        """Create heatmap comparing influence methods on top samples"""
        
        # Get top samples for each method
        top_samples = set()
        for weights in weights_dict.values():
            top_samples.update(np.argsort(weights)[::-1][:top_n])
        
        top_samples = sorted(list(top_samples))
        
        # Create matrix
        methods = list(weights_dict.keys())
        data = np.zeros((len(methods), len(top_samples)))
        
        for i, method in enumerate(methods):
            for j, sample_idx in enumerate(top_samples):
                if sample_idx < len(weights_dict[method]):
                    data[i, j] = weights_dict[method][sample_idx]
        
        fig = go.Figure(data=go.Heatmap(
            z=data,
            x=[f"Sample {s}" for s in top_samples],
            y=methods,
            colorscale='Viridis',
            hovertemplate="<b>%{y}</b><br>%{x}<br>Score: %{z:.4f}<extra></extra>"
        ))
        
        fig.update_layout(
            title=f"<b>Influence Methods Comparison (Top {len(top_samples)} Samples)</b>",
            xaxis_title="Sample",
            yaxis_title="Method",
            height=400,
            template='plotly_white'
        )
        
        return fig


def _bar_text_vs_best(
    values: List[float], value_fmt: str, higher_is_better: bool
) -> List[str]:
    """Значение + отклонение от лучшего в группе, % (как в matplotlib)."""
    deltas = _pct_vs_best([float(v) for v in values], higher_is_better)
    lines = []
    for i, v in enumerate(values):
        main = value_fmt % float(v)
        d = deltas[i]
        if d is not None and _should_show_pct_vs_best(d):
            lines.append(f"{main}<br>к лучш.: {d:+.1f}%")
        else:
            lines.append(main)
    return lines


def plotly_removal_auc_bars(
    aucs: Dict[str, Any],
    methods_filter: List[str],
    metric_name: str,
    metric_short: str = "AUC",
) -> go.Figure:
    """
    Столбцы AUC только для методов из methods_filter (те же, что на графике removal).
    Сортировка по rank_score (как experiment_summary).
    """
    colors = _trend_colors_for_methods()
    present: List[str] = []
    for m in methods_filter:
        v = aucs.get(m)
        if v is None:
            continue
        try:
            vf = float(v)
        except (TypeError, ValueError):
            continue
        if not np.isfinite(vf):
            continue
        present.append(m)
    fig = go.Figure()
    if not present:
        fig.update_layout(
            title="AUC кривых removal — нет данных для выбранных серий",
            template="plotly_white",
            height=360,
        )
        return fig
    sub = {m: float(aucs[m]) for m in present}
    rank_scores = removal_curve_rank_scores(sub, metric_name, METRIC_METADATA)
    order = sorted(
        present,
        key=lambda m: (
            rank_scores.get(m, float("-inf"))
            if np.isfinite(rank_scores.get(m, float("nan")))
            else float("-inf")
        ),
        reverse=True,
    )
    vals = [sub[m] for m in order]
    bar_colors = [_resolve_method_color(m, colors) for m in order]
    meta = (METRIC_METADATA or {}).get(metric_name) or {}
    higher = bool(meta.get("higher_is_better", True))
    text_lines = _bar_text_vs_best(vals, "%.4f", higher)
    fig.add_trace(
        go.Bar(
            x=order,
            y=vals,
            marker=dict(color=bar_colors, line=dict(color="#333", width=1)),
            text=text_lines,
            textposition="outside",
            textfont=dict(size=10),
            hovertemplate="<b>%{x}</b><br>AUC: %{y:.4f}<extra></extra>",
        )
    )
    direction = "выше лучше" if higher else "ниже лучше"
    fig.update_layout(
        title=(
            f"Интеграл кривой removal (AUC), {metric_short} — {direction}<br>"
        ),
        xaxis_title="Метод / стратегия",
        yaxis_title="AUC",
        template="plotly_white",
        height=max(420, min(720, 60 * len(order) + 200)),
        margin=dict(t=100, b=120),
        showlegend=False,
        xaxis=dict(tickangle=-38),
    )
    return fig


def plotly_removal_mean_pct_diff_from_pointwise_best_bars(
    removal_data: Dict[str, Any],
    methods_filter: List[str],
    metric_name: str,
    metric_short: str = "метрика",
) -> go.Figure:
    """
    Среднее по точкам |v−ref|/|ref|·100%, где ref — лучшее значение среди выбранных кривых в этой точке.
    """
    meta = (METRIC_METADATA or {}).get(metric_name) or {}
    higher = bool(meta.get("higher_is_better", True))
    means, n_pts = mean_pct_abs_diff_from_pointwise_best(
        removal_data, methods_filter, higher
    )
    fig = go.Figure()
    colors = _trend_colors_for_methods()
    present: List[str] = []
    for m in methods_filter:
        v = means.get(m)
        if v is None:
            continue
        if not np.isfinite(float(v)):
            continue
        present.append(m)
    if not present or n_pts <= 0:
        fig.update_layout(
            title="Нет общих точек % удаления у выбранных кривых",
            template="plotly_white",
            height=360,
        )
        return fig

    sub = {m: float(means[m]) for m in present}
    order = sorted(present, key=lambda m: sub[m])
    vals = [sub[m] for m in order]
    bar_colors = [_resolve_method_color(m, colors) for m in order]
    text_lines = [f"{v:.2f}" for v in vals]
    fig.add_trace(
        go.Bar(
            x=order,
            y=vals,
            marker=dict(color=bar_colors, line=dict(color="#333", width=1)),
            text=text_lines,
            textposition="outside",
            textfont=dict(size=10),
            hovertemplate=(
                f"<b>%{{x}}</b><br>Среднее |v−best|/|best|·100%: %{{y:.2f}}% "
                f"<br>(точек: {n_pts})<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        title=f"Среднее отклонение от лучшей кривой в точке, {metric_short}",
        xaxis_title="Метод",
        yaxis_title="Среднее отклонение, %",
        template="plotly_white",
        height=max(420, min(720, 60 * len(order) + 200)),
        margin=dict(t=72, b=120),
        showlegend=False,
        xaxis=dict(tickangle=-38),
    )
    return fig


def plotly_computation_metric_bars(
    rows: List[Dict[str, Any]],
    field: str,
    title: str,
    yaxis_title: str,
    value_fmt: str,
) -> go.Figure:
    """Один из графиков max_wanted_mb / ram_mb / duration_s по этапам *_computation."""
    fig = go.Figure()
    if not rows:
        fig.update_layout(
            title=title + " — нет данных",
            template="plotly_white",
            height=320,
        )
        return fig
    colors = _trend_colors_for_methods()
    methods = [r["method"] for r in rows]
    vals = [float(r[field]) for r in rows]
    bar_colors = [_resolve_method_color(m, colors) for m in methods]
    # Память и время: чем меньше тем лучше
    text_lines = _bar_text_vs_best(vals, value_fmt, higher_is_better=False)
    fig.add_trace(
        go.Bar(
            x=methods,
            y=vals,
            marker=dict(color=bar_colors, line=dict(color="#222", width=0.5)),
            text=text_lines,
            textposition="outside",
            textfont=dict(size=10),
            hovertemplate=(
                f"<b>%{{x}}</b><br>{yaxis_title}: "
                f"%{{y:{value_fmt[1:]}}}<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        title=title + "<br><sub>к лучш. — отклонение от минимума в группе (меньше лучше), %</sub>",
        xaxis_title="Метод",
        yaxis_title=yaxis_title,
        template="plotly_white",
        height=max(380, min(680, 52 * len(methods) + 180)),
        margin=dict(t=90, b=100),
        showlegend=False,
        xaxis=dict(tickangle=-36),
    )
    return fig
