import argparse
import json
import pickle
from pathlib import Path
from typing import Dict, Any, List

import numpy as np
import pandas as pd
import sys

# Ensure project root on path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from config import EXPERIMENTS_BASE_DIR  # type: ignore


def _iter_results_files(base_dir: Path) -> List[Path]:
    if not base_dir.exists():
        return []
    return sorted(base_dir.rglob("results.pkl"))


def _load_pickle(path: Path) -> Dict[str, Any]:
    with path.open("rb") as f:
        return pickle.load(f)


def _load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _parse_method_and_strategy(method_key: str) -> (str, str):
    """
    Разбирает имя метода вида:
      Influence_lowest, Influence_highest, Influence_extremes, Influence_median,
      Influence_few_bad_rand, Influence_few_median_rand, Influence_few_good_rand,
      random.
    Возвращает (base_method, strategy).
    """
    if method_key == "random":
        return "random", "random"

    suffix_map = {
        "_lowest": "lowest",
        "_highest": "highest",
        "_extremes": "extremes",
        "_median": "median",
        "_few_bad_rand": "few_bad_then_random",
        "_few_median_rand": "few_median_then_random",
        "_few_good_rand": "few_good_then_random",
    }
    for suffix, strategy in suffix_map.items():
        if method_key.endswith(suffix):
            return method_key[: -len(suffix)], strategy
    return method_key, "base"


def aggregate_large_study(base_dir: Path, output: Path) -> None:
    rows: List[Dict[str, Any]] = []

    result_files = _iter_results_files(base_dir)
    if not result_files:
        print(f"No results.pkl found under {base_dir}")
        return

    for res_path in result_files:
        try:
            data = _load_pickle(res_path)
        except Exception as e:
            print(f"Failed to load {res_path}: {e}")
            continue

        results = data.get("results", {})
        scores_raw = data.get("scores_raw", {})
        n_remove_list = data.get("n_remove_list", [])
        experiment_dir = Path(data.get("experiment_dir", res_path.parent))

        config_path = experiment_dir / "config.json"
        cfg = _load_config(config_path)

        dataset_info = cfg.get("dataset", {})
        training_info = cfg.get("training", {})
        model_info = cfg.get("model", {})

        dataset_name = dataset_info.get("name") or dataset_info.get("dataset_name") or "unknown"
        task_type = dataset_info.get("task_type", "")

        removal_cfg = training_info.get("removal", {}) if isinstance(training_info, dict) else {}
        removal_strategy_cfg = removal_cfg.get("strategy")

        baseline = results.get("orig", {})
        baseline_final = baseline.get("final_mae")
        baseline_best = baseline.get("best_val_mae")

        # Собираем основные методы и проценты
        for key, hist in results.items():
            if key == "orig":
                # Базовая точка, pct_removed = 0
                rows.append(
                    {
                        "dataset": dataset_name,
                        "task_type": task_type,
                        "model_type": model_info.get("type"),
                        "strategy": "baseline",
                        "base_method": "baseline",
                        "pct_removed": 0,
                        "final_mae": baseline_final,
                        "best_val_mae": baseline_best,
                        "removal_strategy_cfg": removal_strategy_cfg,
                        "experiment_dir": str(experiment_dir),
                    }
                )
                continue

            if key.startswith("random_") and "run" in key:
                # Индивидуальные random-run истории уже агрегированы в median в main/runner и plot_removal
                continue

            # Ожидаемый формат: method_or_random_<pct>pct
            if "_" not in key or not key.endswith("pct"):
                continue

            name_part, pct_part = key.rsplit("_", 1)
            pct_str = pct_part[:-3]  # remove 'pct'
            if not pct_str.isdigit():
                continue

            pct = int(pct_str)

            base_method, strategy = _parse_method_and_strategy(name_part)

            final_mae = hist.get("final_mae")
            best_val_mae = hist.get("best_val_mae")

            n_scores = 0
            if base_method in scores_raw:
                vals = scores_raw[base_method]
                try:
                    n_scores = len(vals)
                except Exception:
                    n_scores = 0

            rows.append(
                {
                    "dataset": dataset_name,
                    "task_type": task_type,
                    "model_type": model_info.get("type"),
                    "strategy": strategy,
                    "base_method": base_method,
                    "pct_removed": pct,
                    "final_mae": final_mae,
                    "best_val_mae": best_val_mae,
                    "baseline_final_mae": baseline_final,
                    "baseline_best_val_mae": baseline_best,
                    "n_scores": n_scores,
                    "removal_strategy_cfg": removal_strategy_cfg,
                    "experiment_dir": str(experiment_dir),
                }
            )

    if not rows:
        print("No rows aggregated.")
        return

    df = pd.DataFrame(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Aggregated {len(df)} rows into {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate large influence study experiments into a single CSV summary."
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=None,
        help="Base directory with large study experiments (default: EXPERIMENTS_BASE_DIR/large_study).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path (default: <base-dir>/large_study_summary.csv).",
    )
    args = parser.parse_args()

    base_dir = args.base_dir
    if base_dir is None:
        base_dir = Path(EXPERIMENTS_BASE_DIR) / "large_study"

    if not base_dir.is_absolute():
        base_dir = base_dir.resolve()

    if args.output is None:
        output = base_dir / "large_study_summary.csv"
    else:
        output = args.output
        if not output.is_absolute():
            output = base_dir / output

    aggregate_large_study(base_dir, output)


if __name__ == "__main__":
    main()

