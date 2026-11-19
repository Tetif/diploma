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
    # [AUDIT-FIX P1] damping sweep: lambda_eff = swept damping for both Direct and LiSSA (LiSSA dampen = 0)
    for m in ('Influence', 'LissaInfluence'):
        r = io.load_json(io.run_dir(tmp_path, 'lin', 'wine', m, 0) / 'results.json')
        assert r['effective_damping'] == pytest.approx(1e-2), m
    r = io.load_json(io.run_dir(tmp_path, 'lin', 'wine', 'LissaInfluence', 0) / 'results.json')
    assert r['lissa']['dampen'] == 0.0 and r['lissa']['implicit_damping_floor'] > 0
    # default (non-sweep) settings unchanged: Direct lambda = dataset regularization
    r = io.load_json(io.run_dir(tmp_path, 'src', 'wine', 'Influence', 0) / 'results.json')
    assert r['effective_damping'] == pytest.approx(S.get_influence_params('wine')['regularization'])
    b = io.load_json(io.run_dir(tmp_path, 'dist', 'wine', '_baseline', 0) / 'results.json')
    assert b['model'] == 'distill-lightgbm' and 'teacher_metric' in b and b['fidelity'] > 0.3
    assert {'r2_student_vs_teacher', 'r2_student_vs_teacher_train', 'fidelity_train', 'student_best_epoch'} <= set(b)
    assert io.load_json(io.run_dir(tmp_path, 'lin', 'wine', '_baseline', 0) / 'results.json')['model'] == 'linear'

    sources = [('src', 'pytorch', 'LossHigh'), ('cb', 'catboost', 'CatBoostLFC'), ('missing', 'pytorch', 'LOO')]
    run_transfer_seed(tmp_path, RunSpec('transfer-lightgbm', model_type='lightgbm', **kw), ds, 0, sources,
                      logs.append)
    for name in ('pytorch.LossHigh', 'catboost.CatBoostLFC', 'random'):
        r = io.load_json(io.run_dir(tmp_path, 'transfer-lightgbm', 'wine', name, 0) / 'results.json')
        assert r['status'] == 'ok' and r['curves'], name
    assert not (io.run_dir(tmp_path, 'transfer-lightgbm', 'wine', 'pytorch.LOO', 0) / 'results.json').exists()



def test_lightgbm_fits_are_serialised():
    """[AUDIT-FIX B12] concurrent LightGBM fits from joblib threads deadlocked (LOO on adult): fits hold a lock."""
    import threading
    import numpy as np
    from models import tree_models
    assert isinstance(tree_models._LGB_LOCK, type(threading.Lock()))
    rng = np.random.default_rng(0)
    X, y = rng.normal(size=(200, 4)), rng.normal(size=200)
    out = []

    def fit():
        m = tree_models.LightGBMModel(params={'n_estimators': 20, 'verbose': -1, 'n_jobs': 1})
        m.fit(X, y)
        out.append(m.predict(X[:5]).shape)
    ts = [threading.Thread(target=fit) for _ in range(4)]
    [t.start() for t in ts]
    [t.join(60) for t in ts]
    assert out == [(5,)] * 4


def test_catboost_object_importance_sign():
    """[AUDIT-FIX B13] CatBoost LossFunctionChange is positive for harmful objects; we return higher = more
    useful, so flipped labels must get lower values than clean ones."""
    import numpy as np
    import catboost as cb
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import FunctionTransformer
    from experiments.catboost_importance import compute_catboost_object_importance
    rng = np.random.default_rng(0)
    X = rng.normal(size=(400, 3))
    y = (X[:, 0] + 0.3 * X[:, 1] > 0).astype(int)
    noisy = rng.choice(300, 30, replace=False)
    y_tr = y[:300].copy()
    y_tr[noisy] = 1 - y_tr[noisy]

    class _W:
        model = None
    w = _W()
    w.model = cb.CatBoostClassifier(iterations=100, depth=4, verbose=False, random_seed=0,
                                    allow_writing_files=False).fit(X[:300], y_tr)
    pipe = Pipeline([('preproc', FunctionTransformer()), ('model', FunctionTransformer())])
    pipe.named_steps['preproc'].fit(X[:300])
    pipe.steps[1] = ('model', w)
    v = compute_catboost_object_importance(pipe, X[:300], y_tr, X[300:], y[300:], 'binary_classification',
                                           'catboost')
    is_noisy = np.zeros(300, bool)
    is_noisy[noisy] = True
    assert v[is_noisy].mean() < v[~is_noisy].mean()


@pytest.mark.skipif(not HAS_WINE, reason='wine dataset not available')
def test_tmc_shapley_is_seeded_and_lissa_default_damping(tmp_path, monkeypatch):
    """[AUDIT-FIX P2] TMC permutations follow the run seed (reproducible); budget is written to results.json.
    [AUDIT-FIX P1] outside the damping sweep LiSSA keeps the dataset dampen: lambda_eff = reg + scale*dampen."""
    import config.settings as S
    from study import io
    from study.config import DatasetSpec, RunSpec
    from study.protocol import run_seed
    monkeypatch.setattr(S, 'DEVICE', 'cpu')
    monkeypatch.chdir(ROOT)
    ds = DatasetSpec('wine', n_train=40, max_holdout=100)
    spec = RunSpec('tmc', task='clean', fracs=(10,), strategies=('lowest',), n_epochs=10, valuation_epochs=2,
                   tmc_permutations=2)
    vals = []
    for k in range(2):
        root = tmp_path / f'r{k}'
        run_seed(root, spec, ds, 0, ['TMCShapley'] + (['LissaInfluence'] if k == 0 else []), lambda *_: None)
        r = io.load_json(io.run_dir(root, 'tmc', 'wine', 'TMCShapley', 0) / 'results.json')
        assert r['status'] == 'ok', r.get('error')
        assert r['tmc']['permutations'] == 2 and r['tmc']['seed'] == 0
        vals.append(np.load(io.run_dir(root, 'tmc', 'wine', 'TMCShapley', 0) / 'values.npy'))
    assert np.array_equal(vals[0], vals[1])
    r = io.load_json(io.run_dir(tmp_path / 'r0', 'tmc', 'wine', 'LissaInfluence', 0) / 'results.json')
    p = S.get_influence_params('wine')
    assert r['status'] == 'ok', r.get('error')
    assert r['effective_damping'] == pytest.approx(p['regularization'] + p['lissa_params']['scale']
                                                   * p['lissa_params']['damping'])
