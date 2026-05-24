"""Объём выборки для подсказок в UI: точные значения где известны, иначе оценка."""

from __future__ import annotations

from typing import Optional

# Число наблюдений после загрузки (wine — по фактическому WineQT.csv в репозитории)
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
