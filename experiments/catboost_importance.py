"""CatBoost object importance (LossFunctionChange) as an alternative influence score."""
import numpy as np
from sklearn.preprocessing import StandardScaler

from config import settings as settings_module

from experiments.removal_strategies import CLASSIFICATION_TASKS


def _extract_catboost_model(model_wrapper):
    """Extract the actual CatBoost model from potentially wrapped model objects."""
    import catboost as cb
    _cb_types = (cb.CatBoostRegressor, cb.CatBoostClassifier, cb.CatBoost)

    inner = getattr(model_wrapper, 'model', None)
    if isinstance(inner, _cb_types):
        return inner

    base = getattr(model_wrapper, 'base_model', None)
    if base is not None:
        inner = getattr(base, 'model', None)
        if isinstance(inner, _cb_types):
            return inner

    return None


def compute_catboost_object_importance(pipeline, X_train, y_train, X_val, y_val,
                                       task_type, model_type, logger=None):
    """
    Per-sample object importance via CatBoost (LossFunctionChange paper).

    If the pipeline already contains a CatBoost model it is reused;
    otherwise a lightweight proxy CatBoost is trained on the same data.

    Sign convention (same as pyDVL influence):
      positive = helpful (removing increases loss),
      negative = harmful  (removing decreases loss).
    """
    import catboost as cb

    preproc = pipeline.named_steps['preproc']
    X_train_t = preproc.transform(X_train)
    X_val_t = preproc.transform(X_val)
    if hasattr(X_train_t, 'toarray'):
        X_train_t = X_train_t.toarray()
        X_val_t = X_val_t.toarray()
    X_train_t = np.asarray(X_train_t)
    X_val_t = np.asarray(X_val_t)

    y_train_arr = np.asarray(y_train).ravel()
    y_val_arr = np.asarray(y_val).ravel()

    if task_type == 'regression':
        y_scaler = StandardScaler()
        y_train_arr = y_scaler.fit_transform(y_train_arr.reshape(-1, 1)).ravel()
        y_val_arr = y_scaler.transform(y_val_arr.reshape(-1, 1)).ravel()

    catboost_model = None
    if model_type == 'catboost':
        catboost_model = _extract_catboost_model(pipeline.named_steps['model'])

    if catboost_model is None:
        if logger:
            logger.log_message("Training proxy CatBoost for object importance...")
        if task_type in CLASSIFICATION_TASKS:
            catboost_model = cb.CatBoostClassifier(
                iterations=500, learning_rate=0.05, depth=6,
                verbose=False, random_seed=settings_module.RANDOM_STATE,
            )
        else:
            catboost_model = cb.CatBoostRegressor(
                iterations=500, learning_rate=0.05, depth=6,
                loss_function='RMSE', verbose=False, random_seed=settings_module.RANDOM_STATE,
            )
        catboost_model.fit(X_train_t, y_train_arr, verbose=False)
        if logger:
            logger.log_message("Proxy CatBoost trained.")

    train_pool = cb.Pool(X_train_t, y_train_arr)
    val_pool = cb.Pool(X_val_t, y_val_arr)

    if logger:
        logger.log_message("Computing CatBoost object importance...")

    raw = catboost_model.get_object_importance(
        val_pool, train_pool,
        type='Average',
        update_method='AllPoints',
        thread_count=-1,
        verbose=False,
    )

    n_train = len(y_train_arr)
    if isinstance(raw, (list, tuple)) and len(raw) == 2:
        indices, scores_arr = raw
        importance = np.zeros(n_train, dtype=float)
        for idx, sc in zip(np.asarray(indices).ravel().astype(int),
                           np.asarray(scores_arr).ravel()):
            if 0 <= idx < n_train:
                importance[idx] = sc
    else:
        importance = np.asarray(raw, dtype=float).ravel()
        if importance.shape[0] != n_train:
            if logger:
                logger.log_message(
                    f"WARNING: importance length {importance.shape[0]} != n_train {n_train}"
                )
            if importance.shape[0] > n_train:
                importance = importance[:n_train]
            else:
                importance = np.pad(importance, (0, n_train - importance.shape[0]))

    if logger:
        logger.log_message(
            f"CatBoost importance: {len(importance)} samples, "
            f"min={importance.min():.6g}, max={importance.max():.6g}, "
            f"mean={importance.mean():.6g}, std={importance.std():.6g}"
        )
        logger.log_message(
            f"  Helpful (>0): {(importance > 0).sum()}, "
            f"Harmful (<0): {(importance < 0).sum()}"
        )

    return importance
