#!/usr/bin/env python3
"""Run influence investigation via API (phase A + B) and append analysis to report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

REPO = Path(__file__).resolve().parents[1]
API = "http://localhost:8000"
REPORT = REPO / "docs" / "INFLUENCE_REMOVAL_INVESTIGATION_REPORT.md"
ANALYZE = REPO / ".cursor/skills/diploma-experiment-review/scripts/analyze_experiment_dir.py"

DEFAULT_REMOVAL = {
    "removal_strategies": ["lowest", "highest", "extremes", "random"],
    "n_remove_percentages": [1, 5, 10, 20, 30, 50],
    "n_random_runs": 3,
    "n_retrain_runs": 3,
    "removal_adaptive_model": False,
}

ZILLOW_FINE_REMOVAL = {
    "removal_strategies": [
        "lowest",
        "highest",
        "extremes",
        "random",
        "few_bad_then_random",
    ],
    "n_remove_percentages": [1, 2, 3, 5, 7, 10, 15, 20],
    "n_random_runs": 3,
    "n_retrain_runs": 3,
    "removal_adaptive_model": False,
}

HEAVY_REMOVAL = {
    "removal_strategies": ["lowest", "extremes", "random"],
    "n_remove_percentages": [5, 10, 20, 30, 50],
    "n_random_runs": 2,
    "n_retrain_runs": 2,
    "removal_adaptive_model": False,
}

# Все быстрые gradient/Hessian-методы (без Shapley/LOO/CgInfluence).
INFLUENCE_METHODS_ALL = [
    "Influence",
    "ArnoldiInfluence",
    "LissaInfluence",
    "NystroemSketchInfluence",
]

# На очень больших train — без Arnoldi (медленнее), если нужно ускорить.
INFLUENCE_METHODS_LARGE = [
    "Influence",
    "LissaInfluence",
    "NystroemSketchInfluence",
]


def poll_experiment(
    exp_id: str,
    timeout_s: float,
    interval_s: float = 5.0,
) -> Dict[str, Any]:
    deadline = time.time() + timeout_s
    last = None
    while time.time() < deadline:
        try:
            r = requests.get(f"{API}/experiments/{exp_id}/status", timeout=30)
            if r.status_code == 404:
                print(f"  [WARN] 404 for {exp_id} (API reload?) — retry…")
                time.sleep(interval_s)
                continue
            r.raise_for_status()
        except requests.RequestException as exc:
            print(f"  [WARN] status poll error: {exc} — retry…")
            time.sleep(interval_s)
            continue
        st = r.json()
        last = st
        status = st.get("status")
        if status in ("completed", "failed"):
            return st
        prog = st.get("progress")
        msg = st.get("message", "")
        eta = st.get("eta_seconds")
        print(f"  [{status}] {prog}% {msg} eta={eta}")
        time.sleep(interval_s)
    if last and last.get("status") == "running":
        print(f"  TIMEOUT — cancelling {exp_id}")
        try:
            requests.post(f"{API}/experiments/{exp_id}/cancel", timeout=15)
        except Exception:
            pass
    return last or {"status": "timeout"}


def start_phase_a(
    dataset: str,
    model_type: str,
    sample_pct: float,
    use_distillation: bool,
    n_epochs: int = 200,
    influence_methods: Optional[List[str]] = None,
) -> str:
    methods = influence_methods or INFLUENCE_METHODS_ALL
    cfg: Dict[str, Any] = {
        "dataset_name": dataset,
        "model_type": model_type,
        "run_mode": "influence_only",
        "sample_size_percentage": sample_pct,
        "selected_influence_methods": list(methods),
        "n_epochs": n_epochs,
        "n_random_runs": 1,
        "cv_folds": 1,
        "random_state": 42,
        "use_distillation": use_distillation,
        "distillation_epochs": 200,
        "student_architecture": "simple",
        "model_params": {"model_architecture": "simple"},
    }
    r = requests.post(f"{API}/experiments/start", json={"config": cfg}, timeout=60)
    r.raise_for_status()
    exp_id = r.json()["experiment_id"]
    print(
        f"Phase A started: {exp_id} ({dataset}/{model_type} @ {sample_pct}%) "
        f"methods={methods}"
    )
    return exp_id


def start_phase_b(parent_id: str, removal: Dict[str, Any]) -> str:
    r = requests.post(
        f"{API}/experiments/{parent_id}/removal-runs/start",
        json=removal,
        timeout=60,
    )
    r.raise_for_status()
    exp_id = r.json()["experiment_id"]
    print(f"Phase B started: {exp_id} (parent {parent_id})")
    return exp_id


def get_results_meta(exp_id: str) -> Dict[str, Any]:
    r = requests.get(f"{API}/experiments/{exp_id}/results", timeout=60)
    r.raise_for_status()
    return r.json()


def run_analyzer(exp_dir: str) -> str:
    path = REPO / exp_dir if not Path(exp_dir).is_absolute() else Path(exp_dir)
    if not path.is_dir():
        return f"Missing dir: {exp_dir}"
    proc = subprocess.run(
        [sys.executable, str(ANALYZE), str(path)],
        capture_output=True,
        text=True,
        cwd=str(REPO),
    )
    return proc.stdout + proc.stderr


def append_run_section(
    run_id: str,
    dataset: str,
    model_type: str,
    sample_pct: float,
    phase: str,
    exp_id: str,
    exp_dir: str,
    analyzer_out: str,
    verdict: str = "PENDING",
) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    block = f"""
### {run_id} — {dataset} / {model_type} / {sample_pct}% / {phase}

