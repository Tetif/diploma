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

## P7–P8. По разбору дистилляции (`docs/DISTILL_REVIEW.md`)

| Код | Что было | Что сделано | Где |
|---|---|---|---|
| P7 | В results.json только F1/accuracy при пороге 0.5 — сравнение моделей с разной калибровкой (деревья без весов против MLP с `pos_weight`) было нечестным. В `distill_diagnostics` только `teacher_metric` и `fidelity` (holdout). | `holdout_roc_auc` (бинарная; мультикласс — one-vs-rest macro) и `holdout_logloss` полной модели в `_baseline` и во всех results.json исследования/transfer (одно `predict_proba` на holdout, без переобучений). Дистилляция: `teacher_holdout_roc_auc/logloss`, `student_best_epoch`, `student_epochs_run`, `student_max_epochs`, `fidelity_train`; регрессия — `r2_student_vs_teacher` (holdout) и `_train`. Кривые удаления (переобученные модели) по-прежнему хранят только основную метрику. | `study/protocol.py` (`holdout_prob_metrics`, `distill_diagnostics`), `models/torch_models.py` (`best_epoch_`, `epochs_run_`) |
| P8 | Деревья в классификации учились без весов классов, MLP — с `pos_weight = neg/pos`: на adult F1 деревьев 0.50–0.56 против 0.63 у MLP при сопоставимом ROC-AUC; ученик дистилляции наследовал порог учителя. | `RunSpec.tree_class_weight = 'balanced'` (None — старое поведение) → `params['class_weight']='balanced'` для всех деревьев в классификации, включая учителей дистилляции и цели transfer. Веса считаются на метках каждого fit (LOO/removal-refit — по своему подмножеству): LightGBM/XGBoost бинарная — `scale_pos_weight = neg/pos`; мультикласс — в этих API нет class_weight → sample weights n/(K·n_c) (= sklearn 'balanced'); CatBoost — `auto_class_weights='Balanced'`; RF — `class_weight='balanced'`. Фактические веса полной модели — `class_weighting` в results.json, настройка — `spec.tree_class_weight`. Для регрессии ключ игнорируется. | `models/tree_models.py` (`_class_weighting`), `study/protocol.py` (`Trainer`), `study/config.py`; тесты `tests/test_class_weights.py` (в т.ч. CatBoost LFC и pyDVL LOO с весами) |

Следствие P8: пилотные результаты `models-*`, `distill-*`, `transfer-*` для adult/covertype получены без весов и с полным прогоном не сравнимы напрямую. LightGBM early stopping по val остаётся на невзвешенном logloss.

## P9–P11. Influence для GBDT через дистилляцию (`docs/GBDT_INFLUENCE_PLAN.md`)

| Код | Что было | Что сделано | Где |
|---|---|---|---|
| P9 | Influence студента считался только по настоящим (шумным) меткам, хотя студент учился на выходах учителя. | `RunSpec.distill_influence_target` ∈ {`true_labels`, `teacher`}. `teacher`: train-цели = `_teacher_targets` (цели обучения студента), loss = loss обучения студента (BCEWithLogits к p; `T²·CE(z/T, p_T)` ≡ KL·T² по градиенту; MSE к предсказанию учителя); валидация — настоящие метки. Вариант пишется в `spec` и `influence_target`. Новые исследования `distill-*-noise10-tgtteacher` (Influence, LiSSA). | `study/values.py` (`TemperedSoftCE`, `_teacher_influence_setup`), `influence/methods.py` (`train_target_override`, `criterion_override`), `study/config.py` |
| P10 | Не было BoostIn (Brophy et al., JMLR 2023) — главного прямого baseline influence для GBDT. | Метод `BoostIn` через пакет авторов `tree_influence` (из git, см. requirements.txt): прокси для `lgb.Booster` (совпадает с эталоном пакета), взвешенные train-градиенты при balanced весах, шим sklearn ≥ 1.4, расхождение парсинга → ошибка. Только LightGBM: CatBoost (`leaf_estimation_iterations=10`) и XGBoost 3 (`base_score`) пакетом не парсятся корректно → skipped. Добавлен в `models-lightgbm-*` и `distill-lightgbm-noise10`. | `experiments/boostin.py`, `study/values.py`, `study/config.py`, `tests/test_gbdt_influence.py` |
| P11 | В `distill-*` не было прямых baseline'ов на том же сплите (CatBoost LFC запрещён при distill). | В `distill-*-noise10`: `BoostIn` (учитель LightGBM), `CatBoostLFC` (учитель CatBoost; регрессия — skipped), `DataOOB`; `explained_model: teacher`. Кривые удаления distill (подтверждено): переобучается учитель на оставшихся точках + студент заново, метрика — студента. | `study/values.py`, `study/config.py` |

