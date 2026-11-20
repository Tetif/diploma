# Итоги полного прогона (20–21.11.2026)

Прогон: `run_overnight.ps1 -Workers 6 -ThreadsPerWorker 2 -MinFreeMB 1000 -MaxHeavy 1`, старт 05:17, конец 15:17 МСК. Фазы: main 149.5 мин, sweep 154.8 мин, ext 295.4 мин. Итог: ok = 2955, skipped = 116, упавших единиц 0. 21.11 после P14 пересчитаны LossHigh для adult/covertype и transfer, после P15 добавлены 30 единиц damphigh: всего ok = 2985, skipped = 116, failed = 0. Лог: `run_logs\overnight-20261120-051718.log`.

Источники: `results/*/<dataset>/<method>/seed*/results.json` (пилоты `pilot*` и `probe` исключены), `assets/summary.csv`, `assets/paired_stats.md`, `assets/sensitivity.csv`, `assets/transfer.csv`, `assets/cost.csv`, рисунки `assets/1_…13_*.png`.

Обозначения:
- **Detection AUC** — ROC-AUC отделения зашумлённых точек по ценности (низкая ценность = подозрительная точка); 0.5 = случайно.
- **Δ vs random** — средний знаковый выигрыш метрики при удалении точек с наименьшей ценностью относительно случайного удаления на тех же сидах (paired). «+» = лучше при любой ориентации метрики (для MAE знак уже развёрнут). Строка `auc` — среднее по сетке удаления (5/10/20/30 %), `10 %` — при удалении 10 %. `*` = p < 0.05 (paired-тест из `assets/paired_stats.md`).
- Сиды: clean/noise10 — 5, остальные исследования — 3. Значимость при n = 3–5 даёт малую мощность.
- Метрики: wine и housing — MAE (housing в долларах), adult — F1, covertype — accuracy.
- Модель main-исследования — MLP (pytorch). LossHigh — baseline «высокий train loss = подозрительная точка».

## 1. Основное исследование (MLP)

### 1.1 Детекция шума (detection AUC, mean ± std по сидам)


**noise5**

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | 0.982 ± 0.02 | 0.998 ± 0.00 | 0.918 ± 0.02 | 0.959 ± 0.01 |
| Influence | 0.535 ± 0.02 | 0.508 ± 0.03 | 0.506 ± 0.04 | — |
| KNNShapley | — | — | 0.871 ± 0.01 | 0.927 ± 0.01 |
| LissaInfluence | 0.575 ± 0.09 | 0.582 ± 0.06 | 0.838 ± 0.07 | 0.792 ± 0.10 |
| LossHigh | 0.980 ± 0.01 | 0.998 ± 0.00 | 0.928 ± 0.00 | 0.952 ± 0.01 |
| random | 0.513 ± 0.03 | 0.527 ± 0.05 | 0.527 ± 0.05 | 0.527 ± 0.05 |


**noise10**

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | 0.985 ± 0.01 | 0.998 ± 0.00 | 0.888 ± 0.01 | 0.950 ± 0.01 |
| Influence | 0.519 ± 0.05 | 0.540 ± 0.03 | 0.519 ± 0.03 | 0.498 ± 0.04 |
| KNNShapley | — | — | 0.881 ± 0.01 | 0.916 ± 0.01 |
| LOO | 0.566 ± 0.03 | 0.514 ± 0.01 | 0.512 ± 0.02 | 0.498 ± 0.01 |
| LissaInfluence | 0.581 ± 0.08 | 0.539 ± 0.03 | 0.879 ± 0.02 | 0.851 ± 0.07 |
| LossHigh | 0.987 ± 0.01 | 0.998 ± 0.00 | 0.915 ± 0.02 | 0.933 ± 0.02 |
| TMCShapley | 0.573 ± 0.03 | — | — | — |
| random | 0.471 ± 0.03 | 0.497 ± 0.03 | 0.497 ± 0.03 | 0.497 ± 0.03 |


**noise20**

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | 0.973 ± 0.01 | 0.996 ± 0.00 | 0.857 ± 0.01 | 0.949 ± 0.00 |
| Influence | 0.496 ± 0.03 | 0.495 ± 0.02 | 0.535 ± 0.03 | — |
| KNNShapley | — | — | 0.877 ± 0.01 | 0.925 ± 0.01 |
| LissaInfluence | 0.558 ± 0.03 | 0.528 ± 0.04 | 0.845 ± 0.06 | 0.915 ± 0.01 |
| LossHigh | 0.980 ± 0.01 | 0.997 ± 0.00 | 0.908 ± 0.02 | 0.947 ± 0.01 |
| random | 0.479 ± 0.05 | 0.495 ± 0.02 | 0.495 ± 0.02 | 0.495 ± 0.02 |


**sysnoise5**

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | 0.676 ± 0.10 | 0.486 ± 0.06 | 0.919 ± 0.01 | 0.818 ± 0.02 |
| Influence | 0.604 ± 0.04 | 0.651 ± 0.10 | 0.519 ± 0.03 | — |
| KNNShapley | — | — | 0.943 ± 0.00 | 0.793 ± 0.03 |
| LissaInfluence | 0.822 ± 0.09 | 0.927 ± 0.03 | 0.939 ± 0.03 | 0.724 ± 0.31 |
| LossHigh | 0.784 ± 0.04 | 0.913 ± 0.01 | 0.930 ± 0.01 | 0.824 ± 0.03 |
| random | 0.552 ± 0.02 | 0.503 ± 0.02 | 0.485 ± 0.02 | 0.515 ± 0.03 |


**sysnoise10**

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | 0.635 ± 0.02 | 0.582 ± 0.04 | 0.902 ± 0.01 | 0.729 ± 0.01 |
| Influence | 0.518 ± 0.18 | 0.615 ± 0.07 | 0.512 ± 0.03 | — |
| KNNShapley | — | — | 0.947 ± 0.00 | 0.778 ± 0.02 |
| LissaInfluence | 0.899 ± 0.05 | 0.928 ± 0.01 | 0.964 ± 0.00 | 0.613 ± 0.44 |
| LossHigh | 0.835 ± 0.07 | 0.859 ± 0.01 | 0.922 ± 0.01 | 0.773 ± 0.02 |
| random | 0.514 ± 0.01 | 0.501 ± 0.02 | 0.509 ± 0.03 | 0.495 ± 0.04 |


**sysnoise20**

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | 0.587 ± 0.04 | 0.667 ± 0.04 | 0.804 ± 0.01 | 0.557 ± 0.01 |
| Influence | 0.654 ± 0.20 | 0.607 ± 0.10 | 0.546 ± 0.04 | — |
| KNNShapley | — | — | 0.940 ± 0.00 | 0.752 ± 0.02 |
| LissaInfluence | 0.957 ± 0.02 | 0.906 ± 0.08 | 0.929 ± 0.05 | 0.895 ± 0.01 |
| LossHigh | 0.849 ± 0.04 | 0.776 ± 0.11 | 0.850 ± 0.02 | 0.687 ± 0.05 |
| random | 0.505 ± 0.01 | 0.502 ± 0.01 | 0.504 ± 0.02 | 0.479 ± 0.01 |


Выводы по детекции:
- **Случайный шум меток (noise5/10/20)** — лидируют **Data-OOB** и **LossHigh**.
  - Регрессия (wine, housing): AUC 0.97–0.998 у обоих.
  - adult: LossHigh (взвешенный, P14) 0.91–0.93, Data-OOB 0.86–0.92.
  - covertype: Data-OOB 0.95–0.96, LossHigh 0.93–0.95.
  - **KNN-Shapley** (только классификация) идёт следом: 0.87–0.93.
  - **LiSSA** хорош на классификации (adult 0.84–0.88, covertype 0.79–0.92), но на регрессии близок к случайному (0.53–0.58).
