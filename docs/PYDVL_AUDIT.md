# Аудит использования pyDVL в дипломе (ветка `refactor`)

Дата: 19.11.2026. Режим: только чтение (никаких прогонов). Установлено: pyDVL **0.10.0**, scikit-learn 1.8.0, torch 2.5.1+cu121.
Исходники pyDVL сверялись по wheel 0.10.0 (PyPI), документация: docs/ на теге v0.10.0 и pydvl.org.

## 0. Где используется pyDVL

| Файл | Что |
|---|---|
| `influence/methods.py` | `Dataset`, `ModelUtility`, `SupervisedScorer`, `LOOValuation`, `TMCShapleyValuation` (+ Shapley/Beta/Banzhaf/LeastCore, в study не используются), `DirectInfluence`, `LissaInfluence`, `NystroemSketchInfluence`, `Arnoldi`, `Cg` |
| `study/values.py` | диспетчер методов study: LOO/TMC/Influence/LiSSA через `InfluenceMethods`; `KNNShapleyValuation`, `DataOOBValuation` напрямую |
| `influence/utils.py` | извлечение `ValuationResult` → массив по индексам |
| `synthetic_data/*.py` | синтетические эксперименты (старый код, вне study) |
| `config/settings.py` | `PYDVL_CONFIG`, `DATASET_INFLUENCE_PARAMS` |

Разбиение (study/data.py): holdout (только итоговая метрика) / train (оцениваем и удаляем) / val (early stopping + utility pyDVL). **Утечки holdout в valuation нет.**

## 1. Сверка по методам (код ↔ pyDVL 0.10.0)

### 1.1 Dataset / SupervisedScorer / ModelUtility — **корректно**
- `Dataset(x, y, feature_names=...)` — правильная сигнатура 0.10 (фикс B10 верный; старый вызов `Dataset(x_tr, y_tr, x_te, y_te)` действительно ломал смысл).
- `SupervisedScorer(scoring=callable(model,x,y), test_data=val_dataset, default=u(∅), range=None)` — по докам `scoring` может быть callable `(model, X, y) -> float`; `test_data` = val (не holdout) — правильно. Для регрессии скорер возвращает **−MAE** (больше = лучше), как требует pyDVL. `default` = качество константного предсказателя (B4) — соответствует смыслу u(∅).
  - Мелочь: `range=None` — в 0.10 ожидается кортеж `(-inf, inf)`; используется только в `compose_score`/`ClasswiseScorer`, у нас не вызывается → безвредно, но лучше убрать аргумент.
- `ModelUtility(model, scorer, catch_errors=False, clone_before_fit=True, show_warnings=True)` — правильно. `clone()` воссоздаёт `PyTorchModelWrapper` из `_ctor_params` (B1), refit с фиксированным `refit_seed` (B9) — это «common random numbers», хорошая практика для LOO.
- joblib: `parallel_config(backend="threading", n_jobs=N_JOBS)` — pyDVL 0.10 берёт параллелизм из joblib-контекста, так и надо (в доке рекомендуется loky/processes для CPU-bound sklearn; threading допустим, для torch с `_REFIT_LOCK` фактически последовательный).

### 1.2 LOO — **API корректно; метод по сути шумный (ожидаемо)**
- `LOOValuation(utility, progress=True)` = `u(N) − u(N\{i})`, больше = полезнее. Соответствует докам.
- Причины AUC≈0.5 (не баг кода): (а) utility = F1/accuracy/−MAE на val ~300–400 точек — дискретная метрика, вклад одной точки из 1500 обычно меньше шага метрики; (б) MLP при удалении одной точки получает другую последовательность мини-батчей (`randperm(n)` при другом n) → разница u(N)−u(N\i) доминируется шумом SGD, даже при одинаковом seed. В литературе LOO для нейросетей и для детекции шума ≈ random (Ghorbani & Zou 2019; Kwon & Zou 2023, табл. детекции; Jiang et al. 2023 OpenDataVal). 

