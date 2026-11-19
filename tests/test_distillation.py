"""[AUDIT-FIX D1-D4] tree-model probabilities and teacher -> student distillation."""
import numpy as np
import pytest


def _data(n=240, k=2, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 5)).astype(np.float32)
    logits = X[:, :k] @ np.eye(k) * 2.0 if k > 2 else (X[:, 0] + 0.5 * X[:, 1])[:, None]
    y = (logits.argmax(1) if k > 2 else (logits[:, 0] > 0)).astype(int)
    return X, y


def _tree(model_type, task, k):
    from models.factory import ModelFactory
    import config.settings as S
    params = dict(S.get_model_config('covertype' if k > 2 else 'adult', model_type))
    params['iterations' if model_type == 'catboost' else 'n_estimators'] = 30
    if model_type == 'catboost':
        params['allow_writing_files'] = False
    params.update(model_type=model_type, task_type=task, valuation_epochs=10, input_size=5)
    if k > 2:
        params['num_class'] = k
    return ModelFactory.create_model(**params)


@pytest.mark.parametrize('model_type', ['xgboost', 'random_forest', 'catboost'])
@pytest.mark.parametrize('k', [2, 3])
def test_tree_models_have_predict_proba(model_type, k):
    """D1 + D3: probabilities exist and sum to 1; torch-only keys do not crash CatBoost / RF."""
    task = 'multiclass_classification' if k > 2 else 'binary_classification'
    X, y = _data(k=k)
    m = _tree(model_type, task, k)
    m.fit(X, y)
    p = m.predict_proba(X)
    assert p.shape == (len(X), k)
    assert np.allclose(p.sum(1), 1.0, atol=1e-5)
    assert ((p > 1e-3) & (p < 1 - 1e-3)).mean() > 0.2          # genuinely soft


def test_proba_columns_follow_class_labels_when_a_class_is_missing():
    from models.tree_models import _sklearn_style_proba
    from sklearn.ensemble import RandomForestClassifier
    X, y = _data(k=3)
    keep = y != 1
    rf = RandomForestClassifier(n_estimators=10, random_state=0).fit(X[keep], y[keep])
    p = _sklearn_style_proba(rf, X)
    assert p.shape[1] == 3 and np.allclose(p[:, 1], 0.0)


def _distilled(model_type, task, k, epochs=300):
    from models.factory import ModelFactory
    import config.settings as S
    params = dict(S.get_model_config('covertype' if k > 2 else 'adult', model_type))
    params['iterations' if model_type == 'catboost' else 'n_estimators'] = 30
    params.update(model_type=model_type, task_type=task, input_size=5, use_distillation=True,
                  distillation_epochs=epochs, temperature=2.0, device='cpu')
    if k > 2:
        params['num_class'] = k
    return ModelFactory.create_model(**params)


def test_distillation_uses_soft_teacher_targets_for_xgboost():
    """D1: an XGBoost teacher gave hard 0/1 targets before (no predict_proba)."""
    X, y = _data()
    m = _distilled('xgboost', 'binary_classification', 2, epochs=5)
    m.fit(X, y)
    t = m._teacher_targets(X).ravel()
    assert ((t > 0.01) & (t < 0.99)).mean() > 0.2


def test_tempered_teacher_targets():
    """D2: student is trained on softmax(z/T) -> the target must be the teacher at temperature T."""
    from models.torch_models import DistilledModelWrapper
    w = DistilledModelWrapper.__new__(DistilledModelWrapper)
    w.temperature = 2.0
    p = np.array([[0.7, 0.2, 0.1]])
    q = w._soften(p)
    expect = np.sqrt(p) / np.sqrt(p).sum()
    assert np.allclose(q, expect, atol=1e-6)


def test_student_matches_teacher_probabilities_multiclass():
    """D2 end to end: after distillation the student's T=1 probabilities are close to the teacher's."""
    import torch
    torch.manual_seed(0)
    X, y = _data(n=300, k=3)
    m = _distilled('lightgbm', 'multiclass_classification', 3, epochs=800)
    m.fit(X, y)
    pt = m.base_model.predict_proba(X)
    ps = m.predict_proba(X)
    assert np.mean(np.abs(pt - ps)) < 0.08
    assert np.mean(pt.argmax(1) == ps.argmax(1)) > 0.9


def test_refit_restarts_student():
    """D4: a second fit() must start from a fresh student, not continue the old one."""
    X, y = _data()
    m = _distilled('lightgbm', 'binary_classification', 2, epochs=20)
    m.fit(X, y)
    first = m.student_model
    m.fit(X[:120], y[:120])
    assert m.student_model is not first and m.is_distilled
