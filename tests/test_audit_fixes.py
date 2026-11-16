"""Тесты к исправлениям из AUDIT.md (см. FIXES.md). Запуск: python -m pytest tests -q"""
import numpy as np
import pandas as pd
import pytest
import torch
from sklearn.base import clone
from sklearn.metrics import f1_score, accuracy_score

import config.settings as S
from models.torch_models import PyTorchModelWrapper
from influence.methods import SafeModelWrapper, InfluenceMethods
from influence.scorers import (
    ScorerFactory, pred_to_labels, constant_predictor_score,
)


def _binary_data(n=300, d=5, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d)).astype(np.float32)
    y = (X[:, 0] + 0.2 * rng.normal(size=n) > 0).astype(int)
    return X, y


# ---------- B1: clone() воспроизводит модель ----------

def test_pytorch_clone_roundtrip_keeps_full_config():
    m = PyTorchModelWrapper(5, model_architecture='simple', device='cpu',
                            task_type='binary_classification', pos_weight=2.0,
                            layers=[16, 8], dropout=0.0, learning_rate=0.01,
                            default_epochs=150, refit_seed=7)
    c = clone(SafeModelWrapper(m)).model
    assert c.get_params() == m.get_params()
    assert c.task_type == 'binary_classification'
    assert isinstance(c.criterion, torch.nn.BCEWithLogitsLoss)
    assert float(c.criterion.pos_weight) == 2.0
    assert c.default_epochs == 150
    assert c.optimizer.param_groups[0]['lr'] == 0.01
    assert [l.out_features for l in c.model.modules() if isinstance(l, torch.nn.Linear)] == [16, 8, 1]


def test_clone_fit_without_epochs_actually_trains():
    X, y = _binary_data()
    m = PyTorchModelWrapper(5, device='cpu', task_type='binary_classification',
                            layers=[16], dropout=0.0, learning_rate=0.01, refit_seed=0)
    c = clone(SafeModelWrapper(m))
    c.fit(X, y)  # так вызывает pyDVL
    acc = accuracy_score(y, (c.predict(X) >= 0.5).astype(int))
    assert acc > 0.9, acc


def test_refit_is_deterministic_with_refit_seed():
    X, y = _binary_data()
    m = PyTorchModelWrapper(5, device='cpu', task_type='binary_classification',
                            layers=[8], dropout=0.0, refit_seed=3, default_epochs=20)
    a, b = clone(m), clone(m)
    a.fit(X, y)
    b.fit(X, y)
    np.testing.assert_allclose(a.predict(X), b.predict(X))


def test_incremental_fit_with_epochs_does_not_reinit():
    X, y = _binary_data()
    m = PyTorchModelWrapper(5, device='cpu', task_type='binary_classification',
                            layers=[8], dropout=0.0, learning_rate=0.01, refit_seed=0)
    losses = [m.fit(X, y, epochs=1) for _ in range(60)]
    assert losses[-1] < losses[0] * 0.9


def test_tree_model_clone_keeps_task_type():
    pytest.importorskip('lightgbm')
    from models.tree_models import LightGBMModel
    m = LightGBMModel(params={'n_estimators': 10, 'verbose': -1}, task_type='binary_classification')
    c = clone(m)
    assert c.task_type == 'binary_classification'
    assert c.params['n_estimators'] == 10


# ---------- B2: скореры ----------

class _Fixed:
    def __init__(self, out):
        self.out = np.asarray(out)

    def predict(self, X):
        return self.out


def test_pred_to_labels():
    assert pred_to_labels(np.array([0.2, 0.7, 0.5])).tolist() == [0, 1, 1]
    assert pred_to_labels(np.array([[0.1, 0.9], [0.8, 0.2]])).tolist() == [1, 0]


def test_f1_scorer_on_probabilities_is_not_zero():
    y = np.array([0, 1, 1, 0, 1])
    probs = np.array([0.1, 0.9, 0.6, 0.4, 0.3])
    s = ScorerFactory.create_scorer('f1')(_Fixed(probs), np.zeros((5, 2)), y)
    assert s == pytest.approx(f1_score(y, [0, 1, 1, 0, 0]))
    assert s > 0


def test_multiclass_accuracy_from_logits():
    y = np.array([2, 0, 1])
    logits = np.array([[0, 1, 5], [3, 0, 0], [0, 2, 1]], dtype=float)
    s = ScorerFactory.create_scorer('accuracy')(_Fixed(logits), np.zeros((3, 2)), y)
    assert s == 1.0


