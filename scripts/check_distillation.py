"""Sanity check of teacher -> student distillation (DistilledModelWrapper).

For every dataset (n_train 1500, seed 0 split as in the study) and every tree teacher:
  teacher alone, distilled student (teacher trained inside the wrapper), MLP trained directly on the labels.
Prints holdout metrics, student-teacher agreement, the student's train loss / epochs and the share of
"soft" teacher targets (a hard-label teacher gives 0/1 targets only).

    python scripts/check_distillation.py [--datasets adult covertype] [--teachers lightgbm catboost]
"""
import argparse
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--datasets', nargs='*', default=['adult', 'covertype', 'housing', 'wine'])
    ap.add_argument('--teachers', nargs='*', default=['lightgbm', 'xgboost', 'catboost', 'random_forest'])
    ap.add_argument('--n-train', type=int, default=1500)
    ap.add_argument('--seed', type=int, default=0)
    a = ap.parse_args()
    for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
        os.environ.setdefault(v, '2')
    os.environ.setdefault('DIPLOMA_DEVICE', 'cpu')
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    import warnings
    warnings.filterwarnings('ignore')
    import numpy as np
    import torch
    torch.set_num_threads(2)
    import experiments.logger as L
    L.debug_print = lambda *x, **k: None
    from study.config import EXT_DATASETS, RunSpec
    from study.data import make_split
    from study.protocol import Trainer, distill_diagnostics

    print(f"{'dataset':<10} {'teacher':<14} {'metric':<9} {'teacher':>9} {'student':>9} {'direct MLP':>10} "
          f"{'fidelity':>9} {'soft tgt':>8} {'s':>5}")
    for dname in a.datasets:
        ds = EXT_DATASETS[dname]
        split = make_split(dname, a.seed, a.n_train if ds.n_train else None, ds.max_holdout)
        seed = 42 + 1000 * a.seed
        mlp = Trainer(split, RunSpec('chk'), seed)
        m_direct = mlp.fit(split.X_train, split.y_train, seed)[0]
        for t in a.teachers:
            t0 = time.time()
            tr_t = Trainer(split, RunSpec('chk', model_type=t), seed)
            m_teacher_alone = tr_t.fit(split.X_train, split.y_train, seed)[0]
            tr = Trainer(split, RunSpec('chk', model_type=t, distill=True), seed)
            m_student, model, ysc = tr.fit(split.X_train, split.y_train, seed)
            diag = distill_diagnostics(tr, model, ysc)
            Xt = tr.pre.transform(split.X_train)
            Xt = Xt.toarray() if hasattr(Xt, 'toarray') else np.asarray(Xt)
            tg = np.asarray(model._teacher_targets(Xt), float)
            soft = float(np.mean((tg > 1e-3) & (tg < 1 - 1e-3))) if split.is_classification else float('nan')
            print(f"{dname:<10} {t:<14} {tr.metric:<9} {diag['teacher_metric']:9.4f} {m_student:9.4f} "
                  f"{m_direct:10.4f} {diag['fidelity']:9.3f} {soft:8.2f} {time.time() - t0:5.0f}"
                  f"   (teacher alone {m_teacher_alone:.4f})", flush=True)


if __name__ == '__main__':
    main()
