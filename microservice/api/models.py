"""Pydantic models for API"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Dict, Any, Optional
from enum import Enum


class TaskType(str, Enum):
    REGRESSION = "regression"
    BINARY_CLASSIFICATION = "binary_classification"
    MULTICLASS_CLASSIFICATION = "multiclass_classification"


_MODEL_TYPES = frozenset(
    {"random_forest", "lightgbm", "xgboost", "catboost", "pytorch"}
)
_REMOVAL_STRATEGIES = frozenset(
    {"remove_lowest_influence", "remove_highest_influence"}
)

_MODEL_FIT_MODES = frozenset({"normal", "underfit", "overfit"})

# Стратегии удаления (MODEL_RUN_CONFIG / runner), не путать с legacy removal_strategy API.
_RUNNER_REMOVAL_STRATEGIES = frozenset(
    {
        "lowest",
        "highest",
        "random",
        "extremes",
        "median",
        "few_bad_then_random",
        "few_median_then_random",
        "few_good_then_random",
    }
)

_LOSS_REMOVAL_KEYS = frozenset({"loss_high", "loss_low"})

_METRIC_BY_TASK = {
    "regression": frozenset({"mae", "rmse", "r2"}),
    "binary_classification": frozenset(
        {"accuracy", "f1", "precision", "recall"}
    ),
    "multiclass_classification": frozenset(
        {"accuracy", "f1_weighted", "f1_macro"}
    ),
}

_STUDENT_ARCH = frozenset({"simple", "improved"})


class ExperimentConfig(BaseModel):
    """Configuration for experiment (flat fields + optional nested overrides)."""

    model_config = ConfigDict(use_enum_values=True, extra="allow")

    dataset_name: str
    model_type: str
    removal_strategy: str = "remove_lowest_influence"
    n_remove_percentages: List[int] = Field(
        default_factory=lambda: list(range(1, 100, 5))
    )
    sample_size_percentage: float = Field(default=100, ge=1, le=100)
    test_size: float = Field(default=0.2, ge=0.05, le=0.5)
    val_size: float = Field(default=0.1, ge=0.05, le=0.3)
    n_epochs: int = Field(default=500, ge=1)
    n_random_runs: int = Field(default=3, ge=1, le=10)
    cv_folds: int = Field(default=1, ge=1, le=10)
    selected_influence_methods: List[str] = Field(default_factory=list)
    model_params: Dict[str, Any] = Field(default_factory=dict)
    use_distillation: bool = False
    distillation_epochs: int = 200
    distillation_temperature: Optional[float] = None
    student_architecture: Optional[str] = None
    random_state: int = 42
    debug_mode: bool = False
    overrides: Optional[Dict[str, Any]] = None

    # --- Расширение под config/settings.py (плоские поля → config_merge) ---
    model_fit_mode: Optional[str] = None
    removal_strategies: Optional[List[str]] = None
    metric_config: Optional[Dict[str, str]] = None
    n_retrain_runs: Optional[int] = None
    loss_removal_methods: Optional[List[str]] = None
    use_catboost_influence: Optional[bool] = None
    show_top_bottom_influence: Optional[int] = None
    use_tfidf_lsa: bool = False
    lsa_components: Optional[int] = None
    influence_params: Optional[Dict[str, Any]] = None
    device: Optional[str] = None
    use_cache: Optional[bool] = None
    n_jobs: Optional[int] = None
    fit_mode_epochs: Optional[Dict[str, int]] = None
    run_mode: Optional[str] = Field(
        default=None,
        description="full (default) or influence_only (skip removal phase)",
    )
    removal_adaptive_model: bool = False
    # Классификация: удаление по доле внутри каждого класса (см. MODEL_RUN_CONFIG['removal_per_class'])
    removal_per_class: Optional[bool] = None
    # Регрессия: удаление по доле внутри квантильных страт целевой (см. MODEL_RUN_CONFIG)
    removal_stratify_target: Optional[bool] = None
    removal_stratify_n_bins: Optional[int] = Field(
        default=None,
        ge=2,
        le=100,
        description="Число квантильных бинов по y для removal_stratify_target",
    )

    @field_validator("run_mode")
    @classmethod
    def validate_run_mode(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        vv = str(v).lower()
        if vv not in ("full", "influence_only"):
            raise ValueError("run_mode must be 'full' or 'influence_only'")
        return vv

    @field_validator("dataset_name")
    @classmethod
    def validate_dataset(cls, v: str) -> str:
        from config import DatasetRegistry

        if v not in DatasetRegistry.list():
            raise ValueError(
                f"Unknown dataset: {v}. Valid: {DatasetRegistry.list()}"
            )
        return v

    @field_validator("model_type")
    @classmethod
    def validate_model_type(cls, v: str) -> str:
        if v not in _MODEL_TYPES:
            raise ValueError(
                f"Unknown model_type: {v}. Valid: {sorted(_MODEL_TYPES)}"
            )
        return v

    @field_validator("removal_strategy")
    @classmethod
    def validate_removal_strategy(cls, v: str) -> str:
        if v not in _REMOVAL_STRATEGIES:
            raise ValueError(
                f"Unknown removal_strategy: {v}. Valid: {sorted(_REMOVAL_STRATEGIES)}"
            )
        return v

    @field_validator("model_fit_mode")
    @classmethod
    def validate_model_fit_mode(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v not in _MODEL_FIT_MODES:
            raise ValueError(
                f"Unknown model_fit_mode: {v}. Valid: {sorted(_MODEL_FIT_MODES)}"
            )
        return v

    @field_validator("removal_strategies")
    @classmethod
    def validate_removal_strategies(
        cls, v: Optional[List[str]]
    ) -> Optional[List[str]]:
        if not v:
            return v
        bad = [x for x in v if x not in _RUNNER_REMOVAL_STRATEGIES]
        if bad:
            raise ValueError(
                f"Unknown removal_strategies: {bad}. "
                f"Valid: {sorted(_RUNNER_REMOVAL_STRATEGIES)}"
            )
        return v

    @field_validator("loss_removal_methods")
    @classmethod
    def validate_loss_removal_methods(
        cls, v: Optional[List[str]]
    ) -> Optional[List[str]]:
        if not v:
            return v
        bad = [x for x in v if x not in _LOSS_REMOVAL_KEYS]
        if bad:
            raise ValueError(
                f"Unknown loss_removal_methods: {bad}. "
                f"Valid: {sorted(_LOSS_REMOVAL_KEYS)}"
            )
        return v

    @field_validator("metric_config")
    @classmethod
    def validate_metric_config(
        cls, v: Optional[Dict[str, str]]
    ) -> Optional[Dict[str, str]]:
        if not v:
            return v
        for task, metric in v.items():
            if task not in _METRIC_BY_TASK:
                raise ValueError(
                    f"Unknown metric_config task key: {task}. "
                    f"Valid: {list(_METRIC_BY_TASK)}"
                )
            allowed = _METRIC_BY_TASK[task]
            if metric not in allowed:
                raise ValueError(
                    f"Metric '{metric}' not allowed for {task}. Valid: {sorted(allowed)}"
                )
        return v

    @field_validator("student_architecture")
    @classmethod
    def validate_student_architecture(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v not in _STUDENT_ARCH:
            raise ValueError(
                f"Unknown student_architecture: {v}. Valid: {sorted(_STUDENT_ARCH)}"
            )
        return v

    @field_validator("device")
    @classmethod
    def validate_device(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if v not in ("cpu", "cuda"):
            raise ValueError("device must be 'cpu' or 'cuda'")
        return v

    @field_validator("n_retrain_runs")
    @classmethod
    def validate_n_retrain_runs(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        if v < 1 or v > 20:
            raise ValueError("n_retrain_runs must be between 1 and 20")
        return v

    @field_validator("n_jobs")
    @classmethod
    def validate_n_jobs(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        if v < 1 or v > 64:
            raise ValueError("n_jobs must be between 1 and 64")
        return v

    @field_validator("lsa_components")
    @classmethod
    def validate_lsa_components(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return v
        if v < 10 or v > 1000:
            raise ValueError("lsa_components must be between 10 and 1000")
        return v

    @field_validator("fit_mode_epochs")
    @classmethod
    def validate_fit_mode_epochs(
        cls, v: Optional[Dict[str, int]]
    ) -> Optional[Dict[str, int]]:
        if not v:
            return v
        for key in v:
            if key not in ("underfit", "overfit"):
                raise ValueError(
                    "fit_mode_epochs keys must be 'underfit' and/or 'overfit'"
                )
        return v


class ExperimentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ExperimentStartRequest(BaseModel):
    """Request to start experiment"""

    config: ExperimentConfig


class RemovalChildRequest(BaseModel):
    """Removal-only run using parent's saved influence weights."""

    removal_strategies: List[str]
    n_remove_percentages: List[int] = Field(
        default_factory=lambda: list(range(1, 100, 5))
    )
    n_random_runs: Optional[int] = Field(default=None, ge=1, le=50)
    removal_strategy: Optional[str] = "remove_lowest_influence"
    n_retrain_runs: Optional[int] = Field(default=None, ge=1, le=20)
    removal_adaptive_model: bool = False
    removal_per_class: Optional[bool] = None
    removal_stratify_target: Optional[bool] = None
    removal_stratify_n_bins: Optional[int] = Field(default=None, ge=2, le=100)

    @field_validator("removal_strategies")
    @classmethod
    def validate_removal_strategies(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("removal_strategies must be non-empty")
        bad = [x for x in v if x not in _RUNNER_REMOVAL_STRATEGIES]
        if bad:
            raise ValueError(
                f"Unknown removal_strategies: {bad}. "
                f"Valid: {sorted(_RUNNER_REMOVAL_STRATEGIES)}"
            )
        return v


class ExportTrainSubsetRequest(BaseModel):
    """Export training subset after removing top fraction by method + strategy."""

    method: str = Field(..., description="Influence method name (e.g. NystroemSketchInfluence)")
    strategy: str = Field(
        ...,
        description="Removal strategy: lowest, highest, extremes, median, random, ...",
    )
    removal_percent: int = Field(..., ge=0, le=100)
    removal_per_class: Optional[bool] = None
    removal_stratify_target: Optional[bool] = None
    removal_stratify_n_bins: Optional[int] = Field(default=None, ge=2, le=100)


class ExperimentStatusResponse(BaseModel):
    """Response with experiment status"""

    experiment_id: str
    status: ExperimentStatus
    progress: float = 0.0
    message: Optional[str] = None
    results_path: Optional[str] = None


class InfluenceWeightsResponse(BaseModel):
    """Response with influence weights"""

    experiment_id: str
    method: str
    weights: List[float]
    sample_indices: List[int]
    statistics: Dict[str, Any]


class ExperimentResultsResponse(BaseModel):
    """Response with experiment results"""

    experiment_id: str
    config: Dict[str, Any]
    results: Dict[str, Any]
    influence_weights: Dict[str, List[float]]
    scores_raw: Dict[str, List[float]]
    execution_time: float
