"""[AUDIT-FIX P12] Process-parallel execution of the study (``run_study.py ... --workers N``).

Unit of work = one (study, dataset, seed) block, with the expensive methods split off into their own units:
every method in ``HEAVY`` is a unit of its own, the cheap rest of the block is one unit. Each unit calls the
usual ``run_seed`` (or ``run_transfer_seed``) with its method subset, so the per-method results.json, the
resume logic (finished methods are skipped) and seeding are exactly those of the sequential run; the full-data
baseline is retrained (deterministically, same seed) in every unit of a block.

* Phases run one after another (``ext``: all sections, then ``transfer``, which reads their values); inside a
  phase the units are dispatched longest-first (LPT, ``unit_cost``) to a ``spawn`` process pool.
* Only the parent dispatches, every unit exactly once; a root lock (results/_logs/run.lock) stops a second
  orchestrator on the same results folder.
* Threads per worker are capped before torch / numpy import (OMP/MKL/OPENBLAS, torch.set_num_threads,
  DIPLOMA_N_JOBS for pyDVL / bagging; trees use 1 thread each, see protocol._tree_params). LightGBM's
  in-process lock (B12) stays; spawn (not fork) avoids inheriting a locked OpenMP / LightGBM state.
* Memory: a new unit is started only while the free RAM is above ``min_free_mb`` (or nothing runs); workers
  are recycled every ``MAX_TASKS_PER_CHILD`` units. A crashed pool (e.g. a worker killed) is rebuilt and its
  unfinished units are retried once.
* Webhook: the parent posts once per finished block (all its units), as the sequential run did.
"""
from __future__ import annotations

import os
import time
from collections import Counter, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

HEAVY = ('LOO', 'TMCShapley', 'Influence', 'LissaInfluence')
MAX_TASKS_PER_CHILD = 20

# rough relative cost per method (seconds at n_train ~1500, one seed) for LPT ordering only
_METHOD_COST = {'LOO': 900.0, 'TMCShapley': 2400.0, 'Influence': 60.0, 'LissaInfluence': 40.0,
                'KNNShapley': 5.0, 'DataOOB': 10.0, 'LossHigh': 2.0, 'random': 2.0, 'CatBoostLFC': 5.0,
                'BoostIn': 5.0}
_DATASET_FACTOR = {'covertype': 3.0, 'adult': 1.5, 'housing': 1.0, 'wine': 0.7}
_MODEL_FACTOR = {'pytorch': 1.0, 'lightgbm': 0.6, 'xgboost': 0.8, 'catboost': 1.5, 'random_forest': 1.2}


@dataclass
class Unit:
    phase: int
    kind: str                       # 'seed' | 'transfer'
    spec: object                    # RunSpec
    ds: object                      # DatasetSpec
    seed: int
    methods: Optional[Tuple[str, ...]]
    sources: Optional[list] = None
    cost: float = 0.0
    block: Tuple[str, str, int] = field(default=('', '', 0))
    mem_mb: float = 0.0             # [P13] expected peak RSS of the worker while running this unit

    @property
    def key(self) -> str:
        ms = '+'.join(self.methods) if self.methods else 'transfer'
        return f'{self.spec.study}/{self.ds.name}/seed{self.seed}/{ms}'


def unit_cost(spec, ds, methods, kind='seed') -> float:
    n = float(ds.n_train or 1500) * float(getattr(spec, 'sample_scale', 1.0) or 1.0) / 1500.0
    f = _DATASET_FACTOR.get(ds.name, 1.0) * _MODEL_FACTOR.get(spec.model_type, 1.0) * (2.0 if spec.distill else 1.0)
    if kind == 'transfer':
        return 60.0 * f * n
    base = 10.0 * f * n
    c = 0.0
    for m in methods:
        w = _METHOD_COST.get(m, 5.0)
        if m in ('LOO', 'TMCShapley'):
            w *= n ** 1.7 * (spec.valuation_epochs / 30.0) * (spec.tmc_permutations / 10.0 if m == 'TMCShapley' else 1.0)
        elif m == 'Influence' and ds.name == 'covertype':
            w *= 8.0
        c += w * f
    return base + c + 3.0 * f * n * len(spec.fracs) * len(spec.strategies) * len(methods)


