"""[AUDIT-FIX P9-P11] GBDT influence: BoostIn baseline, teacher-target influence of the distilled student."""
import os

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAS_ADULT = os.path.isdir(os.path.join(ROOT, 'datasets', 'adult'))
ti = pytest.importorskip('tree_influence')


def _data(n=260, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 5))
    y = (X[:, 0] + 0.5 * rng.normal(size=n) > 0.7).astype(int)
    return X, y


def test_boostin_lightgbm_booster_matches_reference_package():
    """Our Booster proxy gives exactly the values of tree_influence on the equivalent LGBMClassifier."""
    import lightgbm as lgb
    from tree_influence.explainers import BoostIn
    from experiments.boostin import boostin_values
    from models.tree_models import LightGBMModel
    X, y = _data()
    p = {'objective': 'binary', 'n_estimators': 15, 'verbose': -1, 'n_jobs': 1, 'min_data_in_leaf': 5,
         'learning_rate': 0.1}
    m = LightGBMModel(params=p, task_type='binary_classification')
    m.fit(X[:200], y[:200])
    v, info = boostin_values(m, X[:200], y[:200], X[200:], y[200:], 'binary_classification')
    ref = lgb.LGBMClassifier(n_estimators=15, verbose=-1, n_jobs=1, min_child_samples=5, learning_rate=0.1)
    ref.fit(X[:200], y[:200])
    vr = BoostIn().fit(ref, X[:200], y[:200]).get_local_influence(X[200:], y[200:], verbose=0).sum(axis=1)
    np.testing.assert_allclose(v, vr, rtol=1e-6, atol=1e-9)
    assert info['boostin']['weighted_train_gradients'] is False
    # balanced weights: weighted train gradients, still finite and informative
    mw = LightGBMModel(params={**p, 'class_weight': 'balanced'}, task_type='binary_classification')
    mw.fit(X[:200], y[:200])
    vw, iw = boostin_values(mw, X[:200], y[:200], X[200:], y[200:], 'binary_classification')
    assert iw['boostin']['weighted_train_gradients'] and np.isfinite(vw).all() and np.std(vw) > 0


def test_boostin_multiclass_catboost_and_not_applicable():
    from experiments.boostin import BoostInNotApplicable, boostin_values
    from models.tree_models import CatBoostModel, LightGBMModel, RandomForestModel
    X, _ = _data()
    y3 = np.digitize(X[:, 0], [-0.5, 0.9])
    m3 = LightGBMModel(params={'objective': 'multiclass', 'num_class': 3, 'n_estimators': 8, 'verbose': -1,
                               'n_jobs': 1, 'class_weight': 'balanced'}, task_type='multiclass_classification')
    m3.fit(X[:200], y3[:200])
    v3, _ = boostin_values(m3, X[:200], y3[:200], X[200:], y3[200:], 'multiclass_classification')
    assert v3.shape == (200,) and np.isfinite(v3).all()
    X, y = _data()
    c = CatBoostModel(params={'iterations': 10, 'verbose': False, 'thread_count': 1, 'allow_writing_files': False,
                              'loss_function': 'Logloss', 'class_weight': 'balanced'},
                      task_type='binary_classification')
    c.fit(X[:200], y[:200])
    vc, ic = boostin_values(c, X[:200], y[:200], X[200:], y[200:], 'binary_classification')
    assert np.isfinite(vc).all() and ic['boostin']['weighted_train_gradients']
    rf = RandomForestModel(params={'n_estimators': 5, 'n_jobs': 1}, task_type='binary_classification')
    rf.fit(X[:200], y[:200])
    with pytest.raises(BoostInNotApplicable):
        boostin_values(rf, X[:200], y[:200], X[200:], y[200:], 'binary_classification')