- **Прямой Influence (DirectInfluence) ≈ случаен везде: 0.45–0.6.** LOO и TMC-Shapley тоже ≈ 0.5–0.57. Это ожидаемо: при n = 1500 удаление одной точки почти не меняет модель, а SGD-шум сильнее эффекта точки.
- **Систематический шум (sysnoise5/10/20)** — картина меняется.
  - Лучший метод — **LiSSA**: housing 0.91–0.93, wine 0.82–0.96, adult 0.93–0.96; covertype нестабилен (0.61–0.90).
  - На adult рядом **KNN-Shapley** (0.94–0.95).
  - **Data-OOB** проседает на регрессии (0.49–0.67) и на covertype (0.56–0.82).
  - **LossHigh** держится на среднем уровне (0.69–0.93; на adult 0.85–0.93).
  - Систематически сдвинутые метки «выглядят правдоподобно» для ансамбля Data-OOB, а градиентный метод видит их согласованное влияние.

### 1.2 Очистка данных: удаление точек с наименьшей ценностью


**clean** — Δ vs random, среднее по сетке (`auc`):

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | -0.0013 | -91 | +0.0003 | +0.0016 |
| Influence | -0.0039 | +303 | -0.0017 | -0.0038 |
| KNNShapley | — | — | -0.0038 | -0.0194* |
| LOO | +0.0058 | +276 | +0.0018 | +0.0001 |
| LissaInfluence | -0.0058 | -274 | -0.0196 | -0.0280* |
| LossHigh | +0.0029 | +179 | +0.0004 | -0.0044* |
| TMCShapley | -0.0008 | — | — | — |

**clean** — Δ vs random при удалении 10 %:

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | -0.0112* | -87 | -0.0014 | +0.0024 |
| Influence | -0.0057 | +8.6481 | +0.0004 | -0.0013 |
| KNNShapley | — | — | +0.0020 | -0.0040 |
| LOO | +0.0061 | +85 | +0.0035 | +0.0017 |
| LissaInfluence | -0.0005 | +220 | -0.0140 | -0.0096* |
| LossHigh | -0.0101* | +346 | +0.0075* | -0.0003 |
| TMCShapley | -0.0037 | — | — | — |


**noise5** — Δ vs random, среднее по сетке (`auc`):

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | -0.0059 | +1921 | -0.0055 | +0.0049 |
| Influence | +0.0007 | +1136 | -0.0039 | — |
| KNNShapley | — | — | -0.0108 | -0.0029 |
| LissaInfluence | -0.0130 | +492 | -0.0134 | -0.0082 |
| LossHigh | -0.0051 | +2248 | -0.0049* | +0.0014 |

**noise5** — Δ vs random при удалении 10 %:

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | -0.0084 | +2158 | -0.0088 | +0.0061 |
| Influence | -0.0009 | +1204 | -0.0061 | — |
| KNNShapley | — | — | -0.0175 | -0.0005 |
| LissaInfluence | -0.0157 | +1013 | -0.0151 | -0.0034* |
| LossHigh | -0.0069 | +2570 | -0.0062 | +0.0001 |


**noise10** — Δ vs random, среднее по сетке (`auc`):

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | -0.0001 | +1896* | +0.0003 | +0.0019 |
| Influence | -0.0023 | +705 | +0.0002 | -0.0042 |
| KNNShapley | — | — | -0.0061 | -0.0067* |
| LOO | +0.0122* | +1205* | -0.0032 | +0.0014 |
| LissaInfluence | -0.0067 | -960 | -0.0005 | -0.0117* |
| LossHigh | -0.0010 | +1353 | -0.0035* | +0.0005 |
| TMCShapley | +0.0110 | — | — | — |

**noise10** — Δ vs random при удалении 10 %:

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | +0.0014 | +2809* | -0.0009 | -0.0009 |
| Influence | -0.0022 | +1103* | -0.0016 | -0.0084 |
| KNNShapley | — | — | -0.0044 | -0.0044 |
| LOO | +0.0139* | +1307* | -0.0075 | +0.0005 |
| LissaInfluence | -0.0078 | -143 | -0.0026 | -0.0166* |
| LossHigh | +0.0038 | +2650* | -0.0031 | +0.0006 |
| TMCShapley | +0.0143* | — | — | — |


**noise20** — Δ vs random, среднее по сетке (`auc`):

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | +0.0136 | +639 | +0.0003 | +0.0075 |
| Influence | +0.0077 | +1163 | +0.0066 | — |
| KNNShapley | — | — | -0.0070 | -0.0022 |
| LissaInfluence | -0.0099 | -3736 | -0.0013 | -0.0040 |
| LossHigh | +0.0030 | -1037 | +0.0055 | +0.0030 |

**noise20** — Δ vs random при удалении 10 %:

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | +0.0225 | -1348 | -0.0012 | +0.0125 |
| Influence | +0.0199 | +1693 | +0.0032 | — |
| KNNShapley | — | — | -0.0082* | +0.0055 |
| LissaInfluence | +0.0019 | -3991 | +0.0046 | -0.0001 |
| LossHigh | +0.0005 | -4068* | +0.0101 | +0.0051 |


**sysnoise5** — Δ vs random, среднее по сетке (`auc`):

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | -0.0068 | -63 | -0.0011 | +0.0068 |
| Influence | +0.0066 | +1770 | -0.0004 | — |
| KNNShapley | — | — | -0.0076 | -0.0061* |
| LissaInfluence | +0.0268* | +3452* | -0.0097 | -0.0157* |
| LossHigh | +0.0055* | +2923* | -0.0007 | +0.0025 |

**sysnoise5** — Δ vs random при удалении 10 %:

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | -0.0105 | -357 | -0.0000 | +0.0071 |
| Influence | +0.0064 | +2047 | -0.0027 | — |
| KNNShapley | — | — | -0.0077 | -0.0043 |
| LissaInfluence | +0.0349* | +4066 | -0.0138 | -0.0136* |
| LossHigh | +0.0020 | +3284 | -0.0009 | +0.0022 |


**sysnoise10** — Δ vs random, среднее по сетке (`auc`):

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | +0.0033 | +141 | -0.0065 | +0.0080 |
| Influence | +0.0191 | +2230 | +0.0004 | — |
| KNNShapley | — | — | -0.0025 | -0.0002 |
| LissaInfluence | +0.0491* | +8370* | +0.0014 | -0.0078 |
| LossHigh | +0.0139* | +3663* | -0.0080 | +0.0031 |

**sysnoise10** — Δ vs random при удалении 10 %:

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | +0.0101 | -739 | -0.0016 | +0.0141 |
| Influence | +0.0285 | +2407* | +0.0035 | — |
| KNNShapley | — | — | -0.0005 | +0.0149 |
| LissaInfluence | +0.0750 | +11321* | +0.0068 | +0.0069 |
| LossHigh | +0.0238* | +3908 | -0.0070 | +0.0133 |


**sysnoise20** — Δ vs random, среднее по сетке (`auc`):

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | -0.0011 | +4974* | -0.0052 | +0.0365* |
| Influence | +0.0190 | +4544 | -0.0012 | — |
| KNNShapley | — | — | -0.0110* | +0.0292* |
| LissaInfluence | +0.0461* | +11949* | -0.0125 | +0.0211 |
| LossHigh | +0.0239* | +7960* | -0.0102 | +0.0336* |

**sysnoise20** — Δ vs random при удалении 10 %:

| method | wine | housing | adult | covertype |
|---|---|---|---|---|
| DataOOB | -0.0063 | +5111* | -0.0020 | +0.0567* |
| Influence | +0.0189 | +4506 | -0.0030 | — |
| KNNShapley | — | — | -0.0083 | +0.0519* |
| LissaInfluence | +0.0436 | +13040* | -0.0117 | +0.0409 |
| LossHigh | +0.0323* | +9321* | -0.0092* | +0.0505* |


Выводы по очистке:
- **На чистых данных** удаление «худших» точек не помогает.
  - Значимые эффекты только отрицательные: KNN-Shapley и LiSSA на covertype (−0.019* и −0.028* accuracy по сетке).
  - Удаляются информативные, а не плохие точки.
