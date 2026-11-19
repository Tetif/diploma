"""Figures 8-13 of plot_results.py: the secondary studies of `run_study.py ext`.

  8_models.png             MLP vs LightGBM / XGBoost / CatBoost / RandomForest: full-data metric, detection AUC
                           of 10 % corrupted labels, gain over random removal on clean data
  9_convex_damping.png     influence on logistic / linear regression (convex) vs the MLP, damping 1e-6 .. 1
  10_distillation.png      tree teacher vs distilled MLP student vs MLP trained directly; values via the student
  11_transfer.png          values from a source model, removal retrained with a target model (mean over seeds)
  12_systematic_noise.png  random vs systematic (class-pair / subgroup) corruption at 5 / 10 / 20 %
  13_cost_quality.png      wall time of the values vs detection AUC, Pareto front; cost.csv (+ peak RAM)
Called from plot_results.main(); P is the plot_results module (style, colours, helpers).
"""
import csv
import os
from collections import defaultdict

import numpy as np

MODEL_ORDER = ["pytorch", "lightgbm", "xgboost", "catboost", "random_forest"]
MODEL_LABELS = {"pytorch": "MLP", "lightgbm": "LightGBM", "xgboost": "XGBoost", "catboost": "CatBoost",
                "random_forest": "RandomForest", "linear": "linear", "distill-lightgbm": "LGBM→MLP",
                "distill-catboost": "CatBoost→MLP", "any": "any"}
MODEL_MARKERS = {"pytorch": "o", "lightgbm": "s", "xgboost": "^", "catboost": "D", "random_forest": "v",
                 "distill-lightgbm": "P", "distill-catboost": "X", "linear": "*"}


def _model_study(model, task):
    return task if model == "pytorch" else f"models-{model}-{task}"


def _at(r, strat, frac="10"):
    v = r.get("curves", {}).get(strat, {}).get(frac)
    return None if v is None else float(v)


def _delta(runs, m, strat="lowest", frac="10"):
    """Per-seed signed gain of method m over the same study's random removal at frac %."""
    rnd = runs.get("random", {})
    out = []
    for s, r in runs.get(m, {}).items():
        v = _at(r, strat, frac)
        rv = _at(rnd[s], "random", frac) if s in rnd else None
        if v is not None and rv is not None:
            out.append((1.0 if r.get("higher_is_better", True) else -1.0) * (v - rv))
    return out


def _aucs(runs, m):
    return [r["detection"]["auc"] for r in runs.get(m, {}).values() if "detection" in r]


def _datasets(P, data, studies):
    ds = set()
    for st in studies:
        ds |= set(data.get(st, {}))
    return [d for d in P.DS_ORDER if d in ds] + sorted(ds - set(P.DS_ORDER))


