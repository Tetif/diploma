"""
Скореры для pyDVL (utility u(S) = качество модели, обученной на S, на тестовом множестве).

[AUDIT-FIX B2] Изменения относительно старой версии:
- метки классов получаются через pred_to_labels (порог 0.5 для вероятностей, argmax для
  (N, K)), а не через astype(int) на вероятностях (из-за него F1/accuracy всегда были 0);
- несовпадение длин y_true / y_pred => ValueError (раньше молча обрезалось по min_len);
- ошибки не глотаются (раньше возвращался fail_score=-1e6 или 0.0 => «идеальный» MAE);
- регрессия: скорер возвращает -MAE (больше = лучше), как ожидает pyDVL для utility.
  Поэтому ценности valuation-методов теперь всегда в конвенции «больше = ценнее».
"""
import numpy as np
import torch
from sklearn.metrics import f1_score, accuracy_score


def pred_to_labels(y_pred):
    """Предсказания модели -> метки классов (та же логика, что runner._pred_to_labels)."""
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
        out = 1.0 / (1.0 + np.exp(-out))  # логит -> вероятность
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
    """Возвращает -MAE (больше = лучше)."""
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
    [AUDIT-FIX B4] Utility пустого множества u(∅) = качество константного предсказателя
    (медиана y_train для MAE; мажоритарный класс для классификации). Раньше было -1e6,
    из-за чего первая точка каждой перестановки в TMC/Shapley получала вклад ~1e6.
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
    """Фабрика для создания скореров"""

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
