#!/usr/bin/env python3
"""
Plots for the influence / data-valuation study: reads results/<study>/<dataset>/<method>/seed<k>/results.json
(written by run_study.py) and writes PNGs + summary tables (style of the ijepa-cifar10 repo).

  python plot_results.py                                   # results/ -> assets/
  python plot_results.py --root results/pilot --out results/pilot/plots --clean pilot-clean --noise pilot-noise10

Figures:
  1_removal_curves.png    holdout metric vs % of train removed (clean data); row 1 = lowest-value first,
                          row 2 = highest-value first. Line = mean over seeds, band = min..max over seeds,
                          grey = random removal, dashed = full-data model.
  2_noise_removal.png     same, on data with corrupted labels, lowest-value first
  3_detection_auc.png     AUC of finding the corrupted points by low value; dot = seed, tick = mean, dashed = 0.5
  4_found_at.png          share of corrupted points found vs % of train inspected (lowest value first)
  5_paired_vs_random.png  per-seed gain over random removal at 10 % (same seed / split), tick = mean, p = t-test
  6_removal_auc.png       mean gain over the full-data model across the removal grid; dot = seed
  7_sensitivity.png       sweep (adult): detection AUC and gain vs random as a function of each parameter
  8-13                    secondary studies (models, convex, distillation, transfer, systematic noise, cost):
                          see plot_extensions.py
  summary.md / summary.csv / cost.csv / transfer.csv
Requires: matplotlib, numpy, scipy.
"""
import argparse
import csv
import os
import sys
import textwrap
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from study.summary import load, paired_test, removal_auc, sign  # noqa: E402

ORDER = ["LOO", "TMCShapley", "KNNShapley", "DataOOB", "Influence", "LissaInfluence", "LossHigh"]
LABELS = {"LOO": "LOO", "TMCShapley": "TMC-Shapley", "KNNShapley": "KNN-Shapley", "DataOOB": "Data-OOB",
          "Influence": "Influence", "LissaInfluence": "LiSSA", "LossHigh": "high loss", "random": "random", "CatBoostLFC": "CatBoost LFC"}
# one fixed colour per method (colour follows the entity, never its rank)
COLORS = {"LOO": "#2a78d6", "TMCShapley": "#6250d6", "KNNShapley": "#1baf7a", "DataOOB": "#eda100",
          "Influence": "#eb6834", "LissaInfluence": "#e87ba4", "LossHigh": "#008300", "random": "#8a8984",
          "CatBoostLFC": "#7a4a1e"}
DS_ORDER = ["wine", "housing", "adult", "covertype"]
INK, INK2, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1", "#fcfcfb"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.edgecolor": MUTED, "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "legend.frameon": False, "lines.solid_capstyle": "round",
})


# ----------------------------------------------------------------------------- helpers
def methods_in(runs):
    ms = [m for m in ORDER if m in runs]
    return ms + sorted(set(runs) - set(ms) - {"random", "_baseline"})


def datasets_in(study_data):
    ds = [d for d in DS_ORDER if d in study_data]
    return ds + sorted(set(study_data) - set(ds))


def any_run(runs):
    for seeds in runs.values():
        for r in seeds.values():
            return r
    return None


def metric_label(r):
    m = r.get("metric", "metric")
    return f"{m.upper() if m in ('mae', 'rmse') else m} on holdout ({'higher' if r.get('higher_is_better') else 'lower'} = better)"