# ----------------------------------------------------------------------------- 8 models
def fig_models(P, data, outdir):
    models = [m for m in MODEL_ORDER if _model_study(m, "noise10") in data or _model_study(m, "clean") in data]
    if len([m for m in models if m != "pytorch"]) == 0:
        return
    dss = _datasets(P, data, [_model_study(m, t) for m in models for t in ("clean", "noise10")])
    fig, axes = P.grid(len(dss), rows=3, w=5.6, h=3.4)
    methods_seen = set()
    for col, ds in enumerate(dss):
        ax0, ax1, ax2 = axes[0][col], axes[1][col], axes[2][col]
        r0 = None
        for i, mo in enumerate(models):
            runs = data.get(_model_study(mo, "clean"), {}).get(ds, {}) or \
                data.get(_model_study(mo, "noise10"), {}).get(ds, {})
            b = [r["baseline"] for r in runs.get("_baseline", {}).values()]
            if b:
                P.dots(ax0, i, b, P.INK2)
                r0 = r0 or P.any_run(runs)
            for k, (task, ax, getter) in enumerate((("noise10", ax1, _aucs), ("clean", ax2, _delta))):
                runs_t = data.get(_model_study(mo, task), {}).get(ds, {})
                ms = [m for m in P.methods_in(runs_t)]
                width = 0.8 / max(len(ms), 1)
                for j, m in enumerate(ms):
                    vals = getter(runs_t, m)
                    if not vals:
                        continue
                    methods_seen.add(m)
                    x = i - 0.4 + width * (j + 0.5)
                    c = P.COLORS.get(m, P.INK2)
                    ax.scatter(np.full(len(vals), x), vals, s=14, color=c, alpha=0.55, lw=0, zorder=3)
                    ax.scatter([x], [np.mean(vals)], s=46, color=c, edgecolor=P.INK, lw=0.8, zorder=4)
        ticks = [MODEL_LABELS.get(m, m) for m in models]
        for ax in (ax0, ax1, ax2):
            ax.set_xticks(range(len(models)), ticks, fontsize=8.5)
            ax.grid(axis="x", visible=False)
        ax0.set_title(ds)
        if r0:
            ax0.set_ylabel(P.metric_label(r0).replace(" on holdout", "\non holdout"), fontsize=9)
        ax1.axhline(0.5, color=P.MUTED, ls="--", lw=1.1)
        ax1.set_ylabel("detection AUC\n(10 % corrupted)", fontsize=9)
        ax2.axhline(0.0, color=P.MUTED, ls="--", lw=1.1)
        ax2.set_ylabel("Δ vs random @10 %\nclean data (better > 0)", fontsize=9)
    P.legend(axes[1][-1], [m for m in P.ORDER + ["CatBoostLFC"] if m in methods_seen], outside=True)
    P.finish(fig, os.path.join(outdir, "8_models.png"), "Does the model matter? MLP vs tree ensembles",
             note="Top: full-data holdout metric, dot = seed, tick = mean. Middle: AUC of finding the 10 % corrupted "
                  "labels by low value (0.5 = random). Bottom: gain of removing the 10 % lowest-valued points over "
                  "random removal on clean data. Small dots = seeds, large dot = mean. MLP = main study.")


# ----------------------------------------------------------------------------- 9 convex vs MLP
def fig_convex(P, data, outdir):
    from study.config import DAMPINGS
    arches = [a for a in ("linear", "mlp") if any(s.startswith(f"damp-{a}-") for s in data)]
    if not arches:
        return
    dss = _datasets(P, data, [s for s in data if s.startswith("damp-")])
    fig, axes = P.grid(len(dss), rows=1, w=5.2, h=4.0)
    xs = np.log10(DAMPINGS)
    for ax, ds in zip(axes[0], dss):
        sub = []
        for arch in arches:
            ls = "-" if arch == "linear" else "--"
            for m in ("Influence", "LissaInfluence"):
                mean, lo, hi, xx = [], [], [], []
                for x, d in zip(xs, DAMPINGS):
                    v = _aucs(data.get(f"damp-{arch}-{d:g}", {}).get(ds, {}), m)
                    if v:
                        xx.append(x), mean.append(np.mean(v)), lo.append(min(v)), hi.append(max(v))
                if xx:
                    c = P.COLORS[m]
                    if len(xx) > 1:
                        ax.fill_between(xx, lo, hi, color=c, alpha=0.10, lw=0)
                    ax.plot(xx, mean, color=c, ls=ls, lw=2, marker="o", ms=4.5, mfc=c, mec=P.SURFACE)
            lh = [a for d in DAMPINGS for a in _aucs(data.get(f"damp-{arch}-{d:g}", {}).get(ds, {}), "LossHigh")]
            if lh:
                ax.axhline(np.mean(lh), color=P.COLORS["LossHigh"], ls=ls, lw=1.2, alpha=0.8)
            b = [r["baseline"] for d in DAMPINGS[:1]
                 for r in data.get(f"damp-{arch}-{d:g}", {}).get(ds, {}).get("_baseline", {}).values()]
            if b:
                sub.append(f"{arch}: {np.mean(b):.3g}")
        ax.axhline(0.5, color=P.MUTED, ls=":", lw=1.1)
        ax.set_xticks(xs, [f"{d:g}" for d in DAMPINGS])
        ax.set_xlabel("damping λ (H + λI)")
        ax.set_ylabel("detection AUC (10 % corrupted)")
        ax.set_title(f"{ds}\n" + ", ".join(sub), fontsize=10)
        ax.set_ylim(0.0, 1.02)
    import matplotlib.pyplot as plt
    extra = [plt.Line2D([0], [0], color=P.INK2, lw=2, ls="-", label="convex (logistic / linear)"),
             plt.Line2D([0], [0], color=P.INK2, lw=2, ls="--", label="MLP"),
             plt.Line2D([0], [0], color=P.COLORS["LossHigh"], lw=1.2, label="high loss (reference)")]
    P.legend(axes[0][-1], ["Influence", "LissaInfluence"], extra, outside=True)
    P.finish(fig, os.path.join(outdir, "9_convex_damping.png"),
             "Influence functions on a convex model vs the MLP, as a function of damping",
             note="Detection AUC of 10 % corrupted labels by low influence. Solid = logistic / linear regression "
                  "(convex loss: the influence approximation is exact up to damping), dashed = MLP. Band = min..max "
                  "over seeds. Subtitle: full-data holdout metric of each model. Horizontal lines = high-loss baseline.")


