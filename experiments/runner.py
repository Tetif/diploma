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

from experiments.logger import debug_print
from config.settings import (
    EXPERIMENT_CONFIG,
    RANDOM_STATE,
    get_n_remove_list,
    get_selected_loss_removal_methods,
    DEBUG_MODE,
    get_selected_metric,
    get_metric_metadata,
    REMOVAL_STRATEGIES,
)
from models.factory import ModelFactory
from influence.methods import InfluenceMethods

CLASSIFICATION_TASKS = ('binary_classification', 'multiclass_classification')


def _pred_to_labels(y_pred, task_type):
    """Convert predictions to class labels for classification metrics."""
    if task_type not in CLASSIFICATION_TASKS:
        return y_pred
    y_pred = np.asarray(y_pred)
    # Multiclass: probability matrix (N, num_classes) -> class indices (N,)
    if y_pred.ndim == 2 and y_pred.shape[1] > 1:
        return np.argmax(y_pred, axis=1).astype(int)
    # Binary: probabilities or logits
    if np.issubdtype(y_pred.dtype, np.floating) and y_pred.size > 0 and y_pred.min() >= 0 and y_pred.max() <= 1:
        return (np.asarray(y_pred).ravel() >= 0.5).astype(int)
    return np.asarray(y_pred).ravel().astype(int)