# ------------------------------------------------------------------ [AUDIT-FIX P13] memory model
# DirectInfluence materialises the full Hessian (P x P, float32) of the MLP. pyDVL's hessian() does it with
# torch.func.hessian (jacfwd over all P directions) per mini-batch plus an accumulator, and linalg.solve
# copies it again: measured peak ~ 8 x H on top of the worker (covertype MLP 54-128-64-7, P = 15751,
# H = 0.95 GB -> 7.6 GB peak; adult 74-64-32-16-1, P = 7425 -> ~2.6 GB). Everything else stays ~1-1.5 GB.
WORKER_BASE_MB = 1200.0
HESSIAN_FACTOR = 8.5
HEAVY_MB = 2500.0                   # units above this are 'heavy': own process, at most max_heavy at a time
N_FEATURES = {'wine': 11, 'housing': 12, 'adult': 74, 'covertype': 54}     # after preprocessing
N_OUTPUTS = {'covertype': 7}
_P_CACHE = {}


def _layers(dataset: str, spec) -> list:
    if spec.distill:                # the student is SimpleNN with the default layers
        from models.torch_models import DEFAULT_PYTORCH_PARAMS
        return list(DEFAULT_PYTORCH_PARAMS['simple']['layers'])
    if spec.model_architecture == 'linear':
        return []
    try:
        import config.settings as S
        old = S.MODEL_FIT_MODE
        S.MODEL_FIT_MODE = spec.fit_mode
        try:
            cfg = S.get_model_config(dataset, 'pytorch')
        finally:
            S.MODEL_FIT_MODE = old
        return list(cfg['simple']['layers'])
    except Exception:  # noqa: BLE001 - conservative fallback
        return [128, 64]


def mlp_param_count(spec, ds) -> int:
    key = (ds.name, spec.distill, spec.model_architecture, spec.fit_mode)
    if key not in _P_CACHE:
        sizes = [N_FEATURES.get(ds.name, 64)] + _layers(ds.name, spec) + [N_OUTPUTS.get(ds.name, 1)]
        _P_CACHE[key] = int(sum(a * b + b for a, b in zip(sizes[:-1], sizes[1:])))
    return _P_CACHE[key]


def unit_mem_mb(spec, ds, methods) -> float:
    """Expected peak RSS (MB) of a worker running this unit (conservative)."""
    mem = WORKER_BASE_MB + (300.0 if ds.name == 'covertype' else 0.0)
    if 'Influence' in methods and (spec.model_type == 'pytorch' or spec.distill):
        p = mlp_param_count(spec, ds)
        h = HESSIAN_FACTOR * p * p * 4 / 2 ** 20
        if h <= hessian_limit_mb():     # otherwise compute_values skips it at once (NotApplicable)
            mem += h
    return mem


def hessian_limit_mb() -> float:
    """Largest expected DirectInfluence peak that is attempted: 60 % of the physical RAM."""
    try:
        import psutil
        return 0.6 * psutil.virtual_memory().total / 2 ** 20
    except Exception:  # noqa: BLE001
        return 9000.0


def split_block(phase, kind, spec, ds, seed, methods, sources=None) -> List[Unit]:
    blk = (spec.study, ds.name, int(seed))
    if kind == 'transfer':
        return [Unit(phase, kind, spec, ds, seed, None, sources, unit_cost(spec, ds, [], 'transfer'), blk,
                     unit_mem_mb(spec, ds, ()))]
    heavy = [m for m in methods if m in HEAVY]
    light = [m for m in methods if m not in HEAVY]
    groups = [(m,) for m in heavy] + ([tuple(light)] if light else [])
    return [Unit(phase, kind, spec, ds, seed, g, None, unit_cost(spec, ds, g), blk, unit_mem_mb(spec, ds, g))
            for g in groups]


def unit_pending(root, u: Unit, retry_failed: bool = True) -> bool:
    from study import io
    if u.kind == 'transfer':
        return True                 # run_transfer_seed skips finished sources itself (cheap check)
    for m in u.methods:
        r = io.load_json(io.run_dir(root, u.spec.study, u.ds.name, m, u.seed) / 'results.json')
        if not (r and (r.get('status') in io.DONE_STATUSES or (r.get('status') == 'failed' and not retry_failed))):
            return True
    return False


