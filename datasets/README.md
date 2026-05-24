# Данные для экспериментов

Большие файлы **не хранятся в репозитории**. Скачайте их локально в указанные пути перед запуском `main.py` или микросервиса.

Подробнее о датасетах: [docs/DATASETS_OVERVIEW_RU.md](../docs/DATASETS_OVERVIEW_RU.md).

## Быстрый старт (без скачивания)

В репозитории уже есть небольшие табличные наборы — можно сразу запустить:

```bash
python main.py --dataset wine
python main.py --dataset housing
python main.py --dataset adult
```

## Структура каталога

```
datasets/
├── README.md                 # этот файл
├── train_2016_v2.csv         # Zillow (малый файл, в репозитории)
├── zillow_data_dictionary.xlsx
├── adult/adult.csv           # в репозитории
├── wine/WineQT.csv           # в репозитории
├── housing/housing.csv       # в репозитории
├── covertype/covtype.data    # скачать
├── electric/household_power_consumption.txt
├── imdb/IMDB Dataset.csv
├── mnist/                    # PNG или auto-download
└── cifar/cifar10/            # PNG-классы или auto-download
```

## Zillow Prize (Kaggle)

- **Источник:** [Kaggle Zillow Prize: Zillow's Home Value Prediction](https://www.kaggle.com/c/zillow-prize-1/data)
- **Нужные файлы** (положить в `datasets/`):
  - `properties_2016.csv` (~620 MB) — обязателен для полного пайплайна
  - `train_2016_v2.csv` — уже в репозитории (2 MB)
  - `sample_submission.csv` — опционален, для экспериментов не требуется

```bash
# после скачивания с Kaggle (нужен аккаунт и принятие правил соревнования)
# kaggle competitions download -c zillow-prize-1 -p datasets/
```

## Covertype (UCI)

- **Источник:** [UCI Covertype](https://archive.ics.uci.edu/ml/datasets/covertype)
- **Файл:** `datasets/covertype/covtype.data` (без заголовка, 581k строк)

## Electric (UCI)

- **Источник:** [Individual household electric power consumption](https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption)
- **Файл:** `datasets/electric/household_power_consumption.txt` (разделитель `;`, ~127 MB)

## IMDB

- **Источник:** [Kaggle IMDB Dataset of 50K Movie Reviews](https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews) или аналог
- **Файл:** `datasets/imdb/IMDB Dataset.csv`

## MNIST

- **Вариант 1:** положить PNG в `datasets/mnist/` (структура см. `config/datasets/mnist.py`)
- **Вариант 2:** при первом запуске torchvision может скачать стандартный MNIST (если настроено в loader)

## CIFAR-10

- **Источник:** [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) или torchvision
- **Путь:** `datasets/cifar/cifar10/train/<class>/` и `test/<class>/` (см. `config/datasets/cifar10.py`)

## Adult, Wine, Housing

Уже включены в репозиторий. Источники для справки:

| Датасет | Источник |
|---------|----------|
| Adult | [UCI Adult](https://archive.ics.uci.edu/ml/datasets/adult) |
| Wine | Wine Quality (Red/White) — файл `WineQT.csv` |
| Housing | California Housing (StatLib) |

## Проверка

После размещения файлов:

```bash
python -c "from config import DatasetRegistry; print(DatasetRegistry.list())"
python main.py --dataset wine
```