### 1.3 TMC-Shapley — **API корректно, но 2 проблемы постановки**
- `TMCShapleyValuation(utility, is_done=MaxUpdates(n), progress=True)`: truncation по умолчанию `RelativeTruncation(rtol=0.01, burn_in_fraction=0.4)`; `MaxUpdates(n)` для permutation sampler = число перестановок (по докстрингу 0.10).
- (важно) **`seed` не передаётся** → `PermutationSampler(seed=None)`: значения TMC невоспроизводимы между запусками, хотя всё остальное засеяно. Фикс: `TMCShapleyValuation(..., seed=seed)` (пробросить seed study).
- (важно, методика) **10 перестановок** — крайне мало. Ghorbani & Zou 2019 используют критерий сходимости (средн. изменение <5%), на практике сотни–тысячи перестановок; дефолт pyDVL — `HistoryDeviation(n_steps=100, rtol=0.05)`. При 10 перестановках дисперсия оценки сопоставима с самим значением; плюс `RelativeTruncation(rtol=1%)` на шумной MLP-utility срабатывает случайно. Вывод «TMC слабый» надо формулировать как «TMC при бюджете 10 перестановок», либо добавить `HistoryDeviation | MaxUpdates(...)` и показать сходимость (pyDVL умеет сохранять `result.counts`/`variances`).

### 1.4 KNN-Shapley — **корректно**
- `KNNShapleyValuation(KNeighborsClassifier(k), test_data=Dataset(Xval, yval), progress=False)`, `fit(Dataset(Xtr, ytr))` — точная формула Jia et al. 2019, как в доке. k=5 (в статье/OpenDataVal обычно k=5…10).
- Значения не зависят от обучаемой модели (MLP/деревья) — **по построению**, в отчётах «по моделям» это нужно явно оговаривать.
- Использует признаки после препроцессора (OHE+скейлинг) — нормально; для регрессии не определён (корректно пропускается).

### 1.5 Data-OOB — **API корректно; «одинаковые значения на всех деревьях» — это не баг, а свойство нашей реализации**
- Код (`study/values.py:118-135`): строится **собственный** `BaggingClassifier(DecisionTreeClassifier(), n_estimators=200, random_state=seed)` (регрессия: `BaggingRegressor(DecisionTreeRegressor(min_samples_leaf=3))` на стандартизованном y), `bag.fit(Xtr, y)`, затем `DataOOBValuation(bag).fit(Dataset(Xtr, y))`.
- По исходникам pyDVL 0.10 (`methods/data_oob.py`): модель должна быть **уже обученной** bagging-моделью (`check_is_fitted`); для `Bagging*` OOB-индексы берутся из `estimators_samples_`, оценка — `point_wise_accuracy` (классификация) или `−(y−ŷ)²` (регрессия), значение точки = среднее по деревьям, где она OOB. Наш вызов полностью соответствует доке и туториалу pyDVL «Data-OOB» и статье Kwon & Zou 2023 (там тоже bagging decision trees, B=800; у нас 200 — нормально, точка OOB в ~74 деревьях).
- **Почему значения совпадают для LightGBM/XGBoost/CatBoost/RF/MLP**: пакет ни разу не смотрит на `model` — входы `(Xtr, y_train, seed)` одинаковы во всех исследованиях `models-*` (тот же `make_split`), значит values.npy и detection AUC **бит-в-бит одинаковы**. Различаются только кривые удаления (их переобучают на целевой модели). Это корректно как «модель-агностичный бейзлайн» (так он и используется в OpenDataVal), но:
  - (важно, интерпретация) в таблицах/графиках «по моделям» AUC Data-OOB (и KNN-Shapley) нельзя подавать как результат «для LightGBM/CatBoost…»; надо одну строку «model-agnostic» или сноску. В `README.md:39` формулировка «Data-OOB… AUC 0.86–0.99 почти на всех моделях» вводит в заблуждение — это один и тот же расчёт.
  - Если нужна «модельно-специфичная» версия: для `random_forest` можно передать в `DataOOBValuation` **саму обученную RF** (pyDVL поддерживает RandomForest через `_generate_unsampled_indices`; нужен `bootstrap=True`). Для бустингов OOB в смысле Kwon & Zou не определён (LightGBM `bagging_fraction` — подвыборка без возвращения на итерацию, не независимые модели).
  - Мелочь: `n_jobs=S.N_JOBS` внутри bagging + `random_state=seed` — детерминировано, ок. Дублирование `bag.fit` не нужно убирать: pyDVL требует обученную модель.
- Близость Data-OOB и LossHigh по качеству объяснима: оба по сути «ошибка модели на точке»; Data-OOB — out-of-sample (честнее), LossHigh — in-sample.

