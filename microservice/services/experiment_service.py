"""Experiment service wrapper"""
import matplotlib

matplotlib.use("Agg")

import copy
import sys
import time
import uuid
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
import threading
from queue import Queue
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import EXPERIMENTS_BASE_DIR, REMOVAL_STRATEGIES, METRIC_METADATA
from config import DatasetRegistry
from data.loader import DataLoaderFactory
from data.preprocessing import PreprocessorFactory
from experiments.runner import ExperimentRunner
from experiments.logger import ExperimentLogger
from utils.helpers import set_random_seeds, sample_data, split_data
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from visualization.plots import (
    plot_influence_distribution,
    plot_results_enhanced,
    plot_method_comparison_bars,
)
from microservice.storage.influence_storage import InfluenceWeightsStorage
from microservice.config_merge import build_merged_config, runtime_settings_patch
from influence.utils import get_influence_statistics


def _try_write_experiment_summary(
    logger: ExperimentLogger,
    results: Dict[str, Any],
    model_params: Dict[str, Any],
    n_epochs: int,
    config_for_summary: Dict[str, Any],
    influence_weights: Dict[str, Any],
    scores_raw: Optional[Dict[str, Any]],
    n_remove_list: Optional[List[int]] = None,
    run_mode: str = "full",
) -> None:
    """Пишет experiment_summary.txt в каталог эксперимента (experiment_logs/дата/время/…)."""
    orig = results.get("orig")
    if not isinstance(orig, dict):
        return
    model_metrics = {
        "baseline_metric": orig.get("final_metric"),
        "best_validation_metric": orig.get("best_val_metric"),
        "metric_name": orig.get("metric_name"),
        "metric_label_ru": orig.get("metric_label_ru"),
        "best_epoch": orig.get("best_epoch"),
        "total_training_epochs": n_epochs,
        "model_type": model_params.get("model_type"),
        "used_distillation": model_params.get("use_distillation", False),
        "distillation_epochs": (
            model_params.get("distillation_epochs", 0)
            if model_params.get("use_distillation", False)
            else 0
        ),
        "student_architecture": (
            model_params.get("student_architecture", "none")
            if model_params.get("use_distillation", False)
            else "none"
        ),
    }
    sr: Dict[str, Any] = scores_raw if scores_raw is not None else {}
    influence_stats = get_influence_statistics(sr)
    _rm = str(run_mode).lower()
    _show_removal = _rm in ("full", "removal_child")
    logger.generate_summary(
        config_for_summary,
        model_metrics,
        influence_stats,
        influence_weights,
        sr,
        removal_results=results if _show_removal else None,
        n_remove_list=n_remove_list if _show_removal else None,
    )


class ExperimentCancelled(Exception):
    """User requested stop via cancel event."""


