# График Influence_lowest при разных параметрах регуляризации

Этот документ описывает как создать график, сравнивающий только метод `Influence_lowest` при разных параметрах регуляризации (1e-05, 1e-04, 1e-03, 1e-02).

## Функция для создания графика

### `plot_influence_lowest_by_regularization`

Находится в: `visualization/plots.py`

```python
def plot_influence_lowest_by_regularization(
    results_dict,
    n_remove_list,
    logger=None,
    title_suffix="",
    regularization_values=None
):
    """
    График MAE на валидации в зависимости от доли удалённых объектов.
    Сравнивает только метод Influence_lowest при разных параметрах регуляризации.
    
    Args:
        results_dict: Словарь {regularization_param: results_dict}
                     Например: {'1e-05': results1, '1e-04': results2, ...}
                     ИЛИ список результатов (тогда используется regularization_values)
        n_remove_list: Список процентов удаляемых образцов [10, 20, 30, ...]
        logger: Логгер для сохранения графика
        title_suffix: Дополнительный текст к заголовку
        regularization_values: Список названий параметров регуляризации для легенды
    """
```

## Стиль графика

- **Фиолетовая гамма**: Все линии используют фиолетовые цвета (как в оригинальных графиках)
- **Разные стили линий**:
  - `1e-05`: сплошная (-)
  - `1e-04`: пунктир (--)
  - `1e-03`: штрих-пунктир (-.)
  - `1e-02`: точки (:)
- **Разные маркеры**:
  - `1e-05`: круг (o)
  - `1e-04`: квадрат (s)
  - `1e-03`: треугольник (^)
  - `1e-02`: ромб (D)
- **Базовая модель**: черная пунктирная линия
- **Легенда**: в верхнем правом углу
- **Сетка**: для удобства чтения графика

## Использование

### Вариант 1: С синтетическими данными (для примера)

```bash
python scripts/plot_influence_by_regularization_example.py
```

Это создаст фиктивные данные и график. Результат сохранится в `visualization_results/`.

### Вариант 2: С реальными данными из экспериментов

```bash
python scripts/plot_influence_by_regularization.py \
    --dataset electric \
    --model-type pytorch \
    --base-dir experiment_logs
```

**Параметры**:
- `--dataset`: Название датасета (например: electric, zillow, housing)
- `--model-type`: Тип модели (по умолчанию: pytorch)
- `--base-dir`: Базовая директория с результатами экспериментов (по умолчанию: experiment_logs)
- `--output-dir`: Директория для сохранения графика (по умолчанию: base_dir)
- `--title-suffix`: Дополнительный текст к заголовку графика

### Вариант 3: В коде Python

```python
from visualization.plots import plot_influence_lowest_by_regularization
from experiments.logger import ExperimentLogger

# Подготавливаем результаты для разных регуляризаций
results_dict = {
    '1e-05': results_1e_05,  # результаты экспериментов с reg=1e-05
    '1e-04': results_1e_04,  # результаты экспериментов с reg=1e-04
    '1e-03': results_1e_03,  # результаты экспериментов с reg=1e-03
    '1e-02': results_1e_02,  # результаты экспериментов с reg=1e-02
}

n_remove_list = [10, 20, 30, 40, 50, 60, 70, 80]

# Создаём логгер (опционально)
logger = ExperimentLogger(base_dir="results")

# Рисуем график
plot_influence_lowest_by_regularization(
    results_dict,
    n_remove_list,
    logger=logger,
    title_suffix="(датасет Electric)"
)
```

## Формат результатов

Каждый результат должен быть словарём вида:

```python
results = {
    'orig': {
        'final_mae': 0.0173,
        'best_val_mae': 0.0173,
        'metric_name': 'mae',
        'metric_short_label_ru': 'MAE',
        'metric_label_ru': 'Средняя абсолютная ошибка',
    },
    'Influence_lowest_10pct': {
        'final_mae': 0.0175,
        'best_val_mae': 0.0174,
    },
    'Influence_lowest_20pct': {
        'final_mae': 0.0178,
        'best_val_mae': 0.0177,
    },
    # ... остальные процентты ...
}
```

## Запуск экспериментов с разными параметрами регуляризации

Если вы хотите создать результаты для разных параметров регуляризации:

### Способ 1: Редактирование config/settings.py

1. Откройте `config/settings.py`
2. Найдите `DATASET_INFLUENCE_PARAMS['electric']` (или другой датасет)
3. Измените значение `regularization`:

```python
'electric': {
    'regularization': 1e-05,  # Измените это значение
    ...
}
```

4. Запустите эксперимент:
```bash
python main.py
```

5. Повторите для каждого значения регуляризации (1e-05, 1e-04, 1e-03, 1e-02)

### Способ 2: Модификация конфига в script_run_time

Создайте скрипт, который запускает эксперименты с разными параметрами:

```python
from config.settings import DATASET_INFLUENCE_PARAMS
from main import main

for reg_value in [1e-05, 1e-04, 1e-03, 1e-02]:
    DATASET_INFLUENCE_PARAMS['electric']['regularization'] = reg_value
    main(dataset_name='electric')
```

## Примеры

### Пример 1: Создание графика для датасета Electric

```bash
python scripts/plot_influence_by_regularization.py \
    --dataset electric \
    --title-suffix "Dataset: Electric"
```

### Пример 2: Создание графика с синтетическими данными

Результаты будут сохранены в `visualization_results/`:

```bash
python scripts/plot_influence_by_regularization_example.py
```

## Вывод графика

График сохраняется как:
- **PNG файл**: `influence_lowest_by_regularization.png`
- **Директория логов**: указанная через `logger` или `--output-dir`

## Сравнение с оригинальными фотографиями

Ваш новый график будет содержать:
- ✓ Только **фиолетовые линии** (Influence_lowest метод)
- ✓ **Разные параметры регуляризации** (1e-05, 1e-04, 1e-03, 1e-02)
- ✓ **Точно такой же стиль** как оригинальные графики:
  - Фиолетовая цветовая гамма
  - Разные стили линий для визуального различия
  - Маркеры на каждой точке
  - Грид для удобства чтения
  - Легенда справа

## Вопросы и проблемы

### Проблема: "No results found!"

**Решение**: Убедитесь что:
1. Вы указали правильное имя датасета
2. Результаты действительно находятся в директории `experiment_logs`
3. В конфиге эксперимента указан правильный датасет

### Проблема: Не найдены результаты для Influence_lowest

**Решение**: Убедитесь что:
1. В конфиге включен метод `Influence` в `INFLUENCE_METHODS_CONFIG`
2. Эксперименты были запущены с `removal_strategies: ['lowest']`
