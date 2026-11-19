"""Study definitions: what to run (datasets x methods x seeds x tasks) and with which settings.

A *study* is a named set of runs that share all settings except dataset / method / seed.
Results go to ``results/<study>/<dataset>/<method>/seed<k>/results.json``.

Two tasks:
  * ``clean``  - removal curves on clean data: remove the lowest- / highest-value points first,
                 compare with random removal and the full-data model.
  * ``noise``  - ``noise_rate`` of training labels corrupted (classification: label flip,
                 regression: y outliers of +-3 std). Report detection AUC / found@k of the
                 corrupted points and the removal curve "lowest first".
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Dict, List, Optional, Tuple

# Methods. "random" is the removal baseline and has no values.
VALUATION = ['LOO', 'TMCShapley']                 # retrain-based (pyDVL), cost ~ n_train * refits
CLOSED_FORM = ['KNNShapley', 'DataOOB']           # cheap, model-agnostic baselines
INFLUENCE = ['Influence', 'LissaInfluence']       # Hessian-based, need a torch model
BASELINES = ['LossHigh', 'random']
ALL_METHODS = VALUATION + CLOSED_FORM + INFLUENCE + BASELINES
METHOD_LABELS = {
    'LOO': 'LOO', 'TMCShapley': 'TMC-Shapley', 'KNNShapley': 'KNN-Shapley', 'DataOOB': 'Data-OOB',
    'Influence': 'Influence (direct)', 'LissaInfluence': 'Influence (LiSSA)', 'LossHigh': 'Loss (high first)',
    'random': 'random',
}

MAIN_METHODS = ['LOO', 'KNNShapley', 'DataOOB', 'Influence', 'LissaInfluence', 'LossHigh', 'random']


@dataclass(frozen=True)
class RunSpec:
    """All settings of one study (everything except dataset / method / seed)."""
    study: str
    task: str = 'clean'                      # 'clean' | 'noise'
    noise_rate: float = 0.0
    fracs: Tuple[int, ...] = (5, 10, 20, 30)  # % of train removed
    strategies: Tuple[str, ...] = ('lowest', 'highest')
    model_type: str = 'pytorch'               # 'pytorch' | 'lightgbm'
    fit_mode: str = 'normal'                  # 'normal' | 'underfit' | 'overfit'
    n_epochs: int = 300                       # main training (early stopping, patience 70)
    valuation_epochs: int = 100               # full-batch epochs of every pyDVL refit
    tmc_permutations: int = 10
    damping: Optional[float] = None           # Influence/LiSSA regularization; None = dataset default
    knn_k: int = 5
    oob_estimators: int = 200
    sample_scale: float = 1.0                 # multiplies the dataset's n_train (sweep: 0.1 / 0.3 / 1.0)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    n_train: Optional[int]                    # None = all available (after holdout)
    max_holdout: int = 5000
    methods: Tuple[str, ...] = tuple(MAIN_METHODS)


# ---------------------------------------------------------------- main study
MAIN_DATASETS: Dict[str, DatasetSpec] = {
    'wine': DatasetSpec('wine', n_train=None, methods=tuple(MAIN_METHODS + ['TMCShapley'])),
    'housing': DatasetSpec('housing', n_train=1500),
    'adult': DatasetSpec('adult', n_train=1500),
    'covertype': DatasetSpec('covertype', n_train=1500),
}
MAIN_SEEDS = [0, 1, 2, 3, 4]
MAIN_STUDIES = {
    'clean': RunSpec('clean', task='clean'),
    'noise10': RunSpec('noise10', task='noise', noise_rate=0.10, strategies=('lowest',), fracs=(5, 10, 20)),
}

# ---------------------------------------------------------------- sensitivity sweep
# One factor at a time around SWEEP_BASE on SWEEP_DATASET; each point is its own study
# "sweep-<param>-<value>". Only the methods affected by the parameter are rerun.
SWEEP_DATASET = DatasetSpec('adult', n_train=1500)
SWEEP_SEEDS = [0, 1, 2]
SWEEP_BASE = RunSpec('sweep-base', task='noise', noise_rate=0.10, strategies=('lowest',), fracs=(5, 10, 20))
_ALL_BUT_TMC = ['LOO', 'KNNShapley', 'DataOOB', 'Influence', 'LissaInfluence', 'LossHigh', 'random']
SWEEP_GRID: Dict[str, Tuple[List, List[str]]] = {
    # param: (values, methods to run)
    'noise_rate': ([0.0, 0.05, 0.10, 0.20], _ALL_BUT_TMC),
    'sample_scale': ([0.1, 0.3, 1.0], _ALL_BUT_TMC),
    'damping': ([1e-4, 1e-3, 1e-2, 1e-1], ['Influence', 'LissaInfluence', 'random']),
    'valuation_epochs': ([20, 50, 200], ['LOO', 'random']),
    'fit_mode': (['underfit', 'normal', 'overfit'], _ALL_BUT_TMC),
    'model_type': (['pytorch', 'lightgbm'], ['LOO', 'KNNShapley', 'DataOOB', 'LossHigh', 'random']),
}


def sweep_specs() -> List[Tuple[str, object, RunSpec, List[str]]]:
    """[(param, value, spec, methods)] for every sweep point."""
    out = []
    for param, (values, methods) in SWEEP_GRID.items():
        for v in values:
            spec = replace(SWEEP_BASE, study=f'sweep-{param}-{v}', **{param: v})
            if param == 'noise_rate' and v == 0.0:
                spec = replace(spec, task='clean', strategies=('lowest',))
            out.append((param, v, spec, list(methods)))
    return out


def methods_for(model_type: str, task_type: str, methods: List[str]) -> List[str]:
    """Drop methods that cannot run for this model / task (reported as skipped)."""
    out = []
    for m in methods:
        if m in INFLUENCE and model_type != 'pytorch':
            continue
        out.append(m)
    return out