- **Случайный шум.** Выигрыш над случайным удалением небольшой и редко значим.
  - Значимые плюсы: housing noise10 — Data-OOB (+1896 $ MAE*) и LOO (+1205*); wine noise10 — LOO (+0.012*).
  - На adult и covertype эффекты в пределах ±0.01, часто отрицательные.
  - Причина: MLP с early stopping по val и так устойчив к 5–20 % шума, а удаление 10–30 % выборки дорого стоит.
- **Систематический шум** — здесь очистка работает лучше всего.
  - **LiSSA**: housing +3452*/+8370*/+11949* $ MAE (sysnoise 5/10/20), wine +0.027*/+0.049*/+0.046*.
  - **LossHigh**: housing +2923*/+3663*/+7960*, wine +0.006*/+0.014*/+0.024*.
  - **Data-OOB**: housing sysnoise20 +4974*, covertype sysnoise20 +0.037*.
  - **KNN-Shapley**: covertype sysnoise20 +0.029*.
- Итог: **детекция ≠ очистка**. Почти идеальная детекция Data-OOB/LossHigh на регрессии при случайном шуме даёт значимый выигрыш метрики только на housing. Реальный выигрыш появляется там, где шум систематический и смещает модель.

## 2. Influence для GBDT через дистилляцию (P9–P11)

Постановка: учитель LightGBM или CatBoost обучается на данных с шумом 10 %, MLP-студент дистиллирует учителя, influence считается на студенте.
- `true_labels` — влияние по настоящим (шумным) меткам.
- `tgtteacher` — влияние по целям учителя.

Baselines на том же сплите: BoostIn (учитель LightGBM), CatBoost LFC (учитель CatBoost), Data-OOB, LossHigh. По 3 сида.

Detection AUC:


| study / method | wine | housing | adult | covertype |
|---|---|---|---|---|
| distill-catboost-noise10 / CatBoostLFC | — | — | 0.748 | — |
| distill-catboost-noise10 / DataOOB | 0.984 | 0.998 | 0.896 | 0.950 |
| distill-catboost-noise10 / Influence | 0.446 | 0.535 | 0.537 | 0.501 |
| distill-catboost-noise10 / LissaInfluence | 0.586 | 0.546 | 0.764 | 0.878 |
| distill-catboost-noise10 / LossHigh | 0.978 | 0.995 | 0.870 | 0.939 |
| distill-catboost-noise10 / random | 0.476 | 0.489 | 0.489 | 0.489 |
| distill-catboost-noise10-tgtteacher / Influence | 0.500 | 0.503 | 0.503 | 0.563 |
| distill-catboost-noise10-tgtteacher / LissaInfluence | 0.511 | 0.503 | 0.767 | 0.911 |
| distill-lightgbm-noise10 / BoostIn | 0.568 | 0.529 | 0.829 | 0.908 |
| distill-lightgbm-noise10 / DataOOB | 0.984 | 0.998 | 0.896 | 0.950 |
| distill-lightgbm-noise10 / Influence | 0.463 | 0.474 | 0.532 | 0.517 |
| distill-lightgbm-noise10 / LissaInfluence | 0.555 | 0.507 | 0.760 | 0.788 |
| distill-lightgbm-noise10 / LossHigh | 0.984 | 0.998 | 0.878 | 0.944 |
| distill-lightgbm-noise10 / random | 0.476 | 0.489 | 0.489 | 0.489 |
| distill-lightgbm-noise10-tgtteacher / Influence | 0.473 | 0.509 | 0.448 | 0.523 |
| distill-lightgbm-noise10-tgtteacher / LissaInfluence | 0.533 | 0.506 | 0.747 | 0.924 |


Δ vs random (удаление по сетке; переобучаются учитель и студент, метрика студента):

| study / method | wine | housing | adult | covertype |
|---|---|---|---|---|
| distill-catboost-noise10 / CatBoostLFC | — | — | +0.0082 | — |
| distill-catboost-noise10 / DataOOB | +0.0058* | +258 | +0.0045 | +0.0034 |
| distill-catboost-noise10 / Influence | +0.0036 | -303 | -0.0015 | +0.0011 |
| distill-catboost-noise10 / LissaInfluence | +0.0141* | -409 | +0.0002 | +0.0014 |
| distill-catboost-noise10 / LossHigh | +0.0063 | -758* | +0.0010 | -0.0007 |
| distill-lightgbm-noise10 / BoostIn | +0.0006 | +987* | +0.0025 | -0.0014 |
| distill-lightgbm-noise10 / DataOOB | -0.0008 | +3743* | +0.0027* | +0.0003 |
| distill-lightgbm-noise10 / Influence | -0.0014 | +1526* | -0.0022 | -0.0033 |
| distill-lightgbm-noise10 / LissaInfluence | +0.0057 | +334 | -0.0001 | -0.0042 |
| distill-lightgbm-noise10 / LossHigh | -0.0039 | +2902* | +0.0019 | +0.0002 |


Для сравнения — прямые GBDT-модели (`models-*-noise10`), detection AUC:

| study / method | wine | housing | adult | covertype |
|---|---|---|---|---|
| models-catboost-noise10 / CatBoostLFC | 0.524 | 0.505 | 0.748 | — |
| models-catboost-noise10 / DataOOB | 0.984 | 0.998 | 0.896 | 0.950 |
| models-catboost-noise10 / KNNShapley | — | — | 0.878 | 0.913 |
| models-catboost-noise10 / LOO | 0.508 | 0.517 | 0.524 | 0.527 |
| models-catboost-noise10 / LossHigh | 0.978 | 0.996 | 0.917 | 0.905 |
| models-catboost-noise10 / random | 0.476 | 0.489 | 0.489 | 0.489 |
| models-lightgbm-noise10 / BoostIn | 0.547 | 0.553 | 0.829 | 0.908 |
| models-lightgbm-noise10 / DataOOB | 0.984 | 0.998 | 0.896 | 0.950 |
| models-lightgbm-noise10 / KNNShapley | — | — | 0.878 | 0.913 |
| models-lightgbm-noise10 / LOO | 0.536 | 0.558 | 0.508 | 0.489 |
| models-lightgbm-noise10 / LossHigh | 0.983 | 0.997 | 0.889 | 0.826 |
| models-lightgbm-noise10 / random | 0.476 | 0.489 | 0.489 | 0.489 |
| models-random_forest-noise10 / DataOOB | 0.984 | 0.998 | 0.896 | 0.950 |
| models-random_forest-noise10 / KNNShapley | — | — | 0.878 | 0.913 |
| models-random_forest-noise10 / LOO | 0.541 | 0.531 | 0.494 | 0.471 |
| models-random_forest-noise10 / LossHigh | 0.975 | 0.996 | 0.930 | 0.933 |
| models-random_forest-noise10 / random | 0.476 | 0.489 | 0.489 | 0.489 |
| models-xgboost-noise10 / DataOOB | 0.984 | 0.998 | 0.896 | 0.950 |
| models-xgboost-noise10 / KNNShapley | — | — | 0.878 | 0.913 |
| models-xgboost-noise10 / LOO | 0.536 | 0.527 | 0.508 | 0.502 |
| models-xgboost-noise10 / LossHigh | 0.573 | 0.807 | 0.827 | 0.919 |
| models-xgboost-noise10 / random | 0.476 | 0.489 | 0.489 | 0.489 |


Примечание: LossHigh в `models-*` для adult/covertype уже взвешенный (P14). В `distill-*` студент обучается без весов, его LossHigh не менялся.

**Вердикт по гипотезе** «influence студента-дистиллята — рабочая замена influence для GBDT»:
- **Не подтверждается для DirectInfluence** — ни в варианте `true_labels`, ни в `teacher`.
  - Detection AUC 0.45–0.56, то есть уровень случайного.
  - BoostIn на тех же данных: adult 0.83, covertype 0.91.
  - CatBoost LFC на adult: 0.75.
- **Частично подтверждается для LiSSA-студента на классификации.**
  - adult: 0.75–0.77, на уровне CatBoost LFC (0.75), ниже BoostIn (0.83).
  - covertype: 0.79–0.88 с `true_labels`; с `teacher` 0.91–0.92 — на уровне BoostIn (0.91).
  - Вариант `teacher` помогает только на covertype; на adult эффекта нет, на регрессии AUC ≈ 0.5.