def _calculate_metric(y_true, y_pred, task_type, metric_name):
    """Calculate the selected metric value for regression or classification."""
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
    """Compare metric values respecting optimization direction."""
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

    def train_and_evaluate(self, preprocessor, model_params, X_train, y_train, X_test, y_test, X_val, y_val, n_epochs=50):
        """Обучение и оценка модели"""
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
            if k not in ('available_metrics', 'removal_strategy', 'removal_strategies')
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
                    if DEBUG_MODE:
                        self.logger.log_message(
                            f"Epoch {epoch + 1}/{n_epochs} - Train Loss: {train_loss:.4f} - "
                            f"Val {metric_short_label}: {val_metric:.4f} "
                            f"(Best: {history['best_val_metric']:.4f} at epoch {history['best_epoch'] + 1})"
                        )

                # Early stopping
                if patience_counter >= patience:
                    if self.logger:
                        self.logger.log_message(f"Early stopping at epoch {epoch + 1} (patience {patience} exceeded)")
                    break

            if best_model_weights is not None and hasattr(model, 'model'):
                model.model.load_state_dict(best_model_weights)
                if self.logger:
                    self.logger.log_message(f"Loaded best PyTorch model from epoch {history['best_epoch'] + 1}")

        else:
            # Для tree-based моделей и дистиллированных моделей
            if model_params.get('model_type') == 'lightgbm' or model_params.get('use_distillation', False):
                train_loss = model.fit(X_train_transformed, y_train_vals,
                                       X_val=X_test_transformed, y_val=y_test_vals)
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

        return history, model

    def run_experiments(self, X_train, y_train, X_test, y_test, X_val, y_val,
                        preprocessor, model_params,
                        n_remove_list=None,
                        n_epochs=50,
                        dataset_config=None,
                        selected_methods=None
                        ):
        """Запуск экспериментов с удалением данных"""
        if self.logger:
            self.logger.log_message("Starting experiments...")

        if n_remove_list is None:
            n_remove_list = get_n_remove_list()

        history, model = self.train_and_evaluate(preprocessor, model_params,
                                                 X_train, y_train, X_test, y_test, X_val, y_val, n_epochs)
        self.results['orig'] = history
        if self.logger:
            self.logger.log_message("[OK] Model training and evaluation completed.")

        pipeline = Pipeline([
            ('preproc', preprocessor),
            ('model', model)
        ])
        if self.logger:
            self.logger.log_message("[OK] Pipeline created (preprocessor + model).")

        # Выбор стратегий удаления для influence-методов.
        # Новый вариант: поддерживаем несколько стратегий сразу через
        # model_params['removal_strategies'] (['lowest', 'highest', ...]).
        # Для обратной совместимости обрабатываем legacy-поле 'removal_strategy'.
        removal_strategies = model_params.get('removal_strategies')
        if not removal_strategies:
            legacy = model_params.get('removal_strategy')
            if legacy == 'remove_lowest_influence':
                removal_strategies = ['lowest']
            elif legacy == 'remove_highest_influence':
                removal_strategies = ['highest']
            else:
                removal_strategies = list(REMOVAL_STRATEGIES)
        # Убираем дубли, сохраняя порядок
        seen = set()
        removal_strategies = [s for s in removal_strategies if not (s in seen or seen.add(s))]
        # random обрабатываем отдельно внизу как отдельный baseline
        influence_strategies = [s for s in removal_strategies if s != 'random']
        if not influence_strategies:
            influence_strategies = ['lowest']
        include_random_baseline = 'random' in removal_strategies

        # Настройка методов влияния
        influence_methods = InfluenceMethods(self.logger, dataset_config=dataset_config)
        methods, _ = influence_methods.setup_methods(pipeline, X_train, y_train,
                                                     X_test, y_test, preprocessor, methods_to_use=selected_methods)
        if self.logger:
            self.logger.log_message("[OK] Influence methods configured.")

        # Вычисление influence scores
        scores, scores_raw = influence_methods.compute_scores(methods, X_train, y_train,
                                                              preprocessor, X_test, y_test, pipeline)
        if self.logger:
            self.logger.log_message("[OK] Influence scores computed.")

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

        # Сохранение весов влияния в experiment dir для переиспользования (plot_removal_from_weights.py)
        if self.logger and scores_raw:
            dataset_name = dataset_config.name if dataset_config and getattr(dataset_config, 'name', None) else 'unknown'
            self.logger.save_influence_weights_to_experiment_dir(
                scores_raw, dataset_name=dataset_name, n_train=len(X_train), n_remove_list=n_remove_list
            )
            self.logger.log_message("[OK] Influence weights saved to experiment dir.")

        # Для многоклассовой классификации нужно сохранять все классы в подвыборке (XGBoost/sklearn требуют полный набор)
        n_classes_expected = None
        if dataset_config and dataset_config.task_type in ['binary_classification', 'multiclass_classification']:
            n_classes_expected = int(y_train.nunique())

        # Эксперименты с удалением данных — один прогресс-бар на (метод + стратегия + проценты)
        if self.logger:
            self.logger.log_message("[OK] Starting removal experiments (by method, strategy and percentage).")
        methods_items = list(scores.items())
        influence_method_names = ['Influence', 'ArnoldiInfluence', 'CgInfluence', 'LissaInfluence', 'NystroemSketchInfluence']
        n_influence_methods = sum(1 for name, _ in methods_items if name in influence_method_names)
        n_non_influence_methods = len(methods_items) - n_influence_methods
        total_series = n_non_influence_methods + n_influence_methods * len(influence_strategies)
        total_removal_steps = total_series * len(n_remove_list)
        pbar_methods = tqdm(total=total_removal_steps, desc="Removal (method %)", unit="step")

        for method, vals in methods_items:
            if self.logger:
                self.logger.log_message(f"\nProcessing method: {method}")

            is_influence_method = method in influence_method_names

            if is_influence_method:
                # Для influence-методов запускаем по всем выбранным стратегиям
                for strategy in influence_strategies:
                    # Базовый порядок кандидатов на удаление (по возрастанию/убыванию)
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
                        idx_sorted = np.argsort(vals)  # «плохие» — с наименьшим влиянием
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'few_bad_then_random' for {method}")
                    elif strategy == 'few_median_then_random':
                        plot_method = f"{method}_few_median_rand"
                        idx_sorted = np.argsort(vals)
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'few_median_then_random' for {method}")
                    elif strategy == 'few_good_then_random':
                        plot_method = f"{method}_few_good_rand"
                        idx_sorted = np.argsort(vals)[::-1]  # «хорошие» — с наибольшим влиянием
                        if self.logger:
                            self.logger.log_message(f"  Strategy 'few_good_then_random' for {method}")
                    else:
                        # Неизвестная стратегия — пропускаем
                        if self.logger:
                            self.logger.log_message(f"  Unknown strategy '{strategy}' for {method}, skipping")
                        continue

                    # Строим полный порядок кандидатов на удаление для данной стратегии.
                    # Затем для каждого процента будем выбирать первые n_to_remove с
                    # учётом ограничения "оставить хотя бы один пример каждого класса".
                    n_train = len(X_train)
                    all_indices = np.arange(n_train)

                    if strategy in ('lowest', 'highest'):
                        # Уже задан нужный порядок в idx_sorted
                        candidate_order_base = idx_sorted
                    elif strategy == 'extremes':
                        # Чередуем "худшие" и "лучшие" примеры
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
                        # Начинаем с середины и идём к краям
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
                        # Для смешанных стратегий порядок зависит от процента удаления,
                        # поэтому базовый порядок будем строить внутри цикла по pct.
                        candidate_order_base = None

                    # 0% удаления - baseline
                    self.results[f'{plot_method}_0'] = self.results['orig']

                    fixed_frac = 0.1  # для смешанных стратегий

                    for pct in n_remove_list:
                        pbar_methods.set_postfix_str(f"{plot_method} {pct}%", refresh=True)

                        n_to_remove = int(n_train * pct / 100)
                        n_to_remove = max(1, n_to_remove)
                        n_to_remove = min(n_to_remove, n_train - 10)

                        # Строим порядок кандидатов с учётом процента и стратегии
                        if candidate_order_base is not None:
                            candidate_order = candidate_order_base
                        elif strategy == 'few_bad_then_random':
                            n_total = n_to_remove
                            n_fixed = min(int(fixed_frac * n_train), n_total)
                            if n_fixed <= 0:
                                n_fixed = min(1, n_total)
                            det_idx = idx_sorted[:n_fixed]
                            remaining = np.setdiff1d(all_indices, det_idx, assume_unique=True)
                            np.random.seed(RANDOM_STATE + pct)
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
                            np.random.seed(RANDOM_STATE + pct + 1000)
                            rand_order = np.random.permutation(remaining)
                            candidate_order = np.concatenate([det_idx, rand_order])
                        elif strategy == 'few_good_then_random':
                            n_total = n_to_remove
                            n_fixed = min(int(fixed_frac * n_train), n_total)
                            if n_fixed <= 0:
                                n_fixed = min(1, n_total)
                            det_idx = idx_sorted[:n_fixed]
                            remaining = np.setdiff1d(all_indices, det_idx, assume_unique=True)
                            np.random.seed(RANDOM_STATE + pct + 2000)
                            rand_order = np.random.permutation(remaining)
                            candidate_order = np.concatenate([det_idx, rand_order])
                        else:
                            # На всякий случай, не должно сюда попадать
                            candidate_order = np.array([], dtype=int)

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
                            pbar_methods.update(1)
                            continue

                        if n_classes_expected is not None:
                            unique_in_sub = y_sub.nunique()
                            if unique_in_sub < n_classes_expected:
                                if self.logger:
                                    self.logger.log_message(
                                        f"  Skipping pct={pct} - only {unique_in_sub} class(es) remaining (need all {n_classes_expected})"
                                    )
                                pbar_methods.update(1)
                                continue

                        key = f'{plot_method}_{pct}pct'
                        history, _ = self.train_and_evaluate(preprocessor, model_params,
                                                             X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs)
                        self.results[key] = history
                        pbar_methods.update(1)
            else:
                # Для не-influence методов (Shapley, LossHigh/LossLow и т.п.) оставляем
                # единственный сценарий удаления как раньше.
                plot_method = method
                self.results[f'{plot_method}_0'] = self.results['orig']  # 0% удаления - baseline

                if method == 'LossHigh':
                    idx_sorted = np.argsort(vals)[::-1]
                    if self.logger:
                        self.logger.log_message(f"  LossHigh: remove highest loss first")
                elif method == 'LossLow':
                    idx_sorted = np.argsort(vals)
                    if self.logger:
                        self.logger.log_message(f"  LossLow: remove lowest loss first")
                else:
                    idx_sorted = np.argsort(vals)
                    if self.logger:
                        self.logger.log_message(f"  Using default 'lowest' strategy for {method}")

                for pct in n_remove_list:
                    pbar_methods.set_postfix_str(f"{plot_method} {pct}%", refresh=True)

                    n_to_remove = int(len(X_train) * pct / 100)
                    n_to_remove = max(1, n_to_remove)
                    n_to_remove = min(n_to_remove, len(X_train) - 10)

                    # Базовый порядок кандидатов — по возрастанию/убыванию loss/оценки
                    candidate_order = idx_sorted
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
                        pbar_methods.update(1)
                        continue

                    if n_classes_expected is not None:
                        unique_in_sub = y_sub.nunique()
                        if unique_in_sub < n_classes_expected:
                            if self.logger:
                                self.logger.log_message(
                                    f"  Skipping pct={pct} - only {unique_in_sub} class(es) remaining (need all {n_classes_expected})"
                                )
                            pbar_methods.update(1)
                            continue

                    key = f'{plot_method}_{pct}pct'
                    history, _ = self.train_and_evaluate(preprocessor, model_params,
                                                         X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs)
                    self.results[key] = history
                    pbar_methods.update(1)

        pbar_methods.close()
        if self.logger:
            self.logger.log_message("[OK] Removal experiments (all methods and percentages) completed.")

        # Случайное удаление - запускаем несколько раз для получения доверительных интервалов.
        # Управляется стратегией 'random' в списке removal_strategies.
        random_run_results = {}
        if include_random_baseline:
            if self.logger:
                self.logger.log_message("Processing random removal")

            n_random_runs = EXPERIMENT_CONFIG['n_random_runs']
            total_random_steps = n_random_runs * len(n_remove_list)
            pbar_random = tqdm(total=total_random_steps, desc="Random removal (run %)", unit="step")

            for run_idx in range(n_random_runs):
                if self.logger:
                    self.logger.log_message(f"  Random removal run {run_idx + 1}/{n_random_runs}...")

                for pct in n_remove_list:
                    pbar_random.set_postfix_str(f"run {run_idx + 1} {pct}%", refresh=True)

                    n_to_remove = int(len(X_train) * pct / 100)
                    n_to_remove = max(1, n_to_remove)
                    n_to_remove = min(n_to_remove, len(X_train) - 10)

                    # Случайный порядок кандидатов и выбор с учётом ограничения
                    np.random.seed(RANDOM_STATE + run_idx)
                    candidate_order = np.random.permutation(len(X_train))
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
                        pbar_random.update(1)
                        continue

                    if n_classes_expected is not None and y_sub.nunique() < n_classes_expected:
                        pbar_random.update(1)
                        continue

                    key = f'random_{pct}pct_run{run_idx}'
                    history, _ = self.train_and_evaluate(preprocessor, model_params,
                                                         X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs)
                    self.results[key] = history

                    if pct not in random_run_results:
                        random_run_results[pct] = []
                    random_run_results[pct].append(history['final_mae'])
                    pbar_random.update(1)

            pbar_random.close()
            if self.logger:
                self.logger.log_message("[OK] Random removal runs completed.")

            # Вычисляем и сохраняем статистику для random метода
            self.random_run_results = random_run_results  # Сохраняем для использования в plot
            
            # Сохраняем медианные результаты как основные результаты random метода
            for pct, mae_values in random_run_results.items():
                if mae_values:
                    median_mae = np.median(mae_values)
                    key = f'random_{pct}pct'
                    # Создаём history с медианным значением
                    self.results[key] = {'final_mae': median_mae}

        if self.logger:
            self.logger.log_message("All experiments completed!")

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

        history, model = self.train_and_evaluate(preprocessor, model_params,
                                                 X_train, y_train, X_val, y_val, n_epochs)

        return history, model