class ExperimentService:
    """Service for running experiments with custom configuration"""

    STAGE_LABELS = [
        ("load_data", "Loading dataset"),
        ("split_sample", "Splitting and sampling data"),
        ("preprocess", "Fitting preprocessor"),
        ("model_config", "Building model configuration"),
        ("experiments", "Running experiments (baseline → influence → removal)"),
        ("save", "Saving results"),
    ]

    def __init__(self):
        self.active_experiments = {}
        self.tasks_queue = Queue()
        self.storage = InfluenceWeightsStorage()
        self._cancel_events: Dict[str, threading.Event] = {}

    def _raise_if_cancelled(self, experiment_id: str) -> None:
        ev = self._cancel_events.get(experiment_id)
        if ev is not None and ev.is_set():
            raise ExperimentCancelled()

    def request_cancel(self, experiment_id: str) -> bool:
        """Signal cancellation. Returns True if this id was known (active or in-flight)."""
        ev = self._cancel_events.get(experiment_id)
        if ev is not None:
            ev.set()
        exp = self.active_experiments.get(experiment_id)
        if exp is not None:
            exp["cancel_requested"] = True
        return ev is not None or exp is not None

    def discard_experiment(self, experiment_id: str) -> bool:
        """Cancel if running, delete storage folder, drop from active list."""
        self.request_cancel(experiment_id)
        on_disk = (self.storage.experiments_dir / experiment_id).exists()
        if on_disk:
            self.storage.delete_experiment(experiment_id)
        in_active = experiment_id in self.active_experiments
        self.active_experiments.pop(experiment_id, None)
        return on_disk or in_active

    def start_experiment(
        self, config: Dict[str, Any], experiment_id: Optional[str] = None
    ) -> str:
        if experiment_id is None:
            experiment_id = str(uuid.uuid4())

        rpc_req = config.get("removal_per_class")
        removal_per_class_flag = (
            bool(rpc_req) if rpc_req is not None else False
        )
        rst_req = config.get("removal_stratify_target")
        removal_stratify_flag = bool(rst_req) if rst_req is not None else False
        self.active_experiments[experiment_id] = {
            "status": "running",
            "progress": 0.0,
            "message": "Initializing...",
            "start_time": time.time(),
            "result": None,
            "error": None,
            "stage": "init",
            "stage_index": 0,
            "stages_total": len(self.STAGE_LABELS),
            "eta_seconds": None,
            "_last_progress_time": None,
            "_last_progress_value": 0.0,
            "dataset": config.get("dataset_name"),
            "model": config.get("model_type"),
            "sample_size_percentage": config.get("sample_size_percentage"),
            "removal_adaptive_model": bool(
                config.get("removal_adaptive_model", False)
            ),
            "removal_per_class": removal_per_class_flag,
            "removal_stratify_target": removal_stratify_flag,
            "cancel_requested": False,
        }
        self._cancel_events[experiment_id] = threading.Event()

        thread = threading.Thread(
            target=self._run_experiment_thread,
            args=(experiment_id, config),
            daemon=True,
        )
        thread.start()

        return experiment_id

    def start_removal_child_experiment(
        self, parent_experiment_id: str, removal_config: Dict[str, Any]
    ) -> str:
        """Start a removal-only experiment using influence weights from parent."""
        child_id = str(uuid.uuid4())
        rpc_ch = removal_config.get("removal_per_class")
        removal_per_class_child = (
            bool(rpc_ch) if rpc_ch is not None else False
        )
        rst_ch = removal_config.get("removal_stratify_target")
        removal_stratify_child = bool(rst_ch) if rst_ch is not None else False
        self.active_experiments[child_id] = {
            "status": "running",
            "progress": 0.0,
            "message": "Initializing removal run…",
            "start_time": time.time(),
            "result": None,
            "error": None,
            "stage": "init",
            "stage_index": 0,
            "stages_total": len(self.STAGE_LABELS),
            "eta_seconds": None,
            "_last_progress_time": None,
            "_last_progress_value": 0.0,
            "dataset": None,
            "model": None,
            "sample_size_percentage": None,
            "parent_experiment_id": parent_experiment_id,
            "removal_adaptive_model": bool(
                removal_config.get("removal_adaptive_model", False)
            ),
            "removal_per_class": removal_per_class_child,
            "removal_stratify_target": removal_stratify_child,
            "cancel_requested": False,
        }
        self._cancel_events[child_id] = threading.Event()
        thread = threading.Thread(
            target=self._run_removal_child_thread,
            args=(child_id, parent_experiment_id, removal_config),
            daemon=True,
        )
        thread.start()
        return child_id

    def _set_stage(self, experiment_id: str, index: int, message: Optional[str] = None):
        if experiment_id not in self.active_experiments:
            return
        if 0 <= index < len(self.STAGE_LABELS):
            sid, default_msg = self.STAGE_LABELS[index]
            self.active_experiments[experiment_id]["stage"] = sid
            self.active_experiments[experiment_id]["stage_index"] = index + 1
            self.active_experiments[experiment_id]["stages_total"] = len(self.STAGE_LABELS)
            self.active_experiments[experiment_id]["message"] = message or default_msg

    def _map_runner_progress(
        self, experiment_id: str, event: Dict[str, Any]
    ) -> None:
        """Map ExperimentRunner progress_callback events to 0–100."""
        exp = self.active_experiments.get(experiment_id)
        if not exp:
            return
        kind = event.get("kind")
        now = time.time()
        base_lo, base_hi = 35.0, 90.0

        if kind == "phase":
            ph = event.get("phase")
            if ph == "baseline_train":
                self._update_status(
                    experiment_id,
                    "running",
                    38.0,
                    "Training baseline model…",
                )
            elif ph == "baseline_done":
                self._update_status(
                    experiment_id, "running", 42.0, "Baseline training finished"
                )
            elif ph in ("influence_setup", "influence_compute"):
                self._update_status(
                    experiment_id,
                    "running",
                    44.0,
                    "Computing influence scores…",
                )
            elif ph == "influence_scores_done":
                self._update_status(
                    experiment_id,
                    "running",
                    48.0,
                    "Influence scores ready.",
                )
            elif ph == "removal_loop":
                total = float(event.get("total_steps") or 1)
                self._update_status(
                    experiment_id,
                    "running",
                    50.0,
                    f"Removal experiments (0 / {int(total)} steps)…",
                )
            elif ph == "random_removal":
                total = float(event.get("total_steps") or 1)
                self._update_status(
                    experiment_id,
                    "running",
                    85.0,
                    f"Random removal baseline (0 / {int(total)} steps)…",
                )
            return

        if kind == "removal_step":
            done = float(event.get("done") or 0)
            total = float(event.get("total") or 1)
            frac = min(1.0, done / max(total, 1.0))
            prog = base_lo + (base_hi - base_lo - 10.0) * frac
            msg = f"Removal experiments ({int(done)} / {int(total)} steps)…"
            self._update_status(experiment_id, "running", prog, msg)
            self._touch_eta(experiment_id, prog, now)
            return

        if kind == "random_step":
            done = float(event.get("done") or 0)
            total = float(event.get("total") or 1)
            frac = min(1.0, done / max(total, 1.0))
            prog = 85.0 + 5.0 * frac
            msg = f"Random removal ({int(done)} / {int(total)})…"
            self._update_status(experiment_id, "running", prog, msg)
            self._touch_eta(experiment_id, prog, now)

    def _touch_eta(self, experiment_id: str, progress: float, now: float):
        exp = self.active_experiments.get(experiment_id)
        if not exp:
            return
        prev_t = exp.get("_last_progress_time")
        prev_p = exp.get("_last_progress_value", 0.0)
        if prev_t is not None and progress > prev_p:
            dp = progress - prev_p
            dt = now - prev_t
            if dp > 1e-6 and dt > 0:
                rate = dp / dt
                remaining_pct = 100.0 - progress
                exp["eta_seconds"] = max(0.0, remaining_pct / rate)
        exp["_last_progress_time"] = now
        exp["_last_progress_value"] = progress

    def get_experiment_status(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        return self.active_experiments.get(experiment_id)

    def _run_experiment_thread(self, experiment_id: str, config: Dict[str, Any]):
        try:
            merged = build_merged_config(config)
            mr_m = merged.get("MODEL_RUN_CONFIG") or {}
            if config.get("removal_per_class") is not None:
                self.active_experiments[experiment_id]["removal_per_class"] = bool(
                    config.get("removal_per_class")
                )
            else:
                self.active_experiments[experiment_id]["removal_per_class"] = bool(
                    mr_m.get("removal_per_class", False)
                )
            if config.get("removal_stratify_target") is not None:
                self.active_experiments[experiment_id]["removal_stratify_target"] = bool(
                    config.get("removal_stratify_target")
                )
            else:
                self.active_experiments[experiment_id]["removal_stratify_target"] = bool(
                    mr_m.get("removal_stratify_target", False)
                )
            self.active_experiments[experiment_id]["removal_adaptive_model"] = bool(
                config.get("removal_adaptive_model", False)
            )

            with runtime_settings_patch(merged):
                import config.settings as S

                rs = int(config.get("random_state", S.RANDOM_STATE))
                set_random_seeds(rs)

                self._set_stage(experiment_id, 0)
                self._update_status(
                    experiment_id,
                    "running",
                    5.0,
                    f"Loading dataset {config['dataset_name']}…",
                )
                self._raise_if_cancelled(experiment_id)

                dataset_name = config["dataset_name"]
                dataset_config = DatasetRegistry.get(dataset_name)
                if bool(config.get("use_tfidf_lsa", False)) and hasattr(dataset_config, "use_tfidf_lsa"):
                    dataset_config.use_tfidf_lsa = True
                    lsa_components = config.get("lsa_components")
                    if lsa_components is not None:
                        dataset_config.lsa_n_components = int(lsa_components)
                    logger = ExperimentLogger(base_dir=EXPERIMENTS_BASE_DIR)
                    logger.log_message(
                        f"Используется TF-IDF + LSA: {dataset_config.lsa_n_components} компонент(ы)."
                    )
                else:
                    logger = ExperimentLogger(base_dir=EXPERIMENTS_BASE_DIR)

                X, y, cfg = DataLoaderFactory.load_dataset(dataset_config, logger)
                self._raise_if_cancelled(experiment_id)

                if cfg.task_type in [
                    "binary_classification",
                    "multiclass_classification",
                ]:
                    if y.dtype == "object":
                        le = LabelEncoder()
                        y = pd.Series(le.fit_transform(y), index=y.index)

                self._set_stage(experiment_id, 1)
                self._update_status(
                    experiment_id,
                    "running",
                    10.0,
                    "Splitting train / test / holdout…",
                )

                val_sz = float(
                    merged["EXPERIMENT_CONFIG"].get(
                        "val_size", config.get("val_size", 0.1)
                    )
                )
                X_temp, X_holdout_validation, y_temp, y_holdout_validation = split_data(
                    X,
                    y,
                    test_size=val_sz,
                    random_state=rs,
                    stratify=y if cfg.stratify else None,
                    time_series=cfg.use_time_split,
                )

                sample_pct = (
                    float(merged["EXPERIMENT_CONFIG"].get("sample_size_percentage", 100))
                    / 100.0
                )
                X_sample, y_sample = sample_data(
                    X_temp,
                    y_temp,
                    sample_fraction=sample_pct,
                    random_state=rs,
                    preserve_order=cfg.use_time_split,
                )

                test_sz = float(
                    merged["EXPERIMENT_CONFIG"].get(
                        "test_size", config.get("test_size", 0.2)
                    )
                )
                X_train, X_test, y_train, y_test = split_data(
                    X_sample,
                    y_sample,
                    test_size=test_sz,
                    random_state=rs,
                    time_series=cfg.use_time_split,
                )
                self._raise_if_cancelled(experiment_id)

                self._set_stage(experiment_id, 2)
                self._update_status(
                    experiment_id,
                    "running",
                    18.0,
                    "Fitting preprocessor…",
                )

                preprocessor = PreprocessorFactory.create(dataset_config, logger)
                preprocessor.fit(X_train)

                X_train_processed = preprocessor.transform(X_train)
                X_test_processed = preprocessor.transform(X_test)
                X_val_processed = preprocessor.transform(X_holdout_validation)

                if hasattr(X_train_processed, "toarray"):
                    X_train_processed = X_train_processed.toarray()
                    X_test_processed = X_test_processed.toarray()
                    X_val_processed = X_val_processed.toarray()

                input_size = X_train_processed.shape[1]

                self._set_stage(experiment_id, 3)
                self._update_status(
                    experiment_id,
                    "running",
                    22.0,
                    "Loading model hyperparameters…",
                )

                from config.settings import (
                    get_model_config,
                    MODEL_FIT_MODE,
                    FIT_MODE_EPOCHS,
                    EXPERIMENT_CONFIG,
                )

                model_type = merged["MODEL_RUN_CONFIG"]["model_type"]
                try:
                    dataset_model_config = get_model_config(dataset_name, model_type)
                except ValueError:
                    dataset_model_config = {}

                mr = merged["MODEL_RUN_CONFIG"]
                dist = merged["DISTILLATION_CONFIG"]

                model_params = {
                    "model_type": model_type,
                    "task_type": cfg.task_type,
                    "available_metrics": list(getattr(cfg, "metrics", [])),
                    "input_size": input_size,
                    "device": S.DEVICE,
                    "removal_strategies": mr.get("removal_strategies")
                    or list(REMOVAL_STRATEGIES),
                    "removal_strategy": config.get(
                        "removal_strategy", "remove_lowest_influence"
                    ),
                    "removal_per_class": bool(mr.get("removal_per_class", False)),
                    "removal_stratify_target": bool(mr.get("removal_stratify_target", False)),
                    "removal_stratify_n_bins": int(mr.get("removal_stratify_n_bins", 10) or 10),
                    "use_distillation": dist.get("use_distillation", False),
                    "distillation_epochs": dist.get("distillation_epochs", 200),
                    "temperature": dist.get("temperature", 2.0),
                    "student_architecture": dist.get("student_architecture", "simple"),
                }
                rpc = config.get("removal_per_class")
                if rpc is not None:
                    model_params["removal_per_class"] = bool(rpc)
                rst = config.get("removal_stratify_target")
                if rst is not None:
                    model_params["removal_stratify_target"] = bool(rst)
                rnb = config.get("removal_stratify_n_bins")
                if rnb is not None:
                    model_params["removal_stratify_n_bins"] = int(rnb)

                mp_user = config.get("model_params") or {}
                for key, value in dataset_model_config.items():
                    if key not in model_params or key in (
                        "learning_rate",
                        "num_leaves",
                        "max_depth",
                        "iterations",
                        "n_estimators",
                        "layers",
                        "dropout",
                        "base_channels",
                    ):
                        model_params[key] = value
                model_params.update(mp_user)

                if cfg.task_type == "multiclass_classification":
                    model_params["num_class"] = int(
                        len(np.unique(np.asarray(y_train).ravel()))
                    )

                if (
                    cfg.task_type == "binary_classification"
                    and model_params.get("model_type") == "pytorch"
                ):
                    y_flat = np.asarray(y_train).ravel()
                    n_pos = max(int((y_flat == 1).sum()), 1)
                    n_neg = int((y_flat == 0).sum())
                    model_params["pos_weight"] = n_neg / n_pos

                if model_params["model_type"] == "pytorch" or model_params.get(
                    "use_distillation", False
                ):
                    if MODEL_FIT_MODE != "normal" and MODEL_FIT_MODE in FIT_MODE_EPOCHS:
                        n_epochs = FIT_MODE_EPOCHS[MODEL_FIT_MODE]
                    else:
                        n_epochs = int(EXPERIMENT_CONFIG.get("n_epochs", 500))
                else:
                    n_epochs = 1

                n_remove_list = [
                    int(x) for x in config.get("n_remove_percentages", list(range(1, 100, 5)))
                ]

                self._set_stage(experiment_id, 4)
                self._update_status(
                    experiment_id,
                    "running",
                    28.0,
                    "Running experiments…",
                )
                self.active_experiments[experiment_id]["_last_progress_time"] = time.time()
                self.active_experiments[experiment_id]["_last_progress_value"] = 28.0

                experiment_runner = ExperimentRunner(logger)

                def _progress_cb(ev: Dict[str, Any]):
                    self._raise_if_cancelled(experiment_id)
                    self._map_runner_progress(experiment_id, ev)

                sel_methods = config.get("selected_influence_methods")
                if not sel_methods:
                    sel_methods = None

                run_mode = str(config.get("run_mode") or "full").lower()
                if run_mode not in ("full", "influence_only"):
                    run_mode = "full"

                removal_adaptive_model = bool(config.get("removal_adaptive_model", False))
                if run_mode != "full":
                    removal_adaptive_model = False

                results, scores, scores_raw, random_run_results = (
                    experiment_runner.run_experiments(
                        X_train,
                        y_train,
                        X_test,
                        y_test,
                        X_holdout_validation,
                        y_holdout_validation,
                        preprocessor,
                        model_params,
                        n_remove_list,
                        n_epochs,
                        dataset_config=dataset_config,
                        selected_methods=sel_methods,
                        progress_callback=_progress_cb,
                        run_mode=run_mode,
                        removal_adaptive_model=removal_adaptive_model,
                    )
                )

                self._set_stage(experiment_id, 5)
                self._update_status(
                    experiment_id,
                    "running",
                    92.0,
                    "Finalizing and saving…",
                )

                exp_kind = (
                    "base_influence"
                    if run_mode == "influence_only"
                    else "full"
                )
                saved_config = {
                    "dataset_name": dataset_name,
                    "model_type": model_type,
                    "sample_size": len(X_train),
                    "features": input_size,
                    "n_remove_percentages": n_remove_list,
                    "removal_strategy": config.get("removal_strategy"),
                    "n_epochs": n_epochs,
                    "experiment_dir": str(logger.get_experiment_dir()),
                    "random_state": rs,
                    "test_size": test_sz,
                    "val_size": val_sz,
                    "sample_size_percentage": merged["EXPERIMENT_CONFIG"].get(
                        "sample_size_percentage", 100
                    ),
                    "target_column": getattr(dataset_config, "target_column", "target"),
                    "task_type": cfg.task_type,
                    "selected_influence_methods": config.get("selected_influence_methods") or [],
                    "model_run_config": {
                        "removal_strategies": model_params.get("removal_strategies"),
                        "removal_per_class": model_params.get("removal_per_class"),
                        "removal_stratify_target": model_params.get(
                            "removal_stratify_target"
                        ),
                        "removal_stratify_n_bins": model_params.get(
                            "removal_stratify_n_bins"
                        ),
                    },
                    "experiment_kind": exp_kind,
                    "parent_experiment_id": None,
                    "run_mode": run_mode,
                    "removal_adaptive_model": removal_adaptive_model,
                    "api_request_snapshot": copy.deepcopy(config),
                }

                self.active_experiments[experiment_id]["result"] = {
                    "results": results,
                    "influence_weights": scores,
                    "scores_raw": scores_raw,
                    "random_run_results": random_run_results,
                    "config": saved_config,
                    "execution_time": time.time()
                    - self.active_experiments[experiment_id]["start_time"],
                }

                self._update_status(
                    experiment_id,
                    "completed",
                    96.0,
                    "Saving results to storage…",
                )

                result = self.active_experiments[experiment_id]["result"]
                try:
                    cfg_out = result.get("config", {})
                    influence_weights = result.get("influence_weights", {})
                    scores_raw_out = result.get("scores_raw", {})

                    try:
                        logger.save_results(
                            result.get("results", {}),
                            influence_weights,
                            scores_raw_out,
                            n_remove_list,
                            random_run_results=random_run_results,
                        )
                    except Exception:
                        pass

                    try:
                        _try_write_experiment_summary(
                            logger,
                            result.get("results", {}),
                            model_params,
                            n_epochs,
                            saved_config,
                            influence_weights,
                            scores_raw_out,
                            n_remove_list=n_remove_list,
                            run_mode=run_mode,
                        )
                    except Exception as e_sum:
                        print(f"Warning: failed to save experiment_summary: {e_sum}")

                    try:
                        plot_influence_distribution(
                            scores_raw_out, "influence_scores", logger
                        )
                    except Exception as e_plot:
                        print(
                            f"Warning: failed to save influence distribution plot: {e_plot}"
                        )

                    if run_mode != "influence_only":
                        try:
                            plot_results_enhanced(
                                result.get("results", {}),
                                n_remove_list,
                                logger,
                                random_run_results=getattr(
                                    experiment_runner, "random_run_results", None
                                ),
                            )
                        except Exception as e_plot:
                            print(
                                f"Warning: failed to save results comparison plot: {e_plot}"
                            )

                        try:
                            plot_method_comparison_bars(
                                logger,
                                result.get("results", {}),
                                n_remove_list,
                                metric_metadata=METRIC_METADATA,
                            )
                        except Exception as e_bars:
                            print(
                                f"Warning: failed to save method comparison bar plots: {e_bars}"
                            )

                    meta_save = {
                        "status": "completed",
                        "saved_at": datetime.now().isoformat(),
                    }
                    if run_mode == "influence_only":
                        meta_save["status"] = "influence_ready"

                    self.storage.save_experiment(
                        experiment_id,
                        cfg_out,
                        result.get("results", {}),
                        influence_weights,
                        scores_raw_out,
                        meta_save,
                    )

                    self._update_status(
                        experiment_id,
                        "completed",
                        100.0,
                        "Experiment completed successfully!",
                    )
                except Exception as save_err:
                    print(f"Warning: Failed to save results to storage: {save_err}")
                    self._update_status(
                        experiment_id,
                        "completed",
                        100.0,
                        "Experiment completed (storage save failed)",
                    )

        except ExperimentCancelled:
            if experiment_id in self.active_experiments:
                p = float(self.active_experiments[experiment_id].get("progress", 0.0))
                self._update_status(
                    experiment_id,
                    "cancelled",
                    p,
                    "Остановлено пользователем.",
                )
                self.active_experiments[experiment_id]["error"] = None
        except Exception as e:
            import traceback

            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            if experiment_id in self.active_experiments:
                self._update_status(experiment_id, "failed", 0.0, error_msg)
                self.active_experiments[experiment_id]["error"] = error_msg
        finally:
            self._cancel_events.pop(experiment_id, None)

    def _merge_api_config_for_removal_child(
        self, parent_cfg: Dict[str, Any], removal_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        snap = parent_cfg.get("api_request_snapshot")
        if not isinstance(snap, dict) or not snap.get("dataset_name"):
            snap = {
                "dataset_name": parent_cfg.get("dataset_name"),
                "model_type": parent_cfg.get("model_type"),
                "random_state": parent_cfg.get("random_state"),
                "test_size": parent_cfg.get("test_size"),
                "val_size": parent_cfg.get("val_size"),
                "sample_size_percentage": parent_cfg.get("sample_size_percentage"),
                "n_epochs": parent_cfg.get("n_epochs"),
                "selected_influence_methods": parent_cfg.get("selected_influence_methods")
                or [],
                "model_params": {},
            }
        if not snap.get("dataset_name"):
            raise ValueError(
                "Parent experiment has no api_request_snapshot and insufficient config to reproduce splits."
            )
        out = copy.deepcopy(snap)
        for k, v in removal_config.items():
            if v is not None:
                out[k] = copy.deepcopy(v) if isinstance(v, dict) else v
        return out

    def _run_removal_child_thread(
        self,
        child_id: str,
        parent_experiment_id: str,
        removal_config: Dict[str, Any],
    ):
        try:
            parent_bundle = self.storage.load_experiment(parent_experiment_id)
            if not parent_bundle:
                raise ValueError(f"Parent experiment not found: {parent_experiment_id}")
            parent_cfg = parent_bundle.get("config") or {}
            parent_results = parent_bundle.get("results") or {}
            scores = parent_bundle.get("influence_weights")
            if not scores:
                raise ValueError("Parent has no influence_weights; run influence phase first.")
            baseline_history = parent_results.get("orig")
            if baseline_history is None:
                raise ValueError("Parent results missing baseline ('orig').")

            api_child = self._merge_api_config_for_removal_child(
                parent_cfg, removal_config
            )
            merged = build_merged_config(api_child)
            mr_ch = merged.get("MODEL_RUN_CONFIG") or {}
            if api_child.get("removal_per_class") is not None:
                self.active_experiments[child_id]["removal_per_class"] = bool(
                    api_child.get("removal_per_class")
                )
            else:
                self.active_experiments[child_id]["removal_per_class"] = bool(
                    mr_ch.get("removal_per_class", False)
                )
            if api_child.get("removal_stratify_target") is not None:
                self.active_experiments[child_id]["removal_stratify_target"] = bool(
                    api_child.get("removal_stratify_target")
                )
            else:
                self.active_experiments[child_id]["removal_stratify_target"] = bool(
                    mr_ch.get("removal_stratify_target", False)
                )
            self.active_experiments[child_id]["removal_adaptive_model"] = bool(
                api_child.get("removal_adaptive_model", False)
            )

            with runtime_settings_patch(merged):
                import config.settings as S

                rs = int(api_child.get("random_state", S.RANDOM_STATE))
                set_random_seeds(rs)

                self._set_stage(child_id, 0)
                self._update_status(
                    child_id,
                    "running",
                    5.0,
                    f"Loading dataset {api_child['dataset_name']}…",
                )
                self._raise_if_cancelled(child_id)

                dataset_name = api_child["dataset_name"]
                dataset_config = DatasetRegistry.get(dataset_name)
                if bool(api_child.get("use_tfidf_lsa", False)) and hasattr(dataset_config, "use_tfidf_lsa"):
                    dataset_config.use_tfidf_lsa = True
                    lsa_components = api_child.get("lsa_components")
                    if lsa_components is not None:
                        dataset_config.lsa_n_components = int(lsa_components)
                    logger = ExperimentLogger(base_dir=EXPERIMENTS_BASE_DIR)
                    logger.log_message(
                        f"Используется TF-IDF + LSA: {dataset_config.lsa_n_components} компонент(ы)."
                    )
                else:
                    logger = ExperimentLogger(base_dir=EXPERIMENTS_BASE_DIR)

                X, y, cfg = DataLoaderFactory.load_dataset(dataset_config, logger)
                self._raise_if_cancelled(child_id)

                if cfg.task_type in [
                    "binary_classification",
                    "multiclass_classification",
                ]:
                    if y.dtype == "object":
                        le = LabelEncoder()
                        y = pd.Series(le.fit_transform(y), index=y.index)

                self._set_stage(child_id, 1)
                self._update_status(
                    child_id,
                    "running",
                    10.0,
                    "Splitting train / test / holdout…",
                )

                val_sz = float(
                    merged["EXPERIMENT_CONFIG"].get(
                        "val_size", api_child.get("val_size", 0.1)
                    )
                )
                X_temp, X_holdout_validation, y_temp, y_holdout_validation = split_data(
                    X,
                    y,
                    test_size=val_sz,
                    random_state=rs,
                    stratify=y if cfg.stratify else None,
                    time_series=cfg.use_time_split,
                )

                sample_pct = (
                    float(merged["EXPERIMENT_CONFIG"].get("sample_size_percentage", 100))
                    / 100.0
                )
                X_sample, y_sample = sample_data(
                    X_temp,
                    y_temp,
                    sample_fraction=sample_pct,
                    random_state=rs,
                    preserve_order=cfg.use_time_split,
                )

                test_sz = float(
                    merged["EXPERIMENT_CONFIG"].get(
                        "test_size", api_child.get("test_size", 0.2)
                    )
                )
                X_train, X_test, y_train, y_test = split_data(
                    X_sample,
                    y_sample,
                    test_size=test_sz,
                    random_state=rs,
                    time_series=cfg.use_time_split,
                )
                self._raise_if_cancelled(child_id)

                self._set_stage(child_id, 2)
                self._update_status(
                    child_id,
                    "running",
                    18.0,
                    "Fitting preprocessor…",
                )

                preprocessor = PreprocessorFactory.create(dataset_config, logger)
                preprocessor.fit(X_train)

                X_train_processed = preprocessor.transform(X_train)
                if hasattr(X_train_processed, "toarray"):
                    X_train_processed = X_train_processed.toarray()

                input_size = X_train_processed.shape[1]

                self._set_stage(child_id, 3)
                self._update_status(
                    child_id,
                    "running",
                    22.0,
                    "Loading model hyperparameters…",
                )

                from config.settings import (
                    get_model_config,
                    MODEL_FIT_MODE,
                    FIT_MODE_EPOCHS,
                    EXPERIMENT_CONFIG,
                )

                model_type = merged["MODEL_RUN_CONFIG"]["model_type"]
                try:
                    dataset_model_config = get_model_config(dataset_name, model_type)
                except ValueError:
                    dataset_model_config = {}

                mr = merged["MODEL_RUN_CONFIG"]
                dist = merged["DISTILLATION_CONFIG"]

                model_params = {
                    "model_type": model_type,
                    "task_type": cfg.task_type,
                    "available_metrics": list(getattr(cfg, "metrics", [])),
                    "input_size": input_size,
                    "device": S.DEVICE,
                    "removal_strategies": mr.get("removal_strategies")
                    or list(REMOVAL_STRATEGIES),
                    "removal_strategy": api_child.get(
                        "removal_strategy", "remove_lowest_influence"
                    ),
                    "removal_per_class": bool(mr.get("removal_per_class", False)),
                    "removal_stratify_target": bool(mr.get("removal_stratify_target", False)),
                    "removal_stratify_n_bins": int(mr.get("removal_stratify_n_bins", 10) or 10),
                    "use_distillation": dist.get("use_distillation", False),
                    "distillation_epochs": dist.get("distillation_epochs", 200),
                    "temperature": dist.get("temperature", 2.0),
                    "student_architecture": dist.get("student_architecture", "simple"),
                }
                rpc_ch = api_child.get("removal_per_class")
                if rpc_ch is not None:
                    model_params["removal_per_class"] = bool(rpc_ch)
                rst_ch = api_child.get("removal_stratify_target")
                if rst_ch is not None:
                    model_params["removal_stratify_target"] = bool(rst_ch)
                rnb_ch = api_child.get("removal_stratify_n_bins")
                if rnb_ch is not None:
                    model_params["removal_stratify_n_bins"] = int(rnb_ch)

                mp_user = api_child.get("model_params") or {}
                for key, value in dataset_model_config.items():
                    if key not in model_params or key in (
                        "learning_rate",
                        "num_leaves",
                        "max_depth",
                        "iterations",
                        "n_estimators",
                        "layers",
                        "dropout",
                        "base_channels",
                    ):
                        model_params[key] = value
                model_params.update(mp_user)

                if cfg.task_type == "multiclass_classification":
                    model_params["num_class"] = int(
                        len(np.unique(np.asarray(y_train).ravel()))
                    )

                if (
                    cfg.task_type == "binary_classification"
                    and model_params.get("model_type") == "pytorch"
                ):
                    y_flat = np.asarray(y_train).ravel()
                    n_pos = max(int((y_flat == 1).sum()), 1)
                    n_neg = int((y_flat == 0).sum())
                    model_params["pos_weight"] = n_neg / n_pos

                if model_params["model_type"] == "pytorch" or model_params.get(
                    "use_distillation", False
                ):
                    if MODEL_FIT_MODE != "normal" and MODEL_FIT_MODE in FIT_MODE_EPOCHS:
                        n_epochs = FIT_MODE_EPOCHS[MODEL_FIT_MODE]
                    else:
                        n_epochs = int(EXPERIMENT_CONFIG.get("n_epochs", 500))
                else:
                    n_epochs = 1

                n_remove_list = [
                    int(x)
                    for x in api_child.get(
                        "n_remove_percentages", list(range(1, 100, 5))
                    )
                ]

                self.active_experiments[child_id]["dataset"] = dataset_name
                self.active_experiments[child_id]["model"] = model_type
                self.active_experiments[child_id]["sample_size_percentage"] = merged[
                    "EXPERIMENT_CONFIG"
                ].get("sample_size_percentage", 100)

                self._set_stage(child_id, 4)
                self._update_status(
                    child_id,
                    "running",
                    28.0,
                    "Running removal from saved influence scores…",
                )
                self.active_experiments[child_id]["_last_progress_time"] = time.time()
                self.active_experiments[child_id]["_last_progress_value"] = 28.0

                experiment_runner = ExperimentRunner(logger)

                def _progress_cb(ev: Dict[str, Any]):
                    self._raise_if_cancelled(child_id)
                    self._map_runner_progress(child_id, ev)

                n_rand = api_child.get("n_random_runs")
                if n_rand is None:
                    n_rand = merged["EXPERIMENT_CONFIG"].get("n_random_runs")

                removal_adaptive_model = bool(api_child.get("removal_adaptive_model", False))

                results, scores_out, scores_raw_out, random_run_results = (
                    experiment_runner.run_removal_only(
                        X_train,
                        y_train,
                        X_test,
                        y_test,
                        X_holdout_validation,
                        y_holdout_validation,
                        preprocessor,
                        model_params,
                        scores,
                        baseline_history,
                        n_remove_list=n_remove_list,
                        n_epochs=n_epochs,
                        dataset_config=dataset_config,
                        progress_callback=_progress_cb,
                        n_random_runs=int(n_rand) if n_rand is not None else None,
                        removal_adaptive_model=removal_adaptive_model,
                    )
                )

                self._set_stage(child_id, 5)
                self._update_status(
                    child_id,
                    "running",
                    92.0,
                    "Finalizing and saving…",
                )

                scores_raw_parent = parent_bundle.get("scores_raw") or {}

                saved_config = {
                    "dataset_name": dataset_name,
                    "model_type": model_type,
                    "sample_size": len(X_train),
                    "features": input_size,
                    "n_remove_percentages": n_remove_list,
                    "removal_strategy": api_child.get("removal_strategy"),
                    "n_epochs": n_epochs,
                    "experiment_dir": str(logger.get_experiment_dir()),
                    "random_state": rs,
                    "test_size": test_sz,
                    "val_size": val_sz,
                    "sample_size_percentage": merged["EXPERIMENT_CONFIG"].get(
                        "sample_size_percentage", 100
                    ),
                    "target_column": getattr(dataset_config, "target_column", "target"),
                    "task_type": cfg.task_type,
                    "selected_influence_methods": api_child.get(
                        "selected_influence_methods"
                    )
                    or [],
                    "model_run_config": {
                        "removal_strategies": model_params.get("removal_strategies"),
                        "removal_per_class": model_params.get("removal_per_class"),
                        "removal_stratify_target": model_params.get(
                            "removal_stratify_target"
                        ),
                        "removal_stratify_n_bins": model_params.get(
                            "removal_stratify_n_bins"
                        ),
                    },
                    "experiment_kind": "removal_child",
                    "parent_experiment_id": parent_experiment_id,
                    "run_mode": "removal_child",
                    "removal_adaptive_model": removal_adaptive_model,
                    "api_request_snapshot": copy.deepcopy(api_child),
                }

                self.active_experiments[child_id]["result"] = {
                    "results": results,
                    "influence_weights": scores_out,
                    "scores_raw": scores_raw_out,
                    "random_run_results": random_run_results,
                    "config": saved_config,
                    "execution_time": time.time()
                    - self.active_experiments[child_id]["start_time"],
                }

                result = self.active_experiments[child_id]["result"]
                cfg_out = result.get("config", {})
                influence_weights = result.get("influence_weights", {})

                try:
                    logger.save_results(
                        result.get("results", {}),
                        influence_weights,
                        scores_raw_parent,
                        n_remove_list,
                        random_run_results=random_run_results,
                    )
                except Exception:
                    pass

                try:
                    _try_write_experiment_summary(
                        logger,
                        result.get("results", {}),
                        model_params,
                        n_epochs,
                        saved_config,
                        influence_weights,
                        scores_raw_parent,
                        n_remove_list=n_remove_list,
                        run_mode="removal_child",
                    )
                except Exception as e_sum:
                    print(f"Warning: failed to save experiment_summary (removal child): {e_sum}")

                if scores_raw_parent:
                    try:
                        plot_influence_distribution(
                            scores_raw_parent, "influence_scores", logger
                        )
                    except Exception:
                        pass

                try:
                    plot_results_enhanced(
                        result.get("results", {}),
                        n_remove_list,
                        logger,
                        random_run_results=getattr(
                            experiment_runner, "random_run_results", None
                        ),
                    )
                except Exception as e_plot:
                    print(
                        f"Warning: failed to save results comparison plot (child): {e_plot}"
                    )

                try:
                    plot_method_comparison_bars(
                        logger,
                        result.get("results", {}),
                        n_remove_list,
                        metric_metadata=METRIC_METADATA,
                    )
                except Exception as e_bars:
                    print(
                        f"Warning: failed to save method comparison bar plots (child): {e_bars}"
                    )

                self.storage.save_experiment(
                    child_id,
                    cfg_out,
                    result.get("results", {}),
                    influence_weights,
                    scores_raw_parent,
                    {"status": "completed", "saved_at": datetime.now().isoformat()},
                )

                self._update_status(
                    child_id,
                    "completed",
                    100.0,
                    "Removal experiment completed successfully!",
                )

        except ExperimentCancelled:
            if child_id in self.active_experiments:
                p = float(self.active_experiments[child_id].get("progress", 0.0))
                self._update_status(
                    child_id,
                    "cancelled",
                    p,
                    "Остановлено пользователем.",
                )
                self.active_experiments[child_id]["error"] = None
        except Exception as e:
            import traceback

            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            if child_id in self.active_experiments:
                self._update_status(child_id, "failed", 0.0, error_msg)
                self.active_experiments[child_id]["error"] = error_msg
        finally:
            self._cancel_events.pop(child_id, None)

    def _update_status(
        self,
        experiment_id: str,
        status: str,
        progress: float,
        message: str,
    ):
        if experiment_id in self.active_experiments:
            self.active_experiments[experiment_id].update(
                {
                    "status": status,
                    "progress": min(100.0, max(0.0, float(progress))),
                    "message": message,
                }
            )

    def get_result(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        exp_info = self.active_experiments.get(experiment_id)
        if exp_info:
            return exp_info.get("result")
        return None

    def get_error(self, experiment_id: str) -> Optional[str]:
        exp_info = self.active_experiments.get(experiment_id)
        if exp_info:
            return exp_info.get("error")
        return None