- **Регрессия (wine, housing)**: все influence-подобные методы ≈ 0.5–0.59, включая BoostIn (0.53–0.57) и CatBoost LFC (0.51–0.52).
- **Data-OOB и LossHigh** превосходят все influence-методы на всех четырёх датасетах.
  - Data-OOB: 0.90/0.95/0.998/0.98.
  - LossHigh: 0.87–0.88/0.94/0.995–0.998/0.98.
- **По очистке значимых различий почти нет.**
  - Значимые плюсы: Data-OOB (+3743*), LossHigh (+2902*), BoostIn (+987*) и Influence-студент (+1526*) на housing (учитель LightGBM); Data-OOB (+0.006*) и LiSSA (+0.014*) на wine (учитель CatBoost).
- Честный итог:
  - Influence через студента не превосходит ни специализированный BoostIn, ни дешёвые baseline (Data-OOB, high-loss).
  - Единственный конкурентный вариант — LiSSA-студент с целями учителя на covertype.
  - Как метод детекции шума для GBDT гипотеза **отвергается**. Как приближение к BoostIn она работает только на многоклассовой классификации.

## 3. Демпфирование и чувствительность

### 3.1 Damping sweep (noise10, 3 сида; `damp-linear-*` — линейная модель, `damp-mlp-*` — MLP)

Detection AUC:


| study / method | wine | housing | adult | covertype |
|---|---|---|---|---|
| damp-linear-0.0001 / Influence | 0.577 | 0.532 | 0.786 | 0.862 |
| damp-linear-0.0001 / LissaInfluence | 0.592 | 0.548 | 0.854 | 0.835 |
| damp-linear-0.0001 / LossHigh | 0.982 | 0.995 | 0.917 | 0.921 |
| damp-linear-0.01 / Influence | 0.579 | 0.532 | 0.833 | 0.862 |
| damp-linear-0.01 / LissaInfluence | 0.592 | 0.549 | 0.854 | 0.835 |
| damp-linear-0.01 / LossHigh | 0.982 | 0.995 | 0.917 | 0.921 |
| damp-linear-1 / Influence | 0.588 | 0.551 | 0.841 | 0.793 |
| damp-linear-1 / LissaInfluence | 0.592 | 0.545 | 0.841 | 0.790 |
| damp-linear-1 / LossHigh | 0.982 | 0.995 | 0.917 | 0.921 |
| damp-linear-1e-06 / Influence | 0.577 | 0.532 | 0.781 | 0.856 |
| damp-linear-1e-06 / LissaInfluence | 0.592 | 0.548 | 0.854 | 0.835 |
| damp-linear-1e-06 / LossHigh | 0.982 | 0.995 | 0.917 | 0.921 |
| damp-mlp-0.0001 / Influence | 0.532 | 0.530 | 0.498 | — |
| damp-mlp-0.0001 / LissaInfluence | 0.620 | 0.541 | 0.852 | — |
| damp-mlp-0.0001 / LossHigh | 0.984 | 0.998 | 0.925 | — |
| damp-mlp-0.01 / Influence | 0.498 | 0.505 | 0.696 | — |
| damp-mlp-0.01 / LissaInfluence | 0.620 | 0.541 | 0.853 | — |
| damp-mlp-0.01 / LossHigh | 0.984 | 0.998 | 0.925 | — |
| damp-mlp-0.1 / Influence | 0.599 | 0.546 | 0.852 | 0.818 |
| damp-mlp-1 / Influence | 0.621 | 0.538 | 0.892 | 0.861 |
| damp-mlp-1 / LissaInfluence | 0.619 | 0.540 | 0.877 | — |
| damp-mlp-1 / LossHigh | 0.984 | 0.998 | 0.925 | — |
| damp-mlp-1e-06 / Influence | 0.517 | 0.521 | 0.543 | — |
| damp-mlp-1e-06 / LissaInfluence | 0.620 | 0.541 | 0.852 | — |
| damp-mlp-1e-06 / LossHigh | 0.984 | 0.998 | 0.925 | — |


Δ vs random (по сетке):

| study / method | wine | housing | adult | covertype |
|---|---|---|---|---|
| damp-linear-0.0001 / Influence | -0.0004 | -2421 | +0.0027 | -0.0110* |
| damp-linear-0.0001 / LissaInfluence | -0.0017 | -3219 | +0.0045 | -0.0176* |
| damp-linear-0.0001 / LossHigh | +0.0012 | +681 | +0.0043 | +0.0006 |
| damp-linear-0.01 / Influence | -0.0008 | -2525 | +0.0056 | -0.0144* |
| damp-linear-0.01 / LissaInfluence | -0.0017 | -3349 | +0.0050 | -0.0188* |
| damp-linear-0.01 / LossHigh | +0.0012 | +681 | +0.0043 | +0.0006 |
| damp-linear-1 / Influence | -0.0021 | -3335 | +0.0056 | -0.0209* |
| damp-linear-1 / LissaInfluence | -0.0013 | -3630 | +0.0069 | -0.0201* |
| damp-linear-1 / LossHigh | +0.0012 | +681 | +0.0043 | +0.0006 |
| damp-linear-1e-06 / Influence | -0.0004 | -2438 | +0.0058* | -0.0124* |
| damp-linear-1e-06 / LissaInfluence | -0.0017 | -3226 | +0.0045 | -0.0176* |
| damp-linear-1e-06 / LossHigh | +0.0012 | +681 | +0.0043 | +0.0006 |
| damp-mlp-0.0001 / Influence | -0.0075 | +993 | +0.0003 | — |
| damp-mlp-0.0001 / LissaInfluence | +0.0030 | +142 | -0.0063 | — |
| damp-mlp-0.0001 / LossHigh | -0.0034 | +1850 | -0.0040* | — |
| damp-mlp-0.01 / Influence | +0.0032 | +756 | -0.0003 | — |
| damp-mlp-0.01 / LissaInfluence | +0.0028 | +253 | -0.0074 | — |
| damp-mlp-0.01 / LossHigh | -0.0034 | +1850 | -0.0040* | — |
| damp-mlp-0.1 / Influence | +0.0019 | +1422 | -0.0045 | -0.0031 |
| damp-mlp-1 / Influence | +0.0001 | -369 | -0.0011 | -0.0084 |
| damp-mlp-1 / LissaInfluence | +0.0029 | -993 | -0.0010 | — |
| damp-mlp-1 / LossHigh | -0.0034 | +1850 | -0.0040* | — |
| damp-mlp-1e-06 / Influence | +0.0060 | +1111 | +0.0053 | — |
| damp-mlp-1e-06 / LissaInfluence | +0.0030 | +142 | -0.0063 | — |
| damp-mlp-1e-06 / LossHigh | -0.0034 | +1850 | -0.0040* | — |


Выводы:
- **Линейная (выпуклая) модель.** DirectInfluence работает: adult 0.78–0.84, covertype 0.79–0.86. Демпфирование в диапазоне 1e-6…1e-2 почти ни на что не влияет.
  - При λ = 1 на covertype AUC падает до 0.79, на adult растёт до 0.84.
  - LiSSA ≈ Direct (0.84–0.85 и 0.79–0.84). Это подтверждает, что Direct реализован корректно.
- **MLP (невыпуклая модель).** DirectInfluence с малым λ (1e-6, 1e-4) ≈ случаен: adult 0.50–0.54.
  - С ростом λ качество монотонно растёт: λ = 1e-2 → 0.70, λ = 0.1 → 0.85, λ = 1 → **0.89** на adult — на уровне LiSSA (0.88), но ниже взвешенного LossHigh (0.925). Полная таблица с covertype — в 7.3.
  - Причина: у гессиана MLP есть околонулевые и отрицательные собственные значения, и при малом λ обратная матрица ими доминирует.
  - **Следствие для п. 1:** по умолчанию в main используется λ ≈ 1e-5…1e-4 (`effective_damping`), и это объясняет ≈ 0.5 у Direct Influence. Данные тут ни при чём.
