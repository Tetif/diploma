"""
Собирает сводку большого исследования из уже сохранённых removal_metrics.csv и config.json
(когда results.pkl не сохранялись). Запуск после прогона large_influence_study без изменений
в прошлых сессиях.

Использование:
  python scripts/aggregate_large_study_from_csv.py
  python scripts/aggregate_large_study_from_csv.py --base-dir experiment_logs/large_study --output experiment_logs/large_study/summary_from_csv.csv
"""
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd
import sys

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from config import EXPERIMENTS_BASE_DIR  # type: ignore


def _load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _parse_method_and_strategy(method_key: str) -> Tuple[str, str]:
    """Из имени колонки (random, Influence_lowest, ...) возвращает (base_method, strategy)."""
    if method_key == "random":
        return "random", "random"
    suffix_map = [
        ("_lowest", "lowest"),
        ("_highest", "highest"),
        ("_extremes", "extremes"),
        ("_median", "median"),
        ("_few_bad_rand", "few_bad_then_random"),
        ("_few_median_rand", "few_median_then_random"),
        ("_few_good_rand", "few_good_then_random"),
    ]
    for suffix, strategy in suffix_map:
        if method_key.endswith(suffix):
            return method_key[: -len(suffix)], strategy
    return method_key, "base"


def _iter_removal_csvs(base_dir: Path) -> List[Path]:
    if not base_dir.exists():
        return []
    return sorted(Path(base_dir).rglob("removal_metrics.csv"))


def aggregate_from_csv(base_dir: Path, output: Path) -> None:
    base_dir = Path(base_dir)
    csv_files = _iter_removal_csvs(base_dir)
    if not csv_files:
        print(f"No removal_metrics.csv found under {base_dir}")
        return

    rows: List[Dict[str, Any]] = []

    for csv_path in csv_files:
        experiment_dir = csv_path.parent
        config_path = experiment_dir / "config.json"
        cfg = _load_config(config_path)

        dataset_info = cfg.get("dataset", {}) or {}
        model_info = cfg.get("model", {}) or {}
        dataset_name = dataset_info.get("name") or "unknown"
        task_type = dataset_info.get("task_type", "")
        model_type = model_info.get("type") or "unknown"

        # Из имени папки можно подставить dataset/model, если config пустой
        if dataset_name == "unknown" and experiment_dir.name:
            # adult_xgboost_sf0.100 -> adult
            parts = experiment_dir.name.split("_")
            if parts:
                dataset_name = parts[0]
            if len(parts) >= 2 and model_type == "unknown":
                model_type = parts[1]

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            print(f"Skip {csv_path}: {e}")
            continue

        if "pct_removed" not in df.columns or "baseline" not in df.columns:
            print(f"Skip {csv_path}: missing pct_removed or baseline")
            continue

        # Метрики — все колонки кроме pct_removed и baseline
        method_columns = [c for c in df.columns if c not in ("pct_removed", "baseline")]
        if not method_columns:
            continue

        baseline_mae = df["baseline"].iloc[0] if len(df) > 0 else None

        for _, row in df.iterrows():
            pct = int(row["pct_removed"])
            for col in method_columns:
                val = row[col]
                if pd.isna(val):
                    continue
                base_method, strategy = _parse_method_and_strategy(col)
                rows.append({
                    "dataset": dataset_name,
                    "task_type": task_type,
                    "model_type": model_type,
                    "strategy": strategy,
                    "base_method": base_method,
                    "pct_removed": pct,
                    "final_mae": float(val),
                    "baseline_final_mae": baseline_mae,
                    "experiment_dir": str(experiment_dir),
                })

    if not rows:
        print("No rows collected.")
        return

    out_df = pd.DataFrame(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(output, index=False)
    print(f"Aggregated {len(out_df)} rows from {len(csv_files)} experiments -> {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate large study from existing removal_metrics.csv and config.json (no results.pkl)."
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=None,
        help="Base directory (default: EXPERIMENTS_BASE_DIR/large_study).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path (default: <base-dir>/large_study_summary_from_csv.csv).",
    )
    args = parser.parse_args()

    base_dir = args.base_dir
    if base_dir is None:
        base_dir = Path(EXPERIMENTS_BASE_DIR) / "large_study"
    base_dir = Path(base_dir).resolve()

    if args.output is None:
        output = base_dir / "large_study_summary_from_csv.csv"
    else:
        output = Path(args.output)
        if not output.is_absolute():
            output = base_dir / output

    aggregate_from_csv(base_dir, output)


if __name__ == "__main__":
    main()
