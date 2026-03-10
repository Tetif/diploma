"""Save/load influence weights in pickle format for reuse across runs."""
import pickle
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

import numpy as np


def save_influence_weights(
    scores_raw: Dict[str, np.ndarray],
    metadata: Dict[str, Any],
    path: Path,
) -> Path:
    """
    Save influence weights and metadata to a pickle file.

    Args:
        scores_raw: Dict mapping method name -> array of per-train influence values.
        metadata: Dict with keys: dataset_name, n_train, n_remove_list, methods, optionally timestamp.
        path: File path (e.g. experiment_dir / "influence_weights.pkl").

    Returns:
        The path where the file was written.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = dict(metadata)
    if 'timestamp' not in meta:
        meta['timestamp'] = datetime.now().isoformat()
    if 'methods' not in meta:
        meta['methods'] = list(scores_raw.keys())
    data = {
        'scores_raw': scores_raw,
        'metadata': meta,
    }
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    return path


def load_influence_weights(path: Path) -> tuple[Dict[str, np.ndarray], Dict[str, Any]]:
    """
    Load influence weights and metadata from a pickle file.

    Args:
        path: Path to influence_weights.pkl (or legacy results.pkl that contains scores_raw).

    Returns:
        (scores_raw, metadata). metadata may be empty for legacy results.pkl.

    Raises:
        ValueError: If file does not contain scores_raw or required metadata.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Influence weights file not found: {path}")
    with open(path, 'rb') as f:
        data = pickle.load(f)
    if 'scores_raw' in data:
        scores_raw = data['scores_raw']
        metadata = data.get('metadata', {})
        if not metadata and 'n_remove_list' in data:
            metadata = {
                'n_remove_list': data['n_remove_list'],
                'methods': list(scores_raw.keys()),
            }
        return scores_raw, metadata
    raise ValueError(
        f"File {path} does not contain 'scores_raw'. "
        "Expected format: {{'scores_raw': dict, 'metadata': dict}}."
    )
