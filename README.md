# Удаление «плохих» обучающих точек по их ценности (influence / data valuation)

Дипломный проект. Вопрос: если оценить вклад каждой обучающей точки (LOO, Shapley, influence functions
через [pyDVL](https://pydvl.org/)) и удалить наименее ценные, станет ли модель лучше, чем при случайном
удалении того же числа точек? И находят ли эти оценки специально испорченные метки?

Сравниваются 8 методов на 4 табличных датасетах (wine, housing, adult, covertype), 5 сидов на каждую
комбинацию: у каждого сида своё разбиение, свой испорченный поднабор и свой seed инициализации. Сравнение
со случайным удалением парное, по сидам.

> Результаты основного прогона появятся в `assets/` после `run_overnight.ps1` (графики + `summary.md`,
> `paired_stats.md`). Старые результаты в `experiment_logs/` получены до исправлений аудита (`FIXES.md`)
> и недействительны.

## Что считается

| | |
|---|---|
| Методы | LOO, TMC-Shapley (только wine), KNN-Shapley (классификация), Data-OOB, Influence (direct), Influence (LiSSA), высокий loss, random |
| Модель | MLP `pytorch/simple` с ранней остановкой по val; в sweep ещё LightGBM |
| Задача `clean` | удалить 5/10/20/30 % точек, сначала наименее ценные (и отдельно: сначала самые ценные), переобучить, метрика на holdout |
| Задача `noise10` | испортить 10 % меток (классификация: другой класс, регрессия: y ± 3σ); AUC поиска испорченных точек, доля найденных среди k % наименее ценных, кривая удаления |
| Sweep (adult, 3 сида) | доля шума 0/5/10/20 %, размер выборки ×0.1/0.3/1, демпфирование influence 1e-4…1e-1, эпохи refit в pyDVL 20/50/200, underfit/normal/overfit, MLP vs LightGBM |

## Запуск

```powershell
.venv\Scripts\python.exe -m pytest tests -q          # 23 теста, ~15 с (включая e2e-смоук на wine)
.venv\Scripts\python.exe run_study.py pilot          # ~10 мин, results/pilot (только для проверки)
powershell -ExecutionPolicy Bypass -File .\run_overnight.ps1   # основной прогон + sweep + графики, ~7 ч
.venv\Scripts\python.exe run_study.py status         # что готово / что упало
.venv\Scripts\python.exe plot_results.py             # results/ -> assets/*.png, summary.md
.venv\Scripts\python.exe paired_stats.py             # парные тесты против random -> assets/paired_stats.md
```

Прогон можно прервать и запустить снова: готовые `results/<study>/<dataset>/<method>/seed<k>/results.json`
пропускаются. Оценка времени: `run_study.py probe` (≈10 мин), затем `run_study.py estimate --n-jobs 8`.
Необязательные уведомления о ходе прогона: переменные `DIPLOMA_WEBHOOK_URL`, `DIPLOMA_WEBHOOK_KEY`,
`DIPLOMA_WEBHOOK_HEADER` (см. шапку `run_overnight.ps1`).

## Структура

```
run_study.py            CLI исследования: main | sweep | pilot | probe | estimate | status
study/                  config.py (что запускать), data.py (сплиты, шум), values.py (методы),
                        protocol.py (один сид: baseline → ценности → кривые), summary.py, notify.py, estimate.py
plot_results.py         графики (среднее + min..max по сидам, точки по сидам, парные разности)
paired_stats.py         t-test и bootstrap-ДИ разности с random
main.py                 исходный пайплайн одного эксперимента (experiment_logs/)
experiments/            runner.py (ExperimentRunner) = training.py + removal_phase.py;
                        removal_strategies.py, metrics.py, catboost_importance.py, logger.py
influence/              обёртки pyDVL: methods.py, scorers.py, utils.py
models/                 деревья, PyTorch MLP/CNN/FT-Transformer, фабрика
config/                 settings.py, datasets/<name>.py (загрузка), model_params/<name>.json (гиперпараметры)
data/, utils/, visualization/   загрузка и препроцессинг, утилиты, графики main.py
microservice/           FastAPI + Streamlit UI (необязательно: pip install -r microservice/requirements_microservice.txt)
scripts/legacy/         старые одноразовые скрипты (результаты до аудита)
```

## Ограничения

- Influence functions — линейное приближение для удаления единиц точек; на 10–30 % и на невыпуклом MLP
  это эвристика (поэтому есть sweep по демпфированию).
- KNN-Shapley в pyDVL есть только для классификации; для wine/housing он помечается как `skipped`.
- Размеры обучающих выборок 800–1500 точек: LOO/Shapley стоят O(n) переобучений.
- F1 на маленькой val-выборке — грубая utility для LOO (много одинаковых значений).

## Данные

| Имя | Тип | Источник |
|-----|-----|----------|
| `wine` | регрессия (1143) | [Wine Quality](https://www.kaggle.com/datasets/yasserh/wine-quality-dataset) |
| `housing` | регрессия (20 640) | [California Housing](https://www.kaggle.com/datasets/camnugent/california-housing-prices) |
| `adult` | бинарная классификация (32 561) | [Adult Census Income](https://www.kaggle.com/datasets/uciml/adult-census-income) |
| `covertype` | 7 классов (581 012) | [Forest Cover Type](https://archive.ics.uci.edu/dataset/31/covertype) |

Ещё поддерживаются `zillow`, `electric`, `mnist`, `imdb`, `cifar10` (main.py), см. [datasets/README.md](datasets/README.md).

## Ссылки

Koh & Liang 2017 (influence functions) · Ghorbani & Zou 2019 (Data Shapley, TMC) · Jia et al. 2019 (KNN-Shapley) ·
Kwon & Zou 2023 (Data-OOB) · Agarwal et al. 2017 (LiSSA) · [pyDVL](https://pydvl.org/) · аудит и исправления: `FIXES.md`.

MIT — см. [LICENSE](LICENSE).
