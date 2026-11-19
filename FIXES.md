# FIXES.md — исправления по аудиту (ветка `audit-fixes`)

Основание — `C:\Users\tetif\diploma_audit\AUDIT.md`. Все правки помечены в коде комментарием `[AUDIT-FIX <код>]`, их можно найти поиском по этой строке.
Старые результаты, графики и md не менялись и не пересчитывались.

## Как откатить
- **Всё сразу.** Правки лежат в ветке `audit-fixes`. Вернуться к исходному коду: `git checkout master` (на `master` ничего не коммитилось). Удалить исправления совсем: `git checkout master && git branch -D audit-fixes`.
- **Один файл.** `git checkout master -- <файл>`.
- **Резервная копия.** Полный снимок кода до правок: `C:\Users\tetif\diploma_audit\backup_before_fix.zip`.
- **Вернуть старое поведение без отката кода:**
  - `EXPERIMENT_CONFIG['retrain_aggregate'] = 'best_holdout'`;
  - `n_random_runs = 1`;
  - `valuation_epochs = 5`;
  - `removal_strategies = ['random', 'extremes']`.

## Ошибки в коде

| Код | Что было | Что сделано | Где |
|---|---|---|---|
| B1 | `sklearn.clone()`, который вызывает pyDVL перед каждым fit, пересобирал `PyTorchModelWrapper` только из `input_size/architecture/device`. В итоге получалась регрессия с MSE, архитектура и lr по умолчанию, и всего 5 эпох обучения: valuation-методы считались на почти необученной чужой модели. | `get_params()` возвращает все аргументы конструктора, `set_params()` пересобирает модель. `fit(X, y)` без `epochs` обучает с нуля `default_epochs` эпох (берётся из `EXPERIMENT_CONFIG['valuation_epochs']`, по умолчанию 200) с фиксированным `refit_seed`. `fit(..., epochs=k)` в основном цикле работает как раньше. | `models/torch_models.py:182-200, 263-283, 336-345`; `models/factory.py:133-141`; `config/settings.py:96-98` |
| B1 | Деревья (`LightGBM/XGBoost/RF/CatBoost`) при `clone()` теряли `task_type`: классификатор становился регрессором. У `DistilledModelWrapper` терялся `num_classes`. | `get_params() = {'params', 'task_type'}`, а у `DistilledModelWrapper` добавлен `num_classes`. | `models/tree_models.py:40,100-112,120,146-158,166,191-203,211,236-248`; `models/torch_models.py:563` |
| B2 | Скореры F1/accuracy делали `astype(int)` на вероятностях, поэтому всегда получалось 0. При несовпадении длин результат молча обрезался по `min_len`. Ошибки превращались в −1e6 или 0.0. MAE шёл со знаком «меньше — лучше». | Метки получаются через `pred_to_labels` (порог 0.5, argmax). При несовпадении длин бросается `ValueError`. Исключения не глотаются. MAE заменён на −MAE, так что для всех скореров «больше — лучше». | `influence/scorers.py` (весь файл) |
| B2 | Направление сортировки valuation зависело от метрики. | Ценность теперь всегда трактуется как «больше — ценнее», первыми удаляются наименьшие значения. | `experiments/runner.py:1223-1250` |
| B3 | Ошибки молча заменялись нулями, а `argsort(нулей)` строил «кривую» по исходному порядку строк. Ещё были паддинг нулями и подмена NaN медианой; `SafeModelWrapper` глотал ошибки fit/predict. | Если метод упал, он получает скоры `NaN` и запись в `InfluenceMethods.failed_methods`, а в результатах появляется `results['orig']['invalid_methods']`. Runner такие методы пропускает. `ModelUtility(catch_errors=False)`. Значения pyDVL раскладываются строго по индексам выборки. | `influence/methods.py:66,86,339-341,881,902,943,971-975`; `influence/utils.py:18-33,68,107`; `experiments/runner.py:992-999,1546-1553` |
| B4 | `SupervisedScorer(default=-1e6)`: u(∅) = −1e6, и первая точка каждой перестановки в TMC/Shapley получала вклад около 1e6. | u(∅) теперь равна качеству константного предсказателя: медиана y_train для MAE, мажоритарный класс для классификации. Маскирование «сентинелов» отключено. | `influence/scorers.py:89-108`; `influence/methods.py:322-331`; `influence/utils.py:122` |
| B5 | Регрессия: valuation считалась на немасштабированном y, а модель обучалась на стандартизованном. | `setup_methods(..., y_scaler)` и `compute_scores` переводят y в шкалу обучения. | `influence/methods.py:252-257, 686-698`; `experiments/runner.py:1533` |

## Дизайн эксперимента (на уровне конфига)

