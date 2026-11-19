"""Model hyperparameters per dataset, stored as JSON: config/model_params/<dataset>.json.

Each file has the keys ``normal`` / ``underfit`` / ``overfit`` (see MODEL_FIT_MODE in settings.py);
each of them maps a model type (lightgbm, xgboost, catboost, random_forest, pytorch) to its params.
For ``pytorch`` the value maps an architecture name (simple, improved, ...) to its params.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

PARAMS_DIR = Path(__file__).resolve().parent
FIT_MODES = ('normal', 'underfit', 'overfit')


def load_model_params(dataset: str) -> Dict[str, dict]:
    """Return ``{fit_mode: {model_type: params}}`` for one dataset."""
    path = PARAMS_DIR / f'{dataset}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    return {mode: data[mode] for mode in FIT_MODES}


def load_all_model_params() -> Dict[str, Dict[str, dict]]:
    """Load every ``<dataset>.json`` in this folder."""
    return {p.stem: load_model_params(p.stem) for p in sorted(PARAMS_DIR.glob('*.json'))}
