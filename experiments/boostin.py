"""[AUDIT-FIX P10] BoostIn (Brophy, Hammoudeh & Lowd, JMLR 2023, https://arxiv.org/abs/2205.00359) as a direct
GBDT baseline, through the authors' reference package ``tree_influence``
(https://github.com/jjbrophy47/tree_influence; installed from git, see requirements.txt).

BoostIn = TracIn for boosting: Inf(x_i, x_e) = sum_t lr * dL(y_e, f_{t-1}(x_e))/df * 1[same leaf] * dv_leaf/dw_i,
positive = removing x_i increases the test loss (helpful). Value of x_i = sum over the validation set, so
higher = more useful, as everywhere in the study.

Adapters (the package parses sklearn-API models only):
* LightGBM: our wrapper trains a native ``lgb.Booster`` (lgb.train + early stopping) -> a thin proxy with the
  attributes the parser reads (``booster_``, ``get_params``, ``classes_``, ``objective_``). The parser checks that
  the parsed ensemble reproduces the model's probabilities and prints a WARNING otherwise; we turn a mismatch
  into an error (no silent garbage).
* CatBoost: the package requires ``leaf_estimation_iterations == 1`` (one Newton step per leaf). CatBoost's
  default for Logloss / MultiClass is 10, so BoostIn is NOT applicable to our CatBoost models without changing
  them (NotApplicable); CatBoost has the LeafInfluence-type LossFunctionChange (CatBoostLFC) instead.
* XGBoost >= 2 estimates ``base_score`` from the data, the parser assumes 0 -> parsed predictions differ ->
  NotApplicable.
* Class weights ([AUDIT-FIX P8], scale_pos_weight / balanced sample weights): the package's leaf derivatives use
  unweighted gradients. We use the weighted ones for the TRAIN side (the leaf values were fit with
  w_i * g_i, w_i * h_i), the test side is the plain (unweighted) loss on the validation set.
"""
from __future__ import annotations

import contextlib
import io

import numpy as np


class BoostInNotApplicable(Exception):
    pass


class _LGBMProxy:
    """What tree_influence's LightGBM parser reads from an ``LGBMClassifier`` / ``LGBMRegressor``."""

    def __init__(self, booster, params: dict, task_type: str, n_classes: int):
        self.booster_ = booster
        self._p = params
        self.task_type = task_type
        if task_type != 'regression':
            self.classes_ = np.arange(n_classes)
        self.objective_ = {'binary_classification': 'binary', 'multiclass_classification': 'multiclass'}.get(
            task_type, 'regression')

    def __str__(self):
        return 'LGBMProxy'

    def get_params(self):
        p = self._p
        return {'reg_alpha': float(p.get('lambda_l1', p.get('reg_alpha', 0.0)) or 0.0), 'class_weight': None,
                'boosting_type': p.get('boosting_type', p.get('boosting', 'gbdt')),
                'learning_rate': float(p.get('learning_rate', 0.1)),
                'reg_lambda': float(p.get('lambda_l2', p.get('reg_lambda', 0.0)) or 0.0)}

    def predict(self, X):
        return self.booster_.predict(X)

    def predict_proba(self, X):
        p = np.asarray(self.booster_.predict(X), dtype=np.float64)
        return np.column_stack([1.0 - p, p]) if p.ndim == 1 else p


class _WeightedLoss:
    """Loss whose gradient / hessian are multiplied by per-sample weights (train side of BoostIn)."""

    def __init__(self, base, w):
        self.base, self.w = base, np.asarray(w, dtype=np.float64).reshape(-1, 1)

    def gradient(self, y, f):
        return self.base.gradient(y, f) * self.w

    def hessian(self, y, f):
        return self.base.hessian(y, f) * self.w


def _patch_sklearn_compat(ti_util):
    """tree_influence 0.1.7 calls OneHotEncoder(sparse=False) (multiclass); sklearn >= 1.4 renamed it
    sparse_output. Shim the name inside the package module only."""
    if getattr(ti_util, '_diploma_ohe_patched', False):
        return
    from sklearn.preprocessing import OneHotEncoder

    def _ohe(*a, sparse=None, **k):
        if sparse is not None:
            k.setdefault('sparse_output', sparse)
        return OneHotEncoder(*a, **k)
    ti_util.OneHotEncoder = _ohe
    ti_util._diploma_ohe_patched = True


