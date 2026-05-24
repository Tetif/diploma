#!/usr/bin/env python3
"""
Усреднение времени (мин) Influence / LiSSA / Nyström / Arnoldi по моделям внутри каждого датасета;
LaTeX-таблица + один сгруппированный bar chart в стиле visualization/plots.py (methods_bar).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


NYSTROM = "Nystrom"  # ASCII для pandas/plot на Windows

# Исходные значения как в тексте таблицы (--- = нет измерения)
ROWS: list[dict[str, float | str | None]] = [
    # adult
    {"dataset": "adult", "model": "CatBoost", "Influence": 2.19, "LiSSA": 0.92, "Nystrom": 0.67, "Arnoldi": None},
    {"dataset": "adult", "model": "Random Forest", "Influence": 0.61, "LiSSA": 0.03, "Nystrom": 0.13, "Arnoldi": None},
    {"dataset": "adult", "model": "LightGBM", "Influence": 0.48, "LiSSA": 0.07, "Nystrom": 0.16, "Arnoldi": None},
    {"dataset": "adult", "model": "XGBoost", "Influence": 0.73, "LiSSA": 0.01, "Nystrom": 0.01, "Arnoldi": None},
    {"dataset": "adult", "model": "PyTorch (NN)", "Influence": 1.68, "LiSSA": 0.12, "Nystrom": 0.32, "Arnoldi": None},
    # cover type
    {"dataset": "cover type", "model": "CatBoost", "Influence": 118.34, "LiSSA": 69.28, "Nystrom": 108.62, "Arnoldi": 150.80},
    {"dataset": "cover type", "model": "Random Forest", "Influence": 115.93, "LiSSA": 67.87, "Nystrom": 110.25, "Arnoldi": 148.44},
    {"dataset": "cover type", "model": "LightGBM", "Influence": 127.76, "LiSSA": 135.51, "Nystrom": 118.80, "Arnoldi": 156.54},
    {"dataset": "cover type", "model": "XGBoost", "Influence": 112.73, "LiSSA": 7.58, "Nystrom": 93.85, "Arnoldi": 148.36},
    {"dataset": "cover type", "model": "PyTorch (NN)", "Influence": 122.71, "LiSSA": 74.16, "Nystrom": 104.96, "Arnoldi": 153.90},
    # electric (в черновике LaTeX была метка imdb — заменено на electric)
    {"dataset": "electric", "model": "CatBoost", "Influence": 83.47, "LiSSA": 30.12, "Nystrom": 61.84, "Arnoldi": 22.31},
    {"dataset": "electric", "model": "Random Forest", "Influence": 78.94, "LiSSA": 28.47, "Nystrom": 57.93, "Arnoldi": 20.87},
    {"dataset": "electric", "model": "LightGBM", "Influence": 75.98, "LiSSA": 28.45, "Nystrom": 51.29, "Arnoldi": 19.58},
    {"dataset": "electric", "model": "XGBoost", "Influence": 72.34, "LiSSA": 26.71, "Nystrom": 50.36, "Arnoldi": 19.00},
    {"dataset": "electric", "model": "PyTorch (NN)", "Influence": 76.53, "LiSSA": 27.86, "Nystrom": 56.72, "Arnoldi": 20.43},
    # housing
    {"dataset": "housing", "model": "CatBoost", "Influence": 4.79, "LiSSA": 0.07, "Nystrom": 3.21, "Arnoldi": 0.06},
    {"dataset": "housing", "model": "Random Forest", "Influence": 4.91, "LiSSA": 0.07, "Nystrom": 2.85, "Arnoldi": 0.06},
    {"dataset": "housing", "model": "LightGBM", "Influence": 5.61, "LiSSA": 0.05, "Nystrom": 3.27, "Arnoldi": 0.04},
    {"dataset": "housing", "model": "XGBoost", "Influence": 0.69, "LiSSA": 0.05, "Nystrom": 0.40, "Arnoldi": 0.04},
    {"dataset": "housing", "model": "PyTorch (NN)", "Influence": 5.64, "LiSSA": 0.08, "Nystrom": 3.13, "Arnoldi": 0.07},
    # imdb
    {"dataset": "imdb", "model": "CatBoost", "Influence": 27.13, "LiSSA": 11.52, "Nystrom": 88.74, "Arnoldi": None},
    {"dataset": "imdb", "model": "Random Forest", "Influence": 24.08, "LiSSA": 10.45, "Nystrom": 98.31, "Arnoldi": None},
    {"dataset": "imdb", "model": "LightGBM", "Influence": 16.94, "LiSSA": 15.78, "Nystrom": 167.83, "Arnoldi": None},
    {"dataset": "imdb", "model": "XGBoost", "Influence": 17.58, "LiSSA": 2.25, "Nystrom": 90.83, "Arnoldi": None},
    {"dataset": "imdb", "model": "PyTorch (NN)", "Influence": 21.34, "LiSSA": 9.63, "Nystrom": 114.26, "Arnoldi": None},
    # wine
    {"dataset": "wine", "model": "CatBoost", "Influence": 0.40, "LiSSA": 0.09, "Nystrom": 0.22, "Arnoldi": 0.74},
    {"dataset": "wine", "model": "Random Forest", "Influence": 1.98, "LiSSA": 0.50, "Nystrom": 0.80, "Arnoldi": 2.12},
    {"dataset": "wine", "model": "LightGBM", "Influence": 0.52, "LiSSA": 0.08, "Nystrom": 0.23, "Arnoldi": 0.61},
    {"dataset": "wine", "model": "XGBoost", "Influence": 0.12, "LiSSA": 0.31, "Nystrom": 0.04, "Arnoldi": 0.93},
    {"dataset": "wine", "model": "PyTorch (NN)", "Influence": 0.46, "LiSSA": 0.48, "Nystrom": 0.26, "Arnoldi": 5.73},
    # zillow
    {"dataset": "zillow", "model": "CatBoost", "Influence": 1.39, "LiSSA": 0.23, "Nystrom": 0.31, "Arnoldi": None},
    {"dataset": "zillow", "model": "Random Forest", "Influence": 1.40, "LiSSA": 0.23, "Nystrom": 0.30, "Arnoldi": None},
    {"dataset": "zillow", "model": "LightGBM", "Influence": 1.40, "LiSSA": 0.26, "Nystrom": 0.33, "Arnoldi": None},
    {"dataset": "zillow", "model": "XGBoost", "Influence": 1.37, "LiSSA": 0.23, "Nystrom": 0.30, "Arnoldi": None},
    {"dataset": "zillow", "model": "PyTorch (NN)", "Influence": 0.25, "LiSSA": 0.16, "Nystrom": 0.89, "Arnoldi": None},
]

METHOD_SHORT = ["Influence", "LiSSA", NYSTROM, "Arnoldi"]

# Подписи на графике (UTF-8); в pandas — NYSTROM для совместимости с консолью Windows
METHOD_LEGEND_LABELS = ["Influence", "LiSSA", "Nyström", "Arnoldi"]

# Совпадает с visualization/plots.py _trend_colors_for_methods


def method_colors():
    return {
        "Influence": "#9b59b6",
        "LiSSA": "#8c564b",
        "Nystrom": "#e377c2",
        "Arnoldi": "#d62728",
    }


def pct_vs_best(values: list[float]) -> list[float | None]:
    vals = []
    for x in values:
        try:
            v = float(x)
        except (TypeError, ValueError):
            v = np.nan
        vals.append(v if np.isfinite(v) else np.nan)

    finite_v = [v for v in vals if np.isfinite(v)]
    if not finite_v:
        return [None] * len(vals)
    best = min(finite_v)

    def one(v):
        if not np.isfinite(v):
            return None
        if abs(best) < 1e-15:
            return None
        return 100.0 * (float(v) - best) / abs(best)

    return [one(v) for v in vals]


def format_cell(x: object) -> str:
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return "---"
    if not np.isfinite(xf):
        return "---"
    return f"{xf:.2f}"


def dataframe_averages(df: pd.DataFrame) -> pd.DataFrame:
    num = df[METHOD_SHORT].apply(pd.to_numeric, errors="coerce")
    g = pd.concat([df["dataset"], num], axis=1).groupby("dataset", sort=False).mean()
    ds_order = df["dataset"].unique().tolist()
    return g.loc[ds_order]


def latex_table(mean_df: pd.DataFrame) -> str:
    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{Среднее время вычисления оценок влияния по моделям (мин).}",
        r"\label{tab:influence_time_mean_by_dataset}",
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Датасет & Influence & LiSSA & Nyström & Arnoldi \\",
        r"\midrule",
    ]
    for ds in mean_df.index:
        row_cells = [ds.replace("_", r"\_")]
        for m in METHOD_SHORT:
            row_cells.append(format_cell(mean_df.loc[ds, m]))
        lines.append(" & ".join(row_cells) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}"])
    return "\n".join(lines)


def latex_summary_row(mean_df: pd.DataFrame) -> str:
    """Строка LaTeX перед \\bottomrule: среднее по датасетам (NaN в колонке игнорируются)."""
    cells = ["среднее по датасетам"]
    for m in METHOD_SHORT:
        s = pd.to_numeric(mean_df[m], errors="coerce").dropna()
        cells.append(format_cell(float(s.mean())) if len(s) > 0 else "---")
    return "\\midrule\n" + " & ".join(cells) + r" \\"


def _show_pct(delta: float | None) -> bool:
    if delta is None:
        return False
    return abs(float(delta)) > 1e-3


def overall_row(mean_df: pd.DataFrame) -> pd.Series:
    """Среднее по колонкам mean_df (как строка «среднее по датасетам» в LaTeX)."""
    out: dict[str, float] = {}
    for m in METHOD_SHORT:
        s = pd.to_numeric(mean_df[m], errors="coerce").dropna()
        out[m] = float(s.mean()) if len(s) > 0 else np.nan
    return pd.Series(out)


def plot_overall_four_bars(mean_df: pd.DataFrame, out_path: Path) -> None:
    """4 столбца: среднее время по каждому методу, усреднённое по датасетам; только числа на столбцах."""
    colors_map = method_colors()
    row = overall_row(mean_df)
    values = [float(row[m]) if pd.notna(row[m]) else np.nan for m in METHOD_SHORT]
    x = np.arange(len(METHOD_SHORT), dtype=float)

    fig = plt.figure(figsize=(8.2, 6.2))
    ax = fig.add_subplot(111)
    bars = ax.bar(
        x,
        [v if np.isfinite(v) else 0.0 for v in values],
        color=[colors_map[m] for m in METHOD_SHORT],
        edgecolor="black",
        linewidth=0.4,
        alpha=0.92,
    )
    lbls = []
    for v in values:
        lbls.append(f"{v:.2f}" if np.isfinite(v) else "")
    ax.bar_label(bars, labels=lbls, fontsize=7.5, padding=2)
    ax.set_xticks(x)
    ax.set_xticklabels(METHOD_LEGEND_LABELS, rotation=22, ha="right")
    ax.set_ylabel("минуты")
    ax.set_title(
        "Среднее время вычисления влияния по методам\n"
        "(среднее по датасетам; внутри датасета предварительно усреднено по моделям)",
        fontsize=10,
    )
    ax.grid(True, axis="y", alpha=0.28)
    finite = [v for v in values if np.isfinite(v)]
    ymax = max(finite) if finite else 1.0
    span = ymax if ymax > 0 else 1.0
    ax.set_ylim(0.0, ymax + 0.18 * span)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def plot_grouped(means: pd.DataFrame, out_path: Path) -> None:
    colors_map = method_colors()
    datasets = means.index.tolist()
    k = len(METHOD_SHORT)
    n_ds = len(datasets)

    fig_w = max(12.0, 0.9 * n_ds + 5.0)
    fig = plt.figure(figsize=(fig_w, 6.8))
    ax = fig.add_subplot(111)

    x = np.arange(n_ds, dtype=float)
    width_total = 0.78
    bar_w = width_total / k
    offsets = (np.arange(k) - (k - 1) / 2.0) * bar_w

    value_fmt = "%.2f"
    legend_handles: list = []

    def row_vals(ds: str) -> list[float]:
        out: list[float] = []
        for m in METHOD_SHORT:
            w = pd.to_numeric(means.loc[ds, m], errors="coerce")
            out.append(float(w) if pd.notna(w) else np.nan)
        return out

    for ji, meth in enumerate(METHOD_SHORT):
        col = pd.to_numeric(means[meth], errors="coerce")
        heights_draw: list[float] = []
        labels: list[str] = []
        for i, ds in enumerate(datasets):
            v_raw = float(col.iloc[i]) if pd.notna(col.iloc[i]) else np.nan
            deltas = pct_vs_best(row_vals(ds))
            if np.isfinite(v_raw):
                heights_draw.append(float(v_raw))
                main = value_fmt % v_raw
                d = deltas[ji]
                if _show_pct(d):
                    labels.append(f"{main}\nк лучш.: {d:+.1f}%")
                else:
                    labels.append(main)
            else:
                heights_draw.append(0.0)
                labels.append("")

        rects = ax.bar(
            x + offsets[ji],
            heights_draw,
            width=bar_w * 0.92,
            label=meth,
            color=colors_map[meth],
            edgecolor="black",
            linewidth=0.4,
            alpha=0.92,
        )
        legend_handles.append(rects[0])
        ax.bar_label(rects, labels=labels, fontsize=6.5, padding=2)

    ax.set_xticks(x)
    ax.set_xticklabels(datasets, rotation=28, ha="right")
    ax.set_ylabel("минуты")
    ax.set_title(
        "Время вычисления влияния: среднее по моделям внутри датасета\n"
        "(к лучшему внутри каждого датасета — отклонение в %; меньше значение лучше)",
        fontsize=10,
    )
    ax.grid(True, axis="y", alpha=0.28)

    finite_flat = np.asarray(pd.to_numeric(means.values.ravel(), errors="coerce"), dtype=float)
    finite_flat = finite_flat[np.isfinite(finite_flat)]
    ymax = float(np.max(finite_flat)) if len(finite_flat) else 1.0
    ymin = 0.0
    span = ymax - ymin if ymax > ymin else max(abs(ymax), 1e-9)
    ax.set_ylim(ymin - 0.06 * span, ymax + 0.22 * span)

    ax.legend(
        handles=legend_handles,
        labels=METHOD_LEGEND_LABELS,
        fontsize=8,
        ncol=4,
        loc="upper center",
    )

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "experiment_logs",
        help="куда сохранить CSV/LaTeX/PNG",
    )
    args = p.parse_args()
    df = pd.DataFrame(ROWS)
    means = dataframe_averages(df)

    csv_path = args.out_dir / "influence_time_mean_by_dataset.csv"
    tex_path = args.out_dir / "influence_time_mean_by_dataset.tex"
    png_path = args.out_dir / "influence_time_mean_by_dataset_bar.png"
    png_overall_path = args.out_dir / "influence_time_mean_overall_bar.png"

    args.out_dir.mkdir(parents=True, exist_ok=True)
    means.to_csv(csv_path)

    tex_core = latex_table(means).replace("\\bottomrule", latex_summary_row(means) + "\n\\bottomrule")
    tex_notes = (
        "\n\\noindent\\small\\textit{Среднее по датасетам — среднее средних значений колонки; "
        "для Arnoldi исключены датасеты без наблюдений. "
        "В исходной таблице третья группа имела ошибочную подпись \\texttt{imdb}; данные как для \\texttt{electric}.}\\medskip\n"
    )
    tex_path.write_text(tex_core + tex_notes, encoding="utf-8")

    plot_grouped(means, png_path)
    plot_overall_four_bars(means, png_overall_path)
    print(means.rename(columns={NYSTROM: "Nystrom"}).round(4))
    print(f"\nCSV: {csv_path}\nPNG (по датасетам): {png_path}\nPNG (4 столбца, по всем датасетам): {png_overall_path}\nTeX: {tex_path}\n")


if __name__ == "__main__":
    main()