## P12. Параллельный прогон по процессам

| Код | Что было | Что сделано | Где |
|---|---|---|---|
| P12 | Полный прогон шёл одним процессом (~34 ч); параллелизм только внутри pyDVL (потоки LOO), остальное (кривые, обучение MLP, однопоточный seeded TMC) — на одном ядре. | `run_study.py ... --workers N` (`run_overnight.ps1 -Workers 6 -ThreadsPerWorker 2`): единица = блок (study, dataset, seed), методы LOO/TMCShapley/Influence/LissaInfluence — отдельными единицами; каждая единица вызывает обычный `run_seed` со своим подмножеством методов (baseline блока детерминированно переобучается в каждой единице). Фазы по порядку (main, sweep, ext, затем transfer), внутри фазы LPT по эвристической стоимости; spawn-пул, потоки ограничены до импорта torch (OMP/MKL/OPENBLAS, `torch.set_num_threads`, `DIPLOMA_N_JOBS`; деревья по 1 потоку), joblib внутри воркера — только threading (loky-подпроцессы раздували RAM и вешали завершение пула). Раздаёт только родитель (каждая единица ровно один раз), `results/_logs/run.lock` против второго оркестратора; новая единица стартует, только пока свободно ≥ `--min-free-mb` RAM; воркеры перезапускаются каждые 20 единиц; упавший пул пересоздаётся, незавершённые единицы повторяются один раз. `save_json`: tmp-файл с pid и повтор `os.replace` при PermissionError (Windows). Вебхук — один на завершённый блок, как раньше. `status` показывает выполняемые единицы (маркеры `results/_logs/running/`). `--workers 1` — старый последовательный цикл без изменений. Замер (16 единиц, n_train=200): 81 с последовательно → 30 с при 6×2, значения/кривые/детекция идентичны (40/40), пик RSS воркера 0.72 ГБ. | `study/parallel.py`, `run_study.py` (`_execute`, `status`), `study/io.py`, `run_overnight.ps1`, `tests/test_parallel.py` |


## P13. Память при параллельном прогоне (DirectInfluence на covertype)

| Код | Что было | Что сделано | Где |
|---|---|---|---|
| P13 | Полный прогон `-Workers 6 -ThreadsPerWorker 2` забил RAM и диск (своп): одновременно шли 5 единиц Influence covertype по ~7.5 ГБ, пул упал (05:06). Причина: pyDVL DirectInfluence строит явный гессиан P×P (MLP covertype [128, 64], P = 15751, H = 0.95 ГБ float32) через `torch.func.hessian` (jacfwd∘jacrev) по батчам + аккумулятор + копия в `torch.linalg.solve`; замер: fit 7.7 ГБ, пик не зависит от n_train, память воркер не возвращает ОС. Математику не меняли (чанкованный гессиан через vmap/jvp экономит память, но даёт расхождение ~1e-8 — не применён). | Модель памяти единицы: `unit_mem_mb` = база 1200 МБ (+300 covertype) + для Influence на torch/distill 8.5·P²·4 Б (P из конфигурации MLP). Единица стартует, только если её оценка помещается в свободную RAM за вычетом роста уже идущих единиц (оценка − текущий RSS по pid из маркера) и `--min-free-mb`; единицы ≥ 2500 МБ — «тяжёлые»: отдельный пул на `--max-heavy` (по умолчанию 1) процессов с `max_tasks_per_child=1` (память освобождается после каждой); иначе LPT как раньше (берётся первая подходящая). После падения пула очередь пересортировывается, `max_heavy` принудительно = 1. Гессиан больше 60 % RAM (например sweep overfit adult, P ≈ 0.77M → терабайты) → `NotApplicable` до построения (рекомендуется LiSSA); в `info.hessian` пишутся `n_params`, `expected_peak_mb`. `run_overnight.ps1 -MaxHeavy 1`. Тайминги (`values_s`, `curves_s`, `values_peak_rss_mb`, `total_s`) сохраняются как прежде. | `study/parallel.py`, `study/values.py`, `run_study.py` (`--max-heavy`), `run_overnight.ps1`, `tests/test_parallel.py` |

