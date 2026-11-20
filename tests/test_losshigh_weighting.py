"""[AUDIT-FIX P14] LossHigh ranks by the per-sample term of the weighted training objective."""
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DIPLOMA_N_JOBS', '1')


def _fake(model_type, task, distill=False, cw='balanced', params=None):
    sp = SimpleNamespace(is_classification=task != 'regression')
    return SimpleNamespace(split=sp, model_type=model_type, model_params=params or {},
                           spec=SimpleNamespace(distill=distill, tree_class_weight=cw))


def test_training_sample_weights_mirror_training():
    from study.values import training_sample_weights
    y = np.array([0] * 8 + [1] * 2)
    w, how = training_sample_weights(_fake('lightgbm', 'clf'), y)
    assert how == 'balanced' and np.isclose(w[-1] / w[0], 4.0)          # ~ 1 / n_class
    w, how = training_sample_weights(_fake('pytorch', 'clf', params={'pos_weight': 4.0}), y)
    assert how == 'pos_weight' and w[-1] == 4.0 and w[0] == 1.0
    assert training_sample_weights(_fake('pytorch', 'clf'), y) == (None, 'none')          # multiclass MLP
    assert training_sample_weights(_fake('lightgbm', 'regression'), y) == (None, 'none')
    assert training_sample_weights(_fake('lightgbm', 'clf', distill=True), y) == (None, 'none')
    assert training_sample_weights(_fake('lightgbm', 'clf', cw=None), y) == (None, 'none')


def test_losshigh_detects_noise_on_weighted_multiclass_gbdt():
    """covertype + balanced LightGBM: raw loss gave AUC ~0.37 (rare up-weighted classes memorized)."""
    import config.settings as S
    from sklearn.metrics import roc_auc_score
    from study.config import MAIN_DATASETS, RunSpec
    from study.data import make_split
    from study.protocol import Trainer
    from study.values import compute_values
    ds = MAIN_DATASETS['covertype']
    sp = make_split('covertype', 0, ds.n_train, ds.max_holdout, 0.1, 1.0, 'random')
    spec = RunSpec('t', model_type='lightgbm', task='noise', noise_rate=0.1)
    tr = Trainer(sp, spec, S.RANDOM_STATE)
    _, model, ysc = tr.fit(sp.X_train, sp.y_train, S.RANDOM_STATE)
    v, info = compute_values('LossHigh', tr, model, ysc, spec, 0)
    assert info['loss_weighting'] == 'balanced'
    assert roc_auc_score(np.asarray(sp.is_noisy), -v) > 0.75
