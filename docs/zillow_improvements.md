# Рекомендации по улучшению моделей на датасете Zillow

## Текущая ситуация

- **Целевая переменная:** `logerror` (log(Zestimate) - log(SalePrice)), диапазон примерно [-4.6, 4.7], std ≈ 0.16
- **R² всех моделей ≈ 0** — предсказания не лучше константы (среднего)
- **Данные:** ~90K строк после merge train + properties, ~58 колонок

## Выявленные проблемы

### 1. Признак `transactiondate` не используется

Дата транзакции есть в данных, но **не входит** в `numeric_columns` и `categorical_columns` конфига. `TabularPreprocessor` с `remainder='drop'` отбрасывает все колонки, не указанные в конфиге, поэтому `transactiondate` не попадает в модель.

**Важность:** logerror сильно зависит от месяца (сезонность рынка недвижимости).

### 2. Несоответствие конфига и реальных колонок

В `numeric_columns` указаны колонки, которых нет в данных:
- `garagetypeid` → в данных есть `garagecarcnt`, `garagetotalsqft`
- `structuretaxvalueyear` → есть `structuretaxvaluedollarcnt`
- `poolsizesquarefeet` → есть `poolsizesum`
- `landtaxvalueyear` → есть `landtaxvaluedollarcnt`
- `heatingcodesplit` → есть `heatingorsystemtypeid`

В итоге используется только часть доступных признаков.

### 3. Отсутствуют сильные признаки

- **structuretaxvaluedollarcnt** — оценочная стоимость, сильно связана с ценой
- **taxvaluedollarcnt** — налоговая оценка
- **calculatedfinishedsquarefeet** — площадь (часто надёжнее finishedsquarefeet12)
- **tx_month, tx_year** — производные от transactiondate

### 4. Выбросы в logerror

min ≈ -4.6, max ≈ 4.7 при std ≈ 0.16. Крайние значения искажают обучение.

### 5. Много пропусков

У многих колонок >50% пропусков. Нужна аккуратная стратегия: отбор признаков, imputation, возможно отсечение колонок с >70% пропусков.

---

## Рекомендуемые изменения

### 1. Добавить признаки из transactiondate (обязательно)

В `load_data()` после merge:
```python
df['transactiondate'] = pd.to_datetime(df['transactiondate'])
df['tx_month'] = df['transactiondate'].dt.month
df['tx_year'] = df['transactiondate'].dt.year
# Опционально: sin/cos для цикличности месяца
df['tx_month_sin'] = np.sin(2 * np.pi * df['tx_month'] / 12)
df['tx_month_cos'] = np.cos(2 * np.pi * df['tx_month'] / 12)
```

Добавить `tx_month`, `tx_year` (или `tx_month_sin`, `tx_month_cos`) в `numeric_columns`.

### 2. Обновить список признаков под реальные колонки

Использовать колонки, которые есть в данных:
- **Числовые:** latitude, longitude, bathroomcnt, bedroomcnt, buildingqualitytypeid, calculatedfinishedsquarefeet, finishedsquarefeet12, fips, fullbathcnt, garagecarcnt, garagetotalsqft, yearbuilt, numberofstories, poolcnt, roomcnt, lotsizesquarefeet, **structuretaxvaluedollarcnt**, **taxvaluedollarcnt**, **landtaxvaluedollarcnt**, tx_month, tx_year
- **Категориальные:** propertycountylandusecode, propertylandusetypeid, airconditioningtypeid, heatingorsystemtypeid

### 3. Обработка выбросов logerror

В `load_data()` или перед обучением:
```python
# Клиппинг к разумному диапазону (например, 99% перцентили)
low, high = target.quantile([0.005, 0.995])
target = target.clip(low, high)
```

### 4. Feature engineering (опционально)

- `price_per_sqft` = structuretaxvaluedollarcnt / calculatedfinishedsquarefeet (с защитой от деления на 0)
- `total_finished_sqft` = сумма всех finishedsquarefeet*
- `age` = 2016 - yearbuilt

### 5. Гиперпараметры моделей

Для Zillow в `zillow_config.py`:
- Увеличить `num_leaves` (LightGBM), `max_depth` (XGBoost) — задача сложная
- Больше `iterations` для CatBoost
- Для PyTorch: больше эпох (500+), возможно более глубокая сеть

### 6. Упрощённая задача для проверки

Если R² остаётся ~0, можно проверить предсказуемость:
- Бинарная классификация: logerror > 0 vs ≤ 0
- Или предсказание квартиля/категории logerror

---

## Реализованные изменения (в коде)

### zillow.py
1. **Признаки из transactiondate:** `tx_month`, `tx_year`, `tx_month_sin`, `tx_month_cos`
2. **Обновлены списки признаков** под реальные колонки
3. **Клиппинг выбросов logerror** по перцентилям 0.5% и 99.5%
4. **Feature engineering:** `total_finished_sqft`, `age = 2016 - yearbuilt`, `price_per_sqft`

### zillow_config.py
5. **Гиперпараметры:** num_leaves 255, max_depth 10, iterations 300, более глубокая PyTorch-сеть

### check_overfitting.py
6. **N_EPOCHS_PYTORCH_ZILLOW = 500** для PyTorch на Zillow

### Результат после всех правок (LightGBM)

| Этап | Train R² | Test R² |
|------|----------|---------|
| До | 0.14 | 0.005 |
| После базовых правок | 0.17 | 0.01 |
| После всех правок | **0.20** | **0.014** |

R² всё ещё низкий (задача сложная), но направление верное. Дальнейшие шаги: ансамбли, кросс-валидация, тюнинг.
