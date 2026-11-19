"""One (study, dataset, seed): train the full-data model, value the points, retrain after removal."""
from __future__ import annotations

import time
import traceback
from typing import Dict, List, Optional

import numpy as np

from study import io
from study.config import DatasetSpec, RunSpec
from study.data import Split, make_split
from study.values import NotApplicable, compute_values

CLASSIFICATION_TASKS = ('binary_classification', 'multiclass_classification')

FOUND_AT = (5, 10, 15, 20, 30)   # % of train inspected (lowest value first)


class Trainer:
    """Builds model params like main.py and wraps ExperimentRunner.train_and_evaluate."""

    def __init__(self, split: Split, spec: RunSpec):
        import config.settings as S
        from data.preprocessing import PreprocessorFactory
        from experiments.runner import ExperimentRunner

        self.split, self.spec, self.model_type = split, spec, spec.model_type
        self.pre = PreprocessorFactory.create(split.cfg, None)
        self.pre.fit(split.X_train)
        Xt = self.pre.transform(split.X_train.iloc[:5])
        n_features = int(Xt.shape[1])

        old_mode = S.MODEL_FIT_MODE
        S.MODEL_FIT_MODE = spec.fit_mode
        try:
            ds_params = S.get_model_config(split.dataset, spec.model_type)
        finally:
            S.MODEL_FIT_MODE = old_mode

        mp = {'model_type': spec.model_type, 'model_architecture': 'simple', 'input_size': n_features,
              'device': S.DEVICE, 'task_type': split.task_type, 'available_metrics': list(split.cfg.metrics),
              'valuation_epochs': int(spec.valuation_epochs)}
        for k, v in ds_params.items():
            if k not in mp or k in ('learning_rate', 'num_leaves', 'max_depth', 'iterations', 'n_estimators',
                                    'layers', 'dropout'):
                mp[k] = v
        y = np.asarray(split.y_train)
        if split.task_type == 'multiclass_classification':
            mp['num_class'] = int(len(np.unique(np.concatenate([y, np.asarray(split.y_val)]))))
        if split.task_type == 'binary_classification' and spec.model_type == 'pytorch':
            mp['pos_weight'] = float((y == 0).sum()) / max(int((y == 1).sum()), 1)
        self.model_params = mp
        if spec.model_type == 'pytorch':
            self.n_epochs = int(S.FIT_MODE_EPOCHS.get(spec.fit_mode, spec.n_epochs)) if spec.fit_mode != 'normal' \
                else int(spec.n_epochs)
        else:
            self.n_epochs = 1
        self.metric = S.get_selected_metric(split.task_type, split.cfg.metrics)
        self.higher_is_better = bool(S.get_metric_metadata(self.metric)['higher_is_better'])
        self.n_features = n_features
        self._runner = ExperimentRunner(None)

    def fit(self, X, y, seed: int):
        """Train on (X, y); early stopping on val; returns (holdout metric, model, y_scaler)."""
        sp = self.split
        h, model, ysc = self._runner.train_and_evaluate(self.pre, self.model_params, X, y, sp.X_val, sp.y_val,
                                                        sp.X_hold, sp.y_hold, self.n_epochs, _run_seed=seed)
        return float(h['final_metric']), model, ysc


def _removal_mask(order: np.ndarray, k: int, y: Optional[np.ndarray]) -> np.ndarray:
    """keep-mask after removing k points following `order`.

    Classification (y given): k is split across classes in proportion to their (observed) frequency and
    the first points of `order` within each class are removed; at least one point per class stays.
    Same rule as the thesis runner (removal_indices_per_class_*). Without it, removing 20-30 % of a small
    imbalanced train set can wipe out the minority class and F1 collapses for reasons unrelated to the
    valuation method. Regression (y None): the first k points of `order`.
    """
    n = len(order)
    keep = np.ones(n, bool)
    if k <= 0:
        return keep
    if y is None:
        keep[order[:k]] = False
        return keep
    from experiments.removal_strategies import _allocate_proportional_n_per_class
    alloc = _allocate_proportional_n_per_class(y, k)
    y_ord = y[order]
    for c, n_c in alloc.items():
        if n_c > 0:
            keep[order[y_ord == c][:n_c]] = False
    return keep


def _curve(trainer: Trainer, order: np.ndarray, fracs, seed: int) -> Dict[str, float]:
    sp = trainer.split
    n = len(sp.X_train)
    y = np.asarray(sp.y_train) if sp.task_type in CLASSIFICATION_TASKS else None
    out = {}
    for f in fracs:
        keep = _removal_mask(order, int(round(n * f / 100.0)), y)
        idx = np.flatnonzero(keep)
        out[str(f)] = trainer.fit(sp.X_train.iloc[idx], sp.y_train.iloc[idx], seed)[0]
    return out


