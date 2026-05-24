# Отчёт: расследование influence-removal по датасетам

**Дата:** 2026-05-19  
**Протокол:** API двухфазный (A: `influence_only`, B: `POST .../removal-runs/start`)  
**Методы influence (с WM1 / ночной очереди):** `Influence` (Direct), `ArnoldiInfluence`, `LissaInfluence`, `NystroemSketchInfluence`  
Ранние прогоны **W01–Z05** — только `NystroemSketchInfluence` (недооценка; см. WM1).

---

## Executive summary

1. **«Нет эффекта» на малых/средних датасетах (wine, housing, adult)** — при 4 стратегиях removal кривые influence **не обгоняют `random`** и часто сопоставимы с **`LossHigh`**. Лучший среди influence на wine (WM1): **`Influence_extremes`** (rank 1), но **`random` всё равно rank 8 лучше** (меньше AUC по MAE = лучше).

2. **Главная техническая причина провала на zillow 100% (Nystroem):** в `experiment_logs/2026-05-19/02-01-07` / removal `02-03-53` все **NystroemSketchInfluence scores = 0** (100% zero). Removal по Nystroem ≈ произвольный порядок → «нет результатов». **Нужны Lissa / Direct Influence / Arnoldi** (ночной прогон `zillow-full-multi`).

3. **API-ловушка (H2):** без явного `removal_strategies` остаётся только **`lowest`** — сравнение с `extremes`/`random` не выполняется.

4. **Zillow 15%, Nystroem живой:** scores вариативны; на 1–10% **нет катастрофического провала** относительно baseline (дельта MAE порядка 1e-4). Резкий «провал» на графиках при 1–10% чаще у **`highest`** (удаление полезных точек), не у `extremes`. На 15% подвыборке **`LossHigh` стабильно лучше** influence.

5. **Почему zillow «в целом работает» у вас:** на **больших %** удаления (20–50%) вычищается шум; при **корректных ненулевых scores** (15% subsample) `extremes`/`lowest` дают слабый, но стабильный выигрыш vs random. На **100% + нулевой Nystroem** эффект пропадает.

6. **Деревья:** `lightgbm` + `use_distillation: true` обязателен; influence считается на **студенте PyTorch**. Без дистилляции — нет gradient-influence.

7. **Баг исправлен:** `predict_proba` для **binary** adult (файл `models/torch_models.py`) — иначе adult падал на loss-baseline.

**Ночная очередь:** `scripts/overnight_multi_method.ps1` → лог `docs/overnight_run_log.txt` (housing/adult/zillow multi + heavy).

---

## Сводная таблица прогонов

| ID | Dataset | Model | Sample% | Methods | Verdict | Лучший influence (rank) vs random |
|----|---------|-------|---------|---------|---------|-------------------------------------|
| W01 | wine | pytorch | 100 | Nystroem | WARN | Nystroem_lowest #1, random лучше |
| WM1 | wine | pytorch | 100 | **All 4** | WARN | **Influence_extremes #1**, random #8 (лучше всех) |
| H01–H02 | housing | py/lgbm | 100 | Nystroem | WARN | ≈ random |
| A01–A02 | adult | py/lgbm | 100 | Nystroem | WARN | ≈ random |
| Z01–Z02 | zillow | py/lgbm | 15 | Nystroem | WARN | LossHigh лучше influence |
| Z03–Z04 | zillow | py/lgbm | 15 | Nystroem fine 1–20% | WARN | см. раздел Zillow |
| Z05 | zillow | pytorch | 100 | Nystroem | **FAIL** | scores Nystroem **все 0** |
| X-ele-py | electric | pytorch | 10 | Inf+Lissa+Nystroem | WARN | Nystroem_lowest #1 среди inf. |

Полные логи: `docs/INFLUENCE_REMOVAL_INVESTIGATION_REPORT.md` (секции ниже) + `experiment_logs/2026-05-19/`.

---