def plan(root, blocks, retry_failed=True) -> List[Unit]:
    """blocks: [(phase, kind, spec, ds, seed, methods_or_sources)] -> pending units, phase order, LPT inside."""
    units = []
    for phase, kind, spec, ds, seed, ms in blocks:
        if kind == 'transfer':
            units += split_block(phase, kind, spec, ds, seed, None, ms)
        else:
            units += [u for u in split_block(phase, kind, spec, ds, seed, ms) if unit_pending(root, u, retry_failed)]
    units.sort(key=lambda u: (u.phase, -u.cost, u.key))
    return units


# ------------------------------------------------------------------ worker side
_W = {}


def _worker_init(threads: int, n_jobs: int, device: str, log_dir: str, repo: str):
    for v in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[v] = str(threads)
    os.environ['DIPLOMA_N_JOBS'] = str(n_jobs)
    os.environ['DIPLOMA_DEVICE'] = device
    os.environ.setdefault('PYTHONWARNINGS', 'ignore')
    os.environ['TQDM_DISABLE'] = '1'
    import sys
    os.chdir(repo)
    if repo not in sys.path:
        sys.path.insert(0, repo)
    import warnings
    warnings.filterwarnings('ignore')
    import torch
    torch.set_num_threads(threads)
    try:
        torch.set_num_interop_threads(1)
    except RuntimeError:
        pass
    import experiments.logger as L  # noqa: F401  (same import order as run_study._setup_env)
    L.debug_print = lambda *x, **k: None
    import experiments  # noqa: F401
    # joblib inside a worker: threads, never loky sub-processes (they multiplied the RAM and kept the worker
    # alive at pool shutdown). Inner parallel_config(n_jobs=...) calls inherit this backend.
    from joblib import parallel_config
    _W['joblib_cfg'] = parallel_config(backend='threading')
    _W['joblib_cfg'].__enter__()
    _W['log_path'] = Path(log_dir) / f'worker-{os.getpid()}.log'