def _detection(values: np.ndarray, is_noisy: np.ndarray) -> dict:
    from sklearn.metrics import roc_auc_score
    n, n_bad = len(values), int(is_noisy.sum())
    order = np.argsort(values, kind='stable')
    found = np.cumsum(is_noisy[order])
    res = {'auc': float(roc_auc_score(is_noisy, -values)), 'found_at': {}, 'precision_at': {}}
    for f in FOUND_AT:
        k = max(1, int(round(n * f / 100.0)))
        res['found_at'][str(f)] = float(found[k - 1] / n_bad)
        res['precision_at'][str(f)] = float(found[k - 1] / k)
    return res


def run_seed(root, spec: RunSpec, ds: DatasetSpec, seed: int, methods: List[str], log=print,
             retry_failed: bool = True) -> None:
    """Run every not-yet-finished method for one seed; each method writes its own results.json."""
    todo = []
    for m in methods:
        r = io.load_json(io.run_dir(root, spec.study, ds.name, m, seed) / 'results.json')
        if r and (r.get('status') in io.DONE_STATUSES or (r.get('status') == 'failed' and not retry_failed)):
            continue
        todo.append(m)
    if not todo:
        return
    import config.settings as S
    t0 = time.time()
    split = make_split(ds.name, seed, ds.n_train, ds.max_holdout, spec.noise_rate, spec.sample_scale)
    trainer = Trainer(split, spec)
    model_seed = S.RANDOM_STATE + 1000 * seed
    base_metric, base_model, base_ysc = trainer.fit(split.X_train, split.y_train, model_seed)
    t_base = time.time() - t0
    n = len(split.X_train)
    common = {'study': spec.study, 'dataset': ds.name, 'seed': seed, 'task_type': split.task_type,
              'removal': 'class_proportional' if split.task_type in CLASSIFICATION_TASKS else 'global',
              'metric': trainer.metric, 'higher_is_better': trainer.higher_is_better, 'spec': spec.to_dict(),
              'n_features': trainer.n_features, 'n_epochs': trainer.n_epochs, **split.sizes(),
              'baseline': base_metric, 'device': S.DEVICE, 'n_jobs': S.N_JOBS}
    io.save_json(io.run_dir(root, spec.study, ds.name, '_baseline', seed) / 'results.json',
                 {**common, 'method': '_baseline', 'status': 'ok', 'timing': {'baseline_s': t_base}})
    log(f'[{spec.study}/{ds.name}/seed{seed}] n_train={n} holdout={len(split.X_hold)} '
        f'{trainer.metric}={base_metric:.4f} (baseline {t_base:.0f}s) todo={todo}')

    for m in todo:
        out_dir = io.run_dir(root, spec.study, ds.name, m, seed)
        res = {**common, 'method': m, 'curves': {}, 'timing': {'baseline_s': t_base}}
        t1 = time.time()
        try:
            rng = np.random.default_rng(20_000 + seed)
            if m == 'random':
                values = rng.random(n)
                res['timing']['values_s'] = 0.0
                orders = {'random': rng.permutation(n)}
            else:
                values, info = compute_values(m, trainer, base_model, base_ysc, spec, seed)
                res['timing']['values_s'] = time.time() - t1
                res.update(info)
                bad = ~np.isfinite(values)
                if bad.all():
                    raise RuntimeError(f'{m}: all values are NaN/inf')
                if bad.any():   # rare: a point never out-of-bag etc. -> treat as median value
                    values = np.where(bad, np.nanmedian(values), values)
                    res['n_nonfinite_values'] = int(bad.sum())
                orders = {}
                if 'lowest' in spec.strategies:
                    orders['lowest'] = np.argsort(values, kind='stable')
                if 'highest' in spec.strategies:
                    orders['highest'] = np.argsort(-values, kind='stable')
            res['value_stats'] = {'std': float(np.std(values)), 'n_unique': int(np.unique(values).size)}
            if split.is_noisy.any():
                res['detection'] = _detection(values, split.is_noisy)
            t2 = time.time()
            for name, order in orders.items():
                res['curves'][name] = _curve(trainer, order, spec.fracs, model_seed)
            res['timing']['curves_s'] = time.time() - t2
            res['status'] = 'ok'
            out_dir.mkdir(parents=True, exist_ok=True)
            np.save(out_dir / 'values.npy', values.astype(np.float32))
            if split.is_noisy.any():
                np.save(out_dir / 'is_noisy.npy', split.is_noisy)
        except NotApplicable as e:
            res.update(status='skipped', error=str(e))
        except Exception as e:  # noqa: BLE001 - one failing method must not stop the study
            res.update(status='failed', error=f'{type(e).__name__}: {e}',
                       traceback=traceback.format_exc()[-3000:])
        res['timing']['total_s'] = time.time() - t1
        io.save_json(out_dir / 'results.json', res)
        det = res.get('detection', {}).get('auc')
        log(f'  {m:<15} {res["status"]:<7} {res["timing"]["total_s"]:6.0f}s'
            + (f'  AUC={det:.3f}' if det is not None else '')
            + (f'  {res.get("error", "")[:160]}' if res['status'] != 'ok' else ''))
