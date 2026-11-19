"""Data values per training point. Convention everywhere: higher value = more useful point.

* LOO, TMCShapley, Influence, LissaInfluence - through the project's ``InfluenceMethods`` (pyDVL),
  i.e. exactly the code path of main.py with all [AUDIT-FIX] corrections.
* KNNShapley - pyDVL ``KNNShapleyValuation`` (exact, closed form; classification only).
* DataOOB - pyDVL ``DataOOBValuation`` on a bagged decision-tree ensemble (Kwon & Zou, 2023).
* LossHigh - minus the per-sample training loss of the full model (high loss = low value).
* CatBoostLFC - CatBoost object importance (LossFunctionChange) of the CatBoost model itself.
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Tuple

import numpy as np
from sklearn.pipeline import Pipeline

PYDVL_VIA_PROJECT = ('LOO', 'TMCShapley', 'Influence', 'LissaInfluence')


def _lissa_scale(dataset: str) -> float:
    import config.settings as S
    return float(S.get_influence_params(dataset)['lissa_params']['scale'])


class NotApplicable(Exception):
    """Method does not apply to this dataset / model (stored as status 'skipped')."""


def _dense(X):
    X = X.toarray() if hasattr(X, 'toarray') else X
    return np.asarray(X, dtype=np.float64)


def _result_to_array(result, n: int) -> np.ndarray:
    out = np.full(n, np.nan)
    out[np.asarray(result.indices, dtype=int)] = np.asarray(result.values, dtype=float)
    return out


def _valuation_result(valuation):
    res = getattr(valuation, 'result', None)
    if res is None or callable(res):
        res = valuation.values()
    return res


@contextmanager
def _overrides(dataset: str, spec):
    """Temporarily apply per-study settings that live in config.settings globals."""
    import config.settings as S
    tmc = S.PYDVL_CONFIG['tmc_shapley_params']
    old_tmc = tmc.get('n_samples')
    infl = S.DATASET_INFLUENCE_PARAMS.get(dataset)
    old_reg = infl.get('regularization') if infl else None
    tmc['n_samples'] = int(spec.tmc_permutations)
    if spec.damping is not None and infl is not None:
        infl['regularization'] = float(spec.damping)
    try:
        yield
    finally:
        tmc['n_samples'] = old_tmc
        if infl is not None:
            infl['regularization'] = old_reg


def compute_values(method: str, trainer, model, y_scaler, spec, seed: int) -> Tuple[np.ndarray, dict]:
    """Return (values[n_train], info)."""
    sp = trainer.split
    n = len(sp.X_train)
    info: dict = {}
    if method in PYDVL_VIA_PROJECT:
        from influence.methods import InfluenceMethods, LISSA_MAXITER
        import config.settings as S
        if method in ('Influence', 'LissaInfluence') and not trainer.is_torch:
            raise NotApplicable(f'{method} needs a torch model (MLP, linear or distilled student)')
        pipe = Pipeline([('preproc', trainer.pre), ('model', model)])
        im = InfluenceMethods(None, dataset_config=sp.cfg)
        im.seed = int(seed)                     # [AUDIT-FIX P2/P4] TMC permutations, LiSSA batch shuffling
        if spec.damping is not None:
            # [AUDIT-FIX P1] damping sweep: lambda_eff = regularization (+ scale*0) for BOTH Direct and LiSSA.
            # Before, LiSSA kept dampen from the dataset config, so lambda_eff = reg + scale*dampen = 3..12.
            im.lissa_dampen_override = 0.0
        with _overrides(sp.dataset, spec):
            meths, _ = im.setup_methods(pipe, sp.X_train, sp.y_train, sp.X_val, sp.y_val, trainer.pre,
                                        methods_to_use=[method], y_scaler=y_scaler)
            if method not in meths:
                raise RuntimeError(f'{method}: setup failed ({im.failed_methods or "not created"})')
            scores, _ = im.compute_scores(meths, sp.X_train, sp.y_train, trainer.pre, sp.X_val, sp.y_val,
                                          pipe, y_scaler=y_scaler)
        if method in im.failed_methods:
            raise RuntimeError(f'{method}: {im.failed_methods[method]}')
        if method in im.effective_damping:      # [AUDIT-FIX P1]
            info['effective_damping'] = im.effective_damping[method]
            if method == 'LissaInfluence':
                lp = S.get_influence_params(sp.dataset)['lissa_params'] if spec.damping is None else None
                info['lissa'] = {'scale': _lissa_scale(sp.dataset), 'maxiter': LISSA_MAXITER,
                                 'dampen': 0.0 if spec.damping is not None else float(lp['damping']),
                                 # truncated Neumann series (maxiter terms) cannot resolve damping below ~scale/maxiter
                                 'implicit_damping_floor': _lissa_scale(sp.dataset) / LISSA_MAXITER}
        if method == 'TMCShapley':              # [AUDIT-FIX P2]
            info['tmc'] = {'permutations': int(spec.tmc_permutations), 'seed': int(seed),
                           'truncation': 'RelativeTruncation(rtol=0.01, burn_in_fraction=0.4)'}
        return np.asarray(scores[method], dtype=float), info

    if method == 'LossHigh':
        from experiments.metrics import compute_per_sample_loss
        pipe = Pipeline([('preproc', trainer.pre), ('model', model)])
        return -np.asarray(compute_per_sample_loss(pipe, sp.X_train, sp.y_train, sp.task_type), float), info

    if method == 'CatBoostLFC':
        if trainer.model_type != 'catboost' or trainer.spec.distill:
            raise NotApplicable('CatBoost LossFunctionChange needs the CatBoost model itself')
        if sp.is_classification and len(np.unique(sp.y_train)) > 2:
            # CatBoost get_object_importance: 'MultiClass is not supported yet in ostr mode'
            raise NotApplicable('CatBoost LossFunctionChange does not support MultiClass (covertype)')
        from experiments.catboost_importance import compute_catboost_object_importance
        pipe = Pipeline([('preproc', trainer.pre), ('model', model)])
        v = compute_catboost_object_importance(pipe, sp.X_train, sp.y_train, sp.X_val, sp.y_val, sp.task_type,
                                               'catboost')
        return np.asarray(v, dtype=float), info

    from joblib import parallel_config
    from pydvl.valuation.dataset import Dataset
    import config.settings as S
    Xtr, Xval = _dense(trainer.pre.transform(sp.X_train)), _dense(trainer.pre.transform(sp.X_val))
    ytr, yval = np.asarray(sp.y_train), np.asarray(sp.y_val)

    if method == 'KNNShapley':
        if not sp.is_classification:
            raise NotApplicable('KNN-Shapley (pyDVL) is defined for classification only')
        from sklearn.neighbors import KNeighborsClassifier
        from pydvl.valuation.methods import KNNShapleyValuation
        v = KNNShapleyValuation(KNeighborsClassifier(n_neighbors=spec.knn_k), test_data=Dataset(Xval, yval.astype(int)),
                                progress=False)
        with parallel_config(n_jobs=S.N_JOBS):
            v.fit(Dataset(Xtr, ytr.astype(int)))
        return _result_to_array(_valuation_result(v), n), info

    if method == 'DataOOB':
        from sklearn.ensemble import BaggingClassifier, BaggingRegressor
        from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
        from pydvl.valuation.methods import DataOOBValuation
        if sp.is_classification:
            y_fit = ytr.astype(int)
            bag = BaggingClassifier(DecisionTreeClassifier(), n_estimators=spec.oob_estimators,
                                    random_state=seed, n_jobs=S.N_JOBS)
        else:
            y_fit = ytr.astype(float)
            if y_scaler is not None:
                y_fit = y_scaler.transform(y_fit.reshape(-1, 1)).ravel()
            bag = BaggingRegressor(DecisionTreeRegressor(min_samples_leaf=3), n_estimators=spec.oob_estimators,
                                   random_state=seed, n_jobs=S.N_JOBS)
        bag.fit(Xtr, y_fit)
        v = DataOOBValuation(bag)
        v.fit(Dataset(Xtr, y_fit))
        return _result_to_array(_valuation_result(v), n), info

    raise ValueError(f'unknown method {method}')