- **LiSSA к λ нечувствителен** (0.85 на adult при любом λ). В main у LiSSA есть неявная нижняя граница демпфирования (`lissa.implicit_damping_floor`, `effective_damping` = 3–12), поэтому LiSSA по сути работает как сильно задемпфированный influence, близкий к градиентному скалярному произведению.
- **Регрессия (housing, wine)**: и Direct, и LiSSA ≈ 0.50–0.62 при любом λ, LossHigh 0.98–0.998 (почему — см. 7.2).
- По очистке демпфирование значимого выигрыша не даёт. На covertype (линейная модель) все influence-варианты значимо хуже случайного удаления: от −0.011* до −0.021*.

### 3.2 Sensitivity sweep (adult, noise10, MLP, 3 сида)

Detection AUC по конфигурациям (`base` = batch 128, normal fit, sample_scale 1, valuation_epochs 30):


| method | base | batch_size-0 | fit_mode-overfit | fit_mode-underfit | sample_scale-0.1 | sample_scale-0.3 | valuation_epochs-10 | valuation_epochs-60 |
|---|---|---|---|---|---|---|---|---|
| DataOOB | 0.896 | 0.896 | 0.896 | 0.896 | 0.857 | 0.900 | — | — |
| Influence | 0.524 | 0.547 | — | 0.693 | 0.528 | 0.509 | — | — |
| KNNShapley | 0.878 | 0.878 | 0.878 | 0.878 | 0.816 | 0.861 | — | — |
| LOO | 0.527 | 0.549 | 0.517 | 0.518 | 0.617 | 0.530 | 0.502 | 0.494 |
| LissaInfluence | 0.880 | 0.920 | 0.793 | 0.834 | 0.860 | 0.857 | — | — |
| LossHigh | 0.925 | 0.922 | 0.891 | 0.796 | 0.885 | 0.911 | — | — |
| random | 0.489 | 0.489 | 0.489 | 0.489 | 0.468 | 0.495 | 0.489 | 0.489 |


Базовая F1 модели по конфигурациям: base 0.666, batch_size-0 0.656, fit_mode-overfit 0.644, fit_mode-underfit 0.157, sample_scale-0.1 0.584, sample_scale-0.3 0.637, valuation_epochs-10 0.666, valuation_epochs-60 0.666


Выводы:
- **Data-OOB и KNN-Shapley** не зависят от настроек MLP — они не используют MLP. Ухудшаются только при sample_scale 0.1: 0.86 и 0.82.
- **LiSSA** — лучший среди MLP-зависимых методов.
  - Full-batch (batch_size 0): 0.92, лучше base (0.88).
  - Переобучение и недообучение снижают AUC: 0.79 и 0.83.
- **DirectInfluence** заметно выше случайного только для underfit-модели (0.69). Для overfit-модели (≈ 0.79M параметров) он корректно помечен NotApplicable: гессиану нужно ~19.6 ТБ.
- **LossHigh** (взвешенный, P14) — лучший метод в sweep: base 0.925, full-batch 0.92, overfit 0.89, sample_scale 0.1 0.885. Проседает только у вырожденной underfit-модели (0.80).
- **LOO** ≈ 0.5 при любом числе эпох (10/30/60). Только при sample_scale 0.1 (n_train ≈ 150) он доходит до 0.62: вклад одной точки становится различим.
- **Аномалия:** underfit-конфигурация (`[4]`) имеет базовую F1 **0.157**. Модель вырождена (почти всегда предсказывает мажорный класс), поэтому её Δ интерпретировать нельзя.
- По очистке (Δ при 10 %, `assets/sensitivity.csv`) выигрыш есть только при sample_scale 0.1: +0.05…+0.09 F1 у всех методов, включая Influence (+0.091), против случайного удаления. В остальных конфигурациях |Δ| < 0.02.

## 4. Перенос ценностей между моделями (transfer, noise10, 3 сида)

Ценности, посчитанные на модели-источнике, используются для удаления 10 % точек при обучении модели-цели. Δ — выигрыш над случайным удалением на модели-цели (знак ориентирован, «+» = лучше). `any.*` — модель-независимые методы.


**wine**

| source \ target | catboost | distill-lightgbm | lightgbm | pytorch | random_forest | xgboost |
|---|---|---|---|---|---|---|
| any.DataOOB | +0.0034 | -0.0044 | +0.0208 | +0.0037 | +0.0445 | +0.1320 |
| catboost.CatBoostLFC | +0.0027 | -0.0202 | -0.0172 | -0.0158 | -0.0108 | +0.0071 |
| catboost.LOO | -0.0206 | -0.0223 | -0.0305 | -0.0048 | -0.0111 | +0.0210 |
| catboost.LossHigh | +0.0056 | -0.0099 | +0.0293 | +0.0074 | +0.0392 | +0.1600 |
| distill-lightgbm.Influence | -0.0072 | -0.0158 | -0.0076 | +0.0005 | +0.0024 | +0.0600 |
| distill-lightgbm.LossHigh | +0.0012 | -0.0030 | +0.0346 | +0.0035 | +0.0426 | +0.1354 |
| lightgbm.LOO | +0.0016 | -0.0281 | -0.0126 | -0.0007 | +0.0159 | +0.0173 |
| lightgbm.LossHigh | +0.0019 | -0.0004 | +0.0278 | +0.0017 | +0.0335 | +0.1424 |
| pytorch.Influence | -0.0016 | -0.0199 | -0.0132 | -0.0069 | -0.0096 | +0.0484 |
| pytorch.LOO | +0.0042 | -0.0038 | -0.0118 | +0.0115 | +0.0095 | +0.0211 |
| pytorch.LissaInfluence | +0.0115 | -0.0069 | +0.0087 | +0.0028 | +0.0095 | +0.0612 |
| pytorch.LossHigh | +0.0029 | +0.0040 | +0.0500 | +0.0063 | +0.0445 | +0.1340 |
| random_forest.LOO | +0.0017 | -0.0099 | -0.0281 | +0.0033 | -0.0013 | +0.0220 |
| random_forest.LossHigh | +0.0017 | -0.0062 | +0.0116 | -0.0005 | +0.0299 | +0.1268 |
| xgboost.LOO | +0.0017 | -0.0183 | -0.0100 | +0.0081 | +0.0059 | -0.0079 |
| xgboost.LossHigh | -0.0132 | -0.0028 | -0.0053 | +0.0064 | +0.0126 | +0.0393 |


**housing**

| source \ target | catboost | distill-lightgbm | lightgbm | pytorch | random_forest | xgboost |
|---|---|---|---|---|---|---|
| any.DataOOB | +628 | +5554 | +11158 | +3600 | +6253 | +24639 |
| catboost.CatBoostLFC | -233 | -1709 | -2112 | -1397 | -3285 | +1105 |
| catboost.LOO | +389 | +1178 | +270 | +497 | +466 | -109 |
| catboost.LossHigh | +554 | +4363 | +9809 | +2993 | +5600 | +23813 |
| distill-lightgbm.Influence | -264 | +2260 | +1703 | +1280 | +1441 | +7527 |
| distill-lightgbm.LossHigh | +652 | +4914 | +10516 | +3155 | +6035 | +24402 |
| lightgbm.LOO | +260 | +809 | +425 | +1481 | +1007 | +1765 |
| lightgbm.LossHigh | +676 | +4402 | +9760 | +3154 | +5840 | +24588 |
| pytorch.Influence | +80 | +846 | +2439 | +1394 | +2009 | +8689 |
| pytorch.LOO | +97 | +1280 | +425 | +1068 | -232 | -393 |
| pytorch.LissaInfluence | +800 | -883 | -183 | -499 | -1768 | +8194 |
| pytorch.LossHigh | +741 | +4957 | +10434 | +3343 | +5848 | +24017 |
| random_forest.LOO | +341 | +1585 | +182 | +918 | +574 | -450 |
| random_forest.LossHigh | +606 | +4467 | +10040 | +3358 | +5707 | +24208 |
| xgboost.LOO | -2 | +536 | +88 | +26 | -165 | +161 |
| xgboost.LossHigh | -13 | +2090 | +2198 | +378 | +1938 | +10114 |


