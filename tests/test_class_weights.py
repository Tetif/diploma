"""[AUDIT-FIX P7] threshold-free holdout metrics / distillation diagnostics; [P8] class weights of tree models."""
import os

import numpy as np
import pytest
from sklearn.base import clone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAS_ADULT = os.path.isdir(os.path.join(ROOT, 'datasets', 'adult'))


def _data(k=2, n=120, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 4))
    if k == 2:
        y = (X[:, 0] + 0.3 * rng.normal(size=n) > 0.8).astype(int)       # imbalanced (~20 % positives)
    else:
        y = np.digitize(X[:, 0], [-0.5, 0.9])                            # 3 unequal classes
    return X, y


@pytest.mark.parametrize('cls,lib_params', [
    ('LightGBMModel', {'objective': 'binary', 'n_estimators': 20, 'verbose': -1, 'n_jobs': 1}),
    ('XGBoostModel', {'objective': 'binary:logistic', 'n_estimators': 20, 'n_jobs': 1}),
])
def test_binary_boosting_uses_scale_pos_weight(cls, lib_params):
    from models import tree_models
    X, y = _data(2)
    m = getattr(tree_models, cls)(params={**lib_params, 'class_weight': 'balanced'}, task_type='binary_classification')
    m.fit(X, y)
    assert m.class_weighting_['scale_pos_weight'] == pytest.approx((y == 0).sum() / (y == 1).sum())
    m2 = clone(m)                       # LOO / removal refits keep the setting, weights from their own subset
    m2.fit(X[:80], y[:80])
    assert m2.class_weighting_['scale_pos_weight'] == pytest.approx((y[:80] == 0).sum() / (y[:80] == 1).sum())
    assert m.predict_proba(X).shape == (len(X), 2)


def test_multiclass_and_catboost_rf_weights():
    from models import tree_models
    X, y = _data(3)
    lg = tree_models.LightGBMModel(params={'objective': 'multiclass', 'num_class': 3, 'n_estimators': 10,
                                           'verbose': -1, 'n_jobs': 1, 'class_weight': 'balanced'},
                                   task_type='multiclass_classification')
    lg.fit(X, y)
    cw = lg.class_weighting_['class_weights']
    counts = np.bincount(y)
    assert cw[int(np.argmin(counts))] > cw[int(np.argmax(counts))]
    xg = tree_models.XGBoostModel(params={'objective': 'multi:softprob', 'n_estimators': 10, 'n_jobs': 1,
                                          'class_weight': 'balanced'}, task_type='multiclass_classification')
    xg.fit(X, y)
    assert xg.class_weighting_['sample_weight'] == 'balanced'
    cb = tree_models.CatBoostModel(params={'iterations': 20, 'verbose': False, 'thread_count': 1,
                                           'allow_writing_files': False, 'class_weight': 'balanced'},
                                   task_type='multiclass_classification')
    cb.fit(X, y)
    assert cb.model.get_params()['auto_class_weights'] == 'Balanced'
    rf = tree_models.RandomForestModel(params={'n_estimators': 10, 'n_jobs': 1, 'class_weight': 'balanced'},
                                       task_type='multiclass_classification')
    rf.fit(X, y)
    assert rf.model.class_weight == 'balanced'
    # regression: the key is ignored (dropped), not passed to the library
    r = tree_models.RandomForestModel(params={'n_estimators': 5, 'class_weight': 'balanced'}, task_type='regression')
    r.fit(X, X[:, 0])
    assert r.class_weighting_ == {}


def test_catboost_lfc_and_pydvl_loo_with_class_weights():
    """CatBoost LossFunctionChange and pyDVL LOO (clone + refit) still work with balanced class weights."""
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from experiments.catboost_importance import compute_catboost_object_importance
    from models import tree_models
    X, y = _data(2, n=80)
    cb = tree_models.CatBoostModel(params={'iterations': 30, 'verbose': False, 'thread_count': 1,
                                           'allow_writing_files': False, 'loss_function': 'Logloss',
                                           'class_weight': 'balanced'}, task_type='binary_classification')
    pre = StandardScaler().fit(X)
    cb.fit(pre.transform(X), y)
    v = compute_catboost_object_importance(Pipeline([('preproc', pre), ('model', cb)]), X[:60], y[:60], X[60:],
                                           y[60:], 'binary_classification', 'catboost')
    assert v.shape == (60,) and np.isfinite(v).all() and np.std(v) > 0

    from joblib import parallel_config
    from pydvl.valuation.dataset import Dataset
    from pydvl.valuation.methods import LOOValuation
    from pydvl.valuation.scorers import SupervisedScorer
    from pydvl.valuation.utility import ModelUtility
    lg = tree_models.LightGBMModel(params={'objective': 'binary', 'n_estimators': 10, 'verbose': -1, 'n_jobs': 1,
                                           'min_data_in_leaf': 3, 'class_weight': 'balanced'},
                                   task_type='binary_classification')
    acc = lambda model, x, t: float(np.mean((np.asarray(model.predict(x)) >= 0.5) == t))  # noqa: E731
    u = ModelUtility(lg, SupervisedScorer(acc, Dataset(X[60:], y[60:]), default=0.0), catch_errors=False)
    loo = LOOValuation(u)
    with parallel_config(backend='threading', n_jobs=2):
        loo.fit(Dataset(X[:30], y[:30]))
    assert np.isfinite(loo.result.values).all()


@pytest.mark.skipif(not HAS_ADULT, reason='adult dataset not available')
def test_results_have_holdout_prob_metrics_and_class_weights(tmp_path, monkeypatch):
    import config.settings as S
    from study import io
    from study.config import DatasetSpec, RunSpec
    from study.protocol import run_seed
    monkeypatch.setattr(S, 'DEVICE', 'cpu')
    monkeypatch.chdir(ROOT)
    ds = DatasetSpec('adult', n_train=80, max_holdout=300)
    kw = dict(task='noise', noise_rate=0.1, fracs=(10,), strategies=('lowest',), n_epochs=20)
    run_seed(tmp_path, RunSpec('lgb', model_type='lightgbm', **kw), ds, 0, ['LossHigh'], lambda *_: None)
    run_seed(tmp_path, RunSpec('dist', model_type='lightgbm', distill=True, **kw), ds, 0, ['LossHigh'],
             lambda *_: None)
    r = io.load_json(io.run_dir(tmp_path, 'lgb', 'adult', 'LossHigh', 0) / 'results.json')
    assert r['status'] == 'ok', r.get('error')
    assert 0.0 <= r['holdout_roc_auc'] <= 1.0 and r['holdout_logloss'] > 0
    assert r['class_weighting']['scale_pos_weight'] > 1.0 and r['spec']['tree_class_weight'] == 'balanced'
    b = io.load_json(io.run_dir(tmp_path, 'dist', 'adult', '_baseline', 0) / 'results.json')
    for k in ('teacher_holdout_roc_auc', 'teacher_holdout_logloss', 'holdout_roc_auc', 'fidelity_train',
              'student_best_epoch', 'student_epochs_run'):
        assert b.get(k) is not None, k
    assert 1 <= b['student_best_epoch'] <= b['student_epochs_run'] <= b['student_max_epochs']
    assert b['class_weighting']['scale_pos_weight'] > 1.0          # the teacher is weighted too