- **Время:** {ts}
- **experiment_id:** `{exp_id}`
- **Каталог:** `{exp_dir}`
- **Вердикт:** {verdict}

<details><summary>analyze_experiment_dir.py</summary>

```
{analyzer_out[:12000]}
```

</details>

"""
    text = REPORT.read_text(encoding="utf-8")
    marker = "## Детальные записи по прогонам"
    if marker in text:
        text = text.replace(marker, marker + block)
    else:
        text += block
    REPORT.write_text(text, encoding="utf-8")


def update_summary_row(row: Dict[str, str]) -> None:
    text = REPORT.read_text(encoding="utf-8")
    line = "| " + " | ".join(row.get(k, "") for k in [
        "id", "dataset", "model", "sample", "phase", "strategies",
        "exp_id", "exp_dir", "verdict", "note",
    ]) + " |"
    old = "| _(runs appended below)_ |"
    if old in text:
        text = text.replace(old, line)
    else:
        text = text.replace(
            "| _(runs appended below)_ |\n",
            "| _(runs appended below)_ |\n" + line + "\n",
        )
    # If already has rows, append before Zillow section
    if "## Гипотезы" in text and line not in text:
        insert_at = text.find("\n## Гипотезы")
        if insert_at > 0:
            text = text[:insert_at] + "\n" + line + text[insert_at:]
    REPORT.write_text(text, encoding="utf-8")


def run_full_cycle(
    run_id: str,
    dataset: str,
    model_type: str,
    sample_pct: float,
    use_distillation: bool,
    timeout_a: float,
    timeout_b: float,
    removal: Optional[Dict[str, Any]] = None,
    n_epochs: int = 200,
    poll_interval: float = 5.0,
    influence_methods: Optional[List[str]] = None,
) -> bool:
    removal = removal or DEFAULT_REMOVAL
    health = requests.get(f"{API}/health", timeout=60)
    if health.status_code != 200:
        print("API not healthy")
        return False

    parent = start_phase_a(
        dataset,
        model_type,
        sample_pct,
        use_distillation,
        n_epochs,
        influence_methods=influence_methods,
    )
    st_a = poll_experiment(parent, timeout_a, poll_interval)
    if st_a.get("status") != "completed":
        append_run_section(
            run_id, dataset, model_type, sample_pct, "A",
            parent, "", f"FAILED phase A: {st_a}", "FAIL",
        )
        return False

    meta_a = get_results_meta(parent)
    exp_dir_a = meta_a.get("experiment_dir", "")

    child = start_phase_b(parent, removal)
    st_b = poll_experiment(child, timeout_b, poll_interval)
    if st_b.get("status") != "completed":
        append_run_section(
            run_id, dataset, model_type, sample_pct, "B",
            child, exp_dir_a, f"FAILED phase B: {st_b}", "FAIL",
        )
        return False

    meta_b = get_results_meta(child)
    exp_dir = meta_b.get("experiment_dir", exp_dir_a)
    analysis = run_analyzer(exp_dir)

    verdict = "OK"
    if "FAIL" in analysis or "Traceback" in analysis:
        verdict = "FAIL"
    elif "WARN" in analysis:
        verdict = "WARN"

    strat = ",".join(removal.get("removal_strategies", []))
    append_run_section(
        run_id, dataset, model_type, sample_pct, f"A+B ({strat})",
        child, exp_dir, analysis, verdict,
    )
    methods_note = ",".join(influence_methods or INFLUENCE_METHODS_ALL)
    update_summary_row({
        "id": run_id,
        "dataset": dataset,
        "model": model_type,
        "sample": str(sample_pct),
        "phase": "A+B",
        "strategies": strat[:40],
        "exp_id": child[:8],
        "exp_dir": exp_dir[-25:] if exp_dir else "",
        "verdict": verdict,
        "note": methods_note[:50],
    })
    return True


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "command",
        choices=[
            "wine-pytorch",
            "wine-lgbm",
            "wine-multi",
            "housing-pytorch",
            "housing-lgbm",
            "housing-multi",
            "adult-pytorch",
            "adult-lgbm",
            "adult-multi",
            "zillow-base-pytorch",
            "zillow-base-lgbm",
            "zillow-multi",
            "zillow-fine-pytorch",
            "zillow-fine-lgbm",
            "zillow-full-pytorch",
            "zillow-full-multi",
            "heavy",
            "heavy-multi",
        ],
    )
    p.add_argument("--dataset", default="covertype")
    p.add_argument(
        "--methods",
        default="all",
        choices=["all", "large", "nystroem"],
        help="all=4 methods; large=без Arnoldi; nystroem=только Nystroem",
    )
    args = p.parse_args()

    cmds = {
        "wine-pytorch": ("W01", "wine", "pytorch", 100, False, 900, 1200),
        "wine-lgbm": ("W02", "wine", "lightgbm", 100, True, 900, 1200),
        "housing-pytorch": ("H01", "housing", "pytorch", 100, False, 1200, 1800),
        "housing-lgbm": ("H02", "housing", "lightgbm", 100, True, 1200, 1800),
        "adult-pytorch": ("A01", "adult", "pytorch", 100, False, 2700, 3600),
        "adult-lgbm": ("A02", "adult", "lightgbm", 100, True, 2700, 3600),
        "zillow-base-pytorch": ("Z01", "zillow", "pytorch", 15, False, 3600, 5400),
        "zillow-base-lgbm": ("Z02", "zillow", "lightgbm", 15, True, 3600, 5400),
        "zillow-fine-pytorch": ("Z03", "zillow", "pytorch", 15, False, 600, 7200),
        "zillow-fine-lgbm": ("Z04", "zillow", "lightgbm", 15, True, 600, 7200),
        "zillow-full-pytorch": ("Z05", "zillow", "pytorch", 100, False, 7200, 10800),
    }
    def _methods_for_cmd(ds: str) -> List[str]:
        if args.methods == "nystroem":
            return ["NystroemSketchInfluence"]
        if args.methods == "large" or ds in ("zillow", "covertype", "electric"):
            return INFLUENCE_METHODS_LARGE
        return INFLUENCE_METHODS_ALL

    if args.command == "heavy":
        d = args.dataset
        meth = _methods_for_cmd(d)
        ok = run_full_cycle(
            f"X-{d[:3]}-py", d, "pytorch", 10, False,
            5400, 7200, HEAVY_REMOVAL, poll_interval=15,
            influence_methods=meth,
        )
        ok2 = run_full_cycle(
            f"X-{d[:3]}-lg", d, "lightgbm", 10, True,
            5400, 7200, HEAVY_REMOVAL, poll_interval=15,
            influence_methods=meth,
        )
        sys.exit(0 if ok and ok2 else 1)

    if args.command == "heavy-multi":
        d = args.dataset
        meth = INFLUENCE_METHODS_LARGE
        ok = run_full_cycle(
            f"XM-{d[:3]}-py", d, "pytorch", 10, False,
            10800, 14400, HEAVY_REMOVAL, poll_interval=20,
            influence_methods=meth,
        )
        ok2 = run_full_cycle(
            f"XM-{d[:3]}-lg", d, "lightgbm", 10, True,
            10800, 14400, HEAVY_REMOVAL, poll_interval=20,
            influence_methods=meth,
        )
        sys.exit(0 if ok and ok2 else 1)

    multi_cmds = {
        "wine-multi": ("WM1", "wine", "pytorch", 100, False, 3600, 7200),
        "housing-multi": ("HM1", "housing", "pytorch", 100, False, 5400, 10800),
        "adult-multi": ("AM1", "adult", "pytorch", 100, False, 10800, 14400),
        "zillow-multi": ("ZM1", "zillow", "pytorch", 15, False, 10800, 21600),
        "zillow-full-multi": ("ZM2", "zillow", "pytorch", 100, False, 21600, 43200),
    }
    if args.command in multi_cmds:
        run_id, ds, mt, sp, ud, ta, tb = multi_cmds[args.command]
        meth = _methods_for_cmd(ds)
        poll = 15.0 if ds in ("zillow", "adult") else 8.0
        ok = run_full_cycle(
            run_id, ds, mt, sp, ud, ta, tb, DEFAULT_REMOVAL,
            poll_interval=poll, influence_methods=meth,
        )
        sys.exit(0 if ok else 1)

    spec = cmds.get(args.command)
    if not spec:
        sys.exit(1)
    run_id, ds, mt, sp, ud, ta, tb = spec
    removal = DEFAULT_REMOVAL
    if "zillow-fine" in args.command:
        removal = ZILLOW_FINE_REMOVAL
        ta = 600  # parent already exists — only B; but we run full for simplicity
    poll = 15.0 if sp <= 20 or ds in ("zillow", "adult") else 5.0
    meth = _methods_for_cmd(ds)
    ok = run_full_cycle(
        run_id, ds, mt, sp, ud, ta, tb, removal,
        poll_interval=poll, influence_methods=meth,
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