### 1.6 Influence (DirectInfluence) — **API и знак корректны; проблема — демпфирование на MLP**
- Использование: `DirectInfluence(nn_module, criterion, regularization=λ).fit(DataLoader(train))` → `influence_factors(X_val, y_val)` (= H⁻¹∇ℓ_val) → `influences_from_factors(zf, X_train, y_train, mode=InfluenceMode.Up)` батчами по val → **сумма по val-точкам**. Это ровно схема из доки pyDVL («influence_factors + influences_from_factors» для экономии памяти).
- **Знак**: по докам 0.10 `I_up(z, z_test) = ∇ℓ(z_test)ᵀ H⁻¹ ∇ℓ(z)` (минус уже учтён), «large positive influence → точка улучшает модель на z_test». В исходнике `influences_from_factors` = `zf @ ∇ℓ(train)ᵀ`. Значит «больше = полезнее», и сумма по val = влияние на суммарный val-loss. Наше соглашение (`lowest` = вредные) **корректно**.
- Hessian: `hessian()` усредняет по батчам с весом размера батча (`/= n_samples`) → H эмпирического среднего loss, согласовано с `criterion(reduction='mean')`. Критерий берётся из самой модели (`BCEWithLogitsLoss(pos_weight)`, `CrossEntropyLoss`, `MSELoss`) — то, на чём модель обучалась. y для регрессии в шкале обучения (B5). `model.eval()` выключает dropout/BN. Всё правильно.
- **(важно) λ = 1e-6…1e-4 на MLP** (`config/settings.py` DATASET_INFLUENCE_PARAMS, это и есть M5). Точка после early stopping — не минимум, Hessian MLP неопределён (отрицательные/нулевые собств. значения). `torch.linalg.solve(H+λI)` с крошечным λ даёт решение, доминируемое направлениями с |μ|≈λ → значения огромные по модулю и почти случайные по рангу. Это ровно сценарий Basu et al. 2021 («fragile») и Bae et al. 2022. В доке pyDVL прямо сказано, что H+λI с малым λ — «simplest», а для неконвергентных моделей нужны другие приближения. Рекомендации: (1) `second_order_mode=SecondOrderMode.GAUSS_NEWTON` (GGN/Fisher, PSD — есть в 0.10 у Direct/CG/LiSSA/Arnoldi/Nyström); (2) λ относительно спектра, напр. λ = 0.01–0.1·mean(diag H) или подбирать по корреляции с реальным LOO на маленьком подмножестве; (3) EKFAC (`EkfacInfluence`, есть в 0.10).
- AdamW `weight_decay=1e-4` (`models/torch_models.py`) → обученная θ минимизирует loss + wd‖θ‖²/2, а Hessian считается без этого члена; λ ≥ 1e-4 частично компенсирует, λ=1e-6 — нет. Мелочь, но для «convex sanity check» (logreg) логично ставить λ ≈ weight_decay.
- Мелочь: `DataLoader(batch_size=PYDVL_CONFIG['influence_params']['batch_size'])` (`influence/methods.py:731`) берёт **глобальный** batch_size=16, а не датасетный (8/32/64 в DATASET_INFLUENCE_PARAMS). На Direct не влияет (H усредняется), на LiSSA влияет (размер стохастического батча HVP).

### 1.7 LiSSA — **работает, но фактически это «сильно задемпфированный» influence, а не другой алгоритм**
- `LissaInfluence(model, loss, scale=s, dampen=d, regularization=λ, rtol=0.1, maxiter=100)`.
- По исходнику 0.10 (`operator.py: LissaOperator._lissa_step`): `h ← g + (1−d)h − (H+λ)h/s`, результат `h/s`. Неподвижная точка: **h/s = (H + (λ + s·d)·I)⁻¹ g**. То есть эффективное демпфирование **λ_eff = λ + s·d**:
  | датасет | s | d | λ | λ_eff |
  |---|---|---|---|---|
  | wine | 30 | 0.4 | 1e-4 | **12** |
  | housing | 25 | 0.3 | 1e-4 | **7.5** |
  | adult | 15 | 0.2 | 1e-5 | **3** |
  | covertype | 15 | 0.2 | 1e-5 | **3** |