# ----------------------------------------------------------------------------- 10 distillation
def fig_distill(P, data, outdir):
    studies = sorted(s for s in data if s.startswith("distill-") and s.endswith("-noise10"))
    if not studies:
        return
    teachers = [s[len("distill-"):-len("-noise10")] for s in studies]
    dss = _datasets(P, data, studies)
    fig, axes = P.grid(len(dss), rows=3, w=5.6, h=3.4)
    for col, ds in enumerate(dss):
        ax0, ax1, ax2 = axes[0][col], axes[1][col], axes[2][col]
        labels, i = [], 0
        direct = data.get("noise10", {}).get(ds, {})
        r0 = None
        for t, st in zip(teachers, studies):
            base = data[st].get(ds, {}).get("_baseline", {})
            if not base:
                continue
            tm = [r.get("teacher_metric") for r in base.values() if r.get("teacher_metric") is not None]
            sm = [r["baseline"] for r in base.values()]
            fid = [r.get("fidelity") for r in base.values() if r.get("fidelity") is not None]
            r0 = r0 or next(iter(base.values()))
            P.dots(ax0, i, tm, "#2a78d6")
            P.dots(ax0, i + 1, sm, "#eb6834")
            labels += [f"{MODEL_LABELS.get(t, t)}\nteacher", f"student\nfid {np.mean(fid):.2f}" if fid else "student"]
            i += 2
        db = [r["baseline"] for r in direct.get("_baseline", {}).values()]
        if db:
            P.dots(ax0, i, db, P.INK2)
            labels.append("MLP\ndirect")
        ax0.set_xticks(range(len(labels)), labels, fontsize=8)
        ax0.grid(axis="x", visible=False)
        if r0:
            ax0.set_ylabel(P.metric_label(r0).replace(" on holdout", "\non holdout"), fontsize=9)
        ax0.set_title(ds)
        groups = [(MODEL_LABELS.get(f"distill-{t}", t), data[st].get(ds, {})) for t, st in zip(teachers, studies)]
        groups.append(("MLP direct", direct))
        for ax, getter, ref, lab in ((ax1, _aucs, 0.5, "detection AUC\n(10 % corrupted)"),
                                     (ax2, _delta, 0.0, "Δ vs random @10 %\n(better > 0)")):
            for gi, (gname, runs) in enumerate(groups):
                ms = [m for m in ("Influence", "LissaInfluence", "LossHigh") if m in runs]
                width = 0.8 / 3
                for j, m in enumerate(ms):
                    v = getter(runs, m)
                    if v:
                        x = gi - 0.4 + width * (j + 0.5)
                        c = P.COLORS[m]
                        ax.scatter(np.full(len(v), x), v, s=14, color=c, alpha=0.55, lw=0, zorder=3)
                        ax.scatter([x], [np.mean(v)], s=46, color=c, edgecolor=P.INK, lw=0.8, zorder=4)
            ax.axhline(ref, color=P.MUTED, ls="--", lw=1.1)
            ax.set_xticks(range(len(groups)), [g[0] for g in groups], fontsize=8.5)
            ax.grid(axis="x", visible=False)
            ax.set_ylabel(lab, fontsize=9)
    P.legend(axes[1][-1], ["Influence", "LissaInfluence", "LossHigh"], outside=True)
    P.finish(fig, os.path.join(outdir, "10_distillation.png"),
             "Distillation: tree teacher -> MLP student, and valuing the data through the student",
             note="Top: holdout metric of the teacher (blue), the distilled student (orange; fid = label agreement "
                  "or prediction correlation with the teacher) and an MLP trained directly on the labels (grey), all on "
                  "the 10 % corrupted training labels. Middle / bottom: detection AUC and gain over random removal "
                  "(retraining teacher + student) of influence / high loss computed on the student vs on the direct MLP.")


