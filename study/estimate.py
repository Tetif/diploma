"""Runtime estimate for the main study and the sweep from a timing probe (``run_study.py probe``).

Model: time(values) ~ t_probe * (n / n_probe) ** alpha_method (alpha fitted on adult n=300/600,
default 1), time(retrain) likewise; TMC-Shapley scales with the number of permutations.
It is a rough estimate (+-50 %); n_jobs / threads of the real run should match the probe.
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np

from study import io
from study.config import (MAIN_DATASETS, MAIN_SEEDS, MAIN_STUDIES, SWEEP_DATASET, SWEEP_SEEDS, sweep_specs,
                          methods_for)
from study.data import make_split


def _probe(root):
    """-> t[(dataset, method)] = list of (n, values_s, retrain_s, tmc_permutations)."""
    t = defaultdict(list)
    for r in io.iter_results(root):
        if not r['study'].startswith('probe-') or r.get('status') not in ('ok', 'skipped'):
            continue
        tm = r.get('timing', {})
        n_retr = sum(len(c) for c in r.get('curves', {}).values()) or 1
        t[(r['dataset'], r['method'])].append(
            (r['n_train'], tm.get('values_s', 0.0), tm.get('curves_s', 0.0) / n_retr,
             r.get('spec', {}).get('tmc_permutations', 10), tm.get('baseline_s', 0.0), r.get('status')))
    return t


def _alpha(pts, idx):
    pts = sorted({p[0]: p for p in pts}.values())
    if len(pts) < 2 or pts[0][idx] <= 0 or pts[-1][idx] <= 0:
        return None
    return float(np.log(pts[-1][idx] / pts[0][idx]) / np.log(pts[-1][0] / pts[0][0]))


def _n_train(ds, sample_scale=1.0):
    if ds.n_train is not None:
        return int(round(ds.n_train * sample_scale / 0.8 * 0.8))
    return len(make_split(ds.name, 0, None, ds.max_holdout).X_train)


def estimate(root, log=print, n_jobs=None):
    """``n_jobs``: planned --n-jobs of the real run; LOO/TMC (parallel refits) are scaled by
    (probe_jobs / n_jobs) ** 0.75 - an assumption, not a measurement."""
    t = _probe(root)
    probe_jobs = max((r.get('n_jobs') or 1 for r in io.iter_results(root) if r['study'].startswith('probe-')), default=1)
    par = (probe_jobs / n_jobs) ** 0.75 if n_jobs else 1.0
    log(f'probe ran with n_jobs={probe_jobs}; estimating for n_jobs={n_jobs or probe_jobs} (LOO/TMC x{par:.2f})')
    if not t:
        log('no probe results - run `python run_study.py probe` first')
        return
    alphas = {}
    for (d, m), pts in t.items():
        if d == 'adult':
            av, ar = _alpha(pts, 1), _alpha(pts, 2)
            # clamp: the probe is noisy (early stopping), never assume cost falls with n
            alphas[m] = (float(np.clip(av if av is not None else 1.0, 0.0, 2.0)),
                         float(np.clip(ar if ar is not None else 1.0, 0.5, 1.5)))
    log('scaling exponents from adult probe (values, retrain): ' +
        ', '.join(f'{m}=({a:.2f},{b:.2f})' for m, (a, b) in sorted(alphas.items())))

    def cost(dataset, method, n, n_retrain, spec):
        pts = t.get((dataset, method)) or t.get(('adult', method))
        if not pts:
            return None
        n0, v0, r0, perms0, b0, status = max(pts, key=lambda p: p[0])
        if status == 'skipped':
            return 0.0
        av, ar = alphas.get(method, (1.0, 1.0))
        v = v0 * (n / n0) ** av
        if method == 'TMCShapley':
            v *= spec.tmc_permutations / max(perms0, 1)
        if method == 'LOO':
            v *= spec.valuation_epochs / 100.0
        if method in ('LOO', 'TMCShapley'):
            v *= par
        r = r0 * (n / n0) ** ar * n_retrain
        if spec.fit_mode == 'overfit':
            r *= 3
        return v + r + b0 * (n / n0)

    total_main = 0.0
    rows = []
    for ds in MAIN_DATASETS.values():
        n = _n_train(ds)
        for name, spec in MAIN_STUDIES.items():
            n_retr = len(spec.fracs) * len(spec.strategies)
            for m in methods_for(spec.model_type, '', list(ds.methods)):
                c = cost(ds.name, m, n, len(spec.fracs) if m == 'random' else n_retr, spec)
                if c is None:
                    rows.append(f'  {ds.name:<10} {name:<8} {m:<15} n={n:<5} (no probe)')
                    continue
                c *= len(MAIN_SEEDS)
                total_main += c
                rows.append(f'  {ds.name:<10} {name:<8} {m:<15} n={n:<5} {c / 60:7.1f} min ({len(MAIN_SEEDS)} seeds)')
    for r in rows:
        log(r)
    log(f'MAIN study total: {total_main / 3600:.1f} h')

    total_sweep = 0.0
    for param, value, spec, methods in sweep_specs():
        n = _n_train(SWEEP_DATASET, spec.sample_scale)
        n_retr = len(spec.fracs) * len(spec.strategies)
        c = 0.0
        for m in methods_for(spec.model_type, '', methods):
            ci = cost(SWEEP_DATASET.name, m, n, len(spec.fracs) if m == 'random' else n_retr, spec)
            c += ci or 0.0
        c *= len(SWEEP_SEEDS)
        total_sweep += c
        log(f'  sweep {param}={value!s:<9} n={n:<5} {c / 60:7.1f} min')
    log(f'SWEEP total: {total_sweep / 3600:.1f} h;  MAIN + SWEEP: {(total_main + total_sweep) / 3600:.1f} h')
