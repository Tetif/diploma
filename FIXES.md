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
