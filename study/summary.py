"""Aggregation of results.json files: per-method means over seeds, paired comparison with random.

Sign convention for deltas: positive = better than the reference (metric direction is taken into
account, so for MAE a *lower* error gives a positive delta).
"""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

import numpy as np

from study import io


def load(root, study: Optional[str] = None) -> Dict:
    """-> data[study][dataset][method][seed] = result dict (status 'ok' only; '_baseline' included)."""
    data: Dict = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for r in io.iter_results(root):
        if r.get('status') != 'ok' or (study and r['study'] != study):
            continue
        data[r['study']][r['dataset']][r['method']][int(r['seed'])] = r
    return data


def sign(r: dict) -> float:
    return 1.0 if r.get('higher_is_better', True) else -1.0


def curve_value(r: dict, strategy: str, frac) -> Optional[float]:
    c = r.get('curves', {}).get(strategy, {})
    v = c.get(str(frac))
    return None if v is None else float(v)


def paired_test(d: List[float]) -> dict:
    """Mean / std of paired differences, paired t-test and bootstrap 95% CI of the mean."""
    d = np.asarray(d, float)
    out = {'n': int(d.size), 'mean': float(d.mean()) if d.size else float('nan'),
           'std': float(d.std(ddof=1)) if d.size > 1 else float('nan'),
           'p_t': float('nan'), 'ci_lo': float('nan'), 'ci_hi': float('nan'), 'n_better': int((d > 0).sum())}
    if d.size >= 2:
        from scipy import stats
        if np.allclose(d, d[0]):
            out['p_t'] = 0.0 if d[0] != 0 else 1.0
        else:
            out['p_t'] = float(stats.ttest_1samp(d, 0.0).pvalue)
        rng = np.random.default_rng(0)
        boots = rng.choice(d, size=(10_000, d.size), replace=True).mean(1)
        out['ci_lo'], out['ci_hi'] = (float(x) for x in np.percentile(boots, [2.5, 97.5]))
    return out


def removal_auc(r: dict, strategy: str, base: float) -> Optional[float]:
    """Mean signed gain over the removal grid relative to the full-data model (area / width)."""
    c = r.get('curves', {}).get(strategy)
    if not c:
        return None
    fr = sorted(c, key=float)
    xs = [0.0] + [float(f) for f in fr]
    ys = [0.0] + [sign(r) * (float(c[f]) - base) for f in fr]
    return float(np.trapezoid(ys, xs) / xs[-1]) if hasattr(np, 'trapezoid') else float(np.trapz(ys, xs) / xs[-1])


def block_summary(data: Dict, study: str, dataset: str, frac=10, strategy: str = 'lowest') -> dict:
    """Compact per-method numbers for one (study, dataset) - used by the webhook and summary.md."""
    runs = data.get(study, {}).get(dataset, {})
    rnd = runs.get('random', {})
    base = runs.get('_baseline', {})
    out = {'random_baseline': None, 'full_data_baseline': None, 'methods': []}
    if base:
        b = [r['baseline'] for r in base.values()]
        out['full_data_baseline'] = {'mean': float(np.mean(b)), 'std': float(np.std(b)), 'n_seeds': len(b)}
    if rnd:
        rv = [curve_value(r, 'random', frac) for r in rnd.values()]
        rv = [v for v in rv if v is not None]
        if rv:
            out['random_baseline'] = {'frac': frac, 'mean': float(np.mean(rv)), 'std': float(np.std(rv)),
                                      'n_seeds': len(rv)}
    for m, seeds in sorted(runs.items()):
        if m in ('_baseline', 'random'):
            continue
        vals, deltas = [], []
        aucs = []
        metric = None
        for s, r in seeds.items():
            metric = r.get('metric')
            v = curve_value(r, strategy, frac)
            if v is not None:
                vals.append(v)
                if s in rnd and curve_value(rnd[s], 'random', frac) is not None:
                    deltas.append(sign(r) * (v - curve_value(rnd[s], 'random', frac)))
            if 'detection' in r:
                aucs.append(r['detection']['auc'])
        entry = {'name': m, 'metric': f'{metric}@{frac}% {strategy}-first', 'n_seeds': len(vals),
                 'mean': float(np.mean(vals)) if vals else None, 'std': float(np.std(vals)) if vals else None}
        if deltas:
            t = paired_test(deltas)
            entry.update(delta_vs_random=t['mean'], p_value=None if t['p_t'] != t['p_t'] else t['p_t'])
        if aucs:
            entry.update(detection_auc=float(np.mean(aucs)), detection_auc_std=float(np.std(aucs)))
        out['methods'].append(entry)
    return out


def failed_methods(root, study: str, dataset: Optional[str] = None) -> List[dict]:
    out = []
    for r in io.iter_results(root):
        if r.get('status') == 'failed' and r['study'] == study and (dataset is None or r['dataset'] == dataset):
            out.append({'method': r['method'], 'dataset': r['dataset'], 'seed': r['seed'],
                        'error': (r.get('error') or '')[:300]})
    return out