| X-imd-py | imdb | pytorch | 10 | A+B | lowest,extremes,random | d28a4e95 | _logs\2026-05-19/03-09-59 | FAIL | Influence,ArnoldiInfluence,LissaInfluence,Nystroem |
| HM1 | housing | pytorch | 100 | A+B | lowest,highest,extremes,random | ce22914f | _logs\2026-05-19/03-12-15 | WARN | Influence,ArnoldiInfluence,LissaInfluence,Nystroem |
| X-imd-lg | imdb | lightgbm | 10 | A+B | lowest,extremes,random | 569529c0 | _logs\2026-05-19/03-25-03 | FAIL | Influence,ArnoldiInfluence,LissaInfluence,Nystroem |
| AM1 | adult | pytorch | 100 | A+B | lowest,highest,extremes,random | cc35ea60 | _logs\2026-05-19/03-26-40 | WARN | Influence,ArnoldiInfluence,LissaInfluence,Nystroem |
| ZM1 | zillow | pytorch | 15 | A+B | lowest,highest,extremes,random | 2573198b | _logs\2026-05-19/03-34-04 | FAIL | Influence,LissaInfluence,NystroemSketchInfluence |
| ZM2 | zillow | pytorch | 100 | A+B | lowest,highest,extremes,random | 8d1d8a9e | _logs\2026-05-19/03-37-42 | FAIL | Influence,LissaInfluence,NystroemSketchInfluence |
| XM-cov-lg | covertype | lightgbm | 10 | A+B | lowest,extremes,random | 74133453 | _logs\2026-05-19/07-59-16 | WARN | Influence,LissaInfluence,NystroemSketchInfluence |
| XM-ele-py | electric | pytorch | 10 | A+B | lowest,extremes,random | f57b1567 | _logs\2026-05-19/08-07-06 | WARN | Influence,LissaInfluence,NystroemSketchInfluence |
| XM-ele-lg | electric | lightgbm | 10 | A+B | lowest,extremes,random | e866a439 | _logs\2026-05-19/08-12-51 | WARN | Influence,LissaInfluence,NystroemSketchInfluence |
| XM-imd-py | imdb | pytorch | 10 | A+B | lowest,extremes,random | e64c8bb4 | _logs\2026-05-19/08-19-17 | FAIL | Influence,LissaInfluence,NystroemSketchInfluence |
| XM-imd-lg | imdb | lightgbm | 10 | A+B | lowest,extremes,random | 1d19b1c0 | _logs\2026-05-19/08-22-04 | FAIL | Influence,LissaInfluence,NystroemSketchInfluence |
| XM-mni-py | mnist | pytorch | 10 | A+B | lowest,extremes,random | 4a3ceda1 | _logs\2026-05-19/08-24-11 | FAIL | Influence,LissaInfluence,NystroemSketchInfluence |
| XM-mni-lg | mnist | lightgbm | 10 | A+B | lowest,extremes,random | dba65fd0 | _logs\2026-05-19/08-25-56 | FAIL | Influence,LissaInfluence,NystroemSketchInfluence |
| XM-cif-py | cifar10 | pytorch | 10 | A+B | lowest,extremes,random | cd6686bc | _logs\2026-05-19/08-32-59 | FAIL | Influence,LissaInfluence,NystroemSketchInfluence |
| XM-cif-lg | cifar10 | lightgbm | 10 | A+B | lowest,extremes,random | 6716c9bd | _logs\2026-05-19/08-44-28 | FAIL | Influence,LissaInfluence,NystroemSketchInfluence |
## Гипотезы

| ID | Статус | Вывод |
|----|--------|-------|
| H1 | Подтверждена | `run_mode: influence_only` без phase B → нет кривых |
| H2 | Подтверждена | API default → только `lowest`; нужен явный `removal_strategies` |
| H3 | Подтверждена | Деревья: только с `use_distillation: true` |
| H4 | Частично | На zillow 15% `highest`@10% хуже baseline сильнее, чем `extremes`; полный провал 1–10% на **100% + zero Nystroem** |
| H5 | **Критично** | zillow 100% Nystroem: std=0, все нули → removal бессмысленен |
| H6 | Возможна | `n_retrain_runs=3` даёт шум; на малых датасетах доминирует |
| H7 | Наблюдалась | Долгий covertype / reload API обрывает `experiment_id` |

---

## Сравнение методов influence (wine, WM1, все 4 метода)

Каталог: `experiment_logs/2026-05-19/02-53-21`

| Метод | std scores | Лучшая стратегия removal | AUC rank (1=лучший) |
|-------|------------|--------------------------|---------------------|
| **Influence** (Direct) | 3401 | extremes | **1** |
| NystroemSketch | 1.21e5 | lowest | 3 |
| LossHigh | 0.99 | — | 4 |
| Lissa | 7.13 | extremes | 5 |
| Arnoldi | 56.7 | extremes | 6 |
| random | — | — | **8 (лучше всех influence)** |

**Вывод:** Direct `Influence` на wine чуть лучше Nystroem/Lissa/Arnoldi, но **ни один не бьёт random**. Масштаб raw scores разный (нормализация в UI ≠ raw ranking).

---

## Zillow: поведение на 1–10% удаления

### A. Подвыборка 15% (Nystroem, fine grid Z03)

Baseline MAE ≈ 0.06356. Дельты к baseline (pytorch, Z03):

| % | extremes | lowest | highest | LossHigh |
|---|----------|--------|---------|----------|
| 1 | −0.000014 | −0.000018 | −0.000034 | −0.000143 |
| 5 | −0.000106 | +0.000013 | +0.000016 | −0.000198 |
| 10 | −0.000120 | +0.000038 | **+0.000211** | −0.000245 |

