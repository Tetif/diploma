"""Model training and seed aggregation (TrainingMixin for ExperimentRunner).

[AUDIT-FIX M1] n_retrain_runs runs are averaged over seeds (retrain_aggregate="mean").
"""
import numpy as np
from sklearn.preprocessing import StandardScaler

from config import settings as settings_module
from config.settings import (
    get_selected_metric,
    get_metric_metadata,
)
from models.factory import ModelFactory

from experiments.removal_strategies import CLASSIFICATION_TASKS
from experiments.metrics import _pred_to_labels, _calculate_metric, _is_better_metric


class TrainingMixin:
    """train_and_evaluate + aggregation of several retrain runs."""

    @staticmethod
    def _select_indices_keep_one_per_class(candidate_order, y_train, n_to_remove,
                                           n_classes_expected=None, logger=None, context=""):
        """
        Pick the indices to remove so that each class keeps
        at least one sample (classification tasks).

        Logic:
        - candidate_order sets the removal priority (from "worst" to "best")
        - we walk through candidate_order and add an index to the
          removal list only if the class still has >= 1 sample afterwards.
        - if the constraint does not allow removing all n_to_remove samples,
          fewer are removed and a warning is logged if a logger is given.
        """
        candidate_order = np.asarray(candidate_order, dtype=int)
        if n_to_remove <= 0 or candidate_order.size == 0:
            return np.array([], dtype=int)

        # For regression, or when all classes need not be kept, return
        # the first n_to_remove indices as is.
        if n_classes_expected is None:
            return candidate_order[:n_to_remove]

        # Convert the labels to an array and count the samples of each class.
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
            # Skip the sample if removing it would leave its class empty.
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
        """Train and evaluate a model"""
        # Reset the seed before each model creation/training for determinism.
        # This removes the noise of random weight initialization: different subsets give
        # different results only because of the data, not because of the RNG.
        from utils.helpers import set_random_seeds
        seed = _run_seed if _run_seed is not None else settings_module.RANDOM_STATE
        set_random_seeds(seed)

        if self.logger:
            self.logger.start_timing("model_training")

        # Data preparation
        if not preprocessor.is_fitted:
            preprocessor.fit(X_train)
        X_train_transformed = preprocessor.transform(X_train)
        X_test_transformed = preprocessor.transform(X_test)

        if hasattr(X_train_transformed, 'toarray'):
            X_train_transformed = X_train_transformed.toarray()
            X_test_transformed = X_test_transformed.toarray()

        available_metrics = model_params.get('available_metrics')
        # Parameters unrelated to the model itself are not passed to the factory
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

        # Create the model
        model = ModelFactory.create_model(**model_creation_params)
        task_type = model_params.get('task_type', 'regression')
        metric_name = get_selected_metric(task_type, available_metrics)
        metric_meta = get_metric_metadata(metric_name)
        metric_short_label = metric_meta['short_label_ru']
        metric_label_ru = metric_meta['label_ru']
        higher_is_better = metric_meta['higher_is_better']

        # Regression: scale the target so that MSE/loss is in a reasonable range (especially for Housing etc.)
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

        # Train the model
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
            # For tree-based and distilled models
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

        # Final evaluation on the validation set
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

    @staticmethod
    def _aggregate_runs(run_tuples):
        """
        [AUDIT-FIX M1] Averaging over seeds instead of picking the best on holdout.
        Returns (history, model, y_scaler): the history of the first run, but with
        final_metric = mean over the runs, final_metric_std and final_metric_runs.
        Model/scaler of the first run (fixed seed, no selection on holdout).
        """
        finals = [t[0].get('final_metric', t[0].get('final_mae')) for t in run_tuples]
        finals = [float(v) for v in finals if v is not None]
        bests = [float(t[0].get('best_val_metric')) for t in run_tuples if t[0].get('best_val_metric') is not None]
        hist = dict(run_tuples[0][0])
        if finals:
            hist['final_metric'] = float(np.mean(finals))
            hist['final_mae'] = hist['final_metric']
            hist['final_metric_std'] = float(np.std(finals))
            hist['final_metric_runs'] = finals
        if bests:
            hist['best_val_metric'] = float(np.mean(bests))
            hist['best_val_mae'] = hist['best_val_metric']
        hist['n_seed_runs'] = len(run_tuples)
        return hist, run_tuples[0][1], run_tuples[0][2]

    def _train_best_of_n(self, preprocessor, model_params, X_sub, y_sub,
                         X_test, y_test, X_val, y_val, n_epochs, n_retrain_runs,
                         higher_is_better):
        if settings_module.EXPERIMENT_CONFIG.get('retrain_aggregate', 'mean') == 'mean':
            return self._train_best_of_n_with_model(
                preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val,
                n_epochs, n_retrain_runs, higher_is_better,
            )[0]
        """
        Run train_and_evaluate up to n_retrain_runs times with different seeds and
        return the history with the best final_metric. Implements the "kill bad runs" idea.
        Applied only to PyTorch (tree models are deterministic with a fixed random_state).
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
        Best-of-N version that returns (history, model, y_scaler) of the best run.
        Needed for the baseline so that it is compared with the removal curves in the same mode.
        """
        is_pytorch = model_params.get('model_type') == 'pytorch'
        if not is_pytorch or n_retrain_runs <= 1:
            return self.train_and_evaluate(
                preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs
            )

        if settings_module.EXPERIMENT_CONFIG.get('retrain_aggregate', 'mean') == 'mean':
            runs = [
                self.train_and_evaluate(
                    preprocessor, model_params, X_sub, y_sub, X_test, y_test, X_val, y_val,
                    n_epochs, _run_seed=settings_module.RANDOM_STATE + run_i * 1000,
                )
                for run_i in range(n_retrain_runs)
            ]
            return self._aggregate_runs(runs)

        # Legacy (retrain_aggregate='best_holdout'): picks the best run on holdout -
        # an optimistically biased estimate, kept only to reproduce old plots.
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
