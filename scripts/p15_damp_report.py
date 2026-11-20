"""[P15] DirectInfluence on the MLP vs damping: detection AUC and paired removal gain vs random.

Reads results/{noise10, damp-mlp-*}/<dataset>/{Influence,random}/seed*/results.json (seeds 0-2) and prints a
markdown table. Cheap (no training): python scripts/p15_damp_report.py
"""
import glob
import json
import os
import sys

import numpy as np

ROOT = sys.argv[1] if len(sys.argv) > 1 else 'results'
DS = ['wine', 'housing', 'adult', 'covertype']
STUDIES = [('noise10 (default)', 'noise10'), ('1e-06', 'damp-mlp-1e-06'), ('1e-04', 'damp-mlp-0.0001'),
           ('1e-02', 'damp-mlp-0.01'), ('0.1', 'damp-mlp-0.1'), ('1', 'damp-mlp-1')]


def load(st, ds, m, seed):
    f = os.path.join(ROOT, st, ds, m, f'seed{seed}', 'results.json')
    if not os.path.exists(f):
        return None
    r = json.load(open(f, encoding='utf-8'))
    return r if r.get('status') == 'ok' else None


def gain(r, rnd):
    """mean signed gain of lowest-value removal over random removal across the fraction grid."""
    sgn = 1.0 if r.get('higher_is_better', True) else -1.0
    lo, ra = r['curves'].get('lowest', {}), rnd['curves'].get('random', {})
    ks = [k for k in lo if k in ra]
    return sgn * float(np.mean([lo[k] - ra[k] for k in ks])) if ks else np.nan


print('| damping | ' + ' | '.join(f'{d} AUC | {d} Δ' for d in DS) + ' |')
print('|---|' + '---|---|' * len(DS))
for label, st in STUDIES:
    cells = []
    for ds in DS:
        aucs, gains = [], []
        for seed in (0, 1, 2):
            r, rnd = load(st, ds, 'Influence', seed), load(st, ds, 'random', seed)
            if r is None:
                continue
            aucs.append(r['detection']['auc'])
            if rnd is not None:
                gains.append(gain(r, rnd))
        f = (lambda v: f'{v:+.0f}') if ds == 'housing' else (lambda v: f'{v:+.4f}')
        cells += [f'{np.mean(aucs):.3f} (n={len(aucs)})' if aucs else '—',
                  f(np.nanmean(gains)) if gains else '—']
    print(f'| {label} | ' + ' | '.join(cells) + ' |')