- **`extremes` на 1–10%** — слабое улучшение или нейтрально vs baseline, **не обвал**.
- **`highest` @ 10%** — заметное **ухудшение** (+0.00021 MAE): удаляются высоко-влиятельные «опорные» точки.
- **`LossHigh`** на малых % часто лучше influence.

### B. Полная выборка 100% (Z05, только Nystroem)

- Phase A: `02-01-07` — **все Nystroem scores = 0**.
- Removal `02-03-53` — кривые почти совпадают с random/LossHigh; influence не информативен.
- **Причина «работало раньше»:** другой subsample / другой метод / ненулевые scores.

### C. Почему zillow «работает» в целом

1. На **20–50%** удаления эффект очистки шума доминирует.  
2. Стратегия **`extremes`** при достаточном % выкидывает много «плохих» (min influence) вместе с частью «хороших» (max) — на больших % баланс выгоден.  
3. На **1–10%** смешение хвостов в `extremes` может давать **локальный** провал на кривой (особенно если сравнивать с точкой 0% или с `lowest`), но на наших числах 15% subsample провал **сильнее у `highest`**, не у `extremes`.  
4. **Перезапуск с Lissa + Direct Influence** (`zillow-full-multi`) обязателен для 100% данных.

---

## Рекомендации

### API / UI

```json
"selected_influence_methods": [
  "Influence",
  "ArnoldiInfluence",
  "LissaInfluence",
  "NystroemSketchInfluence"
],
"removal_strategies": ["random", "extremes", "lowest", "highest"]
```

- Не оставлять `selected_influence_methods` пустым (подтянутся LOO/TMCShapley).  
- Не полагаться на `removal_strategy` alone.  
- После influence-only — **child removal**, не полный `full` с пересчётом.  
- Для zillow 100%: проверять summary — **std=0 / 100% zero** → переключить метод или `regularization` / `nystroem rank`.

### Воспроизводимый «рабочий» прогон (zillow)

1. `sample_size_percentage: 15` для отладки, `100` для финала.  
2. Все 4 метода; сравнить rank_score в summary.  
3. `extremes` + `lowest` + `random` + `LossHigh`.  
4. Сетка %: `[1,2,3,5,7,10,15,20,30,50]` для анализа низких %.  
5. `use_distillation: true` для lightgbm/catboost.

### Скрипты

- `scripts/influence_investigation_runner.py` — команды `*-multi`, `heavy-multi`.  
- `scripts/overnight_multi_method.ps1` — ночная очередь.

---

## Детальные записи по прогонам
### XM-cif-lg — cifar10 / lightgbm / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 10:12
- **experiment_id:** `6716c9bd-e04b-46a9-91b7-93b19ef7a2fd`
- **Каталог:** `experiment_logs/2026-05-19/08-44-28`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/08-44-28 ===
Verdict: WARN

Metadata: dataset=cifar10, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.3532
  best_val_metric: 0.33555555555555555
  best_epoch: 0
  metric_name: accuracy
  metric_label_ru: Точность классификации
  status: OK

Influence methods:
  [FAIL] Influence: n=3600, std=0 | zero variance
  [OK] LissaInfluence: n=3600, std=533.1 | -
  [WARN] LossHigh: n=3600, std=1.023 | scores 100.0% one sign
  [WARN] NystroemSketchInfluence: n=3600, std=8.079e+07 | very large magnitude (check ranking only)

Removal (rank_score, higher=better):
  Influence_lowest: auc=0.17252, rank_score=0.17252
  random: auc=0.171007, rank_score=0.171007
  Influence_extremes: auc=0.16942, rank_score=0.16942
  LossHigh: auc=0.166945, rank_score=0.166945
  LissaInfluence_extremes: auc=0.16589, rank_score=0.16589
  NystroemSketchInfluence_extremes: auc=0.164415, rank_score=0.164415
  NystroemSketchInfluence_lowest: auc=0.15779, rank_score=0.15779
  LissaInfluence_lowest: auc=0.145005, rank_score=0.145005

```

</details>


### XM-cif-py — cifar10 / pytorch / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 08:37
- **experiment_id:** `cd6686bc-8823-4703-bdb0-c1878684879d`
- **Каталог:** `experiment_logs/2026-05-19/08-32-59`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/08-32-59 ===
Verdict: WARN

Metadata: dataset=cifar10, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.431
  best_val_metric: 0.4388888888888889
  best_epoch: 47
  metric_name: accuracy
  metric_label_ru: Точность классификации
  status: OK

Influence methods:
  [FAIL] Influence: n=3600, std=0 | zero variance
  [FAIL] LissaInfluence: n=3600, std=0 | zero variance
  [WARN] LossHigh: n=3600, std=0.7368 | scores 100.0% one sign
  [FAIL] NystroemSketchInfluence: n=3600, std=0 | zero variance

Removal (rank_score, higher=better):
  LossHigh: auc=0.206675, rank_score=0.206675
  random: auc=0.20663, rank_score=0.20663
  Influence_lowest: auc=0.205255, rank_score=0.205255
  LissaInfluence_lowest: auc=0.205255, rank_score=0.205255
  NystroemSketchInfluence_lowest: auc=0.205255, rank_score=0.205255
  Influence_extremes: auc=0.204735, rank_score=0.204735
  LissaInfluence_extremes: auc=0.204735, rank_score=0.204735
  NystroemSketchInfluence_extremes: auc=0.204735, rank_score=0.204735

```

