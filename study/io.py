"""results/<study>/<dataset>/<method>/seed<k>/results.json - writing, reading, resuming."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterator, Optional

import numpy as np

DONE_STATUSES = ('ok', 'skipped')


def run_dir(root, study: str, dataset: str, method: str, seed: int) -> Path:
    return Path(root) / study / dataset / method / f'seed{seed}'


def _default(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, tuple)):
        return list(o)
    return str(o)


def save_json(path: Path, data: dict) -> None:
    """Atomic write (tmp + replace) so an interrupted run never leaves a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # [AUDIT-FIX P12] per-process tmp name (parallel workers may write the same _baseline); on Windows
    # os.replace fails while another process reads the target -> short retries
    tmp = path.with_suffix(f'.json.{os.getpid()}.tmp')
    tmp.write_text(json.dumps(data, indent=1, default=_default, ensure_ascii=False), encoding='utf-8')
    for i in range(20):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if i == 19:
                raise
            import time
            time.sleep(0.05 * (i + 1))


def load_json(path: Path) -> Optional[dict]:
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def is_done(root, study, dataset, method, seed) -> bool:
    r = load_json(run_dir(root, study, dataset, method, seed) / 'results.json')
    return bool(r) and r.get('status') in DONE_STATUSES


def iter_results(root) -> Iterator[dict]:
    """Every results.json below ``root`` (any study)."""
    for p in sorted(Path(root).glob('*/*/*/seed*/results.json')):
        r = load_json(p)
        if r:
            r['_path'] = str(p)
            yield r