- **Проверено игрушечным примером** в `.venv` (MLP 5-8-1, 200 точек, 2 с CPU): Spearman(LiSSA(s=15,d=0.2,λ=1e-5), Direct(λ=1e-5)) = **0.33**, Spearman(LiSSA, Direct(λ=3.0)) = **1.00**. LiSSA ≡ DirectInfluence с λ=3.
- При λ_eff ≫ спектра H: `(H+λ_eff I)⁻¹ ≈ I/λ_eff` → LiSSA ≈ скалярное произведение градиентов ∇ℓ_valᵀ∇ℓ_train (как TracIn/GradDot, Pruthi et al. 2020). Отсюда «LiSSA стабильнее Direct» и «LiSSA лучше при систематическом шуме» — **это эффект демпфирования, а не алгоритма LiSSA**. В дипломе надо так и интерпретировать (или переименовать метод в «Influence, λ_eff=…»).
- **(важно) Damping-sweep (`DAMPINGS = [1e-6, 1e-4, 1e-2, 1]`, `study/values.py:_overrides`)** меняет только `regularization`; у LiSSA это λ в λ+s·d → для 1e-6…1e-2 LiSSA практически не меняется (λ_eff ≈ 3–12), реально отличается только точка λ=1. Кривые «LiSSA vs damping» будут плоскими не потому, что LiSSA робастен, а потому что ручка не та. Фикс: в sweep для LiSSA выставлять `dampen=0` и варьировать λ, либо варьировать `d` так, чтобы λ_eff = damping; и подписывать на графиках λ_eff.
- `rtol=0.1` по **max** поэлементной относительной невязке почти никогда не достигается (элементы h≈0 → деление) → всегда 100 итераций; со сжатием (1−d) это ≈ сходимость (0.8¹⁰⁰≈2e-10), так что точность нормальная. Предупреждение «Reached max number of iterations… nan %» — косметика.
- (мелочь) LiSSA перемешивает батчи `DataLoader(shuffle=True)` без seed → значения слегка невоспроизводимы.
- Литература: в LiSSA (Agarwal et al. 2017) и в реализации Koh & Liang 2017 scale/damping нужны только для сходимости ряда Неймана; типичные значения damping ~0.01 (λ_eff = scale·damping порядка 0.1–0.25) и тысячи итераций. Наши d=0.1–0.4 дают λ_eff в 10–50 раз больше.

### 1.8 Nyström / Arnoldi / CG
- Создаются в `setup_methods`, но **в study не используются** (только `Influence`, `LissaInfluence`). API вызовов (`rank`, `regularization`, `eigen_computation_on_gpu=False`, `maxiter`, `rtol`) соответствует 0.10. Для Nyström/Arnoldi с rank 8–20 на MLP тоже стоит GGN-режим (Arnoldi в доке устойчив к неопределённости, Nyström — нет: ему нужна PSD матрица → `second_order_mode=GAUSS_NEWTON`). Если в тексте диплома упоминается Nyström как метод сравнения — результатов по нему в study нет.

### 1.9 Influence через дистиллированного студента — **концептуальная оговорка**
- Студент (`DistilledModelWrapper.fit`) учится на **мягких предсказаниях учителя**, а не на y. Influence считается с `criterion(student(x), y_true)`. θ_student не минимизирует этот loss → предпосылка Koh & Liang (∇L(θ̂)=0, H — Гессиан того же объектива) не выполняется; удаление точки влияет на студента только через учителя. Это не баг кода, но метод измеряет «согласие градиента на настоящей метке», а не влияние точки на модель. Для многокласса критерий CE, а студент учился на KL/T² — ещё одно расхождение. В дипломе надо оговорить; корректнее — считать влияние на студенте с loss по teacher-targets (влияние на «дистилляционный» объектив) либо LossHigh на студенте.

### 1.10 High-loss baseline (`LossHigh`) — **корректно**
- `values = −loss_i` на обученной полной модели (`experiments/metrics.py:compute_per_sample_loss`): CE `−log p(y_i)` по `predict_proba` (бинарный MLP: sigmoid логита; мультикласс: softmax), регрессия `(y_scaled − ŷ)²`; StandardScaler заново фитится на тех же y_train, что и в `train_and_evaluate` → та же шкала. «lowest first» = высокий loss первым — правильно.
- Это in-sample loss: MLP с early stopping не успевает запомнить шум → работает отлично (известный эффект «small-loss trick», Arpit et al. 2017, Han et al. 2018 Co-teaching). На деревьях с глубокими листьями (XGBoost max_depth 7, без регуляризации) модель запоминает шум → AUC падает (у вас XGBoost wine/housing 0.57/0.64) — согласуется с теорией, не баг.

