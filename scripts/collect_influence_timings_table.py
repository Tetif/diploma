#!/usr/bin/env python3
"""
Собирает сводную таблицу времён этапов *_computation из experiment_summary.txt
по всем полным прогонам (sample_size_percentage >= 99.99%).

Для каждой пары (датасет, model_type) выбирается один самый поздний подходящий эксперимент
(по дате/времени в пути experiment_logs/.../YYYY-MM-DD/HH-MM-SS/...); тайминги только из него.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^\d{2}-\d{2}-\d{2}$")
# New summary: "  LOO_computation                              585.03s  ( 97.8%)"
TIMING_LINE_NEW_RE = re.compile(r"^\s+(\S+)\s+([\d.]+)s\s+\(")
# Legacy summary: "  BetaShapley_computation: 388.92 seconds (85.6%)"
TIMING_LINE_LEGACY_RE = re.compile(r"^\s+([^:]+):\s*([\d.]+)\s+seconds\s+", re.IGNORECASE)
LOG_DATASET_UPPER_RE = re.compile(r"DATASET:\s*(\S+)", re.IGNORECASE)
LOG_DATASET_LOAD_RE = re.compile(r"Loading dataset:\s*(\S+)", re.IGNORECASE)
LOG_TAKING_RE = re.compile(r"Taking\s+([\d.]+)\s*%", re.IGNORECASE)
GENERATED_RE = re.compile(r"^Generated:\s*(.+)\s*$", re.MULTILINE)
# experiment_summary MODEL section: "  model_type                           pytorch"
SUMMARY_MODEL_TYPE_RE = re.compile(r"^\s*model_type\s+(\S+)\s*$", re.MULTILINE | re.IGNORECASE)
FULL_SAMPLE_THRESHOLD = 99.99


@dataclass
class ExperimentRecord:
    summary_path: Path
    date_part: str
    time_part: str
    dataset: str
    model_type: str
    sample_pct: float
    computation_timings: Dict[str, float]
    generated_at: Optional[str]
    source_meta: str  # "config.json" | "experiment_log.txt" | "experiment_summary.txt"

    @property
    def sort_key(self) -> Tuple[str, str]:
        return (self.date_part, self.time_part)


def _find_date_time_in_path(path: Path) -> Optional[Tuple[str, str]]:
    parts = path.parts
    for i in range(len(parts) - 1):
        if DATE_RE.match(parts[i]) and TIME_RE.match(parts[i + 1]):
            return parts[i], parts[i + 1]
    return None


def _parse_timing_breakdown(content: str) -> Dict[str, float]:
    m = re.search(
        r"Detailed timing breakdown[^:]*:\s*\r?\n(.*?)(?=\r?\n\r?\n|\r?\n={10,})",
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return {}
    out: Dict[str, float] = {}
    for line in m.group(1).splitlines():
        lm = TIMING_LINE_NEW_RE.match(line)
        if lm:
            out[lm.group(1)] = float(lm.group(2))
            continue
        lm = TIMING_LINE_LEGACY_RE.match(line)
        if lm:
            out[lm.group(1).strip()] = float(lm.group(2))
    return out


def _parse_generated_at(content: str) -> Optional[str]:
    g = GENERATED_RE.search(content)
    return g.group(1).strip() if g else None


def _parse_run_metadata_block(
    content: str,
) -> Tuple[Optional[str], Optional[float], Optional[str]]:
    """RUN METADATA (optional block in experiment_summary from generate_summary)."""
    m = re.search(
        r"RUN METADATA\s*\n-+\s*\n(.*?)(?=\n={10,}|\Z)",
        content,
        flags=re.DOTALL,
    )
    if not m:
        return None, None, None
    block = m.group(1)
    ds_m = re.search(r"^\s*dataset:\s*(\S+)\s*$", block, re.MULTILINE | re.IGNORECASE)
    pct_m = re.search(
        r"^\s*sample_size_percentage:\s*([\d.]+)\s*$", block, re.MULTILINE | re.IGNORECASE
    )
    mt_m = re.search(r"^\s*model_type:\s*(\S+)\s*$", block, re.MULTILINE | re.IGNORECASE)
    dataset = ds_m.group(1).strip() if ds_m else None
    pct = float(pct_m.group(1)) if pct_m else None
    model_type = mt_m.group(1).strip().lower() if mt_m else None
    return dataset, pct, model_type


def _parse_model_type_from_summary(content: str) -> Optional[str]:
    sm = SUMMARY_MODEL_TYPE_RE.search(content)
    if sm:
        return sm.group(1).strip().lower()
    return None


def _load_model_type_from_config_data(data: Dict[str, Any]) -> Optional[str]:
    m = data.get("model")
    if isinstance(m, dict):
        v = m.get("type")
        if v is not None:
            return str(v).strip().lower()
    mp = data.get("model_params")
    if isinstance(mp, dict):
        v = mp.get("model_type")
        if v is not None:
            return str(v).strip().lower()
    return None


def _load_model_type_config(exp_dir: Path) -> Optional[str]:
    cfg_path = exp_dir / "config.json"
    if not cfg_path.is_file():
        return None
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    return _load_model_type_from_config_data(data)


def _resolve_model_type(exp_dir: Path, summary_text: str) -> Tuple[Optional[str], str]:
    """Приоритет: config.json > RUN METADATA в summary > секция MODEL в summary."""
    mt_cfg = _load_model_type_config(exp_dir)
    _d_sum, _p_sum, mt_sum = _parse_run_metadata_block(summary_text)
    mt_summary_sec = _parse_model_type_from_summary(summary_text)

    model_type = mt_cfg
    sources: List[str] = []
    if mt_cfg is not None:
        sources.append("config.json")
    if model_type is None and mt_sum is not None:
        model_type = mt_sum
        sources.append("summary_meta")
    if model_type is None and mt_summary_sec is not None:
        model_type = mt_summary_sec
        sources.append("summary_model_section")

    return model_type, "+".join(sources) if sources else ""


def _load_meta_config(exp_dir: Path) -> Tuple[Optional[str], Optional[float], str]:
    cfg_path = exp_dir / "config.json"
    if not cfg_path.is_file():
        return None, None, ""
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None, None, ""

    name = None
    dset = data.get("dataset")
    if isinstance(dset, dict):
        name = dset.get("name")

    pct = None
    training = data.get("training")
    if isinstance(training, dict):
        v = training.get("sample_size_percentage")
        if v is not None:
            pct = float(v)

    if name or pct is not None:
        return (
            str(name).lower() if name else None,
            pct,
            "config.json",
        )
    return None, None, ""


def _load_meta_log(exp_dir: Path) -> Tuple[Optional[str], Optional[float], str]:
    log_path = exp_dir / "experiment_log.txt"
    if not log_path.is_file():
        return None, None, ""
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None, ""

    dataset = None
    m = LOG_DATASET_UPPER_RE.search(text)
    if m:
        dataset = m.group(1).lower()
    else:
        m = LOG_DATASET_LOAD_RE.search(text)
        if m:
            dataset = m.group(1).lower()

    pct = None
    m = LOG_TAKING_RE.search(text)
    if m:
        pct = float(m.group(1))

    if dataset or pct is not None:
        return dataset, pct, "experiment_log.txt"
    return None, None, ""


def _resolve_metadata(
    exp_dir: Path, summary_text: str
) -> Tuple[Optional[str], Optional[float], str]:
    """По каждому полю: config.json > RUN METADATA в summary > experiment_log.txt."""
    d_cfg, p_cfg, _ = _load_meta_config(exp_dir)
    d_sum, p_sum, _mt_sum = _parse_run_metadata_block(summary_text)
    if d_sum:
        d_sum = d_sum.lower()
    d_log, p_log, _ = _load_meta_log(exp_dir)

    dataset = d_cfg or d_sum or d_log
    if p_cfg is not None:
        pct = p_cfg
    elif p_sum is not None:
        pct = p_sum
    else:
        pct = p_log

    sources: List[str] = []
    if d_cfg is not None or p_cfg is not None:
        sources.append("config.json")
    if d_sum is not None or p_sum is not None:
        sources.append("summary_meta")
    if d_log is not None or p_log is not None:
        sources.append("experiment_log.txt")
    return dataset, pct, "+".join(sources) if sources else ""


def _computation_only(timings: Dict[str, float]) -> Dict[str, float]:
    return {k: v for k, v in timings.items() if str(k).endswith("_computation")}


def collect_records(logs_root: Path) -> Tuple[List[ExperimentRecord], List[str]]:
    skipped: List[str] = []
    records: List[ExperimentRecord] = []

    for summary_path in sorted(logs_root.rglob("experiment_summary.txt")):
        dt = _find_date_time_in_path(summary_path)
        if not dt:
            skipped.append(f"{summary_path}: cannot parse YYYY-MM-DD/HH-MM-SS from path")
            continue
        date_part, time_part = dt
        exp_dir = summary_path.parent

        try:
            content = summary_path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            skipped.append(f"{summary_path}: read error {e}")
            continue

        timings = _parse_timing_breakdown(content)
        if not timings:
            skipped.append(f"{summary_path}: no timing breakdown")
            continue

        dataset, sample_pct, meta_src = _resolve_metadata(exp_dir, content)
        if dataset is None:
            skipped.append(f"{summary_path}: no dataset in config/log/summary metadata")
            continue
        if sample_pct is None:
            skipped.append(f"{summary_path}: no sample_size_percentage / Taking % ({meta_src or 'no meta'})")
            continue
        if sample_pct + 1e-9 < FULL_SAMPLE_THRESHOLD:
            continue

        model_type, model_src = _resolve_model_type(exp_dir, content)
        if not model_type:
            skipped.append(f"{summary_path}: no model_type (config/summary)")
            continue

        comp = _computation_only(timings)
        if not comp:
            skipped.append(f"{summary_path}: no *_computation stages")
            continue

        gen = _parse_generated_at(content)
        meta_full = meta_src or "unknown"
        if model_src:
            meta_full = f"{meta_full}|model:{model_src}"
        records.append(
            ExperimentRecord(
                summary_path=summary_path,
                date_part=date_part,
                time_part=time_part,
                dataset=dataset,
                model_type=model_type,
                sample_pct=sample_pct,
                computation_timings=comp,
                generated_at=gen,
                source_meta=meta_full,
            )
        )

    return records, skipped


def pick_latest_per_dataset_model(
    records: Iterable[ExperimentRecord],
) -> Dict[Tuple[str, str], ExperimentRecord]:
    best: Dict[Tuple[str, str], ExperimentRecord] = {}
    for r in records:
        key = (r.dataset, r.model_type)
        cur = best.get(key)
        if cur is None or r.sort_key > cur.sort_key:
            best[key] = r
    return best


def build_table(
    chosen: Dict[Tuple[str, str], ExperimentRecord],
) -> Tuple[List[Tuple[str, str]], List[str], List[Dict[str, str]]]:
    """Returns (row_keys_sorted, method_columns_sorted, row dicts)."""
    all_methods: set[str] = set()
    for r in chosen.values():
        all_methods.update(r.computation_timings.keys())
    method_cols = sorted(all_methods)

    sorted_keys = sorted(chosen.keys(), key=lambda k: (k[0], k[1]))
    rows: List[Dict[str, str]] = []
    for ds, mt in sorted_keys:
        r = chosen[(ds, mt)]
        row: Dict[str, str] = {"dataset": ds, "model_type": mt}
        row["experiment_dir"] = str(r.summary_path.parent).replace("\\", "/")
        row["date"] = r.date_part
        row["time"] = r.time_part
        row["meta_source"] = r.source_meta
        row["sample_size_percentage"] = f"{r.sample_pct:g}"
        if r.generated_at:
            row["generated_at"] = r.generated_at
        for m in method_cols:
            if m in r.computation_timings:
                row[m] = f"{r.computation_timings[m]:.2f}"
            else:
                row[m] = "—"
        rows.append(row)
    return sorted_keys, method_cols, rows


def fmt_markdown(method_cols: List[str], rows: List[Dict[str, str]]) -> str:
    fixed = [
        "dataset",
        "model_type",
        "date",
        "time",
        "sample_size_percentage",
        "meta_source",
        "generated_at",
        "experiment_dir",
    ]
    headers = fixed + method_cols
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "—")) for h in headers) + " |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parent.parent / "experiment_logs"
    parser.add_argument(
        "--logs-root",
        type=Path,
        default=default_root,
        help="Корень каталога experiment_logs (по умолчанию ../experiment_logs от скрипта)",
    )
    parser.add_argument(
        "--csv-out",
        type=Path,
        default=None,
        help="Путь для CSV (если не задан — influence_timings_table.csv в logs-root)",
    )
    parser.add_argument(
        "--md-out",
        type=Path,
        default=None,
        help="Опционально: записать Markdown-таблицу в файл",
    )
    parser.add_argument(
        "--no-stdout-md",
        action="store_true",
        help="Не печатать Markdown в stdout",
    )
    parser.add_argument(
        "--list-skipped",
        type=Path,
        default=None,
        help="Опционально: записать список пропущенных summary (пояснения)",
    )
    args = parser.parse_args()

    logs_root = args.logs_root.resolve()
    if not logs_root.is_dir():
        print(f"error: logs root is not a directory: {logs_root}", file=sys.stderr)
        return 1

    records, skipped = collect_records(logs_root)
    chosen = pick_latest_per_dataset_model(records)
    _, method_cols, rows = build_table(chosen)

    csv_path = args.csv_out
    if csv_path is None:
        csv_path = logs_root / "influence_timings_table.csv"
    else:
        csv_path = csv_path.resolve()

    fixed = [
        "dataset",
        "model_type",
        "date",
        "time",
        "sample_size_percentage",
        "meta_source",
        "generated_at",
        "experiment_dir",
    ]
    fieldnames = fixed + method_cols

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            out = {k: row.get(k, "") for k in fieldnames}
            w.writerow(out)

    md = fmt_markdown(method_cols, rows)
    if not args.no_stdout_md:
        print(md)
    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(md + "\n", encoding="utf-8")

    if args.list_skipped:
        args.list_skipped.parent.mkdir(parents=True, exist_ok=True)
        args.list_skipped.write_text("\n".join(skipped) + "\n", encoding="utf-8")

    print(f"\nCSV written: {csv_path}", file=sys.stderr)
    print(
        f"Full-sample experiments used: {len(chosen)} (dataset x model_type) row(s)",
        file=sys.stderr,
    )
    print(f"Skipped / non-full / unusable lines logged: {len(skipped)}", file=sys.stderr)
    if skipped and not args.list_skipped:
        print("(use --list-skipped PATH to save the full list)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
