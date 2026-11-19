"""[AUDIT-FIX P12] process-parallel scheduler: no duplicate units, resume, workers=1 == old sequential loop."""
import os
from collections import Counter
from dataclasses import replace

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAS_ADULT = os.path.isdir(os.path.join(ROOT, 'datasets', 'adult'))


def _blocks():
    from study import config as C
    out = []
    for sp, ms, dss in C.models_specs()[:4]:
        for d in dss[:2]:
            for seed in (0, 1):
                out.append((0, 'seed', sp, C.EXT_DATASETS[d], seed, C.methods_for(sp.model_type, '', ms)))
    tsp = C.transfer_target_spec('lightgbm')
    out.append((1, 'transfer', tsp, C.EXT_DATASETS['adult'], 0, C.TRANSFER_SOURCES))
    return out


def test_plan_covers_every_method_once_heavy_split_lpt_and_phases(tmp_path):
    from study.parallel import HEAVY, plan
    blocks = _blocks()
    units = plan(tmp_path, blocks)
    cells = Counter((u.spec.study, u.ds.name, u.seed, m) for u in units if u.kind == 'seed' for m in u.methods)
    expected = Counter((sp.study, ds.name, seed, m) for ph, k, sp, ds, seed, ms in blocks if k == 'seed' for m in ms)
    assert cells == expected and max(cells.values()) == 1          # every (study, dataset, seed, method) once
    assert len({u.key for u in units}) == len(units)
    for u in units:
        if u.kind == 'seed' and any(m in HEAVY for m in u.methods):
            assert len(u.methods) == 1                               # heavy methods are units of their own
    phases = [u.phase for u in units]
    assert phases == sorted(phases) and phases[-1] == 1              # transfer after everything else
    p0 = [u.cost for u in units if u.phase == 0]
    assert p0 == sorted(p0, reverse=True)                            # longest first (LPT)


def test_plan_resume_skips_finished_and_retries_failed(tmp_path):
    from study import io
    from study.parallel import plan
    blocks = [b for b in _blocks() if b[1] == 'seed'][:1]
    _, _, sp, ds, seed, ms = blocks[0]
    n_all = len(plan(tmp_path, blocks))
    for m in ms:                                                     # everything finished except LOO (failed)
        io.save_json(io.run_dir(tmp_path, sp.study, ds.name, m, seed) / 'results.json',
                     {'status': 'failed' if m == 'LOO' else 'ok'})
    left = plan(tmp_path, blocks)
    assert [u.methods for u in left] == [('LOO',)] and n_all > 1
    assert plan(tmp_path, blocks, retry_failed=False) == []
    assert not list(tmp_path.rglob('*.tmp'))                         # atomic writes leave no tmp files


def test_workers_1_is_the_old_sequential_loop():
    import importlib
    rs = importlib.import_module('run_study')
    calls = []

    class P:
        def run(self, spec, ds, seed, ms, retry):
            calls.append(('seed', spec.study, ds.name, seed, tuple(ms)))

        def run_transfer(self, spec, ds, seed, src, retry):
            calls.append(('transfer', spec.study, ds.name, seed, None))

    class A:
        workers, no_retry_failed = 1, False
    blocks = _blocks()
    assert rs._execute(A(), None, print, P(), blocks) is None
    assert calls == [(k, sp.study, ds.name, seed, tuple(ms) if k == 'seed' else None)
                     for _, k, sp, ds, seed, ms in blocks]


@pytest.mark.skipif(not HAS_ADULT, reason='adult dataset not available')
def test_parallel_equals_sequential_and_resumes(tmp_path, monkeypatch):
    import config.settings as S
    from study import io
    from study.config import DatasetSpec, RunSpec
    from study.parallel import run_parallel
    from study.protocol import run_seed
    monkeypatch.setattr(S, 'DEVICE', 'cpu')
    monkeypatch.chdir(ROOT)
    ds = DatasetSpec('adult', n_train=60, max_holdout=200)
    sp = RunSpec('par', model_type='lightgbm', task='noise', noise_rate=0.1, fracs=(10,), strategies=('lowest',))
    ms = ['LOO', 'LossHigh', 'random']
    blocks = [(0, 'seed', sp, ds, s, ms) for s in (0, 1)]
    for s in (0, 1):
        run_seed(tmp_path / 'seq', sp, ds, s, ms, lambda *_: None)
    done = []
    st = run_parallel(tmp_path / 'par', lambda *_: None, None, blocks, 2, 1, 1, 'cpu', repo=ROOT,
                      on_block_done=lambda spec, d, seed: done.append(seed))
    assert st['units'] == 4 and st['failed_units'] == 0 and sorted(done) == [0, 1]   # 1 webhook per block
    for s in (0, 1):
        for m in ms:
            a = io.load_json(io.run_dir(tmp_path / 'seq', 'par', 'adult', m, s) / 'results.json')
            b = io.load_json(io.run_dir(tmp_path / 'par', 'par', 'adult', m, s) / 'results.json')
            assert b['status'] == 'ok' and a['curves'] == b['curves'] and a['detection'] == b['detection']
            va = np.load(io.run_dir(tmp_path / 'seq', 'par', 'adult', m, s) / 'values.npy')
            vb = np.load(io.run_dir(tmp_path / 'par', 'par', 'adult', m, s) / 'values.npy')
            if m != 'random':
                np.testing.assert_array_equal(va, vb)
    st2 = run_parallel(tmp_path / 'par', lambda *_: None, None, blocks, 2, 1, 1, 'cpu', repo=ROOT)
    assert st2['units'] == 0                                          # resume: nothing left
    assert not list((tmp_path / 'par' / '_logs' / 'running').glob('*.json'))
    assert not (tmp_path / 'par' / '_logs' / 'run.lock').exists()