### 1.11 CatBoost LossFunctionChange (`CatBoostLFC`, фикс B13) — **знак после фикса корректный**
- `get_object_importance(val_pool, train_pool, type='Average', update_method='AllPoints')`. По доке CatBoost: «Positive values reflect that the optimized metric increases» — для Logloss/RMSE это рост loss на val, т.е. **положительное = вредное**. Инверсия `importance = −importance` (B13) приводит к «больше = полезнее» — правильно. Возврат `(indices, scores)` (индексы отсортированы по важности) раскладывается по индексам правильно.
- Метод Sharchilev et al. 2018 (LeafRefit/LeafInfluence); `AllPoints` — самый точный (и дорогой) вариант.
- Регрессия: y для пулов стандартизуется заново тем же способом, что и при обучении — согласовано.
- Ограничение MultiClass корректно помечено как skipped. 
- Средний AUC 0.56–0.82 правдоподобен: LFC измеряет влияние на **val-loss**, а не «ошибочность метки»; при 150 итерациях и depth 7 часть шума не влияет на val. В литературе (Sharchilev 2018) метод хорош для поиска вредных объектов при доменном сдвиге, на чистой label-noise детекции обычно уступает loss-based.

## 2. Индексы, разбиение, утечки — **корректно**
- Все пути извлечения `ValuationResult` раскладывают `values` по `result.indices` (`study/values.py:_result_to_array`, `influence/utils.py` fast path) — порядок совпадает с `X_train` (после `reset_index`). Проверка длины и NaN — жёсткая (B3).
- `is_noisy` выровнен с `X_train` (тот же порядок после `reset_index`); `_detection` использует `roc_auc_score(is_noisy, −values)` — правильно для соглашения «низкое значение = подозрительное»; тай-брейки в Data-OOB (дискретные значения) обрабатываются ROC AUC честно (½ за ничью).
- Удаление (`_removal_mask`) — по `argsort(values)` в индексах train; class-proportional по **наблюдаемым** (возможно испорченным) меткам — это нормально.
- Утечки нет: utility pyDVL и influence используют **val**, итоговая метрика — **holdout**, который ни в valuation, ни в early stopping не участвует. Замечание: val используется и для early stopping, и как utility — допустимо (так же в OpenDataVal: valid для utility, test отдельно).

## 3. Сравнение выводов пилота с литературой

| Наш вывод (пилот) | Литература | Вердикт |
|---|---|---|
| Data-OOB и High-loss лучше всех детектируют шум, AUC ≈ 0.94–1.0 | OpenDataVal (Jiang et al. 2023, NeurIPS D&B): Data-OOB — единственный в 1-м кластере по детекции шумных меток на всех датасетах; Kwon & Zou 2023: Data-OOB лучше KNN-/Data-/Beta-Shapley, DVRL. «Small-loss» критерий — стандарт для шумных меток (Arpit 2017, Han 2018, Pleiss 2020 AUM) | **Согласуется** |
| KNN-Shapley — 2-я группа | OpenDataVal: KNN-Shapley во 2-м кластере (MiniBooNE 20%: F1 0.53 vs Data-OOB 0.65) | Согласуется |
| LOO ≈ 0.5 | OpenDataVal: LOO в 3-м кластере ≈ random; Ghorbani & Zou 2019: LOO плохо ловит шум | **Согласуется** |
| Influence (direct) ≈ 0.5, нестабилен на MLP | OpenDataVal: InfluenceFunction ≈ random; Basu et al. 2021 «fragile» (зависимость от damping, глубины, weight decay); Bae et al. 2022 (IF на нейросетях ≈ PBRF, а не LOO); Koh & Liang 2017 — хорошо работает на выпуклых моделях | Согласуется, **но у нас дополнительный вклад — λ=1e-6..1e-4 без GGN** (см. 1.6). На logreg (convex sanity) Direct должен давать заметно > 0.5: если там тоже ≈ 0.5 — это подозрение на баг |
| При систематическом шуме лучше LiSSA | Прямых работ нет. Объяснение: LiSSA у нас = influence с λ_eff=3–12 ≈ GradDot/TracIn (Pruthi 2020), а градиентное сходство устойчивее к «согласованному» шуму, который модель частично выучила (loss на таких точках мал → LossHigh/Data-OOB проигрывают) | Правдоподобно, **но интерпретировать как эффект сильного демпфирования, не алгоритма LiSSA** |
| На чистом wine ничего не лучше random | Ghorbani 2019 и OpenDataVal (point removal): на чистых данных выигрыш от удаления «малоценных» мал и часто в пределах шума, особенно для регрессии и маленьких сетей; в регрессии без выбросов «плохих» точек почти нет | **Согласуется**, не баг |
| CatBoost LFC средний (0.56–0.82) | Sharchilev et al. 2018 — метод для влияния на val-loss; для label-noise детекции уступает loss-based | Согласуется (после фикса знака B13) |
| TMC-Shapley медленный и слабый | Ghorbani 2019: TMC хорош при сходимости (сотни–тысячи перестановок); OpenDataVal: Data/Beta Shapley во 2-м кластере | **Расхождение объясняется бюджетом**: 10 перестановок + без seed (см. 1.3) |