**adult**

| source \ target | catboost | distill-lightgbm | lightgbm | pytorch | random_forest | xgboost |
|---|---|---|---|---|---|---|
| any.DataOOB | -0.0020 | +0.0001 | +0.0105 | -0.0007 | -0.0051 | +0.0609 |
| any.KNNShapley | -0.0062 | +0.0004 | +0.0190 | -0.0079 | -0.0013 | +0.0670 |
| catboost.CatBoostLFC | +0.0052 | +0.0081 | -0.0045 | -0.0005 | -0.0006 | +0.0449 |
| catboost.LOO | -0.0023 | -0.0058 | +0.0091 | -0.0060 | -0.0011 | +0.0032 |
| catboost.LossHigh | -0.0001 | +0.0075 | +0.0173 | +0.0029 | -0.0111 | +0.0804 |
| distill-lightgbm.Influence | +0.0011 | -0.0027 | +0.0120 | +0.0002 | +0.0007 | +0.0392 |
| distill-lightgbm.LossHigh | -0.0007 | +0.0061 | +0.0151 | +0.0033 | -0.0069 | +0.0647 |
| lightgbm.LOO | -0.0013 | +0.0015 | +0.0011 | -0.0014 | -0.0011 | +0.0130 |
| lightgbm.LossHigh | +0.0013 | +0.0001 | +0.0202 | +0.0012 | -0.0061 | +0.0569 |
| pytorch.Influence | +0.0065 | +0.0108 | +0.0168 | +0.0056 | +0.0015 | +0.0442 |
| pytorch.LOO | -0.0027 | -0.0073 | -0.0093 | -0.0107 | +0.0004 | +0.0120 |
| pytorch.LissaInfluence | +0.0035 | +0.0020 | +0.0153 | +0.0008 | -0.0074 | +0.0660 |
| pytorch.LossHigh | -0.0032 | +0.0058 | +0.0160 | -0.0046 | -0.0072 | +0.0672 |
| random_forest.LOO | +0.0018 | -0.0032 | -0.0004 | +0.0063 | -0.0036 | +0.0031 |
| random_forest.LossHigh | -0.0037 | +0.0037 | +0.0169 | -0.0010 | -0.0115 | +0.0759 |
| xgboost.LOO | -0.0015 | -0.0107 | -0.0080 | +0.0034 | -0.0065 | +0.0193 |
| xgboost.LossHigh | +0.0014 | +0.0037 | +0.0101 | +0.0019 | -0.0026 | +0.0379 |


**covertype**

| source \ target | catboost | distill-lightgbm | lightgbm | pytorch | random_forest | xgboost |
|---|---|---|---|---|---|---|
| any.DataOOB | +0.0077 | +0.0013 | +0.0088 | -0.0031 | +0.0059 | +0.0158 |
| any.KNNShapley | +0.0073 | -0.0054 | +0.0071 | -0.0026 | +0.0035 | +0.0091 |
| catboost.LOO | +0.0017 | -0.0020 | -0.0018 | +0.0021 | +0.0047 | +0.0014 |
| catboost.LossHigh | +0.0071 | +0.0019 | +0.0032 | +0.0009 | +0.0059 | +0.0128 |
| distill-lightgbm.Influence | +0.0063 | -0.0049 | -0.0013 | +0.0027 | +0.0044 | +0.0019 |
| distill-lightgbm.LossHigh | +0.0106 | -0.0022 | +0.0095 | +0.0019 | +0.0056 | +0.0164 |
| lightgbm.LOO | -0.0074 | -0.0026 | -0.0001 | -0.0024 | +0.0049 | -0.0024 |
| lightgbm.LossHigh | +0.0064 | -0.0029 | +0.0039 | +0.0055 | +0.0074 | +0.0060 |
| pytorch.Influence | +0.0023 | -0.0105 | +0.0069 | -0.0095 | +0.0038 | +0.0086 |
| pytorch.LOO | +0.0029 | -0.0039 | -0.0047 | +0.0043 | +0.0040 | -0.0001 |
| pytorch.LissaInfluence | +0.0045 | -0.0147 | +0.0038 | -0.0189 | -0.0061 | +0.0081 |
| pytorch.LossHigh | +0.0115 | +0.0038 | +0.0157 | +0.0005 | +0.0074 | +0.0203 |
| random_forest.LOO | +0.0037 | -0.0005 | -0.0035 | -0.0011 | +0.0028 | -0.0014 |
| random_forest.LossHigh | +0.0036 | -0.0030 | +0.0020 | -0.0037 | +0.0073 | +0.0073 |
| xgboost.LOO | -0.0003 | +0.0034 | +0.0003 | -0.0029 | +0.0025 | -0.0035 |
| xgboost.LossHigh | +0.0039 | -0.0009 | +0.0069 | +0.0012 | +0.0050 | +0.0071 |


Выводы:
- **Переносится то, что детектирует шум.** Data-OOB, LossHigh любой модели и KNN-Shapley дают устойчивые плюсы почти на всех целях.
  - Сильнее всего на **XGBoost**: adult +0.06…+0.08 F1; wine +0.13…+0.16 MAE; housing +24 k $ MAE.
  - Значит, XGBoost сильнее всех страдает от шумных меток.
  - LossHigh, посчитанный на MLP (`pytorch.LossHigh`), переносится на GBDT так же хорошо, как родной LossHigh GBDT.
- **LOO любой модели** переносится плохо: |Δ| мал, знак нестабилен.
- **Influence (pytorch, distill-lightgbm)** даёт умеренный плюс в основном на XGBoost (adult +0.04, housing +7.5…8.7 k) и около нуля на остальных целях.
- **CatBoost LFC** на регрессии вне CatBoost отрицателен: housing до −3.3 k, wine до −0.02.
- **Модели-цели.** У MLP (pytorch) и CatBoost |Δ| самые малые: обе модели и без очистки устойчивы к шуму.

## 5. Время расчёта ценностей

Медиана `timing.values_s` (с) по сидам и исследованиям clean/noise*/sysnoise*/models-*/distill-*. Прогон шёл в 6 параллельных процессов × 2 потока, тяжёлые единицы Influence — не больше одной одновременно. Абсолютные значения завышены конкуренцией за CPU, но между методами сравнимы.


| метод @ модель | wine | housing | adult | covertype |
|---|---|---|---|---|
| BoostIn @ lightgbm | 0.2 | 0.9 | 0.5 | 6.6 |
| BoostIn @ lightgbm (distill-студент) | 0.2 | 0.3 | 1.4 | 7.5 |
| CatBoostLFC @ catboost | 0.0 | 0.1 | 1.6 | — |
| CatBoostLFC @ catboost (distill-студент) | — | — | 1.5 | — |
| DataOOB @ catboost | 1.0 | 1.1 | 1.5 | 1.8 |
| DataOOB @ catboost (distill-студент) | 0.8 | 1.2 | 1.4 | 1.8 |
| DataOOB @ lightgbm | 0.8 | 1.2 | 1.6 | 1.8 |
| DataOOB @ lightgbm (distill-студент) | 0.8 | 1.4 | 1.6 | 1.9 |
| DataOOB @ pytorch | 0.9 | 1.4 | 1.5 | 1.8 |
| DataOOB @ random_forest | 0.9 | 1.2 | 1.4 | 2.2 |
| DataOOB @ xgboost | 0.9 | 1.4 | 1.4 | 1.8 |
| Influence @ catboost (distill-студент) | 1.3 | 2.6 | 34.1 | 18.2 |
| Influence @ lightgbm (distill-студент) | 1.8 | 2.6 | 42.0 | 12.0 |
| Influence @ pytorch | 0.6 | 3.5 | 143 | 384 |
| KNNShapley @ catboost | — | — | 1.2 | 1.4 |
| KNNShapley @ lightgbm | — | — | 1.2 | 1.0 |
| KNNShapley @ pytorch | — | — | 1.2 | 1.1 |
| KNNShapley @ random_forest | — | — | 1.1 | 1.3 |
| KNNShapley @ xgboost | — | — | 1.2 | 1.2 |
| LOO @ catboost | 38.4 | 400 | 373 | 5180 |
| LOO @ lightgbm | 72.3 | 302 | 213 | 1701 |
| LOO @ pytorch | 211 | 837 | 1131 | 1070 |
| LOO @ random_forest | 102 | 659 | 283 | 394 |
| LOO @ xgboost | 271 | 165 | 167 | 723 |
| LissaInfluence @ catboost (distill-студент) | 0.8 | 1.1 | 1.8 | 1.6 |
| LissaInfluence @ lightgbm (distill-студент) | 0.8 | 1.5 | 2.6 | 1.7 |
| LissaInfluence @ pytorch | 0.7 | 1.4 | 7.0 | 8.9 |
| LossHigh @ catboost | 0.0 | 0.0 | 0.0 | 0.0 |
| LossHigh @ catboost (distill-студент) | 0.0 | 0.0 | 0.0 | 0.0 |
| LossHigh @ lightgbm | 0.0 | 0.0 | 0.0 | 0.0 |
| LossHigh @ lightgbm (distill-студент) | 0.0 | 0.0 | 0.0 | 0.0 |
| LossHigh @ pytorch | 0.0 | 0.0 | 0.0 | 0.0 |
| LossHigh @ random_forest | 0.0 | 0.0 | 0.0 | 0.0 |
| LossHigh @ xgboost | 0.0 | 0.0 | 0.0 | 0.0 |
| TMCShapley @ pytorch | 684 | — | — | — |


