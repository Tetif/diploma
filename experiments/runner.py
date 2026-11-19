"""Experiment pipeline orchestration (ExperimentRunner).

Layout of the experiments package:
  removal_strategies.py  - ordering / per-class selection of points to remove
  metrics.py             - metrics, per-sample loss
  catboost_importance.py - CatBoost object importance
  training.py            - train_and_evaluate, seed aggregation (TrainingMixin)
  removal_phase.py       - removal curves (RemovalPhaseMixin)
  runner.py              - ExperimentRunner = TrainingMixin + RemovalPhaseMixin + run_* entry points
"""
import numpy as np
from sklearn.pipeline import Pipeline
from typing import Any, Callable, Dict, Optional, Tuple

from config import settings as settings_module
from config.settings import (
    get_n_remove_list,
    get_selected_loss_removal_methods,
    get_selected_metric,
    get_metric_metadata,
)
from influence.methods import InfluenceMethods

# Re-exported for backward compatibility (scripts, microservice, tests import them from here).
from experiments.removal_strategies import (  # noqa: F401
    CLASSIFICATION_TASKS, target_strata_labels, _allocate_proportional_n_per_class,
    build_full_candidate_order_influence, removal_indices_per_class_influence,
    removal_indices_per_class_random, removal_indices_per_class_valuation)
from experiments.metrics import _pred_to_labels, _calculate_metric, _is_better_metric, compute_per_sample_loss  # noqa: F401
from experiments.catboost_importance import _extract_catboost_model, compute_catboost_object_importance  # noqa: F401
from experiments.training import TrainingMixin
from experiments.removal_phase import RemovalPhaseMixin


class ExperimentRunner(TrainingMixin, RemovalPhaseMixin):
    """Full pipeline: baseline training -> influence/valuation scores -> removal curves."""


    def __init__(self, logger=None):
        self.logger = logger
        self.results = {}

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
                                                     X_test, y_test, preprocessor, methods_to_use=selected_methods,
                                                     y_scaler=y_scaler)
        if self.logger:
            self.logger.log_message("[OK] Influence methods configured.")

        if progress_callback:
            progress_callback({"kind": "phase", "phase": "influence_compute"})

        # Вычисление influence scores
        scores, scores_raw = influence_methods.compute_scores(methods, X_train, y_train,
                                                              preprocessor, X_test, y_test, pipeline,
                                                              y_scaler=y_scaler)
        failed = dict(getattr(influence_methods, 'failed_methods', {}) or {})
        if failed:
            # [AUDIT-FIX B3] явная пометка в результатах вместо молчаливых нулей
            self.results['orig']['invalid_methods'] = failed
            if self.logger:
                for _m, _why in failed.items():
                    self.logger.log_message(f"[INVALID] {_m}: {_why} — кривая удаления строиться не будет")
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