| Код | Что сделано | Где |
|---|---|---|
| M1 | Вместо выбора лучшего из `n_retrain_runs` по holdout — среднее по сидам; в history появляются `final_metric_std` и `final_metric_runs`. Holdout используется только для итоговой оценки. Early stopping, LR-scheduler и цель influence/valuation по-прежнему считаются на отдельном test (`X_test`), это и есть валидационная выборка. Старое поведение: `retrain_aggregate='best_holdout'`. | `experiments/runner.py:732-760, 820-830`; `config/settings.py:92-95` |
| M2 | `n_random_runs`: 1 → 5. | `config/settings.py:87` |
| M3 | Включены стратегии `lowest`, `highest` и `random`; `extremes` выключена. | `config/settings.py:37-45` |
| M7 | electric: из признаков убран `Global_intensity` (через него цель почти вычисляется: утечка). | `config/datasets/electric.py:28-30` |
| M7 | zillow: клиппинг logerror по квантилям всех данных до сплита убран. Теперь клиппинг идёт после сплита по квантилям только train и применяется к train и test; holdout не трогается. | `config/datasets/zillow.py:49-51,113-114`; `main.py:159-166` |

## Тесты
`tests/test_audit_fixes.py`, по одному тесту на каждую правку. Запуск:
`.venv\Scripts\python.exe -m pytest tests -q`

## Что не менялось
- Ограничения методики (M4 — influence при удалении до 90%, M5 — Hessian-influence на MLP с маленьким демпфированием, M6 — `sample_size_percentage=10`) не исправлялись: это вопросы постановки, а не багов. Подробнее в AUDIT.md.
- Микросервис и legacy-скрипты (`zillow/*`, `scripts/*`) не трогались. В `microservice/results_format.py` осталась функция `_apply_denoise`, которая сдвигает кривые методов. По умолчанию она выключена (`active: False`), но включается через API (`denoise_active`). Для честных графиков её не включать.

## B9. Гонка глобального RNG torch при параллельном переобучении (найдено в фазе графиков)

pyDVL переобучает модели в потоках (`parallel_config(backend="threading", n_jobs=N_JOBS)`), а `refit_seed` выставлялся через глобальный `torch.manual_seed`. Потоки перемешивали инициализацию и dropout друг друга, поэтому `u(D∖i)` считался на «случайной» модели: pyDVL-LOO совпадал с ручным точным LOO лишь в 25% точек (Spearman −0.11). Исправление: `models/torch_models.py` — refit с `refit_seed` выполняется под `threading.RLock` внутри `torch.random.fork_rng`, создание модели (инициализация весов тоже тратит RNG) — под тем же lock. После исправления значения utility при параллельном и последовательном расчёте совпадают точно. Тест: `test_parallel_refit_is_deterministic`.

## B10. Utility pyDVL считался на обучающей выборке (найдено в фазе графиков)

`influence/methods.py` создавал `Dataset(X_train, y_train, X_val, y_val)`, но в pyDVL 0.10 сигнатура — `Dataset(x, y, feature_names, target_names, ...)`. DataFrame `X_val` молча принимался как список имён признаков (итерация по DataFrame даёт имена колонок), поэтому `SupervisedScorer(test_data=...)` оценивал модель на ОБУЧАЮЩИХ данных. Для LOO/Shapley это означает «насколько точка помогает запомнить саму себя»: точка с перевёрнутой меткой получает положительную ценность — отсюда AUC детекции шума LOO < 0.5. Исправление: `Dataset(X_val, y_val)` как тестовые данные scorer'а и `Dataset(X_train, y_train)` для valuation. Тест: `test_valuation_scorer_uses_validation_data`.

## D1–D4. Дистилляция (ветка `refactor`)

| Код | Что было | Что сделано | Где |
|---|---|---|---|
| D1 | У XGBoost/CatBoost/RF-обёрток не было `predict_proba` (у XGBoost multiclass был `multi:softmax`): учитель отдавал жёсткие 0/1 метки, LossHigh по деревьям считался как 0/1 loss. | `predict_proba` у всех деревьев (столбец на каждый класс 0..max), `multi:softprob`; учитель даёт мягкие вероятности. | `models/tree_models.py` (D1) |
| D2 | Многоклассовые цели учителя не смягчались температурой. | Цели = softmax(log p / T), loss = KL·T². | `models/torch_models.py` (`_teacher_targets`, D2) |
| D3 | Фабрика не пробрасывала общие ключи (или пробрасывала torch-ключи в CatBoost/RF, которые их отвергают). | Общие ключи пробрасываются, torch-only ключи фильтруются для деревьев. | `models/factory.py` (D3) |
| D4 | Повторный `fit()` продолжал обучение студента с прошлых весов и состояния Adam. | Студент и оптимизатор пересоздаются на каждом `fit()`. | `models/torch_models.py` (`_build_student`, D4) |

Тесты: `tests/test_distillation.py`.