Максимальный прирост RSS за расчёт ценностей (`values_peak_rss_mb`, МБ):

| метод @ модель | wine | housing | adult | covertype |
|---|---|---|---|---|
| BoostIn @ lightgbm | 6 | 12 | 10 | 33 |
| BoostIn @ lightgbm (distill-студент) | 3 | 2 | 9 | 34 |
| CatBoostLFC @ catboost | 6 | 11 | 14 | — |
| CatBoostLFC @ catboost (distill-студент) | — | — | 10 | — |
| DataOOB @ catboost | 6 | 4 | 5 | 15 |
| DataOOB @ catboost (distill-студент) | 0 | 6 | 7 | 15 |
| DataOOB @ lightgbm | 0 | 5 | 2 | 14 |
| DataOOB @ lightgbm (distill-студент) | 6 | 9 | 5 | 4 |
| DataOOB @ pytorch | 7 | 10 | 10 | 12 |
| DataOOB @ random_forest | 1 | 5 | 4 | 11 |
| DataOOB @ xgboost | 2 | 8 | 8 | 14 |
| Influence @ catboost (distill-студент) | 3 | 81 | 563 | 271 |
| Influence @ lightgbm (distill-студент) | 83 | 67 | 572 | 252 |
| Influence @ pytorch | 30 | 73 | 2661 | 6841 |
| KNNShapley @ catboost | — | — | 19 | 27 |
| KNNShapley @ lightgbm | — | — | 11 | 10 |
| KNNShapley @ pytorch | — | — | 15 | 14 |
| KNNShapley @ random_forest | — | — | 11 | 27 |
| KNNShapley @ xgboost | — | — | 13 | 10 |
| LOO @ catboost | 32 | 8 | 11 | 62 |
| LOO @ lightgbm | 4 | 14 | 7 | 19 |
| LOO @ pytorch | 1 | 2 | 11 | 10 |
| LOO @ random_forest | 1 | 1 | 6 | 8 |
| LOO @ xgboost | 56 | 10 | 6 | 27 |
| LissaInfluence @ catboost (distill-студент) | 2 | 26 | 70 | 52 |
| LissaInfluence @ lightgbm (distill-студент) | 8 | 23 | 72 | 46 |
| LissaInfluence @ pytorch | 8 | 24 | 139 | 220 |
| LossHigh @ catboost | 0 | 0 | 0 | 2 |
| LossHigh @ catboost (distill-студент) | 0 | 0 | 0 | 0 |
| LossHigh @ lightgbm | 0 | 0 | 0 | 1 |
| LossHigh @ lightgbm (distill-студент) | 0 | 0 | 0 | 0 |
| LossHigh @ pytorch | 0 | 1 | 2 | 3 |
| LossHigh @ random_forest | 0 | 0 | 0 | 1 |
| LossHigh @ xgboost | 0 | 0 | 0 | 1 |
| TMCShapley @ pytorch | 0 | — | — | — |


Выводы:
- **LOO — самый дорогой метод.** На MLP: 1131 с на adult, 1070 с на covertype, 837 с на housing. На CatBoost covertype — 5180 с.
- **TMC-Shapley** (только wine): ~685 с.
- **DirectInfluence на MLP**: 143 с (adult) и 384 с (covertype); на covertype нужно ~7.6 ГБ RAM (см. P13).
- **Остальные методы — секунды:**
  - LiSSA: 1–9 с;
  - Data-OOB: 1–2 с;
  - KNN-Shapley: ~1 с;
  - BoostIn: 0.2–7.5 с;
  - CatBoost LFC: ≤ 1.6 с;
  - LossHigh: ~0 с.
- По соотношению цены и качества лучшие — **Data-OOB, LossHigh и KNN-Shapley** (секунды и лучшая детекция), а для систематического шума — **LiSSA**. LOO, TMC-Shapley и DirectInfluence в этой постановке дороги и не окупаются. См. `assets/13_cost_quality.png`, `assets/cost.csv`.

## 6. Пропущенные единицы (116) и аномалии

Все 116 пропусков имеют `status = skipped` с осмысленной причиной NotApplicable; упавших единиц нет.


| причина | units | исследования |
|---|---|---|
| CatBoost LossFunctionChange does not support MultiClass (covertype) | 9 | distill-catboost-noise10, models-catboost-clean, models-catboost-noise10 |
| KNN-Shapley (pyDVL) is defined for classification only | 98 | clean, models-catboost-clean, models-catboost-noise10, models-lightgbm-clean, models-lightgbm-noise10, models-random_forest-clean, models-random_forest-noise10, models-xgboost-clean, models-xgboost-noise10, noise10, noise20, noise5, sysnoise10, sysnoise20, sysnoise5 |
| distill + regression: the teacher is fit on scaled y (LFC expects raw y) | 6 | distill-catboost-noise10 |
| explicit Hessian of 786433 params needs ~19584 GB (> 9 GB limit); use LiSSA | 1 | sweep-fit_mode-overfit |
| explicit Hessian of 787457 params needs ~19635 GB (> 9 GB limit); use LiSSA | 1 | sweep-fit_mode-overfit |
| explicit Hessian of 788481 params needs ~19686 GB (> 9 GB limit); use LiSSA | 1 | sweep-fit_mode-overfit |


Сводка: 98 — KNN-Shapley на регрессии (wine/housing); 9 — CatBoost LFC на многоклассовом covertype; 6 — CatBoost LFC при distill-регрессии; 3 — явный гессиан для overfit-MLP (P ≈ 0.79M, ~19.6 ТБ; защита P13).

Кроме того, по конфигурации (`study/config.py`) не запускаются DirectInfluence на covertype вне main (noise5/20, sysnoise*, damp-mlp) и LOO/TMC-Shapley вне clean/noise10. Это не пропуски: эти единицы просто не входят в план.

**Аномалии и замечания:**
1. **[P15, см. 7.3] DirectInfluence на MLP ≈ случаен при λ по умолчанию** (AUC 0.45–0.6), а разброс ценностей огромный (std 10³–3·10⁴).
   - Причина — плохая обусловленность невыпуклого гессиана при малом λ (см. 3.1).
   - При λ = 0.1–1 детекция на классификации восстанавливается (adult 0.85–0.89, covertype 0.82–0.86), очистка — нет.