## P14–P16. Проверка аномалий полного прогона (`docs/RESULTS_SUMMARY.md`, раздел 7)

| Код | Что было | Что сделано | Где |
|---|---|---|---|
| P14 | LossHigh на GBDT, covertype: detection AUC 0.355 (LightGBM), 0.364 (CatBoost), 0.445 (XGBoost), то есть ниже случайного. Это **не ошибка соответствия классов**: метки 0..6, столбцы `predict_proba` совпадают (train accuracy по argmax 98 %, со сдвигом на 1 — 1 %). Причина — парадокс Симпсона. Модели обучаются с `tree_class_weight='balanced'` (веса ∝ 1/n_c, до ×30), а случайные перевороты равномерны по остальным классам, поэтому ~80 % шумных точек (seed 0: 124 из 150) попадают в редкие классы. Эти точки получают большой вес, деревья их запоминают, и их *невзвешенный* loss становится меньше, чем у чистых точек мажорных классов. Внутри каждого класса шумные точки по-прежнему имеют больший loss. Без весов LossHigh LightGBM даёт 0.79, XGBoost 0.94. | LossHigh ранжирует по слагаемому **взвешенной** функции обучения: `loss × w`, где `w` — веса, с которыми модель реально обучалась (`study.values.training_sample_weights`). Для деревьев с balanced это 1/n_c, у бинарного MLP — `pos_weight`; у многоклассового MLP, регрессии и distill-студента весов нет, значения не меняются. В `info.loss_weighting` пишется схема. Пересчитаны только затронутые единицы (дёшево): LossHigh для adult/covertype в clean, noise*, sysnoise*, damp-*, sweep-*, models-* (37 единиц) и transfer-* с источником `*.LossHigh` (54 единицы). Старые результаты перенесены в `results_backup_P14/`. Тест: `tests/test_losshigh_weighting.py`. Пересчёт 21.11 подтвердил: кривые удаления и transfer не изменились (удаление в классификации пропорционально классам, вес класса внутри класса постоянен), меняется только detection AUC. Другие методы эту ошибку не повторяют: Data-OOB считает точность собственного бэггинга (0.95 на covertype), BoostIn и CatBoost LFC считают градиенты по своей функции потерь пакета, transfer использует только сохранённые значения. | `study/values.py`, `tests/test_losshigh_weighting.py` |
| P15 | DirectInfluence на MLP при λ по умолчанию (1e-5…1e-4) ≈ случаен (AUC ≈ 0.5); damping sweep показал рост до 0.89 при λ = 1 (adult). | Отдельные исследования, исходные не трогаются: `damp-mlp-0.1` (все датасеты) и `damp-mlp-1` для covertype (wine/housing/adult уже были). Методы Influence и random, 3 сида: `run_study.py ext --sections damphigh` (секция опциональна и не входит в EXT_SECTIONS). Сводка: `python scripts/p15_damp_report.py`. | `study/config.py` (`damp_high_specs`), `run_study.py`, `scripts/p15_damp_report.py` |
| P16 | Регрессия при случайном шуме: все influence-методы (Direct, LiSSA, BoostIn, CatBoost LFC) ≈ 0.5, а при sysnoise LiSSA даёт 0.9+. | **Не ошибка, код не менялся.** Направление детекции корректно: `roc_auc(is_noisy, −values)` одинаково для всех методов, LossHigh на тех же данных даёт 0.99. Шум регрессии — выбросы ±3σ(y) со случайным знаком (`study/data.corrupt`), они симметричны. Influence — первое приближение `−∇L_valᵀ H⁻¹ ∇ℓ_i`: при симметричных выбросах суммарный сдвиг модели ≈ 0, градиент валидационного loss в районе точки ≈ 0, и знак влияния определяется шумом. Вред от выброса имеет второй порядок (∝ сдвиг²), и линейное приближение его не видит. Сами методы выбросы видят: AUC по модулю `|v − median(v)|` 0.85–0.91 для Direct, LiSSA и BoostIn на wine/housing (noise10, damp-linear, distill, models-lightgbm). При sysnoise сдвиг однонаправленный: модель смещается, ∇L_val ≠ 0 согласованно, и знак становится информативным. Описано в RESULTS_SUMMARY. | — |