def test_scorer_raises_on_length_mismatch():
    with pytest.raises(ValueError):
        ScorerFactory.create_scorer('f1')(_Fixed(np.zeros(4)), np.zeros((5, 2)), np.zeros(5))


def test_mae_scorer_sign_higher_is_better():
    y = np.array([1.0, 2.0, 3.0])
    good = ScorerFactory.create_scorer('mae')(_Fixed(y + 0.1), np.zeros((3, 1)), y)
    bad = ScorerFactory.create_scorer('mae')(_Fixed(y + 1.0), np.zeros((3, 1)), y)
    assert good == pytest.approx(-0.1)
    assert good > bad


def test_f1_scorer_on_trained_torch_model_matches_sklearn():
    X, y = _binary_data()
    m = PyTorchModelWrapper(5, device='cpu', task_type='binary_classification',
                            layers=[16], dropout=0.0, learning_rate=0.01, refit_seed=0)
    m.fit(X, y)
    s = ScorerFactory.create_scorer('f1')(m, X, y)
    assert s == pytest.approx(f1_score(y, (m.predict(X) >= 0.5).astype(int)))
    assert s > 0.9


# ---------- B4: u(∅) ----------

def test_constant_predictor_score():
    assert constant_predictor_score('mae', [0, 1, 2], [1, 3]) == pytest.approx(-1.0)
    assert constant_predictor_score('accuracy', [1, 1, 0], [1, 0, 1, 1]) == pytest.approx(0.75)
    assert constant_predictor_score('f1', [0, 0, 1], [1, 1]) == 0.0


# ---------- B3: никаких молчаливых нулей ----------

class _Boom:
    def fit(self, *a, **k):
        raise RuntimeError("model fit failed")

    def predict(self, X):
        return np.zeros(len(X))


def test_safe_wrapper_propagates_fit_errors():
    with pytest.raises(RuntimeError):
        SafeModelWrapper(_Boom()).fit(np.zeros((3, 2)), np.zeros(3))


class _BrokenMethod:
    def fit(self, data):
        raise RuntimeError("valuation exploded")


class _IdPre:
    is_fitted = True

    def transform(self, X):
        return np.asarray(X, dtype=np.float32)


class _Cfg:
    name = 'unit'
    task_type = 'regression'
    metrics = ['mae']


def test_failed_method_gives_nan_and_flag_not_zeros():
    im = InfluenceMethods(None, dataset_config=_Cfg())
    X = pd.DataFrame(np.random.default_rng(0).normal(size=(20, 3)))
    y = pd.Series(np.arange(20, dtype=float))
    pipe = type('P', (), {'named_steps': {'model': _Fixed(np.zeros(20))}})()
    scores, raw = im.compute_scores({'LOO': _BrokenMethod()}, X, y, _IdPre(), X, y, pipe)
    assert np.isnan(scores['LOO']).all()
    assert 'LOO' in im.failed_methods


def test_runner_skips_nan_method_and_flags_it(monkeypatch):
    from experiments.runner import ExperimentRunner
    monkeypatch.setitem(S.EXPERIMENT_CONFIG, 'n_retrain_runs', 1)
    rng = np.random.default_rng(0)
    X = pd.DataFrame(rng.normal(size=(60, 3)), columns=['a', 'b', 'c'])
    y = pd.Series(X['a'].values * 2 + rng.normal(size=60) * 0.1)
    mp = {'model_type': 'pytorch', 'model_architecture': 'simple', 'input_size': 3, 'device': 'cpu',
          'task_type': 'regression', 'available_metrics': ['mae'], 'removal_strategies': ['lowest']}
    r = ExperimentRunner(None)
    r.results = {'orig': {'final_metric': 1.0, 'final_mae': 1.0}}
    scores = {'LOO': np.full(40, np.nan), 'LossHigh': rng.random(40)}
    r._run_removal_phase(X.iloc[:40], y.iloc[:40], X.iloc[40:50], y.iloc[40:50],
                         X.iloc[50:], y.iloc[50:], _IdPre(), mp, scores, [10], 3, None)
    assert not any(k.startswith('LOO_') and k.endswith('pct') for k in r.results)
    assert 'LOO' in r.results['orig']['invalid_methods']
    assert 'LossHigh_10pct' in r.results


