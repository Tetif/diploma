"""Is the MLP trained long enough? Holdout metric vs epochs, legacy full-batch steps vs mini-batch epochs.

One "epoch" of train_and_evaluate is ONE full-batch gradient step (PyTorchModelWrapper.fit(..., epochs=1)),
so n_epochs=300 means 300 optimizer steps. Early stopping (patience 70) still applies.

    python scripts/check_mlp_epochs.py [--epochs 300 1000 3000] [--datasets adult wine]
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
    ap.add_argument('--epochs', nargs='*', type=int, default=[300, 1000, 3000])
    ap.add_argument('--seeds', nargs='*', type=int, default=[0])
    ap.add_argument('--arch', default='simple')
    ap.add_argument('--batch-sizes', nargs='*', type=int, default=[0, 128], help='0 = legacy full-batch steps')
    a = ap.parse_args()
    for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
        os.environ.setdefault(v, '2')
    os.environ.setdefault('DIPLOMA_DEVICE', 'cpu')
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    import warnings
    warnings.filterwarnings('ignore')
    import torch
    torch.set_num_threads(2)
    import experiments.logger as L
    L.debug_print = lambda *x, **k: None
    from study.config import EXT_DATASETS, RunSpec
    from study.data import make_split
    from study.protocol import Trainer
    for dname in a.datasets:
        ds = EXT_DATASETS[dname]
        for seed in a.seeds:
            split = make_split(dname, seed, ds.n_train, ds.max_holdout)
            ms = 42 + 1000 * seed
            row = []
            for t in ('lightgbm',):
                row.append(f'{t}={Trainer(split, RunSpec("c", model_type=t), ms).fit(split.X_train, split.y_train, ms)[0]:.4f}')
            for bs, n in [(bs, n) for bs in a.batch_sizes for n in a.epochs]:
                tr = Trainer(split, RunSpec('c', n_epochs=n, model_architecture=a.arch, batch_size=bs), ms)
                t0 = time.time()
                h, _, _ = tr._runner.train_and_evaluate(tr.pre, tr.model_params, split.X_train, split.y_train,
                                                        split.X_val, split.y_val, split.X_hold, split.y_hold, n,
                                                        _run_seed=ms)
                row.append(f'bs{bs}/ep{n}={h["final_metric"]:.4f} (best ep {h["best_epoch"] + 1}, {time.time() - t0:.0f}s)')
            print(f'{dname:<10} seed{seed} {tr.metric:<8} ' + '  '.join(row), flush=True)


if __name__ == '__main__':
    main()