**Где расхождение подозрительно на баг:** явных противоречий с литературой нет. Проверить после полного прогона: (1) convex study (`damp-linear-*`): Direct Influence на logreg при λ≈1e-4..1e-2 должен детектировать шум заметно лучше 0.5 — если нет, искать баг в критерии/метках для linear-модели; (2) «damp-*» для LiSSA плоские — ожидаемо из-за λ_eff (не баг кода, но баг постановки sweep).

## 4. Список проблем по приоритету

### Критично (искажает выводы, если не оговорить)
_Явных багов в коде, которые портят числа, не найдено._ Ближе всего к критичным:
1. **Damping-sweep не управляет LiSSA** — `study/config.py:155-166` (`DAMPINGS`) + `study/values.py:44-59` (`_overrides` меняет только `regularization`) + `influence/methods.py:570-579`. λ_eff = λ + scale·dampen ≈ 3–12 при λ ≤ 1e-2. Фикс: для `damp-*` исследований ставить `dampen=0` (или `dampen = damping/scale`) и логировать λ_eff в results.json. Влияние: кривые/таблицы «LiSSA vs damping» и вывод «LiSSA робастен к damping» неверны по смыслу.

### Важно
2. **LiSSA ≡ Direct с λ_eff = s·d + λ** (проверено: Spearman 1.00). В тексте диплома называть «Influence с сильным демпфированием / ≈ GradDot», не делать вывод «итеративный LiSSA лучше прямого решения». `config/settings.py` DATASET_INFLUENCE_PARAMS (lissa_params).
3. **Direct Influence на MLP с λ=1e-6..1e-4 и полным Hessian** (M5) — `influence/methods.py:475-479`. Фикс (если будет время): `second_order_mode=SecondOrderMode.GAUSS_NEWTON` и λ из сетки convex-study; иначе — явно оговорить «fragile» (Basu 2021). Влияние: AUC Direct на MLP ≈ 0.5 частично артефакт настроек.
4. **Data-OOB и KNN-Shapley не зависят от модели** — `study/values.py:107-135`. В `models-*` их values/AUC идентичны по всем деревьям. Фикс: в отчёте/графиках одна строка «model-agnostic»; опционально для RF — `DataOOBValuation(обученная RF)`. Поправить `README.md:39`.
5. **TMC-Shapley без seed и с 10 перестановками** — `influence/methods.py:421-425`. Фикс: `seed=seed`, критерий `HistoryDeviation(n_steps=100, rtol=0.05) | MaxUpdates(N)`; в тексте — «TMC при бюджете 10 перестановок».
6. **Influence через дистиллированного студента** использует loss по настоящим y, хотя студент учился на teacher-targets — `influence/methods.py:192-221` + `models/torch_models.py:462-530`. Оговорить или считать на teacher-targets.

