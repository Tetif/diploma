"""Run the influence / data-valuation study (resumable).

    python run_study.py main                       # main study: 4 datasets x 7 methods x 5 seeds x {clean, noise10}
    python run_study.py sweep                      # sensitivity sweep on adult (3 seeds)
    python run_study.py pilot                      # ~10 min end-to-end check -> results/pilot
    python run_study.py probe                      # timing probe (small n) used by `estimate`
    python run_study.py estimate                   # predicted runtime of main + sweep from the probe
    python run_study.py status                     # done / failed / missing per study
    python run_study.py ext                        # secondary studies (3 seeds, seed-major), sections:
                                                   #   models convex distill noise transfer (--sections ...)
    python run_study.py ext --pilot                # same, tiny (n_train 400) -> results/pilot_ext
    python run_study.py estimate-ext               # predicted runtime of `ext` from results/pilot_ext

Every (study, dataset, method, seed) writes results/<study>/<dataset>/<method>/seed<k>/results.json;
finished runs are skipped, so the command can be interrupted and restarted at any time.
Common options: --root results --n-jobs 4 --threads 4 --device cpu --seeds 0 1 --datasets wine --methods LOO random

Optional webhook after every finished block / at the end / on a crash (see study/notify.py):
DIPLOMA_WEBHOOK_URL, DIPLOMA_WEBHOOK_KEY, DIPLOMA_WEBHOOK_HEADER (default "Authorization: Bearer <key>").
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _parse():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('command', choices=['main', 'sweep', 'pilot', 'probe', 'estimate', 'status', 'ext',
                                        'estimate-ext'])
    ap.add_argument('--sections', nargs='*', help='ext: models convex distill noise transfer (default: all)')
    ap.add_argument('--pilot', action='store_true', help='ext: small pilot (n_train 400) into results/pilot_ext')
    ap.add_argument('--n-train', type=int, default=None, help='override n_train of the subsampled datasets')
    ap.add_argument('--root', default=None, help='results folder (default results/, pilot: results/pilot)')
    ap.add_argument('--datasets', nargs='*')
    ap.add_argument('--methods', nargs='*')
    ap.add_argument('--seeds', nargs='*', type=int)
    ap.add_argument('--studies', nargs='*', help='main: clean noise10; sweep: param names')
    ap.add_argument('--n-jobs', type=int, default=4, help='parallel refits inside pyDVL (threads)')
    ap.add_argument('--threads', type=int, default=4, help='torch / BLAS threads')
    ap.add_argument('--device', default='cpu', help='cpu is faster for these tiny MLPs')
    ap.add_argument('--no-retry-failed', action='store_true')
    return ap.parse_args()


def _setup_env(a):
    # must happen before torch / numpy / config are imported
    for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[v] = str(a.threads)
    os.environ['DIPLOMA_N_JOBS'] = str(a.n_jobs)
    os.environ['DIPLOMA_DEVICE'] = a.device
    os.environ.setdefault('PYTHONWARNINGS', 'ignore')
    os.environ.setdefault('TQDM_DISABLE', '1')   # pyDVL progress bars would flood the overnight log
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    import warnings
    warnings.filterwarnings('ignore')
    import torch
    torch.set_num_threads(a.threads)
    import experiments.logger as L  # noqa: F401  (import order: avoids influence <-> experiments cycle)
    L.debug_print = lambda *x, **k: None
    import experiments  # noqa: F401


class _Log:
    def __init__(self, root: Path, name: str):
        (root / '_logs').mkdir(parents=True, exist_ok=True)
        self.path = root / '_logs' / f'{name}-{_dt.datetime.now():%Y%m%d-%H%M%S}.log'

    def __call__(self, msg: str):
        line = f'[{_dt.datetime.now():%H:%M:%S}] {msg}'
        print(line, flush=True)
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(line + '\n')


class _Progress:
    """Counts finished blocks and posts a compact summary to the webhook (if configured)."""

    def __init__(self, root: Path, log, command: str, parts_total: int):
        self.root, self.log, self.command, self.parts_total = root, log, command, parts_total
        self.part, self.t0 = 0, time.time()

    def _base(self, event: str) -> dict:
        return {'event': event, 'command': self.command, 'part_index': self.part, 'parts_total': self.parts_total,
                'elapsed_min': round((time.time() - self.t0) / 60, 1), 'root': str(self.root)}

    def block_done(self, spec, dataset: str, seed: int):
        self.part += 1
        from study import notify
        if not notify.enabled():
            return
        try:
            from study.summary import block_summary, failed_methods, load
            frac = 10 if 10 in spec.fracs else spec.fracs[0]
            summ = block_summary(load(self.root, spec.study), spec.study, dataset, frac, spec.strategies[0])
            fails = failed_methods(self.root, spec.study, dataset)
        except Exception as e:  # noqa: BLE001
            summ, fails = {'methods': [], 'summary_error': str(e)}, []
        task = spec.task if spec.task == 'clean' else f'noise{int(round(spec.noise_rate * 100))}'
        notify.post({**self._base('block'), 'study': spec.study, 'dataset': dataset, 'task': task,
                     'seed': seed, **summ, 'failed_methods': fails, 'error': None}, self.log)

    def run(self, spec, ds, seed: int, methods, retry_failed: bool = True):
        """run_seed + notification; a crash of one block (e.g. data loading) does not stop the study."""
        from study.protocol import run_seed
        try:
            run_seed(self.root, spec, ds, seed, methods, self.log, retry_failed=retry_failed)
        except Exception as e:  # noqa: BLE001
            import traceback
            self.log(f'[{spec.study}/{ds.name}/seed{seed}] BLOCK FAILED: {type(e).__name__}: {e}')
            self.log(traceback.format_exc()[-1500:])
            self.part += 1
            from study import notify
            notify.post({**self._base('block_failed'), 'study': spec.study, 'dataset': ds.name, 'task': spec.task,
                         'seed': seed, 'methods': [], 'random_baseline': None, 'full_data_baseline': None,
                         'failed_methods': [], 'error': f'{type(e).__name__}: {e}'}, self.log)
            return
        self.block_done(spec, ds.name, seed)

    def run_transfer(self, spec, ds, seed: int, sources, retry_failed: bool = True):
        from study.protocol import run_transfer_seed
        try:
            run_transfer_seed(self.root, spec, ds, seed, sources, self.log, retry_failed=retry_failed)
        except Exception as e:  # noqa: BLE001
            import traceback
            self.log(f'[{spec.study}/{ds.name}/seed{seed}] BLOCK FAILED: {type(e).__name__}: {e}')
            self.log(traceback.format_exc()[-1500:])
            self.part += 1
            from study import notify
            notify.post({**self._base('block_failed'), 'study': spec.study, 'dataset': ds.name, 'task': 'transfer',
                         'seed': seed, 'methods': [], 'random_baseline': None, 'full_data_baseline': None,
                         'failed_methods': [], 'error': f'{type(e).__name__}: {e}'}, self.log)
            return
        self.block_done(spec, ds.name, seed)

    def end(self, error: str = None):
        from study import notify
        if not notify.enabled():
            return
        fails = []
        try:
            from study.io import iter_results
            fails = [{'study': r['study'], 'dataset': r['dataset'], 'method': r['method'], 'seed': r['seed'],
                      'error': (r.get('error') or '')[:300]} for r in iter_results(self.root) if r.get('status') == 'failed']
        except Exception:  # noqa: BLE001
            pass
        notify.post({**self._base('crash' if error else 'end'), 'study': None, 'dataset': None, 'task': None,
                     'methods': [], 'random_baseline': None, 'full_data_baseline': None,
                     'failed_methods': fails[:50], 'error': error}, self.log)


def _sel(items, chosen):
    """Keep items (or DatasetSpecs, by .name) that are in ``chosen``; everything if nothing chosen."""
    return [x for x in items if not chosen or getattr(x, 'name', x) in chosen]


def cmd_main(a, root, log):
    from study.config import MAIN_DATASETS, MAIN_SEEDS, MAIN_STUDIES, methods_for
    seeds = a.seeds if a.seeds is not None else MAIN_SEEDS
    datasets = _sel(list(MAIN_DATASETS.values()), a.datasets and set(a.datasets))
    if a.n_train:
        from dataclasses import replace
        datasets = [replace(d, n_train=a.n_train) if d.n_train is not None else d for d in datasets]
    studies = [(n, sp) for n, sp in MAIN_STUDIES.items() if not a.studies or n in a.studies]
    prog = a._progress = _Progress(root, log, 'main', len(seeds) * len(datasets) * len(studies))
    for seed in seeds:                      # seed-major: a cut-short night still gives every dataset k seeds
        for ds in datasets:
            for name, spec in studies:
                methods = _sel(list(ds.methods), a.methods and set(a.methods))
                prog.run(spec, ds, seed, methods_for(spec.model_type, '', methods), not a.no_retry_failed)


def cmd_sweep(a, root, log):
    from study.config import SWEEP_DATASET, SWEEP_SEEDS, sweep_specs, methods_for
    seeds = a.seeds if a.seeds is not None else SWEEP_SEEDS
    points = [p for p in sweep_specs() if not a.studies or p[0] in a.studies]
    prog = a._progress = _Progress(root, log, 'sweep', len(seeds) * len(points))
    for seed in seeds:
        for param, value, spec, methods in points:
            methods = _sel(methods, a.methods and set(a.methods))
            prog.run(spec, SWEEP_DATASET, seed, methods_for(spec.model_type, '', methods), not a.no_retry_failed)


def cmd_pilot(a, root, log):
    """Small end-to-end run: wine (both tasks, 2 seeds) + two sweep points on a tiny adult subsample."""
    from dataclasses import replace
    from study.config import DatasetSpec, MAIN_STUDIES, SWEEP_BASE
    wine = DatasetSpec('wine', n_train=None)
    methods = a.methods or ['LOO', 'DataOOB', 'Influence', 'LissaInfluence', 'LossHigh', 'random']
    seeds = a.seeds or [0, 1]
    prog = a._progress = _Progress(root, log, 'pilot', len(seeds) * 4)
    for seed in seeds:
        for spec in MAIN_STUDIES.values():
            spec = replace(spec, study='pilot-' + spec.study)
            prog.run(spec, wine, seed, methods)
    adult = DatasetSpec('adult', n_train=400)
    for d in (1e-3, 1e-1):
        spec = replace(SWEEP_BASE, study=f'sweep-damping-{d}', damping=d)
        for seed in seeds:
            prog.run(spec, adult, seed, ['Influence', 'LissaInfluence', 'KNNShapley', 'DataOOB', 'random'])


def cmd_probe(a, root, log):
    """Time every main method at small n on every main dataset (1 seed, 1 removal point)."""
    from dataclasses import replace
    from study.config import MAIN_DATASETS, MAIN_STUDIES
    from study.protocol import run_seed
    spec = replace(MAIN_STUDIES['noise10'], fracs=(10,), tmc_permutations=2)
    for ds in _sel(list(MAIN_DATASETS.values()), a.datasets and set(a.datasets)):
        sizes = (300, 600) if ds.name == 'adult' else (300,)
        if ds.n_train is None:      # wine: probe at full size (it is small)
            sizes = (None,)
        for n in sizes:
            d = replace(ds, n_train=n)
            run_seed(root, replace(spec, study=f'probe-n{n or "all"}'), d, 0,
                     _sel(list(ds.methods), a.methods and set(a.methods)), log)


EXT_SECTIONS = ['models', 'distill', 'convex', 'noise', 'transfer']   # transfer last: it reads the others


def _ext_blocks(section):
    """-> [(spec, methods, dataset names, kind)] for one section; kind 'seed' (run_seed) or 'transfer'."""
    from study import config as C
    if section == 'models':
        return [(sp, ms, dss, 'seed') for sp, ms, dss in C.models_specs()]
    if section == 'convex':
        return [(sp, ms, dss, 'seed') for sp, ms, dss in C.convex_specs()]
    if section == 'distill':
        return [(sp, ms, dss, 'seed') for sp, ms, dss in C.distill_specs()]
    if section == 'noise':
        return [(sp, ms, dss, 'seed') for sp, ms, dss in C.noise_specs()]
    if section == 'transfer':
        return [(sp, None, dss, 'transfer') for sp, dss in C.transfer_specs()]
    raise SystemExit(f'unknown section {section}')


def cmd_ext(a, root, log):
    """Secondary studies, seed-major (a night cut short still leaves k complete seeds of every section)."""
    from dataclasses import replace
    from study import config as C
    sections = a.sections or EXT_SECTIONS
    seeds = a.seeds if a.seeds is not None else ([0, 1] if a.pilot else C.EXT_SEEDS)
    n_train = a.n_train or (400 if a.pilot else None)
    dsel = a.datasets and set(a.datasets)
    blocks = [(sec, b) for sec in sections for b in _ext_blocks(sec)]
    n_parts = sum(len(_sel(dss, dsel)) for _, (_, _, dss, _) in blocks) * len(seeds)
    prog = a._progress = _Progress(root, log, 'ext', n_parts)
    for seed in seeds:
        for sec, (spec, methods, dss, kind) in blocks:
            for dname in _sel(dss, dsel):
                ds = C.EXT_DATASETS[dname]
                if n_train and ds.n_train is not None:
                    ds = replace(ds, n_train=n_train)
                if kind == 'transfer':
                    prog.run_transfer(spec, ds, seed, C.TRANSFER_SOURCES, not a.no_retry_failed)
                    continue
                ms = _sel(methods, a.methods and set(a.methods))
                ms = C.methods_for(spec.model_type, '', ms, distill=spec.distill)
                if sec == 'noise':
                    ms = C.noise_methods_for(dname, ms)
                prog.run(spec, ds, seed, ms, not a.no_retry_failed)


def cmd_estimate_ext(a, root, log):
    from study.estimate import estimate_ext
    estimate_ext(root, log, n_jobs=a.n_jobs)


def cmd_estimate(a, root, log):
    from study.estimate import estimate
    estimate(root, log, n_jobs=a.n_jobs)


def cmd_status(a, root, log):
    from collections import Counter
    from study import io
    c = Counter()
    for r in io.iter_results(root):
        if r.get('method') != '_baseline':
            c[(r['study'], r['status'])] += 1
    for (study, status), k in sorted(c.items()):
        log(f'{study:<32} {status:<8} {k}')


def main():
    a = _parse()
    _setup_env(a)
    root = Path(a.root or ('results/pilot' if a.command == 'pilot' else
                           'results/pilot_ext' if (a.command == 'ext' and a.pilot) or a.command == 'estimate-ext' else
                           'results/probe' if a.command in ('probe', 'estimate') else 'results'))
    root = root if root.is_absolute() else ROOT / root
    log = _Log(root, a.command)
    log(f'{a.command}: root={root} n_jobs={a.n_jobs} threads={a.threads} device={a.device}')
    t0 = time.time()
    a._progress = None
    try:
        globals()[f'cmd_{a.command.replace("-", "_")}'](a, root, log)
    except BaseException as e:
        import traceback
        log(f'{a.command} CRASHED: {type(e).__name__}: {e}')
        (a._progress or _Progress(root, log, a.command, 0)).end(
            error=f'{type(e).__name__}: {e}\n' + traceback.format_exc()[-1500:])
        raise
    log(f'{a.command} finished in {(time.time() - t0) / 60:.1f} min')
    if a._progress is not None:
        a._progress.end()


if __name__ == '__main__':
    main()
