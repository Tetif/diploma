"""Sample sizes for UI hints: exact values where known, otherwise an estimate."""

from __future__ import annotations

from typing import Optional

# Number of rows after loading (wine - from the actual WineQT.csv in the repository)
APPROX_N_SAMPLES: dict[str, int] = {
    "adult": 32_561,
    "housing": 20_640,
    "wine": 1143,
    "zillow": 90_000,
    "covertype": 581_012,
    "electric": 2_000_000,
    "mnist": 70_000,
    "imdb": 50_000,
    "cifar10": 60_000,
}


def format_sample_size(n: Optional[int]) -> str:
    if n is None:
        return "—"
    if n >= 1_000_000:
        s = f"{n / 1_000_000:.1f}".rstrip("0").rstrip(".")
        return f"~{s} млн объектов"
    if n >= 10_000:
        k = n // 1000
        return f"~{k} тыс. объектов"
    return f"{n} объектов"
