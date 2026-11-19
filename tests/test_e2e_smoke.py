"""End-to-end smoke test of the study pipeline (wine, CPU, ~30-60 s).

run_seed -> results.json for LOO / Influence / random with 3 removal points on 10 % corrupted labels,
then the summary, paired statistics and every plot are produced from those files.
"""
import json
import os
import subprocess
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pytestmark = pytest.mark.skipif(not os.path.exists(os.path.join(ROOT, 'datasets', 'wine', 'WineQT.csv')),
                                reason='wine dataset not available')


def test_study_pipeline_end_to_end(tmp_path, monkeypatch):
    import config.settings as S
    from study.config import DatasetSpec, RunSpec
    from study.protocol import run_seed
    from study import io
    from study.summary import load, block_summary

    monkeypatch.setattr(S, 'DEVICE', 'cpu')
    monkeypatch.chdir(ROOT)
    spec = RunSpec('smoke-noise', task='noise', noise_rate=0.1, fracs=(5, 10, 20), strategies=('lowest', 'highest'),
                   n_epochs=60, valuation_epochs=10)
    ds = DatasetSpec('wine', n_train=120, max_holdout=200)
    methods = ['LOO', 'Influence', 'random']
    for seed in (0, 1):
        run_seed(tmp_path, spec, ds, seed, methods, log=lambda *a: None)

    for m in methods:
        for seed in (0, 1):
            r = io.load_json(io.run_dir(tmp_path, 'smoke-noise', 'wine', m, seed) / 'results.json')
            assert r['status'] == 'ok', r.get('error')
            assert r['n_train'] == 120 and r['n_noisy'] == 12
            assert 0.0 <= r['detection']['auc'] <= 1.0
            strategies = ['random'] if m == 'random' else ['lowest', 'highest']
            assert sorted(r['curves']) == sorted(strategies)
            assert all(np.isfinite(v) for c in r['curves'].values() for v in c.values())
            assert len(r['curves'][strategies[0]]) == 3

    # resumable: a second call does nothing (files untouched)
    p = io.run_dir(tmp_path, 'smoke-noise', 'wine', 'LOO', 0) / 'results.json'
    mtime = p.stat().st_mtime
    run_seed(tmp_path, spec, ds, 0, methods, log=lambda *a: None)
    assert p.stat().st_mtime == mtime

    summ = block_summary(load(tmp_path), 'smoke-noise', 'wine', frac=10)
    assert {m['name'] for m in summ['methods']} == {'LOO', 'Influence'}
    assert summ['random_baseline']['n_seeds'] == 2
    json.dumps(summ)   # webhook payload must be serialisable

    out = tmp_path / 'plots'
    for script in ('plot_results.py', 'paired_stats.py'):
        args = [sys.executable, os.path.join(ROOT, script), '--root', str(tmp_path), '--out', str(out)]
        if script == 'plot_results.py':
            args += ['--clean', 'smoke-noise', '--noise', 'smoke-noise']
        res = subprocess.run(args, capture_output=True, text=True, timeout=300)
        assert res.returncode == 0, res.stderr[-2000:]
    for f in ('1_removal_curves.png', '3_detection_auc.png', '5_paired_vs_random.png', 'summary.md',
              'paired_stats.md'):
        assert (out / f).exists(), f


def test_webhook_is_silent_without_env(monkeypatch):
    from study import notify
    monkeypatch.delenv('DIPLOMA_WEBHOOK_URL', raising=False)
    assert notify.post({'x': 1}) is False


def test_webhook_never_raises(monkeypatch):
    from study import notify
    monkeypatch.setenv('DIPLOMA_WEBHOOK_URL', 'http://127.0.0.1:9/unreachable')
    assert notify.post({'x': 1}) is False


def test_removal_mask_is_class_proportional():
    import numpy as np
    from study.protocol import _removal_mask
    y = np.array([0] * 90 + [1] * 10)
    order = np.r_[np.arange(90, 100), np.arange(90)]   # minority class ranked lowest
    keep = _removal_mask(order, 20, y)
    assert (~keep).sum() == 20
    assert (~keep[y == 1]).sum() == 2 and (~keep[y == 0]).sum() == 18
    assert not keep[[90, 91]].any() and keep[92:].all()
    keep_reg = _removal_mask(order, 20, None)
    assert (~keep_reg[90:]).all()