def _sample_weights(wrapper, y, task_type) -> np.ndarray | None:
    cw = getattr(wrapper, 'class_weighting_', None) or {}
    y = np.asarray(y).astype(int).ravel()
    if 'scale_pos_weight' in cw:
        return np.where(y == 1, float(cw['scale_pos_weight']), 1.0)
    if cw.get('auto_class_weights') == 'Balanced':      # CatBoost: w_k = max_c n_c / n_k
        classes, counts = np.unique(y, return_counts=True)
        w_c = dict(zip(classes.tolist(), (counts.max() / counts).tolist()))
        return np.array([w_c[int(c)] for c in y], dtype=np.float64)
    if 'class_weights' in cw:
        return np.array([cw['class_weights'][int(c)] for c in y], dtype=np.float64)
    return None


def _explainable(wrapper, task_type: str, n_classes: int):
    """Native model in the form tree_influence parses, or BoostInNotApplicable."""
    name = type(wrapper).__name__
    if name == 'LightGBMModel':
        p = dict(wrapper.params)
        if p.get('boosting_type', p.get('boosting', 'gbdt')) != 'gbdt':
            raise BoostInNotApplicable('BoostIn supports gbdt boosting only')
        return _LGBMProxy(wrapper.model, p, task_type, n_classes)
    if name == 'CatBoostModel':
        ap = wrapper.model.get_all_params()
        if int(ap.get('leaf_estimation_iterations', 1)) != 1 or ap.get('leaf_estimation_method') != 'Newton':
            raise BoostInNotApplicable(
                f"tree_influence BoostIn needs CatBoost leaf_estimation_iterations=1 / Newton, the model has "
                f"{ap.get('leaf_estimation_iterations')} / {ap.get('leaf_estimation_method')}")
        return wrapper.model
    if name == 'XGBoostModel':
        raise BoostInNotApplicable('xgboost>=2 estimates base_score; tree_influence assumes 0 (parse mismatch)')
    raise BoostInNotApplicable(f'BoostIn is defined for GBDTs (LightGBM / CatBoost), not {name}')


def boostin_values(wrapper, X_train, y_train, X_val, y_val, task_type: str):
    """Per-train BoostIn value (sum of local influences over the validation set) and an info dict.

    X_* are the transformed (model-input) features, y_* in the model's training space."""
    try:
        from tree_influence.explainers import BoostIn
        from tree_influence.explainers.parsers import util as ti_util
    except ImportError as e:      # pragma: no cover
        raise BoostInNotApplicable(f'tree_influence is not installed ({e})')
    _patch_sklearn_compat(ti_util)
    Xtr, Xval = np.asarray(X_train, dtype=np.float64), np.asarray(X_val, dtype=np.float64)
    ytr, yval = np.asarray(y_train).ravel(), np.asarray(y_val).ravel()
    n_classes = int(len(np.unique(np.concatenate([ytr, yval])))) if task_type != 'regression' else 0
    model = _explainable(wrapper, task_type, n_classes)

    expl = BoostIn()
    out = io.StringIO()
    with contextlib.redirect_stdout(out):          # the parser reports a prediction mismatch only by print()
        expl.fit(model, Xtr, ytr)
    if 'WARNING' in out.getvalue():
        raise BoostInNotApplicable('tree_influence: parsed ensemble does not reproduce the model: '
                                   + out.getvalue().strip()[:200])
    w = _sample_weights(wrapper, ytr, task_type) if task_type != 'regression' else None
    if w is not None:
        # recompute the train-side leaf derivatives with the weighted gradients / hessians of the fit
        Xc, yc = ti_util.check_data(Xtr, ytr, objective=expl.model_.objective)
        base = expl.loss_fn_
        expl.loss_fn_ = _WeightedLoss(base, w)
        try:
            expl.train_leaf_dvs_ = expl._compute_leaf_derivatives(Xc, yc)
        finally:
            expl.loss_fn_ = base
    inf = expl.get_local_influence(Xval, yval, verbose=0)          # (n_train, n_val), positive = helpful
    v = np.asarray(inf, dtype=np.float64).sum(axis=1)
    info = {'boostin': {'package': 'tree_influence 0.1.7 (git a325794)', 'n_boost': int(expl.model_.n_boost_),
                        'weighted_train_gradients': w is not None, 'n_val': int(len(yval)),
                        'aggregation': 'sum over validation'}}
    return v, info
