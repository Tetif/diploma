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
MODEL_SPECIFIC = ['CatBoostLFC', 'BoostIn']       # CatBoost LossFunctionChange; BoostIn (GBDT, [AUDIT-FIX P10])
# BoostIn via tree_influence: LightGBM only. CatBoost: our models use leaf_estimation_iterations=10 (Logloss
# default), the package needs 1; XGBoost>=2: base_score is estimated, the parser assumes 0 (mismatch).
BOOSTIN_MODELS = ('lightgbm',)
ALL_METHODS = VALUATION + CLOSED_FORM + INFLUENCE + BASELINES + MODEL_SPECIFIC
METHOD_LABELS = {
    'LOO': 'LOO', 'TMCShapley': 'TMC-Shapley', 'KNNShapley': 'KNN-Shapley', 'DataOOB': 'Data-OOB',
    'Influence': 'Influence (direct)', 'LissaInfluence': 'Influence (LiSSA)', 'LossHigh': 'Loss (high first)',
    'random': 'random', 'CatBoostLFC': 'CatBoost LFC', 'BoostIn': 'BoostIn',
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
    model_type: str = 'pytorch'               # 'pytorch' | 'lightgbm' | 'xgboost' | 'catboost' | 'random_forest'
    model_architecture: str = 'simple'        # pytorch: 'simple' (MLP) | 'linear' (logistic / linear regression)
    distill: bool = False                     # tree teacher (model_type) -> MLP student (values via the student)
    noise_kind: str = 'random'                # 'random' | 'systematic' (see study/data.py)
    fit_mode: str = 'normal'                  # 'normal' | 'underfit' | 'overfit'
    n_epochs: int = 300                       # main training epochs (early stopping, patience 70 epochs)
    batch_size: int = 128                     # [AUDIT-FIX B11] mini-batch epochs; 0 = legacy (1 epoch =
                                              # 1 full-batch step, the MLPs stopped after ~30-50 steps)
    valuation_epochs: int = 30                # epochs of every pyDVL refit (no early stopping there)
    tmc_permutations: int = 10
    damping: Optional[float] = None           # Influence/LiSSA regularization; None = dataset default
    knn_k: int = 5
    oob_estimators: int = 200
    sample_scale: float = 1.0                 # multiplies the dataset's n_train (sweep: 0.1 / 0.3 / 1.0)
    distill_influence_target: str = 'true_labels'  # [AUDIT-FIX P9] distill: influence of the student w.r.t.
                                              # 'true_labels' | 'teacher' (its own training targets)
    tree_class_weight: Optional[str] = 'balanced'  # [AUDIT-FIX P8] classification trees (also distillation
                                              # teachers): 'balanced' (like the MLP's pos_weight) | None

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
    # param: (values, methods to run). Noise rate, damping and model type moved to the extension study
    # (sections noise / convex / models), which covers them on all datasets; see run_study.py ext.
    'sample_scale': ([0.1, 0.3, 1.0], _ALL_BUT_TMC),
    'valuation_epochs': ([10, 30, 60], ['LOO', 'random']),
    'batch_size': ([0, 128], _ALL_BUT_TMC),   # 0 = legacy full-batch training (before AUDIT-FIX B11)
    'fit_mode': (['underfit', 'normal', 'overfit'], _ALL_BUT_TMC),
}


def sweep_study(param: str, value) -> str:
    """Study name of a sweep point; points equal to SWEEP_BASE share the study 'sweep-base'."""
    if getattr(SWEEP_BASE, param) == value:
        return 'sweep-base'
    return f'sweep-{param}-{value}'


def sweep_specs() -> List[Tuple[str, object, RunSpec, List[str]]]:
    """[(param, value, spec, methods)] for every distinct sweep point. Points equal to SWEEP_BASE are merged
    into one 'sweep-base' entry (param 'base') that runs the union of their methods."""
    out, base_methods = [], []
    for param, (values, methods) in SWEEP_GRID.items():
        for v in values:
            if sweep_study(param, v) == 'sweep-base':
                base_methods += [m for m in methods if m not in base_methods]
                continue
            out.append((param, v, replace(SWEEP_BASE, study=sweep_study(param, v), **{param: v}), list(methods)))
    if base_methods:
        out.insert(0, ('base', '-', replace(SWEEP_BASE, study='sweep-base'), base_methods))
    return out


def methods_for(model_type: str, task_type: str, methods: List[str], distill: bool = False) -> List[str]:
    """Drop methods that cannot run for this model / task (reported as skipped)."""
    out = []
    for m in methods:
        if m in INFLUENCE and model_type != 'pytorch' and not distill:
            continue
        if m == 'CatBoostLFC' and model_type != 'catboost':     # distill: LFC of the CatBoost teacher [P11]
            continue
        if m == 'BoostIn' and model_type not in BOOSTIN_MODELS:
            continue
        out.append(m)
    return out


# ================================================================ extensions (secondary studies, 3 seeds)
# Same datasets / splits / seeds as the main study (make_split depends only on dataset, seed, noise), so
# every secondary study is paired with the main one seed by seed.
EXT_SEEDS = [0, 1, 2]
EXT_DATASETS: Dict[str, DatasetSpec] = {k: replace(v, methods=()) for k, v in MAIN_DATASETS.items()}
_NOISE10 = dict(task='noise', noise_rate=0.10, strategies=('lowest',), fracs=(5, 10, 20))