# ----------------------------------------------------------------------------- 11 transfer
def _fmt(v):
    a = abs(v)
    if a >= 1000:
        return f"{v / 1000:+.1f}k"
    if a >= 10:
        return f"{v:+.0f}"
    return f"{v:+.3f}" if a < 1 else f"{v:+.2f}"


def fig_transfer(P, data, outdir):
    from study.config import TRANSFER_SOURCES, TRANSFER_TARGETS
    targets = [t for t in TRANSFER_TARGETS if f"transfer-{t}" in data]
    if not targets:
        return None
    sources = [f"{sm}.{m}" for _, sm, m in TRANSFER_SOURCES]
    dss = _datasets(P, data, [f"transfer-{t}" for t in targets])
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(dss), figsize=(1.0 + 0.95 * len(targets) * len(dss) + 2.4 * len(dss),
                                                   0.42 * len(sources) + 2.0), squeeze=False)
    rows_out = []
    for ax, ds in zip(axes[0], dss):
        M = np.full((len(sources), len(targets)), np.nan)
        for j, t in enumerate(targets):
            runs = data[f"transfer-{t}"].get(ds, {})
            for i, s in enumerate(sources):
                d = _delta(runs, s)
                if d:
                    M[i, j] = np.mean(d)
                    rows_out.append({"dataset": ds, "source": s, "target": t, "delta_mean": float(np.mean(d)),
                                     "delta_std": float(np.std(d)), "n": len(d)})
        keep = ~np.all(np.isnan(M), axis=1)
        M, srcs = M[keep], [s for s, k in zip(sources, keep) if k]
        if not len(srcs):
            ax.set_visible(False)
            continue
        lim = np.nanmax(np.abs(M)) or 1.0
        ax.imshow(M, cmap="RdBu", vmin=-lim, vmax=lim, aspect="auto")
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i, j] == M[i, j]:
                    ax.text(j, i, _fmt(M[i, j]), ha="center", va="center", fontsize=7.5,
                            color="white" if abs(M[i, j]) > 0.6 * lim else P.INK)
        ax.set_xticks(range(len(targets)), [MODEL_LABELS.get(t, t) for t in targets], rotation=35, ha="right",
                      fontsize=8.5)
        ax.set_yticks(range(len(srcs)), [f"{MODEL_LABELS.get(s.split('.')[0], s.split('.')[0])}: "
                                          f"{P.LABELS.get(s.split('.', 1)[1], s.split('.', 1)[1])}" for s in srcs],
                      fontsize=8.5)
        ax.grid(False)
        ax.set_xlabel("target model (retrained after removal)")
        r0 = P.any_run(data[f"transfer-{targets[0]}"].get(ds, {}))
        ax.set_title(f"{ds}  (Δ {r0['metric'] if r0 else ''})")
    P.finish(fig, os.path.join(outdir, "11_transfer.png"),
             "Transfer: values from one model, cleaning evaluated with another",
             note="Cell = mean over seeds of (target metric after removing the 10 % lowest-valued points by the source's "
                  "values) minus (target metric after removing 10 % at random), sign flipped for error metrics: "
                  "blue / > 0 = the source's ranking helps the target. 10 % corrupted labels.")
    return rows_out


