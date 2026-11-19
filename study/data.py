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
               noise_rate: float = 0.0, sample_scale: float = 1.0) -> Split:
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
    if noise_rate > 0:
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