### Мелочи
7. `SupervisedScorer(range=None)` — `influence/methods.py:327`: ожидается кортеж; не используется → убрать аргумент.
8. Influence DataLoader берёт глобальный `batch_size=16`, а не датасетный — `influence/methods.py:731`.
9. LiSSA `rtol=0.1` по max-поэлементной невязке никогда не срабатывает (всегда 100 итераций; при d≥0.1 это всё равно сходится) — warning-спам «nan %». Можно `warn_on_max_iteration=False`.
10. LiSSA и мини-батчи без seed → значения слегка невоспроизводимы.
11. AdamW weight_decay=1e-4 не входит в Hessian — при λ<1e-4 (convex-study 1e-6) небольшое несоответствие.
12. В `setup_methods` при отсутствии logger строка `self.logger.log_message("WARNING: RandomForest…")` (`influence/methods.py:309`) упадёт с AttributeError (logger=None в study) — путь срабатывает только у необученной RF, на практике не достигается.
13. `influence/methods.py:436-440` — в «старом» пайплайне (main.py) DataOOB/KNNShapley пропускаются с сообщением «requires BaggingModel»; в study они реализованы — комментарий устарел.
14. `synthetic_data/*.py` используют тот же API 0.10 (не проверялись построчно, в study не участвуют).

### Что корректно (вердикты)
| Метод | Вердикт |
|---|---|
| Dataset / SupervisedScorer / ModelUtility / ValuationResult→массив | корректно |
| LOO | корректно (шум по природе метода на MLP) |
| TMC-Shapley | API корректно; проблема: нет seed, 10 перестановок |
| KNN-Shapley | корректно (model-agnostic) |
| Data-OOB | корректно по доке/статье; model-agnostic → одинаков для всех моделей |
| Influence (Direct) | API/знак/агрегация корректны; проблема: λ и полный Hessian на MLP |
| LiSSA | работает корректно, но = Direct с λ_eff=s·d+λ; sweep damping его не меняет |
| LossHigh | корректно |
| CatBoost LFC | корректно после B13 (знак проверен по доке CatBoost) |
| Индексы / разбиение / утечки | корректно, утечки holdout нет |

## 5. Ссылки
- pyDVL 0.10 docs: https://pydvl.org/stable/ ; influence intro (знак, регуляризация): https://pydvl.org/stable/influence/ ; Data-OOB: https://pydvl.org/stable/value/data-oob/ ; исходники v0.10.0: https://github.com/aai-institute/pyDVL/tree/v0.10.0
- Kwon & Zou 2023, Data-OOB (ICML): https://proceedings.mlr.press/v202/kwon23e.html
- Jiang et al. 2023, OpenDataVal (NeurIPS D&B): https://arxiv.org/abs/2306.10577
- Ghorbani & Zou 2019, Data Shapley (ICML): https://proceedings.mlr.press/v97/ghorbani19c.html
- Jia et al. 2019, Efficient task-specific data valuation for nearest neighbor algorithms (VLDB): https://arxiv.org/abs/1908.08619
- Kwon & Zou 2022, Beta Shapley (AISTATS): https://arxiv.org/abs/2110.14049
- Koh & Liang 2017, Influence functions (ICML): https://arxiv.org/abs/1703.04730
- Basu, Pope, Feizi 2021, Influence functions in deep learning are fragile (ICLR): https://arxiv.org/abs/2006.14651
- Bae et al. 2022, If influence functions are the answer, then what is the question? (NeurIPS): https://arxiv.org/abs/2209.05364
- Schioppa et al. 2022, Scaling up influence functions (Arnoldi, AAAI): https://arxiv.org/abs/2112.03052
- Hataya & Yamada 2023, Nyström method for accurate and scalable implicit differentiation (AISTATS): https://arxiv.org/abs/2302.09726
- Kwon et al. 2024, DataInf (ICLR): https://arxiv.org/abs/2310.00902
- Park et al. 2023, TRAK (ICML): https://arxiv.org/abs/2303.14186
- Pruthi et al. 2020, TracIn (NeurIPS): https://arxiv.org/abs/2002.08484
- Sharchilev et al. 2018, Influential training samples for GBDT (CatBoost LFC): https://arxiv.org/abs/1802.06640 ; CatBoost doc: https://catboost.ai/docs/en/concepts/python-reference_catboost_get_object_importance
- Agarwal, Bullins, Hazan 2017, LiSSA (JMLR): https://arxiv.org/abs/1602.03943
- Pleiss et al. 2020, AUM (шумные метки по margin/loss): https://arxiv.org/abs/2001.10528