# ---------- M1: усреднение по сидам вместо выбора по holdout ----------

def test_aggregate_runs_mean_and_std():
    from experiments.runner import ExperimentRunner
    runs = [({'final_metric': v, 'best_val_metric': v}, f'm{i}', None) for i, v in enumerate([1.0, 2.0, 3.0])]
    h, model, _ = ExperimentRunner._aggregate_runs(runs)
    assert h['final_metric'] == pytest.approx(2.0)
    assert h['final_mae'] == pytest.approx(2.0)
    assert h['final_metric_std'] == pytest.approx(np.std([1, 2, 3]))
    assert model == 'm0'  # не «лучшая по holdout», а первый (фиксированный seed)


# ---------- конфиг ----------

def test_design_config():
    assert S.EXPERIMENT_CONFIG['retrain_aggregate'] == 'mean'
    assert S.EXPERIMENT_CONFIG['n_random_runs'] >= 5
    assert {'lowest', 'highest', 'random'} <= set(S.MODEL_RUN_CONFIG['removal_strategies'])
    assert S.EXPERIMENT_CONFIG['valuation_epochs'] >= 50


def test_dataset_leaks_removed():
    from config.datasets.electric import ElectricConfig
    from config.datasets.zillow import ZillowConfig
    import inspect
    assert 'Global_intensity' not in ElectricConfig.numeric_columns
    assert ZillowConfig.train_target_clip_quantiles == (0.005, 0.995)
    assert 'target.clip(' not in inspect.getsource(ZillowConfig.load_data)


def test_parallel_refit_is_deterministic():
    """[B9] Одновременные fit() в потоках с одинаковым refit_seed дают одинаковые модели."""
    import threading
    from models.factory import ModelFactory
    rng = np.random.default_rng(0)
    X = rng.normal(size=(120, 5)).astype(np.float32)
    y = (X[:, 0] > 0).astype(int)
    mp = dict(model_type='pytorch', model_architecture='simple', input_size=5, device='cpu',
              task_type='binary_classification',
              simple={'layers': [16], 'dropout': 0.2, 'learning_rate': 0.01})
    ref = ModelFactory.create_model(**mp)
    ref.default_epochs = 30
    ref.fit(X, y)
    expected = ref.predict(X)
    models = []

    def work():  # создание (тратит RNG) и обучение — одновременно в разных потоках
        m = ModelFactory.create_model(**mp)
        m.default_epochs = 30
        m.fit(X, y)
        models.append(m)

    th = [threading.Thread(target=work) for _ in range(6)]
    for t in th:
        t.start()
    for t in th:
        t.join()
    for m in models:
        assert np.allclose(m.predict(X), expected, atol=1e-6)


def test_valuation_scorer_uses_validation_data():
    """[B10] Utility pyDVL считается на X_val/y_val, а не на обучающей выборке."""
    from models.factory import ModelFactory
    from influence.methods import InfluenceMethods
    from sklearn.pipeline import Pipeline

    class _Id:
        is_fitted = True

        def transform(self, Z):
            return np.asarray(Z, dtype=np.float32)

    class _Cfg:
        name = 'synthetic'
        task_type = 'binary_classification'
        metrics = ['accuracy', 'f1']

    rng = np.random.default_rng(1)
    Xtr = rng.normal(size=(40, 3)).astype(np.float32)
    ytr = (Xtr[:, 0] > 0).astype(int)
    Xva = rng.normal(size=(25, 3)).astype(np.float32) + 10.0
    yva = (Xva[:, 1] > 10.0).astype(int)
    m = ModelFactory.create_model(model_type='pytorch', model_architecture='simple', input_size=3,
                                  device='cpu', task_type='binary_classification',
                                  simple={'layers': [4], 'dropout': 0.0, 'learning_rate': 0.01})
    m.default_epochs = 2
    m.fit(Xtr, ytr)
    im = InfluenceMethods(None, dataset_config=_Cfg())
    pipe = Pipeline([('preproc', _Id()), ('model', m)])
    meths, _ = im.setup_methods(pipe, pd.DataFrame(Xtr), pd.Series(ytr), pd.DataFrame(Xva),
                                pd.Series(yva), _Id(), methods_to_use=['LOO'])
    test_data = meths['LOO'].utility.scorer.test_data.data()
    assert np.allclose(np.asarray(test_data.x), Xva)
    assert np.array_equal(np.asarray(test_data.y).ravel(), yva)
