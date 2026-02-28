"""Pydantic models for API"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum


class TaskType(str, Enum):
    REGRESSION = "regression"
    BINARY_CLASSIFICATION = "binary_classification"
    MULTICLASS_CLASSIFICATION = "multiclass_classification"


class DatasetType(str, Enum):
    ADULT = "adult"
    HOUSING = "housing"
    WINE = "wine"
    ZILLOW = "zillow"


class ModelType(str, Enum):
    RANDOM_FOREST = "random_forest"
    LIGHTGBM = "lightgbm"
    XGBOOST = "xgboost"
    CATBOOST = "catboost"
    PYTORCH = "pytorch"


class RemovalStrategy(str, Enum):
    REMOVE_LOWEST = "remove_lowest_influence"
    REMOVE_HIGHEST = "remove_highest_influence"


class InfluenceMethod(str, Enum):
    LOO = "LOO"
    DATA_SHAPLEY = "DataShapley"
    BETA_SHAPLEY = "BetaShapley"
    SHAPLEY = "Shapley"
    BANZHAF = "Banzhaf"
    TMC_SHAPLEY = "TMCShapley"
    KNN_SHAPLEY = "KNNShapley"
    DATA_OOB = "DataOOB"
    LEAST_CORE = "LeastCore"
    INFLUENCE = "Influence"
    ARNOLDI_INFLUENCE = "ArnoldiInfluence"
    CG_INFLUENCE = "CgInfluence"
    LISSA_INFLUENCE = "LissaInfluence"
    NYSTROEM_INFLUENCE = "NystroemSketchInfluence"
    PERMUTATION = "PermutationImportance"


class ExperimentConfig(BaseModel):
    """Configuration for experiment"""
    dataset_name: DatasetType
    model_type: ModelType
    removal_strategy: RemovalStrategy = RemovalStrategy.REMOVE_LOWEST
    n_remove_percentages: List[int] = Field(default_factory=lambda: list(range(1, 100, 5)))
    sample_size_percentage: float = Field(default=100, ge=1, le=100)
    test_size: float = Field(default=0.2, ge=0.1, le=0.5)
    val_size: float = Field(default=0.1, ge=0.05, le=0.3)
    n_epochs: int = Field(default=500, ge=1)
    n_random_runs: int = Field(default=3, ge=1, le=10)
    cv_folds: int = Field(default=1, ge=1, le=10)
    selected_influence_methods: List[InfluenceMethod] = Field(default_factory=list)
    model_params: Dict[str, Any] = Field(default_factory=dict)
    use_distillation: bool = False
    distillation_epochs: int = 200
    random_state: int = 39
    debug_mode: bool = False

    class Config:
        use_enum_values = True


class ExperimentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ExperimentStartRequest(BaseModel):
    """Request to start experiment"""
    config: ExperimentConfig


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