# 1. models: the same protocol with tree ensembles instead of the MLP (MLP = the main study)
TREE_MODELS = ['lightgbm', 'xgboost', 'catboost', 'random_forest']
TREE_METHODS = ['LOO', 'KNNShapley', 'DataOOB', 'LossHigh', 'random']


def models_specs() -> List[Tuple[RunSpec, List[str], List[str]]]:
    """[(spec, methods, datasets)]"""
    out = []
    for m in TREE_MODELS:
        meths = TREE_METHODS + (['CatBoostLFC'] if m == 'catboost' else []) \
            + (['BoostIn'] if m in BOOSTIN_MODELS else [])               # [AUDIT-FIX P10]
        for task, kw in (('clean', dict(task='clean')), ('noise10', _NOISE10)):
            out.append((RunSpec(f'models-{m}-{task}', model_type=m, **kw), meths, list(EXT_DATASETS)))
    return out


# 2. convex sanity check: influence on logistic / linear regression vs the MLP, damping 1e-6 .. 1
DAMPINGS = [1e-6, 1e-4, 1e-2, 1.0]
CONVEX_METHODS = ['Influence', 'LissaInfluence', 'LossHigh', 'random']


def convex_specs():
    out = []
    for arch, dss in (('linear', list(EXT_DATASETS)), ('simple', ['wine', 'housing', 'adult'])):
        for d in DAMPINGS:
            out.append((RunSpec(f'damp-{"mlp" if arch == "simple" else arch}-{d:g}', model_architecture=arch,
                                damping=d, **_NOISE10), list(CONVEX_METHODS), dss))
    return out


# 3. distillation: tree teacher -> MLP student; influence through the student
DISTILL_TEACHERS = ['lightgbm', 'catboost']
DISTILL_METHODS = ['Influence', 'LissaInfluence', 'LossHigh', 'random']
# [AUDIT-FIX P9-P11] direct baselines on the same noisy split, computed on the TEACHER (removal curves of every
# method retrain teacher + student, see protocol._curve); influence of the student also w.r.t. the teacher.
DISTILL_DIRECT = ['BoostIn', 'CatBoostLFC', 'DataOOB']
DISTILL_TEACHER_TARGET_METHODS = ['Influence', 'LissaInfluence']


def distill_specs():
    out = []
    for t in DISTILL_TEACHERS:
        out.append((RunSpec(f'distill-{t}-noise10', model_type=t, distill=True, **_NOISE10),
                    list(DISTILL_METHODS) + methods_for(t, '', DISTILL_DIRECT, distill=True), list(EXT_DATASETS)))
        out.append((RunSpec(f'distill-{t}-noise10-tgtteacher', model_type=t, distill=True,
                            distill_influence_target='teacher', **_NOISE10),
                    list(DISTILL_TEACHER_TARGET_METHODS), list(EXT_DATASETS)))
    return out


# 5. systematic vs random noise at 5 / 10 / 20 % (MLP; random 10 % = main study "noise10")
NOISE_METHODS = ['KNNShapley', 'DataOOB', 'Influence', 'LissaInfluence', 'LossHigh', 'random']


def noise_specs():
    out = []
    for rate in (0.05, 0.10, 0.20):
        pct = int(round(rate * 100))
        kinds = [('systematic', f'sysnoise{pct}')] + ([] if pct == 10 else [('random', f'noise{pct}')])
        for kind, name in kinds:
            spec = replace(RunSpec(name, **_NOISE10), noise_rate=rate, noise_kind=kind)
            out.append((spec, list(NOISE_METHODS), list(EXT_DATASETS)))
    return out


def noise_methods_for(dataset: str, methods: List[str]) -> List[str]:
    # covertype direct influence costs ~8 min per run (54 features x 7 classes MLP): main study only
    return [m for m in methods if not (dataset == 'covertype' and m == 'Influence')]


# 4. transfer: values from a source (study, model, method) -> removal retrained with a target model
TRANSFER_TARGETS = ['pytorch', 'lightgbm', 'xgboost', 'catboost', 'random_forest', 'distill-lightgbm']
TRANSFER_SOURCES: List[Tuple[str, str, str]] = (
    [('noise10', 'pytorch', m) for m in ('LOO', 'Influence', 'LissaInfluence', 'LossHigh')]
    + [(f'models-{t}-noise10', t, m) for t in TREE_MODELS for m in ('LOO', 'LossHigh')]
    + [('models-catboost-noise10', 'catboost', 'CatBoostLFC'),
       ('distill-lightgbm-noise10', 'distill-lightgbm', 'Influence'),
       ('distill-lightgbm-noise10', 'distill-lightgbm', 'LossHigh'),
       ('noise10', 'any', 'DataOOB'), ('noise10', 'any', 'KNNShapley')])


def transfer_target_spec(target: str) -> RunSpec:
    distill = target.startswith('distill-')
    mt = target.split('-', 1)[1] if distill else target
    return RunSpec(f'transfer-{target}', model_type=mt, distill=distill, **_NOISE10)


def transfer_specs():
    return [(transfer_target_spec(t), list(EXT_DATASETS)) for t in TRANSFER_TARGETS]
