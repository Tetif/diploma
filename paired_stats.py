#!/usr/bin/env python3
"""
Paired statistics vs random removal for every study / dataset / method / removal fraction.

For each seed the method and random removal share the split and the init seed, so the per-seed
difference is a paired sample. Reports mean difference (> 0 = better than random, metric direction
taken into account), bootstrap 95 % CI, paired t-test p-value and how many seeds were better.
Also: detection AUC vs 0.5 (one-sample t-test) for the corrupted-label studies.

  python paired_stats.py                         # results/ -> assets/paired_stats.md
  python paired_stats.py --root results/pilot --out results/pilot/plots
"""
import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from study.summary import load, paired_test, removal_auc, sign  # noqa: E402


def _auc_by_seed(data, study, ds, m):
    return {s: r["detection"]["auc"] for s, r in data.get(study, {}).get(ds, {}).get(m, {}).items()
            if "detection" in r}


def cross_study(data):
    """Detection AUC of the same method in two studies, paired by seed (same split, same corrupted labels)."""
    pairs = []   # (question, study A, study B, methods)
    for mo in ("lightgbm", "xgboost", "catboost", "random_forest"):
        pairs.append((f"{mo} - MLP", f"models-{mo}-noise10", "noise10", ["LOO", "LossHigh"]))
    for t in ("lightgbm", "catboost"):
        pairs.append((f"student of {t} - MLP direct", f"distill-{t}-noise10", "noise10",
                      ["Influence", "LissaInfluence", "LossHigh"]))
    from study.config import DAMPINGS
    for d in DAMPINGS:
        pairs.append((f"linear - MLP (damping {d:g})", f"damp-linear-{d:g}", f"damp-mlp-{d:g}",
                      ["Influence", "LissaInfluence"]))
    for pct in (5, 10, 20):
        pairs.append((f"systematic - random noise {pct} %", f"sysnoise{pct}", f"noise{pct}",
                      ["KNNShapley", "DataOOB", "Influence", "LissaInfluence", "LossHigh"]))
    out = ["", "# Cross-study comparisons (detection AUC, paired by seed)", "",
           "| comparison | dataset | method | n | AUC A | AUC B | A − B, 95 % CI | p |", "|---|---|---|---|---|---|---|---|"]
    n_rows = 0
    for q, sa, sb, methods in pairs:
        if sa not in data or sb not in data:
            continue
        for ds in sorted(set(data[sa]) & set(data[sb])):
            for m in methods:
                A, B = _auc_by_seed(data, sa, ds, m), _auc_by_seed(data, sb, ds, m)
                common = sorted(set(A) & set(B))
                if not common:
                    continue
                t = paired_test([A[s] - B[s] for s in common])
                out.append(f"| {q} | {ds} | {m} | {t['n']} | {np.mean([A[s] for s in common]):.3f} | "
                           f"{np.mean([B[s] for s in common]):.3f} | {t['mean']:+.3f} [{t['ci_lo']:+.3f}, "
                           f"{t['ci_hi']:+.3f}] | {t['p_t']:.3f} |")
                n_rows += 1
    return "\n".join(out) + "\n" if n_rows else ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="results")
    p.add_argument("--out", default="assets")
    a = p.parse_args()
    data = load(a.root)
    lines = ["| study | dataset | method | strategy | removed | n | Δ vs random | 95 % CI | p | better |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    det = ["| study | dataset | method | n | AUC | AUC − 0.5, 95 % CI | p (vs 0.5) |", "|---|---|---|---|---|---|---|"]
    for st in sorted(data):
        for ds in sorted(data[st]):
            runs = data[st][ds]
            rnd = runs.get("random", {})
            for m in sorted(set(runs) - {"random", "_baseline"}):
                for strat in ("lowest", "highest"):
                    fr = set()
                    for r in runs[m].values():
                        fr |= set(r.get("curves", {}).get(strat, {}))
                    for f in sorted(fr, key=float) + (["auc"] if fr else []):
                        d = []
                        for s, r in runs[m].items():
                            if s not in rnd or strat not in r.get("curves", {}):
                                continue
                            if f == "auc":
                                v = removal_auc(r, strat, r["baseline"])
                                rv = removal_auc(rnd[s], "random", rnd[s]["baseline"])
                                if v is not None and rv is not None:
                                    d.append(v - rv)      # already signed
                            else:
                                v = r["curves"][strat].get(f)
                                rv = rnd[s].get("curves", {}).get("random", {}).get(f)
                                if v is not None and rv is not None:
                                    d.append(sign(r) * (v - rv))
                        if not d:
                            continue
                        t = paired_test(d)
                        lines.append(f"| {st} | {ds} | {m} | {strat} | {f if f == 'auc' else f + ' %'} | {t['n']} | "
                                     f"{t['mean']:+.4f} | [{t['ci_lo']:+.4f}, {t['ci_hi']:+.4f}] | {t['p_t']:.3f} | "
                                     f"{t['n_better']}/{t['n']} |")
                aucs = [r["detection"]["auc"] for r in runs[m].values() if "detection" in r]
                if aucs:
                    t = paired_test(np.array(aucs) - 0.5)
                    det.append(f"| {st} | {ds} | {m} | {t['n']} | {np.mean(aucs):.3f} | "
                               f"[{t['ci_lo']:+.3f}, {t['ci_hi']:+.3f}] | {t['p_t']:.3f} |")
    text = ("# Paired comparison with random removal\n\n'removed = auc' is the mean signed gain over the whole removal "
            "grid (relative to the full-data model).\n\n" + "\n".join(lines) +
            "\n\n# Detection of corrupted points\n\n" + "\n".join(det) + "\n" + cross_study(data))
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, "paired_stats.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)
    print("wrote", path)


if __name__ == "__main__":
    main()