2. **[Исправлено, P14, см. 7.1] LossHigh на GBDT, covertype: было AUC < 0.5** (LightGBM 0.355, CatBoost 0.364, XGBoost 0.445). Причина — невзвешенный loss при balanced-весах классов; после исправления 0.83–0.93.
3. **[Не ошибка, P16, см. 7.2] Регрессия: все influence-методы ≈ 0.5 при случайном шуме** (Direct, LiSSA, BoostIn, CatBoost LFC). Симметричные выбросы ±3σ: первое приближение influence не определяет знак вреда, хотя по модулю выбросы видны (AUC |v| 0.85–0.91).
4. **Data-OOB одинаков во всех `models-*`/`distill-*`** (0.896/0.950/0.998/0.984). Это не ошибка: метод использует собственный бэггинг и от исследуемой модели не зависит (в transfer он помечен как `any.DataOOB`).
5. **LiSSA в main работает с большим неявным демпфированием** (`effective_damping` 3–12). Его хорошие результаты — это результаты сильно регуляризованного influence, а не точного обратного гессиана.
6. **Underfit-конфигурация sweep** вырождена (F1 0.157).
7. На чистых данных очистка любым методом бесполезна или вредна. Это соответствует литературе, но в тексте это стоит подчеркнуть.
8. Значимость: при 3–5 сидах большинство различий в Δ незначимы. Выводы по очистке опираются в основном на sysnoise и housing.


## 7. Проверка аномалий (P14–P16)

### 7.1 LossHigh на GBDT, covertype (P14) — исправлено

- **Причина.** Ошибки соответствия классов нет: метки 0..6, столбцы `predict_proba` совпадают, train accuracy по argmax 98 %.
  - Деревья обучаются с balanced-весами (∝ 1/n_c, до ×30).
  - Случайные перевороты равномерны по «другим» классам, поэтому ~80 % шумных точек попадают в редкие классы (seed 0: 124 из 150).
  - Деревья эти точки запоминают, и их невзвешенный loss ниже, чем у чистых точек мажорных классов (парадокс Симпсона).
  - Внутри каждого класса шумные точки по-прежнему имеют больший loss.
- **Исправление.** LossHigh = −(вес обучения × loss), то есть слагаемое реальной функции обучения (`study/values.training_sample_weights`).
  - Деревья с balanced: вес 1/n_c. Бинарный MLP: `pos_weight`.
  - Многоклассовый MLP, регрессия и distill-студент не меняются.
  - Тест: `tests/test_losshigh_weighting.py`. Старые результаты сохранены в `results_backup_P14/`.
- **Detection AUC до → после** (пересчитано полностью, 21.11):

| исследование | adult | covertype |
|---|---|---|
| models-lightgbm-noise10 | 0.811 → 0.889 | **0.355 → 0.826** |
| models-catboost-noise10 | 0.837 → 0.917 | **0.364 → 0.905** |
| models-xgboost-noise10 | 0.759 → 0.827 | **0.445 → 0.919** |
| models-random_forest-noise10 | 0.875 → 0.930 | 0.745 → 0.933 |
| noise5 / noise10 / noise20 (MLP) | 0.876/0.852/0.830 → 0.928/0.915/0.908 | без изменений (MLP не взвешен) |
| sysnoise5 / 10 / 20 (MLP) | 0.851/0.829/0.787 → 0.930/0.922/0.850 | без изменений |
| damp-mlp-* / damp-linear-* | 0.860 / 0.840 → 0.925 / 0.917 | без изменений |
| sweep base / batch 0 / overfit / underfit / scale 0.1 / 0.3 | 0.86/0.82/0.85/0.71/0.86/0.81 → 0.93/0.92/0.89/0.80/0.89/0.91 | — |

- **Кривые удаления и transfer не изменились — и не должны.**
  - Для классификации удаление идёт пропорционально классам: из каждого класса убираются его k % с наименьшей ценностью.
  - Вес класса постоянен внутри класса, поэтому порядок точек внутри класса и удаляемое множество те же. Пересчитанные curves совпали со старыми до знака.
  - Исправление меняет только глобальное ранжирование, то есть detection AUC.
- **Другие методы эту ошибку не разделяют.**
  - Data-OOB основан на точности собственного бэггинга (covertype 0.95).
  - BoostIn и CatBoost LFC считают градиенты по своей функции потерь пакета, KNN-Shapley не использует loss.
  - Transfer использует только сохранённые значения.

### 7.2 Регрессия при случайном шуме (P16) — не ошибка

- Знак и направление детекции корректны: `roc_auc(is_noisy, −values)` одинаково для всех методов, LossHigh на тех же данных даёт 0.99.
- Шум регрессии — выбросы ±3σ(y) со **случайным знаком**.
- Influence — первое (линейное) приближение `−∇L_valᵀ H⁻¹ ∇ℓ_i`.
  - При симметричных выбросах суммарный сдвиг модели ≈ 0, и ∇L_val в окрестности точки ≈ 0. Знак влияния выброса тогда определяется шумом.
  - Вред от выброса имеет второй порядок (∝ сдвиг²), и линейное приближение его не видит.
- **Методы выбросы видят, но не знают, вредны ли они.** AUC по модулю `|v − median v|` против AUC по знаку:

| исследование | wine Direct / LiSSA | housing Direct / LiSSA |
|---|---|---|
| noise10 | 0.849 / 0.913 (по знаку 0.52 / 0.58) | 0.904 / 0.904 (по знаку 0.54 / 0.54) |
| damp-linear-1e-4 | 0.872 / 0.881 | 0.913 / 0.914 |
| distill-lightgbm | 0.862 / 0.908, BoostIn 0.888 | 0.907 / 0.896, BoostIn 0.878 |

- **При sysnoise** сдвиг однонаправленный: модель смещается, ∇L_val ≠ 0 согласованно, и знак становится информативным (LiSSA 0.90–0.96).
- Вывод: при симметричном шуме в регрессии influence-методы по построению не различают знак вреда. Для детекции в этом случае подходят |influence| или loss-критерии.

### 7.3 DirectInfluence на MLP с большим демпфированием (P15)

- Новые исследования: `damp-mlp-0.1` (все датасеты) и `damp-mlp-1` для covertype. Методы Influence и random, сиды 0–2, исходные исследования не тронуты.
- Таблица ниже — вывод `python scripts/p15_damp_report.py`. Δ — средний выигрыш над random по сетке 5/10/20 %, «+» = лучше.

| λ | wine AUC | wine Δ | housing AUC | housing Δ | adult AUC | adult Δ | covertype AUC | covertype Δ |
|---|---|---|---|---|---|---|---|---|
| по умолчанию (noise10, сиды 0–2) | 0.532 | −0.0089 | 0.530 | +1092 | 0.524 | +0.0061 | 0.496 | −0.0048 |
| 1e-6 | 0.517 | +0.0070 | 0.521 | +1295 | 0.543 | +0.0064 | — | — |
| 1e-4 | 0.532 | −0.0089 | 0.530 | +1092 | 0.498 | +0.0016 | — | — |
| 1e-2 | 0.498 | +0.0042 | 0.505 | +815 | 0.696 | −0.0010 | — | — |
| **0.1** | 0.599 | +0.0025 | 0.546 | +1582 | **0.852** | −0.0062 | **0.818** | −0.0039 |
| **1** | 0.621 | −0.0001 | 0.538 | −505 | **0.892** | −0.0006 | **0.861** | −0.0097 |

- **Детекция на классификации восстанавливается** при λ = 0.1–1: adult 0.52 → 0.85–0.89, covertype 0.50 → 0.82–0.86. Это уровень LiSSA и KNN-Shapley, но ниже Data-OOB (0.89/0.95) и взвешенного LossHigh (0.915/0.93).
- **Регрессия не оживает** (0.54–0.62) — по причине из 7.2.
- **Очистка не улучшается:** ни один Δ не значим (paired p ≥ 0.06), на covertype он даже отрицательный.
- **Цена:** на covertype явный гессиан требует ~7.6 ГБ и ~7 мин на сид при 6×2.
- Итог: прямой influence на MLP работоспособен только при сильной регуляризации гессиана. Тогда он по сути становится задемпфированным градиентным скалярным произведением, как LiSSA, и не даёт преимуществ над дешёвыми критериями.