def test_distill_specs_have_both_targets_and_direct_baselines():
    from study import config as C
    specs = {sp.study: (sp, ms) for sp, ms, _ in C.distill_specs()}
    for t in C.DISTILL_TEACHERS:
        sp, ms = specs[f'distill-{t}-noise10']
        assert sp.distill_influence_target == 'true_labels'
        assert {'Influence', 'LissaInfluence', 'BoostIn', 'DataOOB', 'LossHigh'} <= set(ms)
        assert ('CatBoostLFC' in ms) == (t == 'catboost')
        sp2, ms2 = specs[f'distill-{t}-noise10-tgtteacher']
        assert sp2.distill_influence_target == 'teacher' and set(ms2) == {'Influence', 'LissaInfluence'}
    models = {sp.study: ms for sp, ms, _ in C.models_specs()}
    assert 'BoostIn' in models['models-lightgbm-noise10'] and 'BoostIn' in models['models-catboost-noise10']
    assert 'BoostIn' not in C.methods_for('random_forest', '', ['BoostIn'])


def test_tempered_soft_ce_matches_distillation_kl_gradient():
    """T^2*CE(z/T, p_T) has the same parameter gradient as the student's KL(p_T || softmax(z/T))*T^2."""
    import torch
    from study.values import TemperedSoftCE
    torch.manual_seed(0)
    z = torch.randn(6, 3, requires_grad=True)
    p = torch.softmax(torch.randn(6, 3), dim=1)
    T = 2.0
    g1, = torch.autograd.grad(TemperedSoftCE(T)(z, p), z)
    kl = torch.nn.functional.kl_div(torch.log_softmax(z / T, dim=1), p, reduction='batchmean') * T * T
    g2, = torch.autograd.grad(kl, z)
    torch.testing.assert_close(g1, g2)
    assert torch.isfinite(TemperedSoftCE(T)(z, torch.tensor([0, 1, 2, 0, 1, 2])))   # hard (validation) labels


@pytest.mark.skipif(not HAS_ADULT, reason='adult dataset not available')
def test_distill_teacher_target_influence_and_boostin_on_teacher(tmp_path, monkeypatch):
    import config.settings as S
    from study import io
    from study.config import DatasetSpec, RunSpec
    from study.protocol import run_seed
    monkeypatch.setattr(S, 'DEVICE', 'cpu')
    monkeypatch.chdir(ROOT)
    ds = DatasetSpec('adult', n_train=80, max_holdout=300)
    kw = dict(task='noise', noise_rate=0.1, fracs=(10,), strategies=('lowest',), n_epochs=20)
    run_seed(tmp_path, RunSpec('dt', model_type='lightgbm', distill=True, **kw), ds, 0, ['Influence', 'BoostIn'],
             lambda *_: None)
    run_seed(tmp_path, RunSpec('dtt', model_type='lightgbm', distill=True, distill_influence_target='teacher', **kw),
             ds, 0, ['Influence'], lambda *_: None)
    a = io.load_json(io.run_dir(tmp_path, 'dt', 'adult', 'Influence', 0) / 'results.json')
    b = io.load_json(io.run_dir(tmp_path, 'dtt', 'adult', 'Influence', 0) / 'results.json')
    c = io.load_json(io.run_dir(tmp_path, 'dt', 'adult', 'BoostIn', 0) / 'results.json')
    for r in (a, b, c):
        assert r['status'] == 'ok', r.get('error')
    assert a['influence_target']['distill_influence_target'] == 'true_labels'
    assert b['influence_target']['distill_influence_target'] == 'teacher'
    assert b['spec']['distill_influence_target'] == 'teacher' and 'BCE' in b['influence_target']['train_loss']
    va = np.load(io.run_dir(tmp_path, 'dt', 'adult', 'Influence', 0) / 'values.npy')
    vb = np.load(io.run_dir(tmp_path, 'dtt', 'adult', 'Influence', 0) / 'values.npy')
    assert not np.allclose(va, vb)
    assert c['explained_model'] == 'teacher' and c['boostin']['n_boost'] >= 1
