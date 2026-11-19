"""Optional webhook notifications (never raise, never block the study for more than ~10 s).

Environment:
  DIPLOMA_WEBHOOK_URL     - POST target; if unset, nothing is sent.
  DIPLOMA_WEBHOOK_KEY     - secret sent in a header (optional).
  DIPLOMA_WEBHOOK_HEADER  - header name for the key (default "Authorization", value "Bearer <key>";
                            with any other header name the raw key is sent as the value).
"""
from __future__ import annotations

import json
import os
import urllib.request


def enabled() -> bool:
    return bool(os.environ.get('DIPLOMA_WEBHOOK_URL'))


def post(payload: dict, log=None) -> bool:
    url = os.environ.get('DIPLOMA_WEBHOOK_URL')
    if not url:
        return False
    try:
        headers = {'Content-Type': 'application/json'}
        key = os.environ.get('DIPLOMA_WEBHOOK_KEY')
        if key:
            name = os.environ.get('DIPLOMA_WEBHOOK_HEADER') or 'Authorization'
            headers[name] = f'Bearer {key}' if name.lower() == 'authorization' else key
        body = json.dumps(payload, default=str, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read(200)
        return True
    except Exception as e:  # noqa: BLE001 - notification must never break the run
        if log:
            log(f'  (webhook failed: {type(e).__name__}: {str(e)[:120]})')
        return False