def finish(fig, path, title, note=None):
    width_chars = int(fig.get_figwidth() * 7.5)
    title = "\n".join(textwrap.wrap(title, width_chars)) if len(title) > width_chars else title
    fig.suptitle(title, x=0.01, ha="left", fontsize=13, fontweight="bold", color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    if note:
        # below the axes (outside the canvas); bbox_inches="tight" keeps it in the PNG
        note = "\n".join(textwrap.wrap(note, int(fig.get_figwidth() * 13)))
        fig.text(0.01, -0.01, note, ha="left", va="top", fontsize=8.5, color=INK2)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


def legend(ax, methods, extra=(), loc="best", outside=False):
    h = [plt.Line2D([0], [0], color=COLORS.get(m, INK2), lw=2.2, marker="o", ms=5, label=LABELS.get(m, m))
         for m in methods]
    h += list(extra)
    if outside:
        ax.legend(handles=h, loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8.5, labelcolor=INK2,
                  handlelength=1.8)
    else:
        ax.legend(handles=h, loc=loc, fontsize=8.5, labelcolor=INK2, handlelength=1.8)


def grid(n, rows=1, w=5.2, h=3.9):
    fig, axes = plt.subplots(rows, n, figsize=(w * n, h * rows), squeeze=False)
    return fig, axes


def stack(seeds, strategy):
    """-> fracs, matrix[seeds, 1 + fracs] with the full-data baseline at 0 % (same seed)."""
    rows, fracs = [], None
    for r in seeds.values():
        c = r.get("curves", {}).get(strategy)
        if not c:
            continue
        f = sorted(c, key=float)
        if fracs is None:
            fracs = f
        if f != fracs:
            continue
        rows.append([r["baseline"]] + [c[k] for k in f])
    if not rows:
        return None, None
    return np.array([0.0] + [float(x) for x in fracs]), np.array(rows)


def dots(ax, i, vals, color):
    vals = np.asarray(vals, float)
    jitter = np.linspace(-0.12, 0.12, len(vals)) if len(vals) > 1 else np.array([0.0])
    ax.scatter(i + jitter, vals, s=40, color=color, edgecolor=SURFACE, linewidth=1.1, zorder=3)
    ax.hlines(vals.mean(), i - 0.28, i + 0.28, color=INK, lw=2, zorder=4)


# ----------------------------------------------------------------------------- figures
def fig_curves(sd, strategies, fname, title, outdir, note):
    dss = datasets_in(sd)
    if not dss:
        return
    fig, axes = grid(len(dss), rows=len(strategies))
    for col, ds in enumerate(dss):
        runs = sd[ds]
        r0 = any_run(runs)
        for row, strat in enumerate(strategies):
            ax = axes[row][col]
            shown = []
            if "random" in runs:
                x, M = stack(runs["random"], "random")
                if x is not None:
                    ax.fill_between(x, M.min(0), M.max(0), color=MUTED, alpha=0.18, lw=0)
                    ax.plot(x, M.mean(0), color=MUTED, lw=2, ls=(0, (4, 2)), marker="o", ms=3.5)
            for m in methods_in(runs):
                x, M = stack(runs[m], strat)
                if x is None:
                    continue
                c = COLORS.get(m, INK2)
                if M.shape[0] > 1:
                    ax.fill_between(x, M.min(0), M.max(0), color=c, alpha=0.12, lw=0)
                ax.plot(x, M.mean(0), color=c, lw=2, marker="o", ms=4.5, mfc=c, mec=SURFACE, mew=1)
                shown.append(m)
            if "_baseline" in runs:
                b = np.mean([r["baseline"] for r in runs["_baseline"].values()])
                ax.axhline(b, color=INK2, ls="--", lw=1.1)
            n_seeds = max((len(s) for k, s in runs.items() if k != "_baseline"), default=0)
            strat_txt = {"lowest": "lowest value removed first", "highest": "highest value removed first"}[strat]
            ax.set_title(f"{ds}  (n_train={r0['n_train']}, seeds: {n_seeds})\n{strat_txt}", fontsize=10)
            ax.set_xlabel("% of training points removed")
            ax.set_ylabel(metric_label(r0))
            if col == len(dss) - 1 and row == 0:
                extra = [plt.Line2D([0], [0], color=MUTED, lw=2, ls=(0, (4, 2)), label="random removal"),
                         plt.Line2D([0], [0], color=INK2, lw=1.1, ls="--", label="full data")]
                legend(ax, shown, extra, outside=True)
    finish(fig, os.path.join(outdir, fname), title, note)


def fig_detection(sd, outdir):
    dss = [d for d in datasets_in(sd) if any("detection" in r for s in sd[d].values() for r in s.values())]
    if not dss:
        return
    fig, axes = grid(len(dss), h=3.8)
    for ax, ds in zip(axes[0], dss):
        runs = sd[ds]
        ms = [m for m in methods_in(runs) if any("detection" in r for r in runs[m].values())]
        for i, m in enumerate(ms):
            vals = [r["detection"]["auc"] for r in runs[m].values() if "detection" in r]
            dots(ax, i, vals, COLORS.get(m, INK2))
            ax.text(i, max(vals) + 0.015, f"{np.mean(vals):.2f}", ha="center", va="bottom", fontsize=8.5, color=INK2)
        ax.axhline(0.5, color=MUTED, ls="--", lw=1.2)
        ax.text(len(ms) - 0.5, 0.505, "random order", ha="right", va="bottom", fontsize=8.5, color=INK2)
        ax.set_xticks(range(len(ms)), [f"{LABELS.get(m, m)}\n(n={len(runs[m])})" for m in ms], fontsize=8.5)
        ax.set_ylabel("detection AUC of corrupted points")
        ax.set_ylim(0.3, 1.04)
        ax.grid(axis="x", visible=False)
        r0 = any_run(runs)
        ax.set_title(f"{ds}  ({r0.get('n_noisy', '?')} of {r0['n_train']} corrupted)")
    finish(fig, os.path.join(outdir, "3_detection_auc.png"), "Finding corrupted training points by low value",
           note="Dot = one seed (own split and own corrupted subset); black tick = mean. Classification: flipped labels, "
                "regression: y shifted by +-3 std. AUC 0.5 = random order.")


def fig_found(sd, outdir):
    dss = [d for d in datasets_in(sd) if any("detection" in r for s in sd[d].values() for r in s.values())]
    if not dss:
        return
    fig, axes = grid(len(dss), h=3.8)
    for ax, ds in zip(axes[0], dss):
        runs = sd[ds]
        shown = []
        ax.plot([0, 30], [0, 0.3], color=MUTED, ls="--", lw=1.2)
        for m in methods_in(runs):
            rs = [r for r in runs[m].values() if "detection" in r]
            if not rs:
                continue
            ks = sorted(rs[0]["detection"]["found_at"], key=float)
            x = np.array([0.0] + [float(k) for k in ks])
            M = np.array([[0.0] + [r["detection"]["found_at"][k] for k in ks] for r in rs])
            c = COLORS.get(m, INK2)
            if len(rs) > 1:
                ax.fill_between(x, M.min(0), M.max(0), color=c, alpha=0.12, lw=0)
            ax.plot(x, M.mean(0), color=c, lw=2, marker="o", ms=4, mfc=c, mec=SURFACE, mew=1)
            shown.append(m)
        ax.set_xlabel("% of training points inspected (lowest value first)")
        ax.set_ylabel("share of corrupted points found")
        ax.set_ylim(0, 1.02)
        ax.set_title(ds)
        if ds == dss[-1]:
            legend(ax, shown, [plt.Line2D([0], [0], color=MUTED, ls="--", lw=1.2, label="random order")],
                   outside=True)
    finish(fig, os.path.join(outdir, "4_found_at.png"), "How many corrupted points are among the lowest-valued?",
           note="Line = mean over seeds, band = min..max over seeds. 10 % of the training labels are corrupted, "
                "so the ideal curve reaches 1.0 at 10 %.")


def fig_paired(sd_clean, sd_noise, outdir, frac="10"):
    blocks = [(n, sd) for n, sd in (("clean data", sd_clean), ("corrupted labels", sd_noise)) if sd]
    if not blocks:
        return None
    dss = sorted({d for _, sd in blocks for d in sd}, key=lambda d: DS_ORDER.index(d) if d in DS_ORDER else 99)
    fig, axes = grid(len(dss), rows=len(blocks), h=3.6)
    stats_rows = []
    for row, (bname, sd) in enumerate(blocks):
        for col, ds in enumerate(dss):
            ax = axes[row][col]
            ax.axhline(0, color=MUTED, lw=1.2)
            runs = sd.get(ds, {})
            rnd = runs.get("random", {})
            shown, allv = [], [0.0]
            for m in methods_in(runs):
                d = []
                for s, r in runs[m].items():
                    v = r.get("curves", {}).get("lowest", {}).get(frac)
                    rv = rnd.get(s, {}).get("curves", {}).get("random", {}).get(frac)
                    if v is not None and rv is not None:
                        d.append(sign(r) * (v - rv))
                if not d:
                    continue
                i = len(shown)
                shown.append((m, len(d)))
                allv += d
                dots(ax, i, d, COLORS.get(m, INK2))
                t = paired_test(d)
                stats_rows.append({"block": bname, "dataset": ds, "method": m, **t})
                ptxt = "" if t["p_t"] != t["p_t"] else f"\np={t['p_t']:.2f}"
                ax.text(i, max(d), f"{t['mean']:+.3f}{ptxt}", ha="center", va="bottom", fontsize=7.5, color=INK2)
            span = max(allv) - min(allv) or 0.01
            ax.set_ylim(min(allv) - 0.12 * span, max(allv) + 0.35 * span)
            ax.set_xticks(range(len(shown)), [f"{LABELS.get(m, m)}\n(n={n})" for m, n in shown], fontsize=8)
            ax.grid(axis="x", visible=False)
            r0 = any_run(runs) if runs else None
            if r0:
                ax.set_ylabel(f"Δ {r0['metric']} vs random (better > 0)")
            ax.set_title(f"{ds}: {bname}")
    finish(fig, os.path.join(outdir, "5_paired_vs_random.png"),
           f"Removing the {frac} % lowest-valued points vs removing {frac} % at random, paired by seed",
           note="Each dot = method minus random removal for the same seed (same split, same init seed). Black tick = mean "
                "difference; p = paired t-test. Sign is flipped for error metrics, so > 0 always means better.")
    return stats_rows


def fig_removal_auc(sd, outdir, fname="6_removal_auc.png"):
    dss = datasets_in(sd)
    if not dss:
        return
    fig, axes = grid(len(dss), h=3.8)
    for ax, ds in zip(axes[0], dss):
        runs = sd[ds]
        ms = methods_in(runs)
        allv = [0.0]
        for i, m in enumerate(ms):
            vals = [removal_auc(r, "lowest", r["baseline"]) for r in runs[m].values()]
            vals = [v for v in vals if v is not None]
            if not vals:
                continue
            allv += vals
            dots(ax, i, vals, COLORS.get(m, INK2))
        if "random" in runs:
            rv = [removal_auc(r, "random", r["baseline"]) for r in runs["random"].values()]
            rv = [v for v in rv if v is not None]
            if rv:
                ax.axhline(np.mean(rv), color=MUTED, ls=(0, (4, 2)), lw=1.4)
                ax.text(len(ms) - 0.5, np.mean(rv), " random", ha="right", va="bottom", fontsize=8.5, color=INK2)
                allv += rv
        ax.axhline(0, color=INK2, ls="--", lw=1.1)
        span = max(allv) - min(allv) or 0.01
        ax.set_ylim(min(allv) - 0.15 * span, max(allv) + 0.2 * span)
        ax.set_xticks(range(len(ms)), [LABELS.get(m, m) for m in ms], fontsize=8.5)
        ax.grid(axis="x", visible=False)
        r0 = any_run(runs)
        ax.set_ylabel(f"mean Δ {r0['metric']} vs full data")
        ax.set_title(ds)
    finish(fig, os.path.join(outdir, fname), "Average effect of removing low-value points (lowest first, whole grid)",
           note="Mean signed change of the holdout metric over the removal grid relative to the full-data model of the same "
                "seed (0 = dashed). Grey dashed = random removal. > 0 = removal helped.")


def fig_sensitivity(data, outdir):
    from study.config import SWEEP_GRID, sweep_study
    params = [p for p in SWEEP_GRID if any(s.startswith(f"sweep-{p}-") for s in data)]
    if not params:
        return None
    fig, axes = grid(len(params), rows=2, w=4.4, h=3.5)
    rows_out = []
    for col, p in enumerate(params):
        values = SWEEP_GRID[p][0]
        for row, key in enumerate(("auc", "delta")):
            ax = axes[row][col]
            per_m = defaultdict(lambda: ([], [], []))
            for xi, v in enumerate(values):
                st = data.get(sweep_study(p, v), {})
                for ds, runs in st.items():
                    rnd = runs.get("random", {})
                    for m in methods_in(runs):
                        if key == "auc":
                            vals = [r["detection"]["auc"] for r in runs[m].values() if "detection" in r]
                        else:
                            vals = []
                            for s, r in runs[m].items():
                                strat = "lowest"
                                f = "10" if "10" in r.get("curves", {}).get(strat, {}) else None
                                if f is None or s not in rnd:
                                    continue
                                rv = rnd[s].get("curves", {}).get("random", {}).get(f)
                                if rv is not None:
                                    vals.append(sign(r) * (r["curves"][strat][f] - rv))
                        if vals:
                            xs, mn, rng = per_m[m]
                            xs.append(xi)
                            mn.append(np.mean(vals))
                            rng.append((np.min(vals), np.max(vals)))
                            rows_out.append({"param": p, "value": v, "method": m, "quantity": key,
                                             "mean": float(np.mean(vals)), "min": float(np.min(vals)),
                                             "max": float(np.max(vals)), "n": len(vals)})
            for m, (xs, mn, rng) in per_m.items():
                c = COLORS.get(m, INK2)
                lo, hi = zip(*rng)
                if len(xs) > 1:
                    ax.fill_between(xs, lo, hi, color=c, alpha=0.12, lw=0)
                ax.plot(xs, mn, color=c, lw=2, marker="o", ms=4.5, mfc=c, mec=SURFACE, mew=1)
            ax.axhline(0.5 if key == "auc" else 0.0, color=MUTED, ls="--", lw=1.1)
            ax.set_xticks(range(len(values)), [str(v) for v in values], fontsize=8.5)
            ax.set_xlabel(p)
            ax.set_ylabel("detection AUC" if key == "auc" else "Δ vs random @10 % (better > 0)")
            if row == 0:
                ax.set_title(p)
            if col == 0 and row == 0:
                legend(ax, [m for m in ORDER if m in per_m], loc="lower left")
    finish(fig, os.path.join(outdir, "7_sensitivity.png"), "Sensitivity sweep (one factor at a time)",
           note="Line = mean over seeds, band = min..max over seeds. Top: detection AUC of corrupted labels (0.5 = random). "
                "Bottom: gain of removing the 10 % lowest-valued points over random removal.")
    return rows_out


# ----------------------------------------------------------------------------- tables
def write_summary(data, studies, outdir, paired_rows, sens_rows):
    rows = []
    for st in studies:
        for ds in datasets_in(data.get(st, {})):
            runs = data[st][ds]
            base = [r["baseline"] for r in runs.get("_baseline", {}).values()]
            for m in methods_in(runs) + (["random"] if "random" in runs else []):
                rs = list(runs[m].values())
                strat = "random" if m == "random" else "lowest"
                at10 = [r["curves"].get(strat, {}).get("10") for r in rs]
                at10 = [v for v in at10 if v is not None]
                auc = [r["detection"]["auc"] for r in rs if "detection" in r]
                tval = [r["timing"].get("values_s", 0) for r in rs]
                rows.append({"study": st, "dataset": ds, "method": m, "seeds": len(rs), "metric": rs[0]["metric"],
                             "full_data": float(np.mean(base)) if base else float("nan"),
                             "at10_mean": float(np.mean(at10)) if at10 else float("nan"),
                             "at10_std": float(np.std(at10, ddof=1)) if len(at10) > 1 else float("nan"),
                             "det_auc": float(np.mean(auc)) if auc else float("nan"),
                             "det_auc_std": float(np.std(auc, ddof=1)) if len(auc) > 1 else float("nan"),
                             "values_s": float(np.mean(tval)) if tval else float("nan")})
    if not rows:
        return
    with open(os.path.join(outdir, "summary.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    fmt = lambda m, s: "—" if m != m else (f"{m:.4f}" + (f" ± {s:.4f}" if s == s else ""))
    lines = ["| study | dataset | method | seeds | full data | metric @10 % removed | detection AUC | values, s |",
             "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['study']} | {r['dataset']} | {LABELS.get(r['method'], r['method'])} | {r['seeds']} | "
                     f"{fmt(r['full_data'], float('nan'))} | {fmt(r['at10_mean'], r['at10_std'])} | "
                     f"{fmt(r['det_auc'], r['det_auc_std'])} | {r['values_s']:.1f} |")
    if paired_rows:
        lines += ["", "Paired vs random removal at 10 % (lowest first; > 0 = better than random):", "",
                  "| data | dataset | method | n | Δ mean | 95 % bootstrap CI | p (t-test) | seeds better |",
                  "|---|---|---|---|---|---|---|---|"]
        for r in paired_rows:
            lines.append(f"| {r['block']} | {r['dataset']} | {LABELS.get(r['method'], r['method'])} | {r['n']} | "
                         f"{r['mean']:+.4f} | [{r['ci_lo']:+.4f}, {r['ci_hi']:+.4f}] | {r['p_t']:.3f} | "
                         f"{r['n_better']}/{r['n']} |")
    if sens_rows:
        with open(os.path.join(outdir, "sensitivity.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(sens_rows[0]))
            w.writeheader()
            w.writerows(sens_rows)
    text = "\n".join(lines)
    with open(os.path.join(outdir, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print("\n" + text + "\n")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="results")
    p.add_argument("--out", default="assets")
    p.add_argument("--clean", default="clean", help="name of the clean-data study")
    p.add_argument("--noise", default="noise10", help="name of the corrupted-label study")
    a = p.parse_args()
    data = load(a.root)
    if not data:
        raise SystemExit(f"no results under {a.root}")
    os.makedirs(a.out, exist_ok=True)
    sc, sn = data.get(a.clean, {}), data.get(a.noise, {})
    fig_curves(sc, ("lowest", "highest"), "1_removal_curves.png", "Removal curves on clean data", a.out,
               note="Line = mean over seeds, band = min..max over seeds; 0 % = full-data model of the same seed. "
                    "Grey = random removal, dashed = full data.")
    fig_curves(sn, ("lowest",), "2_noise_removal.png", "Removal curves with 10 % corrupted labels", a.out,
               note="Removing the lowest-valued points first. A good method removes the corrupted points and the metric "
                    "should go up (or the error down) relative to the dashed full-data line.")
    fig_detection(sn, a.out)
    fig_found(sn, a.out)
    paired = fig_paired(sc, sn, a.out)
    fig_removal_auc(sc, a.out)
    sens = fig_sensitivity(data, a.out)
    import plot_extensions
    plot_extensions.make_all(sys.modules[__name__], data, a.out)
    write_summary(data, [s for s in (a.clean, a.noise) if s in data] + plot_extensions.ext_studies(data), a.out,
                  paired, sens)


if __name__ == "__main__":
    main()