# ----------------------------------------------------------------------------- 12 systematic vs random noise
def fig_noise(P, data, outdir):
    rates = [5, 10, 20]
    have = [s for s in ("noise5", "noise20", "sysnoise5", "sysnoise10", "sysnoise20") if s in data]
    if not have:
        return
    name = {("random", 5): "noise5", ("random", 10): "noise10", ("random", 20): "noise20",
            ("systematic", 5): "sysnoise5", ("systematic", 10): "sysnoise10", ("systematic", 20): "sysnoise20"}
    dss = _datasets(P, data, have)
    fig, axes = P.grid(len(dss), rows=2, w=4.6, h=3.5)
    seen = set()
    for col, ds in enumerate(dss):
        for row, getter in enumerate((_aucs, _delta)):
            ax = axes[row][col]
            for kind, ls in (("random", "-"), ("systematic", "--")):
                per_m = defaultdict(lambda: ([], [], [], []))
                for rate in rates:
                    runs = data.get(name[(kind, rate)], {}).get(ds, {})
                    for m in P.methods_in(runs):
                        v = getter(runs, m)
                        if v:
                            xx, mn, lo, hi = per_m[m]
                            xx.append(rate), mn.append(np.mean(v)), lo.append(min(v)), hi.append(max(v))
                for m, (xx, mn, lo, hi) in per_m.items():
                    c = P.COLORS.get(m, P.INK2)
                    seen.add(m)
                    if len(xx) > 1:
                        ax.fill_between(xx, lo, hi, color=c, alpha=0.08, lw=0)
                    ax.plot(xx, mn, color=c, ls=ls, lw=2, marker="o" if kind == "random" else "s", ms=4.5,
                            mfc=c, mec=P.SURFACE)
            ax.axhline(0.5 if row == 0 else 0.0, color=P.MUTED, ls=":", lw=1.1)
            ax.set_xticks(rates, [f"{r} %" for r in rates])
            ax.set_xlabel("share of corrupted labels")
            ax.set_ylabel("detection AUC" if row == 0 else "Δ vs random @10 % (better > 0)")
            if row == 0:
                ax.set_title(ds)
    import matplotlib.pyplot as plt
    extra = [plt.Line2D([0], [0], color=P.INK2, lw=2, ls="-", marker="o", label="random flips / outliers"),
             plt.Line2D([0], [0], color=P.INK2, lw=2, ls="--", marker="s", label="systematic")]
    P.legend(axes[0][-1], [m for m in P.ORDER if m in seen], extra, outside=True)
    P.finish(fig, os.path.join(outdir, "12_systematic_noise.png"), "Random vs systematic label noise",
             note="Solid = random corruption (classification: random other class; regression: +-3 std outliers). "
                  "Dashed = systematic (classification: points of one class of the most confusable pair relabelled as "
                  "the other; regression: the segment with the largest values of the feature most correlated with y "
                  "gets y + 2 std). MLP, line = mean, band = min..max over seeds.")