</details>


### XM-mni-lg — mnist / lightgbm / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 08:30
- **experiment_id:** `dba65fd0-a08f-4a48-9da3-a58408bb2125`
- **Каталог:** `experiment_logs/2026-05-19/08-25-56`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/08-25-56 ===
Verdict: WARN

Metadata: dataset=mnist, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.8175
  best_val_metric: 0.8388888888888889
  best_epoch: 0
  metric_name: accuracy
  metric_label_ru: Точность классификации
  status: OK

Influence methods:
  [FAIL] Influence: n=1440, std=0 | zero variance
  [OK] LissaInfluence: n=1440, std=150.3 | -
  [WARN] LossHigh: n=1440, std=0.6652 | scores 99.7% one sign
  [WARN] NystroemSketchInfluence: n=1440, std=9.911e+06 | very large magnitude (check ranking only)

Removal (rank_score, higher=better):
  Influence_lowest: auc=0.410513, rank_score=0.410513
  Influence_extremes: auc=0.409425, rank_score=0.409425
  random: auc=0.390319, rank_score=0.390319
  LissaInfluence_extremes: auc=0.3683, rank_score=0.3683
  NystroemSketchInfluence_extremes: auc=0.3663, rank_score=0.3663
  NystroemSketchInfluence_lowest: auc=0.365575, rank_score=0.365575
  LissaInfluence_lowest: auc=0.3593, rank_score=0.3593
  LossHigh: auc=0.351813, rank_score=0.351813

```

</details>


### XM-mni-py — mnist / pytorch / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 08:25
- **experiment_id:** `4a3ceda1-6787-47ab-97a8-93989784261b`
- **Каталог:** `experiment_logs/2026-05-19/08-24-11`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/08-24-11 ===
Verdict: WARN

Metadata: dataset=mnist, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.8935
  best_val_metric: 0.9166666666666666
  best_epoch: 127
  metric_name: accuracy
  metric_label_ru: Точность классификации
  status: OK

Influence methods:
  [FAIL] Influence: n=1440, std=0 | zero variance
  [OK] LissaInfluence: n=1440, std=11.33 | -
  [OK] LossHigh: n=1440, std=0.006294 | -
  [OK] NystroemSketchInfluence: n=1440, std=1.655e+05 | -

Removal (rank_score, higher=better):
  Influence_extremes: auc=0.442, rank_score=0.442
  Influence_lowest: auc=0.4417, rank_score=0.4417
  random: auc=0.440756, rank_score=0.440756
  NystroemSketchInfluence_extremes: auc=0.425838, rank_score=0.425838
  LossHigh: auc=0.421625, rank_score=0.421625
  NystroemSketchInfluence_lowest: auc=0.421625, rank_score=0.421625
  LissaInfluence_extremes: auc=0.418038, rank_score=0.418038
  LissaInfluence_lowest: auc=0.3953, rank_score=0.3953

```

</details>


### XM-imd-lg — imdb / lightgbm / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 08:23
- **experiment_id:** `1d19b1c0-1070-4ee2-8869-780cb532cc76`
- **Каталог:** `experiment_logs/2026-05-19/08-22-04`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/08-22-04 ===
Verdict: WARN

Metadata: dataset=imdb, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.8124271844660195
  best_val_metric: 0.8416666666666667
  best_epoch: 0
  metric_name: f1
  metric_label_ru: F1-мера
  status: OK

Influence methods:
  [FAIL] Influence: n=1800, std=0 | zero variance
  [OK] LissaInfluence: n=1800, std=18.48 | -
  [WARN] LossHigh: n=1800, std=0.1939 | scores 100.0% one sign
  [OK] NystroemSketchInfluence: n=1800, std=3.486e+06 | -

Removal (rank_score, higher=better):
  Influence_extremes: auc=0.401355, rank_score=0.401355
  Influence_lowest: auc=0.401293, rank_score=0.401293
  random: auc=0.399944, rank_score=0.399944
  LissaInfluence_extremes: auc=0.399444, rank_score=0.399444
  NystroemSketchInfluence_extremes: auc=0.399385, rank_score=0.399385
  LossHigh: auc=0.392657, rank_score=0.392657
  LissaInfluence_lowest: auc=0.225101, rank_score=0.225101
  NystroemSketchInfluence_lowest: auc=0.22158, rank_score=0.22158

