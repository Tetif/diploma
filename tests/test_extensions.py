"""Secondary studies: tree models (+ CatBoost LFC), linear model influence, distillation, transfer, noise."""
import os

import numpy as np
import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAS_WINE = os.path.exists(os.path.join(ROOT, 'datasets', 'wine', 'WineQT.csv'))


def test_systematic_noise_classification_is_a_class_pair_flip():
    from study.data import corrupt_systematic
    rng = np.random.default_rng(0)
    X = pd.DataFrame(rng.normal(size=(600, 3)), columns=list('abc'))
    y = pd.Series(np.where(X['a'] > 0.8, 2, np.where(X['a'] > -0.2, 1, 0)))
    y2, mask = corrupt_systematic(X, y, 0.1, True, seed=0)
    assert mask.sum() == 60
    src, dst = set(y[mask]), set(y2[mask])
    assert len(src) == 1 and len(dst) == 1 and src != dst           # one direction of one pair
    assert (y2[~mask] == y[~mask]).all()


def test_systematic_noise_regression_is_a_feature_subgroup_shift():
    from study.data import corrupt_systematic
    rng = np.random.default_rng(1)
    X = pd.DataFrame({'f': rng.normal(size=500), 'g': rng.normal(size=500)})
    y = pd.Series(3 * X['f'] + rng.normal(size=500) * 0.1)
    y2, mask = corrupt_systematic(X, y, 0.2, False, seed=0)
    assert mask.sum() == 100
    assert X['f'][mask].min() >= X['f'][~mask].max()                # the top-f segment
    assert np.allclose((y2 - y)[mask], 2 * np.std(y))


@pytest.mark.skipif(not HAS_WINE, reason='wine dataset not available')
def test_extension_blocks_and_transfer(tmp_path, monkeypatch):
    import config.settings as S
    from study import io
    from study.config import DatasetSpec, RunSpec
    from study.protocol import run_seed, run_transfer_seed
    monkeypatch.setattr(S, 'DEVICE', 'cpu')
    monkeypatch.chdir(ROOT)
    ds = DatasetSpec('wine', n_train=80, max_holdout=150)
    kw = dict(task='noise', noise_rate=0.1, fracs=(10,), strategies=('lowest',), n_epochs=40, valuation_epochs=3)
    logs = []
    run_seed(tmp_path, RunSpec('src', **kw), ds, 0, ['LossHigh', 'Influence', 'random'], logs.append)
    run_seed(tmp_path, RunSpec('cb', model_type='catboost', **kw), ds, 0, ['CatBoostLFC', 'LOO', 'LossHigh'],
             logs.append)
    run_seed(tmp_path, RunSpec('lin', model_architecture='linear', damping=1e-2, **kw), ds, 0,
             ['Influence', 'LissaInfluence'], logs.append)
    run_seed(tmp_path, RunSpec('dist', model_type='lightgbm', distill=True, **kw), ds, 0, ['Influence', 'LossHigh'],
             logs.append)
    for st, m in [('src', 'Influence'), ('cb', 'CatBoostLFC'), ('cb', 'LOO'), ('lin', 'LissaInfluence'),
                  ('dist', 'Influence')]:
        r = io.load_json(io.run_dir(tmp_path, st, 'wine', m, 0) / 'results.json')
        assert r['status'] == 'ok', (st, m, r.get('error'))
        assert 'detection' in r and r['timing']['values_s'] >= 0 and 'values_peak_rss_mb' in r['timing']
    b = io.load_json(io.run_dir(tmp_path, 'dist', 'wine', '_baseline', 0) / 'results.json')
    assert b['model'] == 'distill-lightgbm' and 'teacher_metric' in b and b['fidelity'] > 0.3
    assert io.load_json(io.run_dir(tmp_path, 'lin', 'wine', '_baseline', 0) / 'results.json')['model'] == 'linear'

    sources = [('src', 'pytorch', 'LossHigh'), ('cb', 'catboost', 'CatBoostLFC'), ('missing', 'pytorch', 'LOO')]
    run_transfer_seed(tmp_path, RunSpec('transfer-lightgbm', model_type='lightgbm', **kw), ds, 0, sources,
                      logs.append)
    for name in ('pytorch.LossHigh', 'catboost.CatBoostLFC', 'random'):
        r = io.load_json(io.run_dir(tmp_path, 'transfer-lightgbm', 'wine', name, 0) / 'results.json')
        assert r['status'] == 'ok' and r['curves'], name
    assert not (io.run_dir(tmp_path, 'transfer-lightgbm', 'wine', 'pytorch.LOO', 0) / 'results.json').exists()
