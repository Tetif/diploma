"""Per-seed data preparation: holdout / train / val split, subsampling and noise injection.

Split (for every seed k a different random split):
  holdout (cfg.val_size of the data, at most ``max_holdout`` rows) - only for the reported metric;
  the rest is subsampled to ``n_train / 0.8`` rows and split 80/20 into
  train (valued and removed from) and val (early stopping + the utility of pyDVL methods).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

CLASSIFICATION = ('binary_classification', 'multiclass_classification')


@dataclass
class Split:
    dataset: str
    task_type: str
    cfg: object
    X_train: pd.DataFrame
    y_train: pd.Series
    X_val: pd.DataFrame
    y_val: pd.Series
    X_hold: pd.DataFrame
    y_hold: pd.Series
    is_noisy: np.ndarray = field(default_factory=lambda: np.zeros(0, bool))

    @property
    def is_classification(self) -> bool:
        return self.task_type in CLASSIFICATION

    def sizes(self) -> dict:
        return {'n_train': len(self.X_train), 'n_val': len(self.X_val), 'n_holdout': len(self.X_hold),
                'n_noisy': int(self.is_noisy.sum())}


@lru_cache(maxsize=4)
def load_full(dataset: str):
    """Load the whole dataset once per process (X, y, cfg); labels encoded to 0..K-1."""
    from config import DatasetRegistry
    from data.loader import DataLoaderFactory
    cfg = DatasetRegistry.get(dataset)
    X, y, cfg = DataLoaderFactory.load_dataset(cfg, None)
    if cfg.task_type in CLASSIFICATION and (y.dtype == object or not np.issubdtype(y.dtype, np.integer)
                                            or y.min() != 0):
        y = pd.Series(LabelEncoder().fit_transform(y), index=y.index, name=y.name)
    X = X.reset_index(drop=True)
    y = y.reset_index(drop=True)
    return X, y, cfg


def _strat(y: pd.Series, clf: bool):
    if not clf:
        return None
    counts = y.value_counts()
    return y if counts.min() >= 2 else None


def make_split(dataset: str, seed: int, n_train: Optional[int], max_holdout: int = 5000,
               noise_rate: float = 0.0, sample_scale: float = 1.0, noise_kind: str = 'random') -> Split:
    """Build the split for one seed. ``n_train=None`` -> use everything that is left after holdout."""
    X, y, cfg = load_full(dataset)
    clf = cfg.task_type in CLASSIFICATION
    rs = 1000 + int(seed)
    hold_size = min(float(cfg.val_size), max_holdout / len(X))
    X_rest, X_hold, y_rest, y_hold = train_test_split(X, y, test_size=hold_size, random_state=rs,
                                                      stratify=_strat(y, clf))
    if n_train is not None:
        n_sample = int(round(n_train * sample_scale / 0.8))
    else:
        n_sample = int(round(len(X_rest) * sample_scale))
    if n_sample < len(X_rest):
        X_rest, _, y_rest, _ = train_test_split(X_rest, y_rest, train_size=n_sample, random_state=rs,
                                                stratify=_strat(y_rest, clf))
    X_tr, X_val, y_tr, y_val = train_test_split(X_rest, y_rest, test_size=0.2, random_state=rs,
                                                stratify=_strat(y_rest, clf))
    X_tr, y_tr = X_tr.reset_index(drop=True), y_tr.reset_index(drop=True)
    X_val, y_val = X_val.reset_index(drop=True), y_val.reset_index(drop=True)
    X_hold, y_hold = X_hold.reset_index(drop=True), y_hold.reset_index(drop=True)

    # Zillow-style target clipping (train quantiles only, as in main.py) if the dataset asks for it.
    cq = getattr(cfg, 'train_target_clip_quantiles', None)
    if cq and not clf:
        lo, hi = y_tr.quantile(list(cq))
        y_tr, y_val = y_tr.clip(lo, hi), y_val.clip(lo, hi)

    is_noisy = np.zeros(len(X_tr), bool)
    if noise_rate > 0 and noise_kind == 'systematic':
        y_tr, is_noisy = corrupt_systematic(X_tr, y_tr, noise_rate, clf, seed)
    elif noise_rate > 0:
        y_tr, is_noisy = corrupt(y_tr, noise_rate, clf, seed)
    return Split(dataset, cfg.task_type, cfg, X_tr, y_tr, X_val, y_val, X_hold, y_hold, is_noisy)


def corrupt(y: pd.Series, rate: float, classification: bool, seed: int):
    """Corrupt ``rate`` of the labels.

    Classification: replace the label by a different random class (binary: flip).
    Regression: add +-3 standard deviations of y (outliers).
    """
    rng = np.random.default_rng(10_000 + int(seed))
    n = len(y)
    idx = rng.choice(n, size=int(round(rate * n)), replace=False)
    yv = y.to_numpy().copy()
    if classification:
        classes = np.unique(yv)
        for i in idx:
            others = classes[classes != yv[i]]
            yv[i] = rng.choice(others)
    else:
        yv = yv.astype(float)
        sd = float(np.std(yv))
        yv[idx] = yv[idx] + rng.choice([-1.0, 1.0], size=len(idx)) * 3.0 * sd
    mask = np.zeros(n, bool)
    mask[idx] = True
    return pd.Series(yv, index=y.index, name=y.name), mask


def _numeric_frame(X: pd.DataFrame) -> pd.DataFrame:
    Xn = pd.get_dummies(X, dummy_na=False).astype(float)
    Xn = Xn.fillna(Xn.median())
    return (Xn - Xn.mean()) / Xn.std().replace(0, 1.0)


def confusable_pair(X: pd.DataFrame, y: np.ndarray, seed: int):
    """Most confused pair of classes of a 3-fold logistic regression on the (clean) train set."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import cross_val_predict
    pred = cross_val_predict(LogisticRegression(max_iter=300), _numeric_frame(X).to_numpy(), y, cv=3)
    classes = np.unique(y)
    cm = confusion_matrix(y, pred, labels=classes).astype(float)
    sym = cm + cm.T
    np.fill_diagonal(sym, -1)
    i, j = np.unravel_index(np.argmax(sym), sym.shape)
    return int(classes[i]), int(classes[j])