```

</details>


### XM-imd-py — imdb / pytorch / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 08:21
- **experiment_id:** `e64c8bb4-2da1-4916-9434-bb2765612edd`
- **Каталог:** `experiment_logs/2026-05-19/08-19-17`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/08-19-17 ===
Verdict: WARN

Metadata: dataset=imdb, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.8152132155205533
  best_val_metric: 0.8459958932238193
  best_epoch: 7
  metric_name: f1
  metric_label_ru: F1-мера
  status: OK

Influence methods:
  [FAIL] Influence: n=1800, std=0 | zero variance
  [OK] LissaInfluence: n=1800, std=17.15 | -
  [WARN] LossHigh: n=1800, std=0.1618 | scores 100.0% one sign
  [OK] NystroemSketchInfluence: n=1800, std=5.383e+06 | -

Removal (rank_score, higher=better):
  LossHigh: auc=0.405212, rank_score=0.405212
  Influence_extremes: auc=0.404798, rank_score=0.404798
  Influence_lowest: auc=0.404385, rank_score=0.404385
  LissaInfluence_lowest: auc=0.404187, rank_score=0.404187
  random: auc=0.403529, rank_score=0.403529
  NystroemSketchInfluence_extremes: auc=0.403096, rank_score=0.403096
  LissaInfluence_extremes: auc=0.403086, rank_score=0.403086
  NystroemSketchInfluence_lowest: auc=0.40294, rank_score=0.40294

```

</details>


### XM-ele-lg — electric / lightgbm / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 08:14
- **experiment_id:** `e866a439-2533-4567-8338-0be33042013d`
- **Каталог:** `experiment_logs/2026-05-19/08-12-51`
- **Вердикт:** WARN

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/08-12-51 ===
Verdict: WARN

Metadata: dataset=electric, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.1861220232913111
  best_val_metric: 0.18122527584628997
  best_epoch: 0
  metric_name: mae
  metric_label_ru: Средняя абсолютная ошибка
  status: OK

Influence methods:
  [OK] Influence: n=147548, std=4.158e+04 | -
  [OK] LissaInfluence: n=147548, std=1194 | -
  [WARN] LossHigh: n=147548, std=0.08863 | scores 100.0% one sign
  [WARN] NystroemSketchInfluence: n=147548, std=3.622e+08 | very large magnitude (check ranking only)

Removal (rank_score, higher=better):
  Influence_lowest: auc=0.0835781, rank_score=-0.0835781
  NystroemSketchInfluence_lowest: auc=0.0861903, rank_score=-0.0861903
  Influence_extremes: auc=0.0891007, rank_score=-0.0891007
  random: auc=0.0934967, rank_score=-0.0934967
  LissaInfluence_lowest: auc=0.0947167, rank_score=-0.0947167
  LissaInfluence_extremes: auc=0.0965224, rank_score=-0.0965224
  NystroemSketchInfluence_extremes: auc=0.0995858, rank_score=-0.0995858
  LossHigh: auc=0.108576, rank_score=-0.108576

```

</details>


### XM-ele-py — electric / pytorch / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 08:09
- **experiment_id:** `f57b1567-c6f0-4e39-bf2e-a8aec32776d7`
- **Каталог:** `experiment_logs/2026-05-19/08-07-06`
- **Вердикт:** WARN

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/08-07-06 ===
Verdict: WARN

Metadata: dataset=electric, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.12320139724966708
  best_val_metric: 0.1171778911294471
  best_epoch: 199
  metric_name: mae
  metric_label_ru: Средняя абсолютная ошибка
  status: OK

Influence methods:
  [OK] Influence: n=147548, std=4.811e+04 | -
  [OK] LissaInfluence: n=147548, std=538.1 | -
  [WARN] LossHigh: n=147548, std=0.03758 | scores 100.0% one sign
  [WARN] NystroemSketchInfluence: n=147548, std=1.169e+08 | very large magnitude (check ranking only)

Removal (rank_score, higher=better):
  NystroemSketchInfluence_lowest: auc=0.0558387, rank_score=-0.0558387
  random: auc=0.0574694, rank_score=-0.0574694
  Influence_extremes: auc=0.0578355, rank_score=-0.0578355
  Influence_lowest: auc=0.0588945, rank_score=-0.0588945
  LissaInfluence_lowest: auc=0.060227, rank_score=-0.060227
  NystroemSketchInfluence_extremes: auc=0.0635549, rank_score=-0.0635549
  LossHigh: auc=0.0667247, rank_score=-0.0667247
  LissaInfluence_extremes: auc=0.0688352, rank_score=-0.0688352

```

</details>


### XM-cov-lg — covertype / lightgbm / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 08:02
- **experiment_id:** `74133453-2330-46f2-ac6a-9cf68931d45a`
- **Каталог:** `experiment_logs/2026-05-19/07-59-16`
- **Вердикт:** WARN

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/07-59-16 ===
Verdict: WARN