## B11–B13

| Код | Что было | Что сделано | Где |
|---|---|---|---|
| B11 | «Эпоха» MLP = один full-batch шаг Adam; с ReduceLROnPlateau и early stopping модели останавливались после ~30–50 шагов. | Настоящие мини-батч эпохи (`batch_size=128`, перемешивание), и в основном обучении, и в pyDVL-refit. `batch_size=0` = старое поведение (точка sweep). | `models/torch_models.py`, `models/factory.py`, `study/config.py` (B11) |
| B12 | Параллельные fit LightGBM из потоков joblib (pyDVL LOO, backend threading) зависали на Windows. | Fit LightGBM под глобальным `threading.Lock`. | `models/tree_models.py` (B12); тест `test_lightgbm_fits_are_serialised` |
| B13 | CatBoost `get_object_importance` > 0 означает рост loss (вредный объект), а значение брали как «полезность»: перевёрнутые метки получали высшие оценки (AUC 0.19 на adult). | Знак инвертирован: больше = полезнее (проверено по документации CatBoost). | `experiments/catboost_importance.py:117`; тест в `tests/test_extensions.py` |

## P1–P6. По аудиту использования pyDVL (`docs/PYDVL_AUDIT.md`)

| Код | Что было | Что сделано | Где |
|---|---|---|---|
| P1 | pyDVL LiSSA решает (H + (reg + scale·dampen)·I)⁻¹g. Sweep `damp-*` менял только `regularization`, а dampen оставался датасетным → λ_eff = 3…12 при любом damping ≤ 1e-2; кривые LiSSA vs damping были плоскими по построению. | В `damp-*` (`spec.damping` задан) LiSSA идёт с `dampen=0` → λ_eff = damping, как у Direct. Настройки main/sweep/ext без `damping` не изменены (scale/dampen из конфига). В results.json пишется `effective_damping` (Direct: reg; LiSSA: reg + scale·dampen) и `lissa = {scale, dampen, maxiter, implicit_damping_floor = scale/maxiter}`. Почему dampen=0, а не reg=0/dampen=damping/scale: неподвижная точка одна и та же; с dampen=0 граница сходимости по верхнему спектру шире (μ < 2·scale вместо scale·(2−d)); отрицательная кривизна при 100 итерациях растёт максимум как (1+|μ|/scale)¹⁰⁰, NaN ловится pyDVL и метод помечается failed. Проверено на игрушечной MLP: при λ=1 Spearman(LiSSA, Direct)=0.998, при 1e-2 — 0.87; при λ ≤ 1e-4 100 итераций ряда Неймана не разрешают λ < ~scale/100 (это и есть `implicit_damping_floor`), значения конечны. | `influence/methods.py` (`lissa_dampen_override`, `effective_damping`), `study/values.py` |
| P2 | `TMCShapleyValuation` создавался без `seed` → перестановки невоспроизводимы; кроме того, при n_jobs>1 число/набор перестановок, успевших завершиться до `MaxUpdates`, зависел от потоков (joblib отменял остальные). | `seed` = seed прогона; seeded TMC считается с n_jobs=1 (torch-refit и так сериализованы `_REFIT_LOCK`, лишние отменённые перестановки больше не считаются). Бюджет не менялся (10 перестановок); в results.json — `tmc = {permutations, seed, truncation}`. | `influence/methods.py`, `study/values.py`; тест `test_tmc_shapley_is_seeded_and_lissa_default_damping` |
| P3 | README подавал AUC Data-OOB/KNN-Shapley как результат «на моделях». | Явно: оба метода не зависят от модели (свой bagging-ансамбль деревьев / kNN), одинаковы во всех `models-*`; сноска на графике 8 (в графике 13 они уже показывались один раз). | `README.md`, `plot_extensions.py` |
| P4 | LiSSA перемешивает мини-батчи глобальным RNG torch без seed. | На время `fit + influence_factors` RNG фиксируется seed прогона и затем восстанавливается. | `influence/methods.py` (`compute_scores`) |
| P5 | `self.logger.log_message(...)` без проверки на None (study передаёт logger=None). | Проверка добавлена. | `influence/methods.py` (`setup_methods`) |
| P6 | Устаревший комментарий «DataOOB skipped - requires BaggingModel». | Комментарий: в main.py-пути Data-OOB не считается, в study он реализован в `study/values.py`. | `influence/methods.py` |

Не менялось (описано в аудите): batch_size DataLoader для influence берётся из глобального `PYDVL_CONFIG` (16), а не из датасетного — смена изменила бы стохастику LiSSA в main без явной необходимости; полный гессиан и малое λ у Direct на MLP (M5) — вопрос постановки (GGN/EKFAC не добавлялись); бюджет TMC 10 перестановок; influence через студента по настоящим меткам.