def corrupt_systematic(X: pd.DataFrame, y: pd.Series, rate: float, classification: bool, seed: int):
    """Structured (non-uniform) corruption of ``rate`` of the training labels.

    Classification - class-pair flip: take the most confusable pair of classes (3-fold logistic regression;
    for binary data the only pair) and relabel random points of the larger class of the pair as the smaller
    one (at most half of that class). Realistic "annotator confuses A with B" noise; the flipped points look
    like the target class more often than random flips do.
    Regression - subgroup shift: the ``rate`` share of points with the largest value of the numeric feature
    most correlated with y get y + 2 std (a consistently mis-measured segment). The shift is a function of
    the features, so a model can partly learn it - harder to detect than random outliers.
    """
    rng = np.random.default_rng(30_000 + int(seed))
    n = len(y)
    k = int(round(rate * n))
    yv = y.to_numpy().copy()
    mask = np.zeros(n, bool)
    if classification:
        a, b = confusable_pair(X, yv, seed)
        src, dst = (a, b) if (yv == a).sum() >= (yv == b).sum() else (b, a)
        pool = np.flatnonzero(yv == src)
        k = min(k, len(pool) // 2)
        idx = rng.choice(pool, size=k, replace=False)
        yv[idx] = dst
    else:
        yv = yv.astype(float)
        num = X.select_dtypes(include=[np.number])
        corr = num.apply(lambda c: abs(np.corrcoef(c.fillna(c.median()), yv)[0, 1]) if c.std() > 0 else 0.0)
        feat = corr.fillna(0).idxmax()
        order = np.argsort(-num[feat].fillna(num[feat].median()).to_numpy(), kind='stable')
        idx = order[:k]
        yv[idx] = yv[idx] + 2.0 * float(np.std(yv))
    mask[idx] = True
    return pd.Series(yv, index=y.index, name=y.name), mask