# ----------------------------------------------------------------------------- 13 cost vs quality
def fig_cost(P, data, outdir):
    entries = []      # (dataset, model, method, time_s, peak_mb, auc, n)
    for st, model in [("noise10", "pytorch")] + [(f"models-{m}-noise10", m) for m in MODEL_ORDER[1:]] + \
            [(f"distill-{t}-noise10", f"distill-{t}") for t in ("lightgbm", "catboost")]:
        for ds, runs in data.get(st, {}).items():
            for m in P.methods_in(runs):
                rs = [r for r in runs[m].values() if "detection" in r]
                if not rs:
                    continue
                if model != "pytorch" and m in ("KNNShapley", "DataOOB"):
                    continue          # model-agnostic: identical values in every study, shown once (MLP)
                t = [r["timing"].get("values_s", 0.0) for r in rs]
                mem = [r["timing"].get("values_peak_rss_mb") for r in rs if r["timing"].get("values_peak_rss_mb")
                       is not None]
                entries.append((ds, model, m, float(np.mean(t)), float(np.mean(mem)) if mem else float("nan"),
                                float(np.mean([r["detection"]["auc"] for r in rs])), len(rs)))
    if not entries:
        return
    with open(os.path.join(outdir, "cost.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset", "model", "method", "values_s", "values_peak_rss_mb", "detection_auc", "seeds"])
        w.writerows(entries)
    dss = [d for d in P.DS_ORDER if any(e[0] == d for e in entries)]
    fig, axes = P.grid(len(dss), rows=1, w=5.0, h=4.2)
    import matplotlib.pyplot as plt
    for ax, ds in zip(axes[0], dss):
        es = [e for e in entries if e[0] == ds]
        for _, model, m, t, _, auc, _ in es:
            ax.scatter(max(t, 0.05), auc, s=60, marker=MODEL_MARKERS.get(model, "o"), color=P.COLORS.get(m, P.INK2),
                       edgecolor=P.INK, lw=0.6, zorder=3)
        pts = sorted(((max(e[3], 0.05), e[5]) for e in es))
        front, best = [], -1
        for t, a in pts:
            if a > best:
                front.append((t, a))
                best = a
        if front:
            fx, fy = zip(*front)
            ax.step(list(fx) + [max(p[0] for p in pts) * 1.5], list(fy) + [fy[-1]], where="post",
                    color=P.INK2, lw=1.2, ls="--", zorder=2)
        ax.set_xscale("log")
        ax.axhline(0.5, color=P.MUTED, ls=":", lw=1.1)
        ax.set_xlabel("time to compute the values, s (log)")
        ax.set_ylabel("detection AUC (10 % corrupted)")
        ax.set_title(ds)
    methods = sorted({e[2] for e in entries}, key=lambda m: (P.ORDER + ["CatBoostLFC"]).index(m)
                     if m in P.ORDER + ["CatBoostLFC"] else 99)
    models = [m for m in list(MODEL_MARKERS) if any(e[1] == m for e in entries)]
    extra = [plt.Line2D([0], [0], color=P.INK2, marker=MODEL_MARKERS[m], ls="", ms=7, label=MODEL_LABELS.get(m, m))
             for m in models] + [plt.Line2D([0], [0], color=P.INK2, ls="--", lw=1.2, label="Pareto front")]
    P.legend(axes[0][-1], methods, extra, outside=True)
    P.finish(fig, os.path.join(outdir, "13_cost_quality.png"), "Cost vs quality of the valuation methods",
             note="One point = method x model, mean over seeds (n_jobs as in the run; colour = method, marker = model). "
                  "Dashed = Pareto front (best detection AUC for a given time). Peak RAM per method: cost.csv.")


def make_all(P, data, outdir):
    fig_models(P, data, outdir)
    fig_convex(P, data, outdir)
    fig_distill(P, data, outdir)
    rows = fig_transfer(P, data, outdir)
    if rows:
        with open(os.path.join(outdir, "transfer.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    fig_noise(P, data, outdir)
    fig_cost(P, data, outdir)


def ext_studies(data):
    pref = ("models-", "damp-", "distill-", "noise5", "noise20", "sysnoise", "transfer-")
    return sorted(s for s in data if s.startswith(pref))
