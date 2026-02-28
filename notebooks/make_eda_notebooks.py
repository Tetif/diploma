import json
import os
from typing import List, Dict


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NOTEBOOKS_DIR = os.path.dirname(__file__)


def make_notebook(path: str, title: str, description: str, code: str) -> None:
    """Создать простой Jupyter notebook с одной markdown и одной code-ячейкой."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

    markdown_source: List[str] = [f"# {title}\n\n", description.strip() + "\n"]
    code_source: List[str] = [line + "\n" for line in code.lstrip("\n").splitlines()]

    nb: Dict = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": markdown_source,
            },
            {
                "cell_type": "code",
                "metadata": {},
                "execution_count": None,
                "outputs": [],
                "source": code_source,
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)


adult_code = '''
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use("seaborn-v0_8")
sns.set_theme()

DATA_PATH = os.path.join("..", "datasets", "adult", "adult.csv")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

df = pd.read_csv(DATA_PATH)

print("Форма датасета:", df.shape)
display(df.head())

print("\\nТипы столбцов:")
print(df.dtypes)

print("\\nИнформация о данных:")
df.info()

print("\\nОписательная статистика числовых признаков:")
display(df.describe(include=[np.number]).T)

print("\\nОписательная статистика категориальных признаков:")
display(df.describe(include=["object", "category"]).T)

print("\\nЧисло дубликатов:", df.duplicated().sum())

missing = df.isna().sum().sort_values(ascending=False)
print("\\nПропуски по столбцам:")
display(missing[missing > 0])

target_col = "income"

if target_col in df.columns:
    print("\\nРаспределение целевой переменной:")
    display(df[target_col].value_counts())
    print("\\nДоля классов:")
    display(df[target_col].value_counts(normalize=True))

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = [c for c in df.columns if c not in numeric_cols]

sample_df = df.sample(n=min(len(df), 5000), random_state=42)

if numeric_cols:
    sample_df[numeric_cols].hist(bins=30, figsize=(16, 12))
    plt.suptitle("Распределения числовых признаков")
    plt.show()

if categorical_cols:
    for col in categorical_cols:
        plt.figure(figsize=(10, 4))
        sample_df[col].value_counts().head(20).plot(kind="bar")
        plt.title(f"Распределение категориального признака: {col}")
        plt.tight_layout()
        plt.show()

if numeric_cols:
    plt.figure(figsize=(12, 10))
    corr = sample_df[numeric_cols].corr()
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Корреляционная матрица числовых признаков")
    plt.tight_layout()
    plt.show()

if target_col in df.columns:
    for col in numeric_cols[:8]:
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=target_col, y=col, data=sample_df)
        plt.title(f"{col} vs {target_col}")
        plt.tight_layout()
        plt.show()
'''


housing_code = '''
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use("seaborn-v0_8")
sns.set_theme()

DATA_PATH = os.path.join("..", "datasets", "housing", "housing.csv")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

df = pd.read_csv(DATA_PATH)

print("Форма датасета:", df.shape)
display(df.head())

print("\\nТипы столбцов:")
print(df.dtypes)

print("\\nИнформация о данных:")
df.info()

print("\\nОписательная статистика числовых признаков:")
display(df.describe(include=[np.number]).T)

print("\\nОписательная статистика категориальных признаков:")
display(df.describe(include=["object", "category"]).T)

print("\\nЧисло дубликатов:", df.duplicated().sum())

missing = df.isna().sum().sort_values(ascending=False)
print("\\nПропуски по столбцам:")
display(missing[missing > 0])

target_col = "median_house_value"

if target_col in df.columns:
    plt.figure(figsize=(8, 4))
    sns.histplot(df[target_col], kde=True)
    plt.title("Распределение целевой переменной")
    plt.tight_layout()
    plt.show()

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = [c for c in df.columns if c not in numeric_cols]

sample_df = df.sample(n=min(len(df), 5000), random_state=42)

if numeric_cols:
    sample_df[numeric_cols].hist(bins=30, figsize=(16, 12))
    plt.suptitle("Распределения числовых признаков")
    plt.show()

if categorical_cols:
    for col in categorical_cols:
        plt.figure(figsize=(8, 4))
        sample_df[col].value_counts().plot(kind="bar")
        plt.title(f"Распределение категориального признака: {col}")
        plt.tight_layout()
        plt.show()

if numeric_cols:
    plt.figure(figsize=(12, 10))
    corr = sample_df[numeric_cols].corr()
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Корреляционная матрица числовых признаков")
    plt.tight_layout()
    plt.show()

if target_col in df.columns:
    for col in numeric_cols:
        if col == target_col:
            continue
        plt.figure(figsize=(6, 4))
        plt.scatter(sample_df[col], sample_df[target_col], alpha=0.3)
        plt.xlabel(col)
        plt.ylabel(target_col)
        plt.title(f"{col} vs {target_col}")
        plt.tight_layout()
        plt.show()
'''


wine_code = '''
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use("seaborn-v0_8")
sns.set_theme()

DATA_PATH = os.path.join("..", "datasets", "wine", "WineQT.csv")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

df = pd.read_csv(DATA_PATH)

print("Форма датасета:", df.shape)
display(df.head())

print("\\nТипы столбцов:")
print(df.dtypes)

print("\\nИнформация о данных:")
df.info()

print("\\nОписательная статистика числовых признаков:")
display(df.describe(include=[np.number]).T)

print("\\nЧисло дубликатов:", df.duplicated().sum())

missing = df.isna().sum().sort_values(ascending=False)
print("\\nПропуски по столбцам:")
display(missing[missing > 0])

target_col = "quality"

if target_col in df.columns:
    print("\\nРаспределение целевой переменной (качество):")
    display(df[target_col].value_counts().sort_index())

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

sample_df = df.sample(n=min(len(df), 5000), random_state=42)

if numeric_cols:
    sample_df[numeric_cols].hist(bins=20, figsize=(14, 10))
    plt.suptitle("Распределения числовых признаков")
    plt.show()

if target_col in numeric_cols:
    plt.figure(figsize=(8, 4))
    sns.histplot(df[target_col], kde=False, bins=range(int(df[target_col].min()), int(df[target_col].max()) + 2))
    plt.title("Распределение качества вина")
    plt.tight_layout()
    plt.show()

if numeric_cols:
    plt.figure(figsize=(12, 10))
    corr = sample_df[numeric_cols].corr()
    sns.heatmap(corr, cmap="coolwarm", center=0, annot=False)
    plt.title("Корреляционная матрица числовых признаков")
    plt.tight_layout()
    plt.show()

if target_col in df.columns:
    for col in numeric_cols:
        if col == target_col:
            continue
        plt.figure(figsize=(8, 4))
        sns.boxplot(x=target_col, y=col, data=sample_df)
        plt.title(f"{col} vs {target_col}")
        plt.tight_layout()
        plt.show()
'''


imdb_code = '''
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use("seaborn-v0_8")
sns.set_theme()

DATA_PATH = os.path.join("..", "datasets", "imdb", "IMDB Dataset.csv")

pd.set_option("display.max_colwidth", 200)

df = pd.read_csv(DATA_PATH)

print("Форма датасета:", df.shape)
display(df.head())

print("\\nТипы столбцов:")
print(df.dtypes)

print("\\nИнформация о данных:")
df.info()

print("\\nЧисло дубликатов:", df.duplicated().sum())

missing = df.isna().sum().sort_values(ascending=False)
print("\\nПропуски по столбцам:")
display(missing[missing > 0])

target_col = "sentiment"

if target_col in df.columns:
    print("\\nРаспределение целевой переменной (sentiment):")
    display(df[target_col].value_counts(normalize=True))

df["review_length"] = df["review"].astype(str).str.len()

plt.figure(figsize=(8, 4))
sns.histplot(df["review_length"], bins=50, kde=True)
plt.title("Распределение длины отзывов (символы)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 4))
sns.boxplot(x=target_col, y="review_length", data=df)
plt.title("Длина отзывов в разрезе классов sentiment")
plt.tight_layout()
plt.show()
'''


electric_code = '''
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use("seaborn-v0_8")
sns.set_theme()

DATA_PATH = os.path.join("..", "datasets", "electric", "household_power_consumption.txt")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 140)

df = pd.read_csv(
    DATA_PATH,
    sep=";",
    na_values="?",
    parse_dates={"datetime": ["Date", "Time"]},
    infer_datetime_format=True,
    low_memory=False,
)

print("Форма датасета:", df.shape)
display(df.head())

print("\\nТипы столбцов:")
print(df.dtypes)

print("\\nИнформация о данных:")
df.info()

missing = df.isna().sum().sort_values(ascending=False)
print("\\nПропуски по столбцам:")
display(missing[missing > 0])

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

print("\\nОписательная статистика числовых признаков:")
display(df[numeric_cols].describe().T)

sample_df = df.dropna().sample(n=min(len(df), 50000), random_state=42)

for col in numeric_cols:
    plt.figure(figsize=(8, 3))
    sns.lineplot(x="datetime", y=col, data=sample_df.sort_values("datetime").iloc[:5000])
    plt.title(f"Временной ряд: {col}")
    plt.tight_layout()
    plt.show()

target_col = "Global_active_power"
if target_col in df.columns:
    plt.figure(figsize=(8, 4))
    sns.histplot(df[target_col].dropna(), bins=50, kde=True)
    plt.title("Распределение Global_active_power")
    plt.tight_layout()
    plt.show()
'''


covertype_code = '''
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use("seaborn-v0_8")
sns.set_theme()

DATA_PATH = os.path.join("..", "datasets", "covertype", "covtype.data")

col_names = [f"feature_{i}" for i in range(54)] + ["target"]

df = pd.read_csv(DATA_PATH, header=None, names=col_names)

print("Форма датасета:", df.shape)
display(df.head())

print("\\nТипы столбцов:")
print(df.dtypes)

print("\\nИнформация о данных:")
df.info()

print("\\nОписательная статистика числовых признаков:")
display(df.describe().T.head(20))

target_col = "target"

if target_col in df.columns:
    print("\\nРаспределение классов целевой переменной:")
    display(df[target_col].value_counts().sort_index())
    print("\\nДоля классов:")
    display(df[target_col].value_counts(normalize=True).sort_index())

numeric_cols = [c for c in df.columns if c != target_col]

sample_df = df.sample(n=min(len(df), 10000), random_state=42)

for col in numeric_cols[:10]:
    plt.figure(figsize=(8, 3))
    sns.histplot(sample_df[col], bins=30, kde=False)
    plt.title(f"Распределение признака: {col}")
    plt.tight_layout()
    plt.show()

if target_col in df.columns:
    for col in numeric_cols[:6]:
        plt.figure(figsize=(8, 3))
        sns.boxplot(x=target_col, y=col, data=sample_df)
        plt.title(f"{col} vs {target_col}")
        plt.tight_layout()
        plt.show()
'''


zillow_code = '''
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


plt.style.use("seaborn-v0_8")
sns.set_theme()

DATA_DIR = os.path.join("..", "datasets")
TRAIN_2016_PATH = os.path.join(DATA_DIR, "train_2016_v2.csv")
TRAIN_2017_PATH = os.path.join(DATA_DIR, "train_2017.csv")
PROPS_2016_PATH = os.path.join(DATA_DIR, "properties_2016.csv")
PROPS_2017_PATH = os.path.join(DATA_DIR, "properties_2017.csv")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

train2016 = pd.read_csv(TRAIN_2016_PATH)
print("train_2016_v2:", train2016.shape)
display(train2016.head())

print("\\nИнформация train_2016_v2:")
train2016.info()

print("\\nПропуски train_2016_v2:")
display(train2016.isna().sum().sort_values(ascending=False).head(10))

target_col = "logerror"

if target_col in train2016.columns:
    plt.figure(figsize=(8, 4))
    sns.histplot(train2016[target_col], bins=100, kde=True)
    plt.title("Распределение logerror (train_2016_v2)")
    plt.tight_layout()
    plt.show()

train2016["transactiondate"] = pd.to_datetime(train2016["transactiondate"])

train2016["year_month"] = train2016["transactiondate"].dt.to_period("M")
plt.figure(figsize=(10, 4))
train2016.groupby("year_month")[target_col].mean().plot(kind="bar")
plt.title("Средний logerror по месяцам")
plt.tight_layout()
plt.show()

print("\\nЧтение подвыборки properties_2016 для EDA (чтобы не перегружать память)...")
props2016 = pd.read_csv(PROPS_2016_PATH, nrows=200000)
print("properties_2016 (sample):", props2016.shape)
display(props2016.head())

missing_props = props2016.isna().sum().sort_values(ascending=False)
print("\\nПропуски (properties_2016, sample):")
display(missing_props.head(20))

numeric_cols = props2016.select_dtypes(include=[np.number]).columns.tolist()

if numeric_cols:
    sample_props = props2016.sample(n=min(len(props2016), 20000), random_state=42)
    plt.figure(figsize=(12, 10))
    corr = sample_props[numeric_cols].corr()
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Корреляционная матрица (properties_2016, sample)")
    plt.tight_layout()
    plt.show()
'''


mnist_code = '''
import os
import struct

import matplotlib.pyplot as plt
import numpy as np


DATA_DIR = os.path.join("..", "datasets", "mnist")
IMAGES_PATH = os.path.join(DATA_DIR, "t10k-images.idx3-ubyte")


def load_mnist_images(path, max_images=1000):
    with open(path, "rb") as f:
        magic, num, rows, cols = struct.unpack(">IIII", f.read(16))
        assert magic == 2051
        num = min(num, max_images)
        buf = f.read(rows * cols * num)
        data = np.frombuffer(buf, dtype=np.uint8)
        data = data.reshape(num, rows, cols)
    return data


images = load_mnist_images(IMAGES_PATH, max_images=2000)
print("Форма массива изображений:", images.shape)

plt.figure(figsize=(6, 6))
for i in range(1, 17):
    plt.subplot(4, 4, i)
    plt.imshow(images[i - 1], cmap="gray")
    plt.axis("off")
plt.suptitle("Примеры изображений MNIST (t10k)")
plt.tight_layout()
plt.show()

mean_image = images.mean(axis=0)
plt.figure(figsize=(4, 4))
plt.imshow(mean_image, cmap="gray")
plt.title("Среднее изображение")
plt.axis("off")
plt.tight_layout()
plt.show()
'''


cifar_code = '''
import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


DATA_DIR = os.path.join("..", "datasets", "cifar", "cifar10")
TRAIN_DIR = os.path.join(DATA_DIR, "train")
TEST_DIR = os.path.join(DATA_DIR, "test")


def load_sample_images(root_dir, max_images=64):
    images = []
    labels = []
    class_names = sorted(os.listdir(root_dir))
    for cls in class_names:
        cls_dir = os.path.join(root_dir, cls)
        if not os.path.isdir(cls_dir):
            continue
        for fname in os.listdir(cls_dir):
            if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
                continue
            path = os.path.join(cls_dir, fname)
            try:
                img = Image.open(path).convert("RGB")
                images.append(np.array(img))
                labels.append(cls)
            except Exception:
                continue
            if len(images) >= max_images:
                return np.array(images), labels
    return np.array(images), labels


train_images, train_labels = load_sample_images(TRAIN_DIR, max_images=128)
print("Количество загруженных изображений (train sample):", len(train_images))

if len(train_images) > 0:
    plt.figure(figsize=(8, 8))
    for i in range(1, min(17, len(train_images) + 1)):
        plt.subplot(4, 4, i)
        plt.imshow(train_images[i - 1])
        plt.axis("off")
        plt.title(train_labels[i - 1], fontsize=8)
    plt.suptitle("Примеры изображений CIFAR-10 (train)")
    plt.tight_layout()
    plt.show()

    mean_image = train_images.mean(axis=0).astype(np.uint8)
    plt.figure(figsize=(4, 4))
    plt.imshow(mean_image)
    plt.title("Среднее изображение train")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
'''


def main() -> None:
    configs = [
        {
            "filename": "eda_adult.ipynb",
            "title": "Разведочный анализ данных: Adult Income",
            "description": (
                "Полный EDA по датасету Adult (`adult.csv`): базовая структура, пропуски, "
                "распределения признаков, анализ целевой переменной `income`, корреляции "
                "и взаимосвязи признаков с таргетом."
            ),
            "code": adult_code,
        },
        {
            "filename": "eda_housing.ipynb",
            "title": "Разведочный анализ данных: California Housing",
            "description": (
                "EDA для датасета California Housing (`housing.csv`): анализ признаков, "
                "распределения, пропуски, целевая переменная `median_house_value` и связи "
                "с остальными признаками."
            ),
            "code": housing_code,
        },
        {
            "filename": "eda_wine.ipynb",
            "title": "Разведочный анализ данных: Wine Quality",
            "description": (
                "EDA для датасета Wine Quality (`WineQT.csv`): числовые признаки химического "
                "состава, распределение и анализ целевой переменной `quality`, корреляции и "
                "важные зависимости."
            ),
            "code": wine_code,
        },
        {
            "filename": "eda_imdb.ipynb",
            "title": "Разведочный анализ данных: IMDB Reviews",
            "description": (
                "EDA для текстового датасета отзывов IMDB (`IMDB Dataset.csv`): распределение "
                "классов `sentiment`, длина текстов и базовые характеристики корпуса."
            ),
            "code": imdb_code,
        },
        {
            "filename": "eda_electric.ipynb",
            "title": "Разведочный анализ данных: Household Power Consumption",
            "description": (
                "EDA для временного ряда `household_power_consumption.txt`: базовая структура, "
                "пропуски, описательная статистика и визуализация основных временных рядов."
            ),
            "code": electric_code,
        },
        {
            "filename": "eda_covertype.ipynb",
            "title": "Разведочный анализ данных: Forest Covertype",
            "description": (
                "EDA для датасета Forest Covertype (`covtype.data`): распределения признаков, "
                "анализ классов целевой переменной и базовые зависимости признаков от таргета."
            ),
            "code": covertype_code,
        },
        {
            "filename": "eda_zillow.ipynb",
            "title": "Разведочный анализ данных: Zillow (logerror)",
            "description": (
                "EDA для соревнования Zillow: анализ `train_2016_v2.csv` и подвыборки "
                "`properties_2016.csv`, распределение `logerror`, динамика по времени и "
                "корреляции признаков недвижимости."
            ),
            "code": zillow_code,
        },
        {
            "filename": "eda_mnist.ipynb",
            "title": "Разведочный анализ данных: MNIST (изображения)",
            "description": (
                "Базовый EDA для датасета MNIST (файл `t10k-images.idx3-ubyte`): "
                "просмотр примеров изображений и усреднённого изображения."
            ),
            "code": mnist_code,
        },
        {
            "filename": "eda_cifar10.ipynb",
            "title": "Разведочный анализ данных: CIFAR-10 (изображения)",
            "description": (
                "Базовый EDA для датасета CIFAR-10 (папка `cifar/cifar10/train`): "
                "просмотр примеров изображений по классам и усреднённого изображения."
            ),
            "code": cifar_code,
        },
    ]

    for cfg in configs:
        path = os.path.join(NOTEBOOKS_DIR, cfg["filename"])
        print(f"Создаю ноутбук: {path}")
        make_notebook(
            path=path,
            title=cfg["title"],
            description=cfg["description"],
            code=cfg["code"],
        )


if __name__ == "__main__":
    main()