Metadata: dataset=covertype, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.6537812811951396
  best_val_metric: 0.6647863084424898
  best_epoch: 0
  metric_name: accuracy
  metric_label_ru: Точность классификации
  status: OK

Influence methods:
  [WARN] Influence: n=41832, std=2.328e+06 | very large magnitude (check ranking only)
  [WARN] LissaInfluence: n=41832, std=1.259e+20 | very large magnitude (check ranking only)
  [WARN] LossHigh: n=41832, std=1.421 | scores 100.0% one sign
  [WARN] NystroemSketchInfluence: n=41832, std=3.186e+08 | very large magnitude (check ranking only)

Removal (rank_score, higher=better):
  random: auc=0.32682, rank_score=0.32682
  LissaInfluence_extremes: auc=0.32172, rank_score=0.32172
  Influence_extremes: auc=0.315439, rank_score=0.315439
  Influence_lowest: auc=0.313883, rank_score=0.313883
  NystroemSketchInfluence_lowest: auc=0.303245, rank_score=0.303245
  NystroemSketchInfluence_extremes: auc=0.287124, rank_score=0.287124
  LissaInfluence_lowest: auc=0.277884, rank_score=0.277884
  LossHigh: auc=0.258681, rank_score=0.258681

```

</details>


### XM-cov-py — covertype / pytorch / 10% / A

- **Время:** 2026-05-19 06:46
- **experiment_id:** `6df03d8a-04fe-4f0e-8b4a-8f430eb1c516`
- **Каталог:** ``
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```
FAILED phase A: {'experiment_id': '6df03d8a-04fe-4f0e-8b4a-8f430eb1c516', 'status': 'running', 'progress': 44.0, 'message': 'Computing influence scores…', 'stage': 'experiments', 'stage_index': 5, 'stages_total': 6, 'eta_seconds': None}
```

</details>


### ZM2 — zillow / pytorch / 100% / A+B (lowest,highest,extremes,random)

- **Время:** 2026-05-19 03:45
- **experiment_id:** `8d1d8a9e-3927-474b-953e-0c319b9b3e07`
- **Каталог:** `experiment_logs/2026-05-19/03-37-42`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/03-37-42 ===
Verdict: WARN

Metadata: dataset=zillow, sample_size_percentage=100.0

Model (from results.pkl orig):
  final_metric: 0.06353140366317517
  best_val_metric: 0.06213056338553573
  best_epoch: 14
  metric_name: mae
  metric_label_ru: Средняя абсолютная ошибка
  status: OK

Influence methods:
  [FAIL] Influence: n=64997, std=0 | zero variance
  [FAIL] LissaInfluence: n=64997, std=0 | zero variance
  [WARN] LossHigh: n=64997, std=3.825 | scores 100.0% one sign
  [FAIL] NystroemSketchInfluence: n=64997, std=0 | zero variance

Removal (rank_score, higher=better):
  LossHigh: auc=0.0316025, rank_score=-0.0316025
  Influence_lowest: auc=0.0317576, rank_score=-0.0317576
  LissaInfluence_lowest: auc=0.0317576, rank_score=-0.0317576
  NystroemSketchInfluence_lowest: auc=0.0317576, rank_score=-0.0317576
  Influence_extremes: auc=0.0317635, rank_score=-0.0317635
  LissaInfluence_extremes: auc=0.0317635, rank_score=-0.0317635
  NystroemSketchInfluence_extremes: auc=0.0317635, rank_score=-0.0317635
  Influence_highest: auc=0.0317817, rank_score=-0.0317817
  LissaInfluence_highest: auc=0.0317817, rank_score=-0.0317817
  NystroemSketchInfluence_highest: auc=0.0317817, rank_score=-0.0317817
  random: auc=0.0317859, rank_score=-0.0317859

```

</details>


### ZM1 — zillow / pytorch / 15% / A+B (lowest,highest,extremes,random)

- **Время:** 2026-05-19 03:36
- **experiment_id:** `2573198b-c354-4efb-aced-e063a0c9728b`
- **Каталог:** `experiment_logs/2026-05-19/03-34-04`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/03-34-04 ===
Verdict: WARN

Metadata: dataset=zillow, sample_size_percentage=15.0

Model (from results.pkl orig):
  final_metric: 0.06356119525897211
  best_val_metric: 0.06095019467300812
  best_epoch: 3
  metric_name: mae
  metric_label_ru: Средняя абсолютная ошибка
  status: OK

Influence methods:
  [FAIL] Influence: n=9749, std=0 | zero variance
  [OK] LissaInfluence: n=9749, std=54.5 | -
  [WARN] LossHigh: n=9749, std=3.788 | scores 100.0% one sign
  [OK] NystroemSketchInfluence: n=9749, std=4.059e+06 | -

