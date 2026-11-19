"""Quality metrics and per-sample loss used for the LossHigh/LossLow baselines."""
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)


from experiments.removal_strategies import CLASSIFICATION_TASKS


def _pred_to_labels(y_pred, task_type):
    """Приводит предсказания к меткам классов для метрик классификации."""
    if task_type not in CLASSIFICATION_TASKS:
        return y_pred
    y_pred = np.asarray(y_pred)
    if y_pred.ndim == 2 and y_pred.shape[1] > 1:
        return np.argmax(y_pred, axis=1).astype(int)
    if np.issubdtype(y_pred.dtype, np.floating) and y_pred.size > 0 and y_pred.min() >= 0 and y_pred.max() <= 1:
        return (np.asarray(y_pred).ravel() >= 0.5).astype(int)
    return np.asarray(y_pred).ravel().astype(int)


def _calculate_metric(y_true, y_pred, task_type, metric_name):
    """Значение выбранной метрики (регрессия или классификация)."""
    y_true = np.asarray(y_true).reshape(-1)
    y_pred = np.asarray(y_pred)

    if task_type in CLASSIFICATION_TASKS:
        y_pred = _pred_to_labels(y_pred, task_type)
        y_true = y_true.astype(int)

        if metric_name == 'accuracy':
            return accuracy_score(y_true, y_pred)
        if metric_name == 'f1':
            return f1_score(y_true, y_pred, average='binary', zero_division=0)
        if metric_name == 'f1_weighted':
            return f1_score(y_true, y_pred, average='weighted', zero_division=0)
        if metric_name == 'f1_macro':
            return f1_score(y_true, y_pred, average='macro', zero_division=0)
        if metric_name == 'precision':
            return precision_score(y_true, y_pred, average='binary', zero_division=0)
        if metric_name == 'recall':
            return recall_score(y_true, y_pred, average='binary', zero_division=0)
        raise ValueError(f"Unsupported classification metric: {metric_name}")

    y_pred = y_pred.reshape(-1)
    if metric_name == 'mae':
        return mean_absolute_error(y_true, y_pred)
    if metric_name == 'rmse':
        return float(np.sqrt(mean_squared_error(y_true, y_pred)))
    if metric_name == 'r2':
        return r2_score(y_true, y_pred)
    raise ValueError(f"Unsupported regression metric: {metric_name}")


def _is_better_metric(current_value, best_value, higher_is_better):
    """Сравнение метрик с учётом направления оптимизации."""
    if higher_is_better:
        return current_value > best_value
    return current_value < best_value


def compute_per_sample_loss(pipeline, X_train, y_train, task_type):
    """
    Вычисляет loss для каждого примера обучающей выборки на обученной модели.
    Используется для стратегий удаления remove_high_loss / remove_low_loss.

    - Регрессия: квадрат ошибки (y - pred)^2. Предсказания модели могут быть
      в масштабированном пространстве (если модель обучалась на scaled y),
      поэтому y масштабируется тем же способом для согласованности.
    - Классификация: кросс-энтропия по примеру (-log p_correct), при отсутствии
      predict_proba — 0/1 loss (1 при ошибке, 0 при верном предсказании).

    Returns:
        np.ndarray длины len(X_train) — loss для каждого примера.
    """
    X_tr = pipeline.named_steps['preproc'].transform(X_train)
    if hasattr(X_tr, 'toarray'):
        X_tr = X_tr.toarray()
    model = pipeline.named_steps['model']
    y_true = np.asarray(y_train).ravel() if hasattr(y_train, 'values') else np.asarray(y_train).ravel()

    if task_type == 'regression':
        y_pred = model.predict(X_tr)
        y_pred = np.asarray(y_pred).ravel()
        # В train_and_evaluate регрессия обучается на scaled y — масштабируем y_true так же.
        y_scaled = StandardScaler().fit_transform(y_true.reshape(-1, 1)).ravel()
        loss = (y_scaled - y_pred) ** 2
        return np.asarray(loss, dtype=float)

    # Классификация
    if hasattr(model, 'predict_proba'):
        proba = model.predict_proba(X_tr)
        n = len(y_true)
        y_int = np.asarray(y_true, dtype=int)
        if proba.ndim == 2 and proba.shape[1] >= 2:
            p_correct = proba[np.arange(n), y_int]
        else:
            p_correct = np.where(y_int == 1, proba.ravel(), 1 - proba.ravel())
        p_correct = np.clip(p_correct, 1e-15, 1 - 1e-15)
        return -np.log(p_correct)
    # Нет predict_proba: используем 0/1 loss (1 при ошибке)
    y_pred = model.predict(X_tr)
    y_pred = _pred_to_labels(y_pred, task_type)
    y_true_int = np.asarray(y_true, dtype=int)
    return (y_pred != y_true_int).astype(float)
