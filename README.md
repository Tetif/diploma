# Система сравнения методов влияния данных (influence / data valuation)

Дипломный проект: эмпирическое сравнение методов оценки важности обучающих точек ([pyDVL](https://pydvl.org/)) и анализ **кривых последовательного удаления** данных — как меняется качество модели при удалении объектов с наименьшим/наибольшим влиянием, случайно или по функции потерь.

Поддерживаются **9 датасетов** (табличные, текст, изображения), модели на деревьях и PyTorch, **дистилляция** teacher→student, адаптивное переобучение при removal, CLI и **микросервис** (FastAPI + Streamlit).

## Возможности

- Методы valuation и influence через pyDVL (LOO, Shapley-варианты, Direct/LISSA/Nyström influence и др.)
- Стратегии удаления: `lowest`, `highest`, `random`, `extremes`, комбинированные
- Режимы подгонки модели: `normal` / `underfit` / `overfit`
- Дистилляция: дерево → нейросеть для Hessian-based influence
- Веб-интерфейс и REST API для запуска экспериментов и визуализации
- Docker Compose для API и UI

## Требования

- Python 3.10+
- CUDA опционально (PyTorch)
- Зависимости: `pip install -r requirements.txt`
- Для pyDVL influence также нужны `dask[complete]` и `zarr` (уже в requirements.txt)

## Быстрый старт

```bash
git clone https://github.com/Tetif/diploma.git
cd diploma
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

Данные для экспериментов — см. [datasets/README.md](datasets/README.md). Для проверки без скачивания больших файлов:

```bash
python main.py --dataset wine
```

## Конфигурация

Основные настройки в [config/settings.py](config/settings.py):

| Параметр | Описание |
|----------|----------|
| `CURRENT_DATASET` | Датасет по умолчанию (`wine`, `adult`, `zillow`, …) |
| `MODEL_RUN_CONFIG` | Тип модели, стратегии removal |
| `INFLUENCE_METHODS_CONFIG` | Какие методы pyDVL считать |
| `EXPERIMENT_CONFIG` | Сплиты, доли удаления, эпохи |
| `DEBUG_MODE` | Подробное логирование |

CLI-переопределение датасета:

```bash
python main.py --dataset adult
```

## Датасеты

| Имя | Тип | В репозитории |
|-----|-----|---------------|
| `wine` | регрессия | да |
| `housing` | регрессия | да |
| `adult` | бинарная классификация | да |
| `zillow` | регрессия | частично (нужен `properties_2016.csv` с Kaggle) |
| `covertype` | 7 классов | скачать |
| `electric` | временной ряд | скачать |
| `mnist` | изображения | скачать / auto |
| `imdb` | текст | скачать |
| `cifar10` | изображения | скачать / auto |

Подробнее: [docs/DATASETS_OVERVIEW_RU.md](docs/DATASETS_OVERVIEW_RU.md).

## Результаты экспериментов

Артефакты сохраняются в `experiment_logs/YYYY-MM-DD/HH-MM-SS/`:

```
experiment_logs/
└── 2026-05-19/
    └── 12-27-10/
        ├── experiment_log.txt
        ├── config.json
        ├── results.pkl
        ├── experiment_summary.txt
        └── *.png
```

## Микросервис

```bash
pip install -r microservice/requirements_microservice.txt
python microservice/run_services.py
```

- API: http://localhost:8000 (OpenAPI: `/docs`)
- UI: http://localhost:8501

Подробнее: [microservice/README.md](microservice/README.md).

### Docker

```bash
docker compose up --build
```

## Структура проекта

```
├── main.py                 # CLI: полный пайплайн эксперимента
├── config/                 # settings.py, конфиги датасетов и моделей
├── data/                   # загрузка, препроцессинг, кэш
├── models/                 # деревья, PyTorch, дистилляция
├── influence/              # pyDVL, расчёт scores
├── experiments/            # ExperimentRunner, логирование
├── visualization/          # графики и CSV метрик
├── microservice/           # FastAPI + Streamlit
├── scripts/                # утилиты (removal plots, агрегация)
├── notebooks/              # EDA ноутбуки
├── docs/                   # документация (RU)
└── datasets/               # данные (см. datasets/README.md)
```

## Документация

- [Обзор датасетов](docs/DATASETS_OVERVIEW_RU.md)
- [Архитектура (диаграммы)](docs/ARCHITECTURE_DIAGRAMS_RU.md)
- [Быстрый старт микросервиса](QUICK_START_RU.md)

## Решение проблем

**FileNotFoundError при загрузке данных** — проверьте [datasets/README.md](datasets/README.md).

**ImportError (dask, zarr, distributed)**:
```bash
pip install "dask[complete]>=2023.1.0" "zarr>=3.0.0"
```

**CUDA out of memory** — уменьшите выборку в `EXPERIMENT_CONFIG` или используйте CPU (`DEVICE = 'cpu'` в settings).

## Лицензия

MIT — см. [LICENSE](LICENSE).