Removal (rank_score, higher=better):
  LossHigh: auc=0.0316862, rank_score=-0.0316862
  LissaInfluence_extremes: auc=0.0316881, rank_score=-0.0316881
  NystroemSketchInfluence_extremes: auc=0.0317216, rank_score=-0.0317216
  random: auc=0.0317723, rank_score=-0.0317723
  Influence_highest: auc=0.0317729, rank_score=-0.0317729
  Influence_extremes: auc=0.0317748, rank_score=-0.0317748
  Influence_lowest: auc=0.0317751, rank_score=-0.0317751
  NystroemSketchInfluence_lowest: auc=0.0319849, rank_score=-0.0319849
  NystroemSketchInfluence_highest: auc=0.0323936, rank_score=-0.0323936
  LissaInfluence_lowest: auc=0.035804, rank_score=-0.035804
  LissaInfluence_highest: auc=0.0363216, rank_score=-0.0363216

```

</details>


### AM1 — adult / pytorch / 100% / A+B (lowest,highest,extremes,random)

- **Время:** 2026-05-19 03:32
- **experiment_id:** `cc35ea60-e9b8-4ae2-bdc9-94cd853c1ddb`
- **Каталог:** `experiment_logs/2026-05-19/03-26-40`
- **Вердикт:** WARN

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/03-26-40 ===
Verdict: WARN

Metadata: dataset=adult, sample_size_percentage=100.0

Model (from results.pkl orig):
  final_metric: 0.6659793814432989
  best_val_metric: 0.6766874645490641
  best_epoch: 71
  metric_name: f1
  metric_label_ru: F1-мера
  status: OK

Influence methods:
  [OK] ArnoldiInfluence: n=23443, std=969.4 | -
  [OK] Influence: n=23443, std=1.546e+04 | -
  [OK] LissaInfluence: n=23443, std=325.3 | -
  [WARN] LossHigh: n=23443, std=0.5495 | scores 100.0% one sign
  [WARN] NystroemSketchInfluence: n=23443, std=1.155e+07 | very large magnitude (check ranking only)

Removal (rank_score, higher=better):
  Influence_extremes: auc=0.33617, rank_score=0.33617
  Influence_highest: auc=0.3354, rank_score=0.3354
  Influence_lowest: auc=0.335138, rank_score=0.335138
  random: auc=0.334171, rank_score=0.334171
  NystroemSketchInfluence_extremes: auc=0.333357, rank_score=0.333357
  LossHigh: auc=0.331692, rank_score=0.331692
  ArnoldiInfluence_extremes: auc=0.32528, rank_score=0.32528
  NystroemSketchInfluence_lowest: auc=0.322706, rank_score=0.322706
  LissaInfluence_highest: auc=0.322111, rank_score=0.322111
  ArnoldiInfluence_highest: auc=0.318829, rank_score=0.318829
  NystroemSketchInfluence_highest: auc=0.312308, rank_score=0.312308
  LissaInfluence_extremes: auc=0.307853, rank_score=0.307853
  ArnoldiInfluence_lowest: auc=0.275091, rank_score=0.275091
  LissaInfluence_lowest: auc=0.259897, rank_score=0.259897

```

</details>


### X-imd-lg — imdb / lightgbm / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 03:26
- **experiment_id:** `569529c0-7481-482a-a4ad-0a858413f741`
- **Каталог:** `experiment_logs/2026-05-19/03-25-03`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/03-25-03 ===
Verdict: WARN

Metadata: dataset=imdb, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.8124271844660195
  best_val_metric: 0.8416666666666667
  best_epoch: 0
  metric_name: f1
  metric_label_ru: F1-мера
  status: OK

Influence methods:
  [OK] ArnoldiInfluence: n=1800, std=51.63 | -
  [FAIL] Influence: n=1800, std=0 | zero variance
  [OK] LissaInfluence: n=1800, std=17.16 | -
  [WARN] LossHigh: n=1800, std=0.1939 | scores 100.0% one sign
  [OK] NystroemSketchInfluence: n=1800, std=3.486e+06 | -

Removal (rank_score, higher=better):
  Influence_extremes: auc=0.401355, rank_score=0.401355
  Influence_lowest: auc=0.401293, rank_score=0.401293
  random: auc=0.399944, rank_score=0.399944
  ArnoldiInfluence_extremes: auc=0.399855, rank_score=0.399855
  NystroemSketchInfluence_extremes: auc=0.399385, rank_score=0.399385
  LissaInfluence_extremes: auc=0.39893, rank_score=0.39893
  LossHigh: auc=0.392657, rank_score=0.392657
  NystroemSketchInfluence_lowest: auc=0.22158, rank_score=0.22158
  ArnoldiInfluence_lowest: auc=0.20142, rank_score=0.20142
  LissaInfluence_lowest: auc=0.194732, rank_score=0.194732

