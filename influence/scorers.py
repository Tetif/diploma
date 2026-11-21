"""
Scorers for pyDVL (utility u(S) = quality on the test set of a model trained on S).

[AUDIT-FIX B2] Changes compared with the old version:
- class labels come from pred_to_labels (threshold 0.5 for probabilities, argmax for
  (N, K)), not from astype(int) on probabilities (because of it F1/accuracy were always 0);
- mismatched lengths of y_true / y_pred => ValueError (previously silently truncated to min_len);
- errors are not swallowed (previously fail_score=-1e6 or 0.0 was returned => a "perfect" MAE);
- regression: the scorer returns -MAE (higher = better), as pyDVL expects for a utility.
  Hence the values of valuation methods are now always in the "higher = more valuable" convention.
"""
import numpy as np
import torch
from sklearn.metrics import f1_score, accuracy_score


def pred_to_labels(y_pred):
    """Model predictions -> class labels (same logic as runner._pred_to_labels)."""
    y_pred = np.asarray(y_pred)
    if y_pred.ndim == 2 and y_pred.shape[1] > 1:
        return np.argmax(y_pred, axis=1).astype(int)
    y_pred = y_pred.reshape(-1)
    if np.issubdtype(y_pred.dtype, np.floating) and y_pred.size > 0:
        if y_pred.min() >= 0 and y_pred.max() <= 1:
            return (y_pred >= 0.5).astype(int)
        return np.rint(y_pred).astype(int)
    return y_pred.astype(int)


def _to_numpy(a):
    return a.values if hasattr(a, "values") else np.asarray(a)


def _predict(model, x_np, classification):
    if hasattr(model, "predict"):
        return np.asarray(model.predict(x_np))
    module = getattr(model, "model", model)
    module.eval()
    with torch.no_grad():
        device = next(module.parameters()).device
        out = module(torch.FloatTensor(x_np).to(device)).cpu().numpy()
    if classification and out.ndim == 2 and out.shape[1] == 1:
        out = 1.0 / (1.0 + np.exp(-out))  # logit -> probability
    return out


def _prepare(model, x, y, classification):
    x_np = _to_numpy(x)
    y_np = _to_numpy(y).reshape(-1)
    if x_np.shape[0] == 0 or y_np.shape[0] == 0:
        raise ValueError("Scorer received an empty test set")
    y_pred = _predict(model, x_np, classification)
    if classification:
        y_pred = pred_to_labels(y_pred)
    else:
        y_pred = np.asarray(y_pred, dtype=float).reshape(-1)
    if len(y_pred) != len(y_np):
        raise ValueError(
            f"Prediction length {len(y_pred)} != target length {len(y_np)} "
            f"(model output shape/task mismatch)"
        )
    if not classification and not np.isfinite(y_pred).all():
        raise ValueError("Non-finite predictions in scorer")
    return y_np, y_pred


def make_stable_mae():
    """Return -MAE (higher = better)."""
    def neg_mae_model(model, x, y):
        y_true, y_pred = _prepare(model, x, y, classification=False)
        return -float(np.mean(np.abs(y_pred - y_true.astype(float))))
    return neg_mae_model


def make_stable_f1_scorer(average='binary'):
    def f1_model(model, x, y):
        y_true, y_pred = _prepare(model, x, y, classification=True)
        return float(f1_score(y_true.astype(int), y_pred, average=average, zero_division=0))
    return f1_model


def make_stable_accuracy_scorer():
    def accuracy_model(model, x, y):
        y_true, y_pred = _prepare(model, x, y, classification=True)
        return float(accuracy_score(y_true.astype(int), y_pred))
    return accuracy_model


def constant_predictor_score(scorer_type, y_train, y_test):
    """
    [AUDIT-FIX B4] Utility of the empty set u(empty) = quality of the constant predictor
    (median of y_train for MAE; majority class for classification). Previously it was -1e6,
    so the first point of every permutation in TMC/Shapley got a contribution of ~1e6.
    """
    y_train = _to_numpy(y_train).reshape(-1)
    y_test = _to_numpy(y_test).reshape(-1)
    if scorer_type == 'mae':
        return -float(np.mean(np.abs(y_test.astype(float) - np.median(y_train.astype(float)))))
    vals, counts = np.unique(y_train.astype(int), return_counts=True)
    pred = np.full(len(y_test), vals[np.argmax(counts)], dtype=int)
    y_test = y_test.astype(int)
    if scorer_type == 'accuracy':
        return float(accuracy_score(y_test, pred))
    average = {'f1': 'binary', 'f1_weighted': 'weighted', 'f1_macro': 'macro'}[scorer_type]
    return float(f1_score(y_test, pred, average=average, zero_division=0))


class ScorerFactory:
    """Factory that creates scorers"""

    @staticmethod
    def create_scorer(scorer_type='mae', **kwargs):
        if scorer_type == 'mae':
            return make_stable_mae()
        elif scorer_type == 'f1':
            return make_stable_f1_scorer(average='binary')
        elif scorer_type == 'f1_weighted':
            return make_stable_f1_scorer(average='weighted')
        elif scorer_type == 'f1_macro':
            return make_stable_f1_scorer(average='macro')
        elif scorer_type == 'accuracy':
            return make_stable_accuracy_scorer()
        else:
            raise ValueError(f"Unknown scorer type: {scorer_type}. Available: mae, f1, f1_weighted, f1_macro, accuracy")


__all__ = [
    'ScorerFactory',
    'make_stable_mae',
    'make_stable_f1_scorer',
    'make_stable_accuracy_scorer',
    'constant_predictor_score',
    'pred_to_labels',
]
