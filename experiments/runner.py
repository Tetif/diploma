import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
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
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
from typing import Any, Callable, Dict, List, Optional, Tuple

from experiments.logger import debug_print
from config import settings as settings_module
from config.settings import (
    get_n_remove_list,
    get_selected_loss_removal_methods,
    get_selected_metric,
    get_metric_metadata,
    REMOVAL_ADAPTIVE_CONFIG,
)
from models.factory import ModelFactory
from influence.methods import InfluenceMethods
from utils.removal_adaptive_params import model_params_for_removal_subset

CLASSIFICATION_TASKS = ('binary_classification', 'multiclass_classification')


def target_strata_labels(y_train, n_bins: int) -> Optional[np.ndarray]:
    """
    Квантильные страты целевой переменной (регрессия): ~равные частоты по y, метки 0..k-1.
    Если разбить нельзя — None (глобальный removal без страт).
    """
    y_arr = np.asarray(
        y_train.values if hasattr(y_train, "values") else y_train,
        dtype=float,
    ).ravel()
    n = int(y_arr.size)
    if n < 4:
        return None
    nb = max(2, min(int(n_bins), n // 2))
    try:
        q = pd.qcut(
            pd.Series(y_arr),
            q=nb,
            labels=False,
            duplicates="drop",
        )
    except (ValueError, TypeError):
        return None
    arr = np.asarray(q, dtype=float)
    if np.isnan(arr).any():
        arr = np.nan_to_num(arr, nan=0.0)
    arr = arr.astype(int)
    if np.unique(arr).size < 2:
        return None
    return arr


def _allocate_proportional_n_per_class(y_arr: np.ndarray, n_to_remove: int) -> Dict[int, int]:
    """
    Распределяет n_to_remove по классам пропорционально частотам, с верхом (count_c - 1) на класс.
    """
    unique, counts = np.unique(y_arr, return_counts=True)
    n = len(y_arr)
    k = len(unique)
    if n_to_remove <= 0 or n == 0 or k == 0:
        return {}
    max_r = counts - 1
    raw = np.array([n_to_remove * int(c) / n for c in counts], dtype=float)
    floor = np.floor(raw).astype(int)
    floor = np.minimum(floor, max_r)
    short = int(n_to_remove - floor.sum())
    if short > 0:
        frac = raw - np.floor(raw)
        order = np.argsort(-frac)
        i = 0
        guard = 0
        while short > 0 and guard < k * (n + 5):
            j = int(order[i % k])
            if floor[j] < max_r[j]:
                floor[j] += 1
                short -= 1
            i += 1
            guard += 1
    elif short < 0:
        order = np.argsort(raw)
        i = 0
        guard = 0
        while short < 0 and guard < k * (n + 5):
            j = int(order[i % k])
            if floor[j] > 0:
                floor[j] -= 1
                short += 1
            i += 1
            guard += 1
    return {int(unique[i]): int(floor[i]) for i in range(k)}


def build_full_candidate_order_influence(
    asc_sorted: np.ndarray,
    strategy: str,
    n_train: int,
    n_to_remove: int,
    pct: int,
    fixed_frac: float = 0.1,
    seed_extra: int = 0,
    all_indices_scope: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    asc_sorted — глобальные индексы обучающей выборки, отсортированные по возрастанию score.
    n_train = len(asc_sorted). Для стратегий few_* all_indices_scope — индексы того же множества (глобальные).
    """
    if all_indices_scope is None:
        all_indices_scope = np.arange(n_train)
    idx_sorted = asc_sorted
    if strategy == 'highest':
        idx_sorted = asc_sorted[::-1]
    elif strategy == 'few_good_then_random':
        idx_sorted = asc_sorted[::-1]

    if strategy in ('lowest', 'highest'):
        candidate_order_base = idx_sorted
    elif strategy == 'extremes':
        left, right = 0, len(idx_sorted) - 1
        order = []
        while left <= right:
            order.append(idx_sorted[left])
            left += 1
            if left <= right:
                order.append(idx_sorted[right])
                right -= 1
        candidate_order_base = np.asarray(order, dtype=int)
    elif strategy == 'median':
        n_sorted = len(idx_sorted)
        mid = n_sorted // 2
        positions = []
        left = mid
        right = mid + 1
        if 0 <= left < n_sorted:
            positions.append(left)
        while len(positions) < n_sorted:
            if right < n_sorted:
                positions.append(right)
                right += 1
            left -= 1
            if 0 <= left < n_sorted and len(positions) < n_sorted:
                positions.append(left)
        candidate_order_base = idx_sorted[positions]
    else:
        candidate_order_base = None

    if candidate_order_base is not None:
        return candidate_order_base

    n_total = n_to_remove
    if strategy == 'few_bad_then_random':
        n_fixed = min(int(fixed_frac * n_train), n_total)
        if n_fixed <= 0:
            n_fixed = min(1, n_total)
        det_idx = idx_sorted[:n_fixed]
        remaining = np.setdiff1d(all_indices_scope, det_idx, assume_unique=True)
        np.random.seed(settings_module.RANDOM_STATE + pct + seed_extra)
        rand_order = np.random.permutation(remaining)
        return np.concatenate([det_idx, rand_order])
    if strategy == 'few_median_then_random':
        n_fixed = min(int(fixed_frac * n_train), n_total)
        if n_fixed <= 0:
            n_fixed = min(1, n_total)
        n_train_sorted = len(idx_sorted)
        mid = n_train_sorted // 2
        half = n_fixed // 2
        start = max(0, mid - half)
        end = min(n_train_sorted, start + n_fixed)
        if end - start < n_fixed:
            if start == 0:
                end = n_fixed
            else:
                start = end - n_fixed
        det_idx = idx_sorted[start:end]
        remaining = np.setdiff1d(all_indices_scope, det_idx, assume_unique=True)
        np.random.seed(settings_module.RANDOM_STATE + pct + 1000 + seed_extra)
        rand_order = np.random.permutation(remaining)
        return np.concatenate([det_idx, rand_order])
    if strategy == 'few_good_then_random':
        n_fixed = min(int(fixed_frac * n_train), n_total)
        if n_fixed <= 0:
            n_fixed = min(1, n_total)
        det_idx = idx_sorted[:n_fixed]
        remaining = np.setdiff1d(all_indices_scope, det_idx, assume_unique=True)
        np.random.seed(settings_module.RANDOM_STATE + pct + 2000 + seed_extra)
        rand_order = np.random.permutation(remaining)
        return np.concatenate([det_idx, rand_order])
    return np.array([], dtype=int)


def removal_indices_per_class_influence(
    vals: np.ndarray,
    y_train,
    strategy: str,
    n_to_remove: int,
    pct: int,
    seed_extra: int = 0,
) -> np.ndarray:
    vals = np.asarray(vals).ravel()
    y_arr = np.asarray(y_train.values if hasattr(y_train, "values") else y_train).ravel()
    alloc = _allocate_proportional_n_per_class(y_arr, n_to_remove)
    removed: List[int] = []
    for cls in np.unique(y_arr):
        n_c = int(alloc.get(int(cls), 0))
        if n_c <= 0:
            continue
        idx_local = np.where(y_arr == cls)[0]
        m = len(idx_local)
        asc_c = idx_local[np.argsort(vals[idx_local])]
        co = build_full_candidate_order_influence(
            asc_c,
            strategy,
            m,
            n_c,
            pct,
            seed_extra=int(seed_extra) + int(cls) * 17,
            all_indices_scope=idx_local,
        )
        take = co[: min(n_c, len(co))]
        removed.extend(int(i) for i in take.tolist())
    return np.asarray(removed, dtype=int)


def removal_indices_per_class_random(y_train, n_to_remove: int, run_idx: int) -> np.ndarray:
    y_arr = np.asarray(y_train.values if hasattr(y_train, "values") else y_train).ravel()
    alloc = _allocate_proportional_n_per_class(y_arr, n_to_remove)
    removed: List[int] = []
    for cls in np.unique(y_arr):
        n_c = int(alloc.get(int(cls), 0))
        if n_c <= 0:
            continue
        idx_local = np.where(y_arr == cls)[0]
        np.random.seed(settings_module.RANDOM_STATE + run_idx + int(cls) * 31)
        perm = np.random.permutation(idx_local)
        take = perm[: min(n_c, len(perm))]
        removed.extend(int(i) for i in take.tolist())
    return np.asarray(removed, dtype=int)


def removal_indices_per_class_valuation(
    vals: np.ndarray,
    y_train,
    n_to_remove: int,
    scorer_higher_is_better: bool,
    *,
    remove_smallest_first: Optional[bool] = None,
) -> np.ndarray:
    """
    Удаление по долям внутри групп (класс / страта). Порядок внутри группы:
    - remove_smallest_first is None: как для valuation — сначала наименьшие значения,
      если scorer_higher_is_better, иначе наибольшие.
    - remove_smallest_first True / False: явно (для LossLow / LossHigh по per-sample loss).
    """
    vals = np.asarray(vals).ravel()
    y_arr = np.asarray(y_train.values if hasattr(y_train, "values") else y_train).ravel()
    alloc = _allocate_proportional_n_per_class(y_arr, n_to_remove)
    removed: List[int] = []
    for cls in np.unique(y_arr):
        n_c = int(alloc.get(int(cls), 0))
        if n_c <= 0:
            continue
        idx_local = np.where(y_arr == cls)[0]
        sub = idx_local[np.argsort(vals[idx_local])]
        if remove_smallest_first is None:
            order = sub if scorer_higher_is_better else sub[::-1]
        else:
            order = sub if remove_smallest_first else sub[::-1]
        take = order[: min(n_c, len(order))]
        removed.extend(int(i) for i in take.tolist())
    return np.asarray(removed, dtype=int)


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


def _extract_catboost_model(model_wrapper):
    """Extract the actual CatBoost model from potentially wrapped model objects."""
    import catboost as cb
    _cb_types = (cb.CatBoostRegressor, cb.CatBoostClassifier, cb.CatBoost)

    inner = getattr(model_wrapper, 'model', None)
    if isinstance(inner, _cb_types):
        return inner

    base = getattr(model_wrapper, 'base_model', None)
    if base is not None:
        inner = getattr(base, 'model', None)
        if isinstance(inner, _cb_types):
            return inner

    return None


def compute_catboost_object_importance(pipeline, X_train, y_train, X_val, y_val,
                                       task_type, model_type, logger=None):
    """
    Per-sample object importance via CatBoost (LossFunctionChange paper).

    If the pipeline already contains a CatBoost model it is reused;
    otherwise a lightweight proxy CatBoost is trained on the same data.

    Sign convention (same as pyDVL influence):
      positive = helpful (removing increases loss),
      negative = harmful  (removing decreases loss).
    """
    import catboost as cb

    preproc = pipeline.named_steps['preproc']
    X_train_t = preproc.transform(X_train)
    X_val_t = preproc.transform(X_val)
    if hasattr(X_train_t, 'toarray'):
        X_train_t = X_train_t.toarray()
        X_val_t = X_val_t.toarray()
    X_train_t = np.asarray(X_train_t)
    X_val_t = np.asarray(X_val_t)

    y_train_arr = np.asarray(y_train).ravel()
    y_val_arr = np.asarray(y_val).ravel()

    if task_type == 'regression':
        y_scaler = StandardScaler()
        y_train_arr = y_scaler.fit_transform(y_train_arr.reshape(-1, 1)).ravel()
        y_val_arr = y_scaler.transform(y_val_arr.reshape(-1, 1)).ravel()

    catboost_model = None
    if model_type == 'catboost':
        catboost_model = _extract_catboost_model(pipeline.named_steps['model'])

    if catboost_model is None:
        if logger:
            logger.log_message("Training proxy CatBoost for object importance...")
        if task_type in CLASSIFICATION_TASKS:
            catboost_model = cb.CatBoostClassifier(
                iterations=500, learning_rate=0.05, depth=6,
                verbose=False, random_seed=settings_module.RANDOM_STATE,
            )
        else:
            catboost_model = cb.CatBoostRegressor(
                iterations=500, learning_rate=0.05, depth=6,
                loss_function='RMSE', verbose=False, random_seed=settings_module.RANDOM_STATE,
            )
        catboost_model.fit(X_train_t, y_train_arr, verbose=False)
        if logger:
            logger.log_message("Proxy CatBoost trained.")

    train_pool = cb.Pool(X_train_t, y_train_arr)
    val_pool = cb.Pool(X_val_t, y_val_arr)

    if logger:
        logger.log_message("Computing CatBoost object importance...")

    raw = catboost_model.get_object_importance(
        val_pool, train_pool,
        type='Average',
        update_method='AllPoints',
        thread_count=-1,
        verbose=False,
    )

    n_train = len(y_train_arr)
    if isinstance(raw, (list, tuple)) and len(raw) == 2:
        indices, scores_arr = raw
        importance = np.zeros(n_train, dtype=float)
        for idx, sc in zip(np.asarray(indices).ravel().astype(int),
                           np.asarray(scores_arr).ravel()):
            if 0 <= idx < n_train:
                importance[idx] = sc
    else:
        importance = np.asarray(raw, dtype=float).ravel()
        if importance.shape[0] != n_train:
            if logger:
                logger.log_message(
                    f"WARNING: importance length {importance.shape[0]} != n_train {n_train}"
                )
            if importance.shape[0] > n_train:
                importance = importance[:n_train]
            else:
                importance = np.pad(importance, (0, n_train - importance.shape[0]))

    if logger:
        logger.log_message(
            f"CatBoost importance: {len(importance)} samples, "
            f"min={importance.min():.6g}, max={importance.max():.6g}, "
            f"mean={importance.mean():.6g}, std={importance.std():.6g}"
        )
        logger.log_message(
            f"  Helpful (>0): {(importance > 0).sum()}, "
            f"Harmful (<0): {(importance < 0).sum()}"
        )

    return importance


class ExperimentRunner:
    """Класс для запуска экспериментов"""

    def __init__(self, logger=None):
        self.logger = logger
        self.results = {}

    @staticmethod
    def _select_indices_keep_one_per_class(candidate_order, y_train, n_to_remove,
                                           n_classes_expected=None, logger=None, context=""):
        """
        Выбирает индексы для удаления так, чтобы для каждой класса оставался
        хотя бы один пример (для задач классификации).

        Логика:
        - candidate_order задаёт приоритет удаления (от "самых худших" к "лучшим")
        - мы последовательно проходим по candidate_order и добавляем индекс в
          список удаления только если после этого в классе останется >= 1 объект.
        - если constraint не позволяет удалить все n_to_remove объектов,
          удаляем меньше и при наличии logger пишем предупреждение.
        """
        candidate_order = np.asarray(candidate_order, dtype=int)
        if n_to_remove <= 0 or candidate_order.size == 0:
            return np.array([], dtype=int)

        # Для регрессии или когда не требуется сохранять все классы — возвращаем
        # первые n_to_remove индексов как есть.
        if n_classes_expected is None:
            return candidate_order[:n_to_remove]

        # Преобразуем метки в массив и считаем количество примеров каждого класса.
        y_arr = np.asarray(y_train.values if hasattr(y_train, "values") else y_train).ravel()
        unique_classes, counts = np.unique(y_arr, return_counts=True)
        class_counts = dict(zip(unique_classes, counts))
        removed_per_class = {cls: 0 for cls in unique_classes}

        selected = []
        for idx in candidate_order:
            if len(selected) >= n_to_remove:
                break
            cls = y_arr[idx]
            remaining = class_counts[cls] - removed_per_class[cls]
            # Если удаление этого объекта сделает класс пустым — пропускаем его.
            if remaining <= 1:
                continue
            selected.append(idx)
            removed_per_class[cls] += 1

        selected = np.asarray(selected, dtype=int)
        if logger is not None and selected.size < n_to_remove and n_to_remove > 0:
            logger.log_message(
                f"  [WARN] {context}: could only remove {selected.size}/{n_to_remove} "
                f"sample(s) without removing the last sample of some class"
            )
        return selected

    def train_and_evaluate(self, preprocessor, model_params, X_train, y_train, X_test, y_test, X_val, y_val, n_epochs=50, _run_seed=None):
        """Обучение и оценка модели"""
        # Сброс seed перед каждым созданием/обучением модели для детерминированности.
        # Это устраняет шум от случайной инициализации весов: разные подвыборки дают
        # разные результаты только из-за данных, а не из-за ГПСЧ.
        from utils.helpers import set_random_seeds
        seed = _run_seed if _run_seed is not None else settings_module.RANDOM_STATE
        set_random_seeds(seed)

        if self.logger:
            self.logger.start_timing("model_training")

        # Подготовка данных
        if not preprocessor.is_fitted:
            preprocessor.fit(X_train)
        X_train_transformed = preprocessor.transform(X_train)
        X_test_transformed = preprocessor.transform(X_test)

        if hasattr(X_train_transformed, 'toarray'):
            X_train_transformed = X_train_transformed.toarray()
            X_test_transformed = X_test_transformed.toarray()

        available_metrics = model_params.get('available_metrics')
        # Параметры, не относящиеся к самой модели, не передаём в фабрику
        model_creation_params = {
            k: v
            for k, v in model_params.items()
            if k not in (
                'available_metrics',
                'removal_strategy',
                'removal_strategies',
                'removal_per_class',
                'removal_stratify_target',
                'removal_stratify_n_bins',
                'distillation_patience',
                'distillation_min_delta',
            )
        }

        # Создание модели
        model = ModelFactory.create_model(**model_creation_params)
        task_type = model_params.get('task_type', 'regression')
        metric_name = get_selected_metric(task_type, available_metrics)
        metric_meta = get_metric_metadata(metric_name)
        metric_short_label = metric_meta['short_label_ru']
        metric_label_ru = metric_meta['label_ru']
        higher_is_better = metric_meta['higher_is_better']

        # Для регрессии: масштабируем таргет, чтобы MSE/loss был в разумном диапазоне (особенно для Housing и т.п.)
        y_train_vals = np.asarray(y_train.values).reshape(-1, 1)
        y_test_vals = np.asarray(y_test.values).reshape(-1, 1)
        y_val_vals = np.asarray(y_val.values).reshape(-1, 1) if hasattr(y_val, 'values') else np.asarray(y_val).reshape(-1, 1)
        y_scaler = None
        if task_type == 'regression':
            y_scaler = StandardScaler()
            y_scaler.fit(y_train_vals)
            y_train_vals = y_scaler.transform(y_train_vals).ravel()
            y_test_vals = y_scaler.transform(y_test_vals).ravel()
        else:
            y_train_vals = y_train_vals.ravel()
            y_test_vals = y_test_vals.ravel()

        history = {
            'train': [],
            'val': [],
            'best_epoch': 0,
            'metric_name': metric_name,
            'metric_short_label_ru': metric_short_label,
            'metric_label_ru': metric_label_ru,
            'higher_is_better': higher_is_better,
            'best_val_metric': float('-inf') if higher_is_better else float('inf'),
        }

        # Обучение модели
        if model_params.get('model_type') == 'pytorch':
            best_model_weights = None
            patience = 70  # Early stopping patience
            patience_counter = 0

            for epoch in range(n_epochs):
                train_loss = model.fit(X_train_transformed, y_train_vals, epochs=1)
                history['train'].append(train_loss)

                y_pred_test = model.predict(X_test_transformed)
                if y_scaler is not None:
                    y_pred_test = y_scaler.inverse_transform(np.asarray(y_pred_test).reshape(-1, 1)).ravel()
                val_metric = _calculate_metric(y_test.values, y_pred_test, task_type, metric_name)
                history['val'].append(val_metric)
                
                # Update learning rate scheduler based on validation loss
                if hasattr(model, 'scheduler'):
                    scheduler_value = -val_metric if higher_is_better else val_metric
                    model.scheduler.step(scheduler_value)

                if _is_better_metric(val_metric, history['best_val_metric'], higher_is_better):
                    history['best_val_metric'] = val_metric
                    history['best_epoch'] = epoch
                    patience_counter = 0  # Reset patience counter

                    if hasattr(model, 'model'):
                        best_model_weights = {
                            name: param.clone() for name, param in model.model.state_dict().items()
                        }
                else:
                    patience_counter += 1

                if (epoch + 1) % 10 == 0 and self.logger:
                    if settings_module.DEBUG_MODE:
                        self.logger.log_message(
                            f"Epoch {epoch + 1}/{n_epochs} - Train Loss: {train_loss:.4f} - "
                            f"Val {metric_short_label}: {val_metric:.4f} "
                            f"(Best: {history['best_val_metric']:.4f} at epoch {history['best_epoch'] + 1})"
                        )

                # Early stopping
                if patience_counter >= patience:
                    if self.logger and settings_module.DEBUG_MODE:
                        self.logger.log_message(f"Early stopping at epoch {epoch + 1} (patience {patience} exceeded)")
                    break

            if best_model_weights is not None and hasattr(model, 'model'):
                model.model.load_state_dict(best_model_weights)
                if self.logger and settings_module.DEBUG_MODE:
                    self.logger.log_message(f"Loaded best PyTorch model from epoch {history['best_epoch'] + 1}")

        else:
            # Для tree-based моделей и дистиллированных моделей
            tree_fit_kw = {}
            if model_params.get('use_distillation'):
                if model_params.get('distillation_patience') is not None:
                    tree_fit_kw['distillation_patience'] = int(model_params['distillation_patience'])
                if model_params.get('distillation_min_delta') is not None:
                    tree_fit_kw['distillation_min_delta'] = float(model_params['distillation_min_delta'])
            if model_params.get('model_type') == 'lightgbm' or model_params.get('use_distillation', False):
                train_loss = model.fit(
                    X_train_transformed,
                    y_train_vals,
                    X_val=X_test_transformed,
                    y_val=y_test_vals,
                    **tree_fit_kw,
                )
            else:
                train_loss = model.fit(X_train_transformed, y_train_vals)

            history['train'].append(train_loss)

            y_pred_test = model.predict(X_test_transformed)
            if y_scaler is not None:
                y_pred_test = y_scaler.inverse_transform(np.asarray(y_pred_test).reshape(-1, 1)).ravel()
            y_pred_test = _pred_to_labels(y_pred_test, task_type) if task_type in CLASSIFICATION_TASKS else y_pred_test
            test_metric = _calculate_metric(y_test.values, y_pred_test, task_type, metric_name)
            history['val'].append(test_metric)
            history['best_val_metric'] = test_metric
            history['best_epoch'] = 0

        # Финальная оценка на валидационном множестве
        X_final_transformed = preprocessor.transform(X_val)
        if hasattr(X_final_transformed, 'toarray'):
            X_final_transformed = X_final_transformed.toarray()
        y_pred_final = model.predict(X_final_transformed)
        if y_scaler is not None:
            y_pred_final = y_scaler.inverse_transform(np.asarray(y_pred_final).reshape(-1, 1)).ravel()
        if task_type in CLASSIFICATION_TASKS:
            y_pred_final = _pred_to_labels(y_pred_final, task_type)
        y_val_flat = y_val.values if hasattr(y_val, 'values') else np.asarray(y_val).ravel()
        history['final_metric'] = _calculate_metric(y_val_flat, y_pred_final, task_type, metric_name)
        history['best_val_mae'] = history['best_val_metric']
        history['final_mae'] = history['final_metric']

        if self.logger:
            self.logger.end_timing("model_training")

        return history, model, y_scaler

    def _train_best_of_n(self, preprocessor, model_params, X_sub, y_sub,
                         X_test, y_test, X_val, y_val, n_epochs, n_retrain_runs,
                         higher_is_better):
        """
        Запускает train_and_evaluate до n_retrain_runs раз с разными seed,
        возвращает историю с наилучшим final_metric. Реализует идею "kill bad runs".
        Применяется только для PyTorch (tree-модели детерминированы при fixed random_state).
        """
        best_history = None
        is_pytorch = model_params.get('model_type') == 'pytorch'

        if not is_pytorch or n_retrain_runs <= 1:
            history, _, _ = self.train_and_evaluate(preprocessor, model_params,
                                                     X_sub, y_sub, X_test, y_test,
                                                     X_val, y_val, n_epochs)
            return history

        for run_i in range(n_retrain_runs):
            run_seed = settings_module.RANDOM_STATE + run_i * 1000
            history, _, _ = self.train_and_evaluate(preprocessor, model_params,
                                                     X_sub, y_sub, X_test, y_test,
                                                     X_val, y_val, n_epochs,
                                                     _run_seed=run_seed)
            metric = history.get('final_metric', history.get('final_mae'))
            if metric is None:
                continue
            if best_history is None:
                best_history = history
            else:
                prev_metric = best_history.get('final_metric', best_history.get('final_mae'))
                if higher_is_better and metric > prev_metric:
                    best_history = history
                elif not higher_is_better and metric < prev_metric:
                    best_history = history

        return best_history if best_history is not None else history

    def _train_best_of_n_with_model(
        self,
        preprocessor,
        model_params,
        X_sub,
        y_sub,
        X_test,
        y_test,
        X_val,
        y_val,
        n_epochs,
        n_retrain_runs,
        higher_is_better,
    ):
        """
        Версия best-of-N, которая возвращает (history, model, y_scaler) лучшего запуска.
        Нужна для baseline, чтобы сравнение с removal-кривыми было в одинаковом режиме.
        """
        is_pytorch = model_params.get('model_type') == 'pytorch'
        if not is_pytorch or n_retrain_runs <= 1:
            return self.train_and_evaluate(
                preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
            )

        best_tuple = None
        fallback_tuple = None
        for run_i in range(n_retrain_runs):
            run_seed = settings_module.RANDOM_STATE + run_i * 1000
            run_tuple = self.train_and_evaluate(
                preprocessor,
                model_params,
                X_sub,
                y_sub,
                X_test,
                y_test,
                X_val,
                y_val,
                n_epochs,
                _run_seed=run_seed,
            )
            fallback_tuple = run_tuple
            history = run_tuple[0]
            metric = history.get('final_metric', history.get('final_mae'))
            if metric is None:
                continue
            if best_tuple is None:
                best_tuple = run_tuple
            else:
                prev_metric = best_tuple[0].get('final_metric', best_tuple[0].get('final_mae'))
                if higher_is_better and metric > prev_metric:
                    best_tuple = run_tuple
                elif not higher_is_better and metric < prev_metric:
                    best_tuple = run_tuple

        if best_tuple is not None:
            return best_tuple
        return fallback_tuple

    def _run_removal_phase(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
        X_val,
        y_val,
        preprocessor,
        model_params,
        scores: Dict[str, Any],
        n_remove_list: List[int],
        n_epochs: int,
        dataset_config,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
        n_random_runs: Optional[int] = None,
        removal_adaptive_model: bool = False,
    ) -> None:
        """
        Removal curves + random baseline. Requires self.results['orig'] (baseline history).
        Mutates self.results and self.random_run_results.
        """
        n_train_full = len(X_train)

        def _mp_for_subset(y_sub):
            return model_params_for_removal_subset(
                model_params,
                n_train_full,
                len(y_sub),
                y_sub,
                removal_adaptive_model,
                REMOVAL_ADAPTIVE_CONFIG,
            )

        removal_strategies = model_params.get('removal_strategies')
        if not removal_strategies:
            legacy = model_params.get('removal_strategy')
            if legacy == 'remove_lowest_influence':
                removal_strategies = ['lowest']
            elif legacy == 'remove_highest_influence':
                removal_strategies = ['highest']
            else:
                removal_strategies = list(settings_module.REMOVAL_STRATEGIES)
        seen = set()
        removal_strategies = [s for s in removal_strategies if not (s in seen or seen.add(s))]
        influence_strategies = [s for s in removal_strategies if s != 'random']
        if not influence_strategies:
            influence_strategies = ['lowest']
        include_random_baseline = 'random' in removal_strategies

        task_type = model_params.get('task_type', 'regression')
        available_metrics = model_params.get('available_metrics')
        _metric_name = get_selected_metric(task_type, available_metrics)
        scorer_higher_is_better = get_metric_metadata(_metric_name)['higher_is_better']

        n_retrain_runs = settings_module.EXPERIMENT_CONFIG.get('n_retrain_runs', 1)

        n_classes_expected = None
        if dataset_config and dataset_config.task_type in ['binary_classification', 'multiclass_classification']:
            n_classes_expected = int(y_train.nunique())

        removal_per_class = bool(model_params.get('removal_per_class', False))
        if task_type not in CLASSIFICATION_TASKS:
            removal_per_class = False

        removal_stratify_target = bool(model_params.get('removal_stratify_target', False))
        if task_type != 'regression':
            removal_stratify_target = False
        strata_labels: Optional[np.ndarray] = None
        n_strata_expected: Optional[int] = None
        if removal_stratify_target:
            nb = int(model_params.get('removal_stratify_n_bins', 10) or 10)
            strata_labels = target_strata_labels(y_train, nb)
            if strata_labels is not None:
                n_strata_expected = int(np.unique(strata_labels).size)
                if n_strata_expected < 2:
                    strata_labels = None
                    n_strata_expected = None
            if strata_labels is None and self.logger:
                self.logger.log_message(
                    "[WARN] removal_stratify_target: не удалось построить страты по y, используется глобальный removal."
                )

        if self.logger and removal_per_class and n_classes_expected:
            self.logger.log_message(
                "[OK] removal_per_class=True: ранжирование и доля удалений по каждому классу отдельно."
            )
        if self.logger and strata_labels is not None and n_strata_expected:
            self.logger.log_message(
                f"[OK] removal_stratify_target=True: ранжирование и доля удалений по стратам целевой "
                f"(квантильные бины, {n_strata_expected} страт)."
            )

        if self.logger:
            self.logger.log_message("[OK] Starting removal experiments (by method, strategy and percentage).")
        methods_items = list(scores.items())
        influence_method_names = ['Influence', 'ArnoldiInfluence', 'CgInfluence', 'LissaInfluence', 'NystroemSketchInfluence', 'CatBoostInfluence']
        n_influence_methods = sum(1 for name, _ in methods_items if name in influence_method_names)
        n_non_influence_methods = len(methods_items) - n_influence_methods
        total_series = n_non_influence_methods + n_influence_methods * len(influence_strategies)
        total_removal_steps = total_series * len(n_remove_list)
        pbar_methods = tqdm(total=total_removal_steps, desc="Removal (method %)", unit="step")

        removal_done = [0]

        def _m_update():
            pbar_methods.update(1)
            removal_done[0] += 1
            if progress_callback:
                progress_callback({
                    "kind": "removal_step",
                    "done": removal_done[0],
                    "total": max(int(total_removal_steps), 1),
                })

        if progress_callback:
            progress_callback({
                "kind": "phase",
                "phase": "removal_loop",
                "total_steps": int(total_removal_steps),
            })

        for method, vals in methods_items:
            if self.logger:
                self.logger.log_message(f"\nProcessing method: {method}")

            is_influence_method = method in influence_method_names

            if is_influence_method:
                for strategy in influence_strategies:
                    if strategy == 'lowest':
                        plot_method = f"{method}_lowest"
                        idx_sorted = np.argsort(vals)
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'lowest' for {method}: remove lowest influence first")
                    elif strategy == 'highest':
                        plot_method = f"{method}_highest"
                        idx_sorted = np.argsort(vals)[::-1]
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'highest' for {method}: remove highest influence first")
                    elif strategy == 'extremes':
                        plot_method = f"{method}_extremes"
                        idx_sorted = np.argsort(vals)
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'extremes' for {method}: remove both lowest and highest influence")
                    elif strategy == 'median':
                        plot_method = f"{method}_median"
                        idx_sorted = np.argsort(vals)
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'median' for {method}: remove around median influence")
                    elif strategy == 'few_bad_then_random':
                        plot_method = f"{method}_few_bad_rand"
                        idx_sorted = np.argsort(vals)
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'few_bad_then_random' for {method}")
                    elif strategy == 'few_median_then_random':
                        plot_method = f"{method}_few_median_rand"
                        idx_sorted = np.argsort(vals)
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'few_median_then_random' for {method}")
                    elif strategy == 'few_good_then_random':
                        plot_method = f"{method}_few_good_rand"
                        idx_sorted = np.argsort(vals)[::-1]
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'few_good_then_random' for {method}")
                    else:
                        if self.logger:
                            self.logger.log_message(f"  Unknown strategy '{strategy}' for {method}, skipping")
                        continue

                    n_train = len(X_train)
                    all_indices = np.arange(n_train)

                    if strategy in ('lowest', 'highest'):
                        candidate_order_base = idx_sorted
                    elif strategy == 'extremes':
                        left, right = 0, len(idx_sorted) - 1
                        order = []
                        while left <= right:
                            order.append(idx_sorted[left])
                            left += 1
                            if left <= right:
                                order.append(idx_sorted[right])
                                right -= 1
                        candidate_order_base = np.asarray(order, dtype=int)
                    elif strategy == 'median':
                        n_sorted = len(idx_sorted)
                        mid = n_sorted // 2
                        positions = []
                        left = mid
                        right = mid + 1
                        if 0 <= left < n_sorted:
                            positions.append(left)
                        while len(positions) < n_sorted:
                            if right < n_sorted:
                                positions.append(right)
                                right += 1
                            left -= 1
                            if 0 <= left < n_sorted and len(positions) < n_sorted:
                                positions.append(left)
                        candidate_order_base = idx_sorted[positions]
                    else:
                        candidate_order_base = None

                    self.results[f'{plot_method}_0'] = self.results['orig']

                    fixed_frac = 0.1

                    for pct in n_remove_list:
                        pbar_methods.set_postfix_str(f"{plot_method} {pct}%", refresh=True)

                        n_to_remove = int(n_train * pct / 100)
                        n_to_remove = max(1, n_to_remove)
                        n_to_remove = min(n_to_remove, n_train - 10)

                        if candidate_order_base is not None:
                            candidate_order = candidate_order_base
                        elif strategy == 'few_bad_then_random':
                            n_total = n_to_remove
                            n_fixed = min(int(fixed_frac * n_train), n_total)
                            if n_fixed <= 0:
                                n_fixed = min(1, n_total)
                            det_idx = idx_sorted[:n_fixed]
                            remaining = np.setdiff1d(all_indices, det_idx, assume_unique=True)
                            np.random.seed(settings_module.RANDOM_STATE + pct)
                            rand_order = np.random.permutation(remaining)
                            candidate_order = np.concatenate([det_idx, rand_order])
                        elif strategy == 'few_median_then_random':
                            n_total = n_to_remove
                            n_fixed = min(int(fixed_frac * n_train), n_total)
                            if n_fixed <= 0:
                                n_fixed = min(1, n_total)
                            n_train_sorted = len(idx_sorted)
                            mid = n_train_sorted // 2
                            half = n_fixed // 2
                            start = max(0, mid - half)
                            end = min(n_train_sorted, start + n_fixed)
                            if end - start < n_fixed:
                                if start == 0:
                                    end = n_fixed
                                else:
                                    start = end - n_fixed
                            det_idx = idx_sorted[start:end]
                            remaining = np.setdiff1d(all_indices, det_idx, assume_unique=True)
                            np.random.seed(settings_module.RANDOM_STATE + pct + 1000)
                            rand_order = np.random.permutation(remaining)
                            candidate_order = np.concatenate([det_idx, rand_order])
                        elif strategy == 'few_good_then_random':
                            n_total = n_to_remove
                            n_fixed = min(int(fixed_frac * n_train), n_total)
                            if n_fixed <= 0:
                                n_fixed = min(1, n_total)
                            det_idx = idx_sorted[:n_fixed]
                            remaining = np.setdiff1d(all_indices, det_idx, assume_unique=True)
                            np.random.seed(settings_module.RANDOM_STATE + pct + 2000)
                            rand_order = np.random.permutation(remaining)
                            candidate_order = np.concatenate([det_idx, rand_order])
                        else:
                            candidate_order = np.array([], dtype=int)

                        if removal_per_class and n_classes_expected:
                            remove_idx = removal_indices_per_class_influence(
                                np.asarray(vals).ravel(),
                                y_train,
                                strategy,
                                n_to_remove,
                                pct,
                                seed_extra=sum(ord(c) for c in plot_method) % 100000,
                            )
                        elif strata_labels is not None:
                            remove_idx = removal_indices_per_class_influence(
                                np.asarray(vals).ravel(),
                                strata_labels,
                                strategy,
                                n_to_remove,
                                pct,
                                seed_extra=sum(ord(c) for c in plot_method) % 100000,
                            )
                        else:
                            remove_idx = self._select_indices_keep_one_per_class(
                                candidate_order,
                                y_train,
                                n_to_remove,
                                n_classes_expected=n_classes_expected,
                                logger=self.logger,
                                context=f"{plot_method} {pct}%"
                            )

                        keep_mask = np.ones(n_train, dtype=bool)
                        keep_mask[remove_idx] = False

                        X_sub, y_sub = X_train.iloc[keep_mask], y_train.iloc[keep_mask]

                        if len(X_sub) < 10:
                            if self.logger:
                                self.logger.log_message(f"  Skipping - only {len(X_sub)} samples left (min 10 required)")
                            _m_update()
                            continue

                        if n_classes_expected is not None:
                            unique_in_sub = y_sub.nunique()
                            if unique_in_sub < n_classes_expected:
                                if self.logger:
                                    self.logger.log_message(
                                        f"  Skipping pct={pct} - only {unique_in_sub} class(es) remaining (need all {n_classes_expected})"
                                    )
                                _m_update()
                                continue
                        if n_strata_expected is not None and strata_labels is not None:
                            kept_str = strata_labels[keep_mask]
                            if np.unique(kept_str).size < n_strata_expected:
                                if self.logger:
                                    self.logger.log_message(
                                        f"  Skipping pct={pct} - not all target strata represented after removal"
                                    )
                                _m_update()
                                continue

                        key = f'{plot_method}_{pct}pct'
                        history = self._train_best_of_n(
                            preprocessor,
                            _mp_for_subset(y_sub),
                            X_sub,
                            y_sub,
                            X_test,
                            y_test,
                            X_val,
                            y_val,
                            n_epochs,
                            n_retrain_runs,
                            scorer_higher_is_better,
                        )
                        self.results[key] = history
                        _m_update()
            else:
                plot_method = method
                self.results[f'{plot_method}_0'] = self.results['orig']

                loss_remove_smallest_first: Optional[bool] = None
                if method == 'LossHigh':
                    idx_sorted = np.argsort(vals)[::-1]
                    loss_remove_smallest_first = False
                    if self.logger:
                        self.logger.log_message(f"  LossHigh: remove highest loss first")
                elif method == 'LossLow':
                    idx_sorted = np.argsort(vals)
                    loss_remove_smallest_first = True
                    if self.logger:
                        self.logger.log_message(f"  LossLow: remove lowest loss first")
                else:
                    if scorer_higher_is_better:
                        idx_sorted = np.argsort(vals)
                    else:
                        idx_sorted = np.argsort(vals)[::-1]
                    if self.logger:
                        self.logger.log_message(
                            f"  Valuation method {method}: remove {'lowest' if scorer_higher_is_better else 'highest'} first "
                            f"(scorer_higher_is_better={scorer_higher_is_better})"
                        )

                for pct in n_remove_list:
                    pbar_methods.set_postfix_str(f"{plot_method} {pct}%", refresh=True)

                    n_to_remove = int(len(X_train) * pct / 100)
                    n_to_remove = max(1, n_to_remove)
                    n_to_remove = min(n_to_remove, len(X_train) - 10)

                    candidate_order = idx_sorted
                    if removal_per_class and n_classes_expected:
                        remove_idx = removal_indices_per_class_valuation(
                            np.asarray(vals).ravel(),
                            y_train,
                            n_to_remove,
                            scorer_higher_is_better,
                            remove_smallest_first=loss_remove_smallest_first,
                        )
                    elif strata_labels is not None:
                        remove_idx = removal_indices_per_class_valuation(
                            np.asarray(vals).ravel(),
                            strata_labels,
                            n_to_remove,
                            scorer_higher_is_better,
                            remove_smallest_first=loss_remove_smallest_first,
                        )
                    else:
                        remove_idx = self._select_indices_keep_one_per_class(
                            candidate_order,
                            y_train,
                            n_to_remove,
                            n_classes_expected=n_classes_expected,
                            logger=self.logger,
                            context=f"{plot_method} {pct}%"
                        )
                    keep_mask = np.ones(len(X_train), dtype=bool)
                    keep_mask[remove_idx] = False

                    X_sub, y_sub = X_train.iloc[keep_mask], y_train.iloc[keep_mask]

                    if len(X_sub) < 10:
                        if self.logger:
                            self.logger.log_message(f"  Skipping - only {len(X_sub)} samples left (min 10 required)")
                        _m_update()
                        continue

                    if n_classes_expected is not None:
                        unique_in_sub = y_sub.nunique()
                        if unique_in_sub < n_classes_expected:
                            if self.logger:
                                self.logger.log_message(
                                    f"  Skipping pct={pct} - only {unique_in_sub} class(es) remaining (need all {n_classes_expected})"
                                )
                            _m_update()
                            continue
                    if n_strata_expected is not None and strata_labels is not None:
                        kept_str = strata_labels[keep_mask]
                        if np.unique(kept_str).size < n_strata_expected:
                            if self.logger:
                                self.logger.log_message(
                                    f"  Skipping pct={pct} - not all target strata represented after removal"
                                )
                            _m_update()
                            continue

                    key = f'{plot_method}_{pct}pct'
                    history = self._train_best_of_n(
                        preprocessor,
                        _mp_for_subset(y_sub),
                        X_sub,
                        y_sub,
                        X_test,
                        y_test,
                        X_val,
                        y_val,
                        n_epochs,
                        n_retrain_runs,
                        scorer_higher_is_better,
                    )
                    self.results[key] = history
                    _m_update()

        pbar_methods.close()
        if self.logger:
            self.logger.log_message("[OK] Removal experiments (all methods and percentages) completed.")

        random_run_results: Dict[Any, Any] = {}
        self.random_run_results = random_run_results
        n_rand = n_random_runs if n_random_runs is not None else settings_module.EXPERIMENT_CONFIG['n_random_runs']
        if include_random_baseline:
            if self.logger:
                self.logger.log_message("Processing random removal")

            total_random_steps = n_rand * len(n_remove_list)
            pbar_random = tqdm(total=total_random_steps, desc="Random removal (run %)", unit="step")

            random_done = [0]

            def _r_update():
                pbar_random.update(1)
                random_done[0] += 1
                if progress_callback:
                    progress_callback({
                        "kind": "random_step",
                        "done": random_done[0],
                        "total": max(int(total_random_steps), 1),
                    })

            if progress_callback:
                progress_callback({
                    "kind": "phase",
                    "phase": "random_removal",
                    "total_steps": int(total_random_steps),
                })

            for run_idx in range(n_rand):
                if self.logger:
                    self.logger.log_message(f"  Random removal run {run_idx + 1}/{n_rand}...")

                for pct in n_remove_list:
                    pbar_random.set_postfix_str(f"run {run_idx + 1} {pct}%", refresh=True)

                    n_to_remove = int(len(X_train) * pct / 100)
                    n_to_remove = max(1, n_to_remove)
                    n_to_remove = min(n_to_remove, len(X_train) - 10)

                    np.random.seed(settings_module.RANDOM_STATE + run_idx)
                    candidate_order = np.random.permutation(len(X_train))
                    if removal_per_class and n_classes_expected:
                        remove_idx = removal_indices_per_class_random(
                            y_train, n_to_remove, run_idx
                        )
                    elif strata_labels is not None:
                        remove_idx = removal_indices_per_class_random(
                            strata_labels, n_to_remove, run_idx
                        )
                    else:
                        remove_idx = self._select_indices_keep_one_per_class(
                            candidate_order,
                            y_train,
                            n_to_remove,
                            n_classes_expected=n_classes_expected,
                            logger=self.logger,
                            context=f"random run {run_idx + 1} {pct}%"
                        )
                    keep_mask = np.ones(len(X_train), dtype=bool)
                    keep_mask[remove_idx] = False
                    X_sub, y_sub = X_train.iloc[keep_mask], y_train.iloc[keep_mask]

                    if len(X_sub) < 10:
                        _r_update()
                        continue

                    if n_classes_expected is not None and y_sub.nunique() < n_classes_expected:
                        _r_update()
                        continue
                    if (
                        n_strata_expected is not None
                        and strata_labels is not None
                        and np.unique(strata_labels[keep_mask]).size < n_strata_expected
                    ):
                        _r_update()
                        continue

                    key = f'random_{pct}pct_run{run_idx}'
                    history = self._train_best_of_n(
                        preprocessor,
                        _mp_for_subset(y_sub),
                        X_sub,
                        y_sub,
                        X_test,
                        y_test,
                        X_val,
                        y_val,
                        n_epochs,
                        n_retrain_runs,
                        scorer_higher_is_better,
                    )
                    self.results[key] = history

                    if pct not in random_run_results:
                        random_run_results[pct] = []
                    random_run_results[pct].append(history['final_mae'])
                    _r_update()

            pbar_random.close()
            if self.logger:
                self.logger.log_message("[OK] Random removal runs completed.")

            self.random_run_results = random_run_results

            for pct, mae_values in random_run_results.items():
                if mae_values:
                    median_mae = np.median(mae_values)
                    key = f'random_{pct}pct'
                    self.results[key] = {'final_mae': median_mae}

        if self.logger:
            self.logger.log_message("All experiments completed!")

    def run_removal_only(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
        X_val,
        y_val,
        preprocessor,
        model_params,
        scores: Dict[str, Any],
        baseline_history: Dict[str, Any],
        n_remove_list=None,
        n_epochs: int = 50,
        dataset_config=None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
        n_random_runs: Optional[int] = None,
        removal_adaptive_model: bool = False,
    ) -> Tuple[Dict[str, Any], Dict[str, Any], None, Dict[Any, Any]]:
        """
        Removal phase only, using precomputed influence scores (e.g. loaded from parent experiment).
        baseline_history must match the baseline from the same train split (typically parent's orig).
        """
        if n_remove_list is None:
            n_remove_list = get_n_remove_list()
        self.results = {}
        self.results['orig'] = baseline_history
        self._run_removal_phase(
            X_train,
            y_train,
            X_test,
            y_test,
            X_val,
            y_val,
            preprocessor,
            model_params,
            scores,
            n_remove_list,
            n_epochs,
            dataset_config,
            progress_callback,
            n_random_runs=n_random_runs,
            removal_adaptive_model=removal_adaptive_model,
        )
        return self.results, scores, None, self.random_run_results

    def run_experiments(self, X_train, y_train, X_test, y_test, X_val, y_val,
                        preprocessor, model_params,
                        n_remove_list=None,
                        n_epochs=50,
                        dataset_config=None,
                        selected_methods=None,
                        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
                        run_mode: str = "full",
                        removal_adaptive_model: bool = False,
                        ):
        """Запуск экспериментов с удалением данных. run_mode: full | influence_only."""
        if self.logger:
            self.logger.log_message("Starting experiments...")

        if n_remove_list is None:
            n_remove_list = get_n_remove_list()

        if progress_callback:
            progress_callback({"kind": "phase", "phase": "baseline_train"})

        task_type = model_params.get('task_type', 'regression')
        available_metrics = model_params.get('available_metrics')
        metric_name = get_selected_metric(task_type, available_metrics)
        higher_is_better = get_metric_metadata(metric_name)['higher_is_better']
        n_retrain_runs = settings_module.EXPERIMENT_CONFIG.get('n_retrain_runs', 1)

        history, model, y_scaler = self._train_best_of_n_with_model(
            preprocessor,
            model_params,
            X_train,
            y_train,
            X_test,
            y_test,
            X_val,
            y_val,
            n_epochs,
            n_retrain_runs,
            higher_is_better,
        )
        self.results['orig'] = history
        if self.logger:
            self.logger.log_message("[OK] Model training and evaluation completed.")

        if progress_callback:
            progress_callback({"kind": "phase", "phase": "baseline_done"})

        pipeline = Pipeline([
            ('preproc', preprocessor),
            ('model', model)
        ])
        if self.logger:
            self.logger.log_message("[OK] Pipeline created (preprocessor + model).")

        if progress_callback:
            progress_callback({"kind": "phase", "phase": "influence_setup"})

        # Настройка методов влияния
        influence_methods = InfluenceMethods(self.logger, dataset_config=dataset_config)
        methods, _ = influence_methods.setup_methods(pipeline, X_train, y_train,
                                                     X_test, y_test, preprocessor, methods_to_use=selected_methods)
        if self.logger:
            self.logger.log_message("[OK] Influence methods configured.")

        if progress_callback:
            progress_callback({"kind": "phase", "phase": "influence_compute"})

        # Вычисление influence scores
        scores, scores_raw = influence_methods.compute_scores(methods, X_train, y_train,
                                                              preprocessor, X_test, y_test, pipeline,
                                                              y_scaler=y_scaler)
        if self.logger:
            self.logger.log_message("[OK] Influence scores computed.")

        if progress_callback:
            progress_callback({"kind": "phase", "phase": "influence_scores_done"})

        top_bottom_n = settings_module.EXPERIMENT_CONFIG.get('show_top_bottom_influence', 0)
        if dataset_config is not None:
            ds_tb = getattr(dataset_config, "show_top_bottom_influence", None)
            if ds_tb is not None:
                top_bottom_n = int(ds_tb)
        if top_bottom_n and self.logger and scores_raw:
            self.logger.log_top_bottom_influence(scores_raw, X_train, y_train, n=int(top_bottom_n))

        # Методы удаления по loss (отдельные кривые для сравнения с influence на одном графике)
        selected_loss_methods = get_selected_loss_removal_methods()
        if selected_loss_methods:
            task_type = model_params.get('task_type', 'regression')
            per_sample_loss = compute_per_sample_loss(pipeline, X_train, y_train, task_type)
            if 'LossHigh' in selected_loss_methods:
                scores['LossHigh'] = per_sample_loss   # удаляем сначала примеры с наибольшим loss
                if scores_raw is not None:
                    scores_raw['LossHigh'] = per_sample_loss
            if 'LossLow' in selected_loss_methods:
                scores['LossLow'] = per_sample_loss   # удаляем сначала примеры с наименьшим loss
                if scores_raw is not None:
                    scores_raw['LossLow'] = per_sample_loss
            if self.logger:
                self.logger.log_message(
                    f"[OK] Enabled loss removal baselines: {', '.join(selected_loss_methods)}."
                )
        elif self.logger:
            self.logger.log_message("[OK] Loss removal baselines disabled in settings.")

        # CatBoost native object importance
        if settings_module.EXPERIMENT_CONFIG.get('use_catboost_influence', False):
            try:
                task_type = model_params.get('task_type', 'regression')
                cb_importance = compute_catboost_object_importance(
                    pipeline, X_train, y_train, X_test, y_test,
                    task_type, model_params.get('model_type'),
                    logger=self.logger,
                )
                if cb_importance is not None:
                    scores['CatBoostInfluence'] = cb_importance
                    if scores_raw is not None:
                        scores_raw['CatBoostInfluence'] = cb_importance.copy()
                    if self.logger:
                        self.logger.log_message("[OK] CatBoost object importance computed.")
            except Exception as e:
                if self.logger:
                    self.logger.log_message(f"WARNING: CatBoost object importance failed: {e}")
                    import traceback
                    self.logger.log_message(traceback.format_exc())

        # Сохранение весов влияния в experiment dir для переиспользования (plot_removal_from_weights.py)
        if self.logger and scores_raw:
            dataset_name = dataset_config.name if dataset_config and getattr(dataset_config, 'name', None) else 'unknown'
            self.logger.save_influence_weights_to_experiment_dir(
                scores_raw, dataset_name=dataset_name, n_train=len(X_train), n_remove_list=n_remove_list
            )
            self.logger.log_message("[OK] Influence weights saved to experiment dir.")

        if run_mode == "influence_only":
            if self.logger:
                self.logger.log_message("[OK] influence_only: skipping removal phase.")
            self.random_run_results = {}
            return self.results, scores, scores_raw, {}

        self._run_removal_phase(
            X_train,
            y_train,
            X_test,
            y_test,
            X_val,
            y_val,
            preprocessor,
            model_params,
            scores,
            n_remove_list,
            n_epochs,
            dataset_config,
            progress_callback,
            n_random_runs=None,
            removal_adaptive_model=removal_adaptive_model,
        )
        return self.results, scores, scores_raw, self.random_run_results


    def run_single_experiment(self, X_train, y_train, X_val, y_val,
                              preprocessor, model_params,
                              removal_percentage=0,
                              removal_strategy='remove_lowest_influence',
                              influence_scores=None,
                              n_epochs=50):

        if removal_percentage > 0:
            if influence_scores is None:
                raise ValueError("Influence scores required for non-zero removal")

            n_to_remove = int(len(X_train) * removal_percentage / 100)
            n_to_remove = max(1, n_to_remove)
            n_to_remove = min(n_to_remove, len(X_train) - 10)

            # Определяем, нужно ли сохранять хотя бы один пример для каждого класса
            task_type = model_params.get('task_type')
            if task_type in CLASSIFICATION_TASKS:
                y_arr = np.asarray(y_train.values if hasattr(y_train, "values") else y_train).ravel()
                n_classes_expected = int(np.unique(y_arr).size)
            else:
                n_classes_expected = None

            if removal_strategy == 'remove_lowest_influence':
                idx_sorted = np.argsort(influence_scores)
                candidate_order = idx_sorted
            elif removal_strategy == 'remove_highest_influence':
                idx_sorted = np.argsort(influence_scores)
                candidate_order = idx_sorted[::-1]
            elif removal_strategy == 'remove_high_loss':
                idx_sorted = np.argsort(influence_scores)[::-1]
                candidate_order = idx_sorted
            elif removal_strategy == 'remove_low_loss':
                idx_sorted = np.argsort(influence_scores)
                candidate_order = idx_sorted
            else:
                raise ValueError(f"Unknown removal strategy: {removal_strategy}")

            rpc = bool(model_params.get('removal_per_class', False))
            if rpc and task_type not in CLASSIFICATION_TASKS:
                rpc = False

            strata_labels = None
            if task_type == 'regression' and bool(model_params.get('removal_stratify_target', False)):
                nb = int(model_params.get('removal_stratify_n_bins', 10) or 10)
                strata_labels = target_strata_labels(y_train, nb)
                if strata_labels is not None and np.unique(strata_labels).size < 2:
                    strata_labels = None

            available_metrics = model_params.get('available_metrics')
            _metric_name = get_selected_metric(task_type, available_metrics)
            scorer_higher_is_better = get_metric_metadata(_metric_name)['higher_is_better']

            if rpc and n_classes_expected:
                inf = np.asarray(influence_scores).ravel()
                if removal_strategy == 'remove_lowest_influence':
                    remove_idx = removal_indices_per_class_influence(
                        inf, y_train, 'lowest', n_to_remove, int(removal_percentage),
                    )
                elif removal_strategy == 'remove_highest_influence':
                    remove_idx = removal_indices_per_class_influence(
                        inf, y_train, 'highest', n_to_remove, int(removal_percentage),
                    )
                elif removal_strategy == 'remove_high_loss':
                    remove_idx = removal_indices_per_class_valuation(
                        inf, y_train, n_to_remove, scorer_higher_is_better,
                        remove_smallest_first=False,
                    )
                elif removal_strategy == 'remove_low_loss':
                    remove_idx = removal_indices_per_class_valuation(
                        inf, y_train, n_to_remove, scorer_higher_is_better,
                        remove_smallest_first=True,
                    )
                else:
                    remove_idx = self._select_indices_keep_one_per_class(
                        candidate_order,
                        y_train,
                        n_to_remove,
                        n_classes_expected=n_classes_expected,
                        logger=self.logger,
                        context=f"{removal_strategy} {removal_percentage}% (single run)",
                    )
            elif strata_labels is not None:
                inf = np.asarray(influence_scores).ravel()
                if removal_strategy == 'remove_lowest_influence':
                    remove_idx = removal_indices_per_class_influence(
                        inf, strata_labels, 'lowest', n_to_remove, int(removal_percentage),
                    )
                elif removal_strategy == 'remove_highest_influence':
                    remove_idx = removal_indices_per_class_influence(
                        inf, strata_labels, 'highest', n_to_remove, int(removal_percentage),
                    )
                elif removal_strategy == 'remove_high_loss':
                    remove_idx = removal_indices_per_class_valuation(
                        inf, strata_labels, n_to_remove, scorer_higher_is_better,
                        remove_smallest_first=False,
                    )
                elif removal_strategy == 'remove_low_loss':
                    remove_idx = removal_indices_per_class_valuation(
                        inf, strata_labels, n_to_remove, scorer_higher_is_better,
                        remove_smallest_first=True,
                    )
                else:
                    remove_idx = self._select_indices_keep_one_per_class(
                        candidate_order,
                        y_train,
                        n_to_remove,
                        n_classes_expected=None,
                        logger=self.logger,
                        context=f"{removal_strategy} {removal_percentage}% (single run)",
                    )
            else:
                remove_idx = self._select_indices_keep_one_per_class(
                    candidate_order,
                    y_train,
                    n_to_remove,
                    n_classes_expected=n_classes_expected,
                    logger=self.logger,
                    context=f"{removal_strategy} {removal_percentage}% (single run)"
                )

            keep_mask = np.ones(len(X_train), dtype=bool)
            keep_mask[remove_idx] = False
            X_train = X_train.iloc[keep_mask]
            y_train = y_train.iloc[keep_mask]

        history, model, _ = self.train_and_evaluate(preprocessor, model_params,
                                                     X_train, y_train, X_val, y_val, n_epochs)

        return history, model