```

</details>


### HM1 — housing / pytorch / 100% / A+B (lowest,highest,extremes,random)

- **Время:** 2026-05-19 03:15
- **experiment_id:** `ce22914f-68b1-4afa-89d4-28d86a0c8b57`
- **Каталог:** `experiment_logs/2026-05-19/03-12-15`
- **Вердикт:** WARN

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/03-12-15 ===
Verdict: WARN

Metadata: dataset=housing, sample_size_percentage=100.0

Model (from results.pkl orig):
  final_metric: 46297.757365855134
  best_val_metric: 45433.89654744685
  best_epoch: 199
  metric_name: mae
  metric_label_ru: Средняя абсолютная ошибка
  status: OK

Influence methods:
  [OK] ArnoldiInfluence: n=14860, std=344.8 | -
  [OK] Influence: n=14860, std=2.562e+04 | -
  [OK] LissaInfluence: n=14860, std=107.3 | -
  [WARN] LossHigh: n=14860, std=0.6935 | scores 100.0% one sign
  [OK] NystroemSketchInfluence: n=14860, std=1.634e+06 | -

Removal (rank_score, higher=better):
  Influence_lowest: auc=22934.9, rank_score=-22934.9
  random: auc=23154.9, rank_score=-23154.9
  ArnoldiInfluence_extremes: auc=23155.1, rank_score=-23155.1
  LissaInfluence_extremes: auc=23287.8, rank_score=-23287.8
  NystroemSketchInfluence_extremes: auc=23297.6, rank_score=-23297.6
  Influence_extremes: auc=23359.6, rank_score=-23359.6
  NystroemSketchInfluence_lowest: auc=23485.4, rank_score=-23485.4
  Influence_highest: auc=23666.6, rank_score=-23666.6
  LossHigh: auc=23728.9, rank_score=-23728.9
  ArnoldiInfluence_lowest: auc=23885.6, rank_score=-23885.6
  LissaInfluence_lowest: auc=24595.3, rank_score=-24595.3
  NystroemSketchInfluence_highest: auc=26748, rank_score=-26748
  LissaInfluence_highest: auc=27087.6, rank_score=-27087.6
  ArnoldiInfluence_highest: auc=27223.3, rank_score=-27223.3

```

</details>


### X-imd-py — imdb / pytorch / 10% / A+B (lowest,extremes,random)

- **Время:** 2026-05-19 03:12
- **experiment_id:** `d28a4e95-c037-499b-b15a-5cfd48d588ca`
- **Каталог:** `experiment_logs/2026-05-19/03-09-59`
- **Вердикт:** FAIL

<details><summary>analyze_experiment_dir.py</summary>

```

=== Experiment review: experiment_logs/2026-05-19/03-09-59 ===
Verdict: WARN

Metadata: dataset=imdb, sample_size_percentage=10.0

Model (from results.pkl orig):
  final_metric: 0.8152132155205533
  best_val_metric: 0.8459958932238193
  best_epoch: 7
  metric_name: f1
  metric_label_ru: F1-мера
  status: OK

Influence methods:
  [OK] ArnoldiInfluence: n=1800, std=26.43 | -
  [FAIL] Influence: n=1800, std=0 | zero variance
  [OK] LissaInfluence: n=1800, std=17.8 | -
  [WARN] LossHigh: n=1800, std=0.1618 | scores 100.0% one sign
  [OK] NystroemSketchInfluence: n=1800, std=5.383e+06 | -

Removal (rank_score, higher=better):
  LissaInfluence_lowest: auc=0.407885, rank_score=0.407885
  LissaInfluence_extremes: auc=0.405401, rank_score=0.405401
  LossHigh: auc=0.405212, rank_score=0.405212
  Influence_extremes: auc=0.404798, rank_score=0.404798
  Influence_lowest: auc=0.404385, rank_score=0.404385
  random: auc=0.403529, rank_score=0.403529
  ArnoldiInfluence_lowest: auc=0.403504, rank_score=0.403504
  ArnoldiInfluence_extremes: auc=0.403269, rank_score=0.403269
  NystroemSketchInfluence_extremes: auc=0.403096, rank_score=0.403096
  NystroemSketchInfluence_lowest: auc=0.40294, rank_score=0.40294

```

</details>



_(см. историю append в git / предыдущие версии файла; ключевые: WM1 `02-53-21`, Z05 `02-01-07`+`02-03-53`, Z03 `01-55-48`)_

### WM1 — wine / pytorch / 4 метода

- **Каталог:** `experiment_logs/2026-05-19/02-53-21`  
- **Вердикт:** WARN — Influence лучший среди influence, random всё ещё лучше.

---

_Отчёт дополняется по `docs/overnight_run_log.txt` после завершения ночных прогонов (housing-multi, adult-multi, zillow-multi, zillow-full-multi, heavy)._
