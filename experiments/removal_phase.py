"""Removal phase: retrain on subsets after removing points by score / random / loss (RemovalPhaseMixin)."""
import numpy as np
from tqdm import tqdm
from typing import Any, Callable, Dict, List, Optional

from config import settings as settings_module
from config.settings import (
    get_selected_metric,
    get_metric_metadata,
    REMOVAL_ADAPTIVE_CONFIG,
)
from utils.removal_adaptive_params import model_params_for_removal_subset

from experiments.removal_strategies import (
    CLASSIFICATION_TASKS, target_strata_labels, removal_indices_per_class_influence,
    removal_indices_per_class_random, removal_indices_per_class_valuation)


class RemovalPhaseMixin:
    """Sequential-removal curves for every score/strategy."""

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
            if not np.all(np.isfinite(np.asarray(vals, dtype=float))):
                # [AUDIT-FIX B3] невалидные скоры (NaN) не сортируем — метод пропускается
                invalid = self.results.setdefault('orig', {}).setdefault('invalid_methods', {})
                invalid.setdefault(method, 'non-finite scores')
                if self.logger:
                    self.logger.log_message(f"  [SKIP] {method}: невалидные скоры (NaN/inf), кривая не строится")
                continue

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
                    # [AUDIT-FIX B2] Скореры теперь всегда «больше = лучше» (MAE -> -MAE),
                    # поэтому ценность valuation-методов: больше = ценнее. Удаляем наименее ценные.
                    idx_sorted = np.argsort(vals)
                    if self.logger:
                        self.logger.log_message(f"  Valuation method {method}: remove lowest value first")

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
                            True,  # [AUDIT-FIX B2] ценности: больше = ценнее
                            remove_smallest_first=loss_remove_smallest_first,
                        )
                    elif strata_labels is not None:
                        remove_idx = removal_indices_per_class_valuation(
                            np.asarray(vals).ravel(),
                            strata_labels,
                            n_to_remove,
                            True,  # [AUDIT-FIX B2] ценности: больше = ценнее
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