def _wlog(msg: str):
    import datetime as dt
    line = f'[{dt.datetime.now():%H:%M:%S}] [w{os.getpid()}] {msg}'
    print(line, flush=True)
    try:
        with open(_W['log_path'], 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except (KeyError, OSError):
        pass


def _peak_rss_mb() -> float:
    try:
        import psutil
        mi = psutil.Process().memory_info()
        return float(getattr(mi, 'peak_wset', mi.rss)) / 2 ** 20
    except Exception:  # noqa: BLE001
        return float('nan')


def _worker_run(u: Unit, root: str, retry_failed: bool):
    from study import io
    marker = Path(root) / '_logs' / 'running' / (u.key.replace('/', '__') + '.json')
    t0 = time.time()
    io.save_json(marker, {'unit': u.key, 'pid': os.getpid(), 'started': time.time()})
    try:
        if u.kind == 'transfer':
            from study.protocol import run_transfer_seed
            run_transfer_seed(root, u.spec, u.ds, u.seed, u.sources, _wlog, retry_failed=retry_failed)
        else:
            from study.protocol import run_seed
            run_seed(root, u.spec, u.ds, u.seed, list(u.methods), _wlog, retry_failed=retry_failed)
        err = None
    except Exception as e:  # noqa: BLE001 - one failing unit must not stop the study
        import traceback
        err = f'{type(e).__name__}: {e}'
        _wlog(f'[{u.key}] UNIT FAILED: {err}\n{traceback.format_exc()[-1500:]}')
    finally:
        try:
            marker.unlink()
        except OSError:
            pass
    return {'key': u.key, 'error': err, 'elapsed_s': time.time() - t0, 'peak_rss_mb': _peak_rss_mb(),
            'pid': os.getpid()}


# ------------------------------------------------------------------ parent side
def _avail_mb() -> float:
    try:
        import psutil
        return psutil.virtual_memory().available / 2 ** 20
    except Exception:  # noqa: BLE001
        return float('inf')


class RootLock:
    """One orchestrator per results folder (a stale lock of a dead process is taken over)."""

    def __init__(self, root):
        self.path = Path(root) / '_logs' / 'run.lock'

    def __enter__(self):
        import psutil
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            pid = int(self.path.read_text().strip() or 0)
        except (OSError, ValueError):
            pid = 0
        if pid and pid != os.getpid() and psutil.pid_exists(pid):
            raise RuntimeError(f'{self.path} is held by running process {pid}: another run on the same root?')
        self.path.write_text(str(os.getpid()))
        return self

    def __exit__(self, *exc):
        try:
            self.path.unlink()
        except OSError:
            pass


def _shutdown(ex):
    """Stop the pool without waiting on lingering workers (all units are finished or abandoned here)."""
    procs = list(getattr(ex, '_processes', {}).values())
    ex.shutdown(wait=False, cancel_futures=True)
    try:
        import psutil
        ps = []
        for p in procs:
            try:
                pp = psutil.Process(p.pid)
                ps += pp.children(recursive=True) + [pp]
            except psutil.Error:
                pass
        for p in ps:
            try:
                p.terminate()
            except psutil.Error:
                pass
        psutil.wait_procs(ps, timeout=10)
    except Exception:  # noqa: BLE001
        for p in procs:
            try:
                p.terminate()
            except Exception:  # noqa: BLE001
                pass


def _rss_mb(pid) -> float:
    try:
        import psutil
        return psutil.Process(pid).memory_info().rss / 2 ** 20
    except Exception:  # noqa: BLE001
        return 0.0


def _marker_pids(log_dir) -> dict:
    from study import io
    out = {}
    for p in (Path(log_dir) / 'running').glob('*.json'):
        r = io.load_json(p) or {}
        if r.get('unit'):
            out[r['unit']] = r.get('pid')
    return out


def run_parallel(root, log, prog, blocks, workers: int, threads: int, n_jobs: int, device: str,
                 retry_failed: bool = True, min_free_mb: float = 1500.0, repo: Optional[str] = None,
                 on_block_done=None, max_heavy: int = 1, heavy_mb: float = HEAVY_MB) -> dict:
    """Execute ``blocks`` with up to ``workers`` spawn processes. Returns stats (units, peak RSS, wall time).

    [AUDIT-FIX P13] memory-aware dispatch: every unit has an expected peak (``unit_mem_mb``). A unit starts only
    if its peak plus the still-expected growth of the running units plus ``min_free_mb`` fits into the RAM that is
    free now (the first unit always starts). Heavy units (> ``heavy_mb``) run in a separate pool whose process
    exits after every unit (the allocator keeps the Hessian's memory otherwise), at most ``max_heavy`` at a time.
    LPT order is kept: if the longest pending unit does not fit, the next one that fits is started."""
    import multiprocessing as mp
    from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
    from concurrent.futures.process import BrokenProcessPool
    root = str(root)
    repo = repo or str(Path(__file__).resolve().parent.parent)
    log_dir = Path(root) / '_logs'
    (log_dir / 'running').mkdir(parents=True, exist_ok=True)
    for stale in (log_dir / 'running').glob('*.json'):      # markers of an interrupted run
        stale.unlink()
    stats = {'units': 0, 'failed_units': 0, 'max_worker_peak_rss_mb': 0.0, 'min_avail_mb': _avail_mb(),
             'wall_s': 0.0, 'max_heavy_running': 0, 'max_running': 0}
    t_all = time.time()
    max_heavy = max(1, int(max_heavy))
    with RootLock(root):
        phases = sorted({b[0] for b in blocks})
        for phase in phases:
            units = plan(root, [b for b in blocks if b[0] == phase], retry_failed)
            left = Counter(u.block for u in units)
            info = {u.block: (u.spec, u.ds, u.seed) for u in units}
            n_skip = sum(1 for b in blocks if b[0] == phase) - len(left)
            if prog is not None:
                prog.part += max(n_skip, 0)         # blocks already complete (resume)
            n_heavy = sum(u.mem_mb > heavy_mb for u in units)
            log(f'phase {phase}: {len(units)} units in {len(left)} blocks ({n_skip} blocks already done), '
                f'{n_heavy} heavy (> {heavy_mb:.0f} MB, max {max_heavy} at a time), '
                f'workers={workers} x threads={threads} (pyDVL n_jobs={n_jobs})')
            queue, attempts = list(units), Counter()
            while queue:
                ctx = mp.get_context('spawn')
                init = dict(initializer=_worker_init, initargs=(threads, n_jobs, device, str(log_dir), repo))
                light = ProcessPoolExecutor(max_workers=workers, mp_context=ctx,
                                            max_tasks_per_child=MAX_TASKS_PER_CHILD, **init)
                heavy = ProcessPoolExecutor(max_workers=max_heavy, mp_context=ctx, max_tasks_per_child=1, **init)
                running = {}
                try:
                    while queue or running:
                        while queue and len(running) < workers:
                            pids = _marker_pids(log_dir)
                            growth = sum(max(0.0, r.mem_mb - _rss_mb(pids[r.key]) if r.key in pids else r.mem_mb)
                                         for r in running.values())
                            budget = _avail_mb() - growth - min_free_mb
                            n_h = sum(r.mem_mb > heavy_mb for r in running.values())
                            pick = None
                            for j, u in enumerate(queue):            # LPT order, first unit that fits
                                if u.mem_mb > heavy_mb and n_h >= max_heavy:
                                    continue
                                if not running or u.mem_mb <= budget:
                                    pick = j
                                    break
                            if pick is None:
                                break
                            u = queue.pop(pick)
                            attempts[u.key] += 1
                            ex = heavy if u.mem_mb > heavy_mb else light
                            running[ex.submit(_worker_run, u, root, retry_failed)] = u
                            stats['max_running'] = max(stats['max_running'], len(running))
                            stats['max_heavy_running'] = max(stats['max_heavy_running'],
                                                             sum(r.mem_mb > heavy_mb for r in running.values()))
                            if u.mem_mb > heavy_mb:
                                log(f'start heavy unit {u.key} (expected {u.mem_mb:.0f} MB, free '
                                    f'{_avail_mb():.0f} MB)')
                        if not running:
                            break
                        done, _ = wait(list(running), timeout=10, return_when=FIRST_COMPLETED)
                        stats['min_avail_mb'] = min(stats['min_avail_mb'], _avail_mb())
                        for f in done:
                            u = running.pop(f)
                            res = f.result()
                            stats['units'] += 1
                            stats['max_worker_peak_rss_mb'] = max(stats['max_worker_peak_rss_mb'],
                                                                  res['peak_rss_mb'] or 0.0)
                            if res['error']:
                                stats['failed_units'] += 1
                            log(f'unit done {u.key} in {res["elapsed_s"]:.0f}s (w{res["pid"]}, process peak '
                                f'{res["peak_rss_mb"]:.0f} MB, expected {u.mem_mb:.0f})'
                                f'{" ERROR " + res["error"] if res["error"] else ""}'
                                f' | left {len(queue) + len(running)}')
                            left[u.block] -= 1
                            if left[u.block] == 0:
                                sp, ds, seed = info[u.block]
                                if on_block_done:
                                    on_block_done(sp, ds, seed)
                                elif prog is not None:
                                    prog.block_done(sp, ds.name, seed)
                except BrokenProcessPool as e:
                    lost = list(running.values())
                    log(f'process pool broke ({e}); {len(lost)} running units: '
                        + ', '.join(u.key for u in lost))
                    retry = []
                    for u in lost:
                        if attempts[u.key] < 2:
                            retry.append(u)
                        else:
                            stats['failed_units'] += 1
                            log(f'giving up on {u.key} (crashed twice)')
                            left[u.block] -= 1
                    # retried units go back in LPT order; the heavy limit / memory check still applies, and
                    # after a crash heavy units run strictly one at a time for the rest of the phase
                    queue = sorted(retry + queue, key=lambda x: (-x.cost, x.key))
                    max_heavy = 1
                finally:
                    _shutdown(light)
                    _shutdown(heavy)
    stats['wall_s'] = time.time() - t_all
    return stats
