# GBDT influence через дистилляцию: план и статус (P9–P11)

Статус (19.11.2026, ~00:30 МСК): **сделано**, pytest 51/51 до последней правки, 5/5 в `tests/test_gbdt_influence.py`
после неё. Тяжёлых прогонов не было; пилот — adult, n_train=400, 1 сид.

## Что код делал до правок

**(a) Прямые методы для GBDT.** Был только CatBoost LFC (`get_object_importance`, LossFunctionChange —
LeafInfluence-семейство, Sharchilev et al. 2018) и только в `models-catboost-*`; в `distill-*` его не было
(`methods_for` выкидывал при `distill=True`). BoostIn (Brophy et al., JMLR 2023) не было. Остальные сравнения
для деревьев — модель-агностичные LOO / KNN-Shapley / Data-OOB / LossHigh.

**(b) Influence студента** считался по **настоящим (зашумлённым) меткам** `y_train` с критерием студента
(BCEWithLogits / CE / MSE), т. е. «влияние точки (x_i, y_i) на дифф. суррогат», хотя студент учился не на y_i,
а на выходах учителя.

**(c) Кривые удаления для distill-\*** (`protocol._curve` → `Trainer.fit` на оставшихся точках →
`DistilledModelWrapper.fit`): **переобучается учитель** (бустинг) на оставшихся точках, затем студент
дистиллируется заново с нуля (AUDIT-FIX D4). Метрика кривой — holdout-метрика **студента**. Детекция шума
переобучения не требует (AUC по значениям). П. 2 задания уже выполнен — только подтверждено.

## Что сделано

* **P9 `distill_influence_target`** ∈ {`true_labels` (по умолчанию), `teacher`} в `RunSpec`.
  `teacher`: train-цели = ровно цели обучения студента `DistilledModelWrapper._teacher_targets` (binary p,
  multiclass softmax(log p / T), регрессия — предсказание учителя в шкале y_scaler); loss = loss обучения студента:
  BCEWithLogits(z, p), `T²·CE(z/T, p_T)` (градиент = градиент KL·T², есть тест), MSE. Валидационная (test) сторона —
  настоящие метки. В results.json: `spec.distill_influence_target` и `influence_target` {target, train_loss, val_target}.
  В полном прогоне: новые исследования `distill-{lightgbm,catboost}-noise10-tgtteacher` (Influence, LiSSA).
* **P10 BoostIn** — пакет авторов `tree_influence` (git a325794; на PyPI колёса только для py3.9/3.10, а sdist без
  .pyx → сборка из git с Cython, MSVC есть). Адаптер `experiments/boostin.py`: прокси для нашего `lgb.Booster`
  (совпадает с эталоном пакета на LGBMClassifier до 1e-9, тест), взвешенные train-градиенты при balanced весах (P8),
  шим `OneHotEncoder(sparse=)` для sklearn 1.8, расхождение распарсенной модели → ошибка, а не тихий мусор.
  Применимость: **только LightGBM**. CatBoost: у наших моделей `leaf_estimation_iterations=10` (дефолт Logloss),
  пакет требует 1 → NotApplicable (менять модель не стал). XGBoost 3.x: `base_score` оценивается из данных, парсер
  считает 0 → расхождение предсказаний 0.035 → NotApplicable. LeafInfluence/TREX из пакета не подключал: LeafInfluence
  для CatBoost у нас уже есть (LFC), для LightGBM он O(n²·T) и требует тех же условий; TREX — отдельная kernel-модель.
* **P11 прямые baseline'ы в distill-\***: `BoostIn` (учитель LightGBM), `CatBoostLFC` (учитель CatBoost),
  `DataOOB` — на том же зашумлённом сплите; `explained_model: teacher` в results.json. Кривые для них, как и для всех
  методов distill, переобучают учителя+студента. В `models-lightgbm-*` добавлен BoostIn.

## Пилот (adult, n_train=400, 10 % шума, seed 0; AUC детекции шума, кривая = F1 после удаления 10 % «худших»)

| исследование | метод | AUC | F1@10% |
|---|---|---|---|
| distill-lightgbm | Influence (true_labels) | 0.597 | 0.623 |
| distill-lightgbm | LiSSA (true_labels) | 0.629 | 0.660 |
| distill-lightgbm tgt=teacher | Influence (teacher) | 0.376 | 0.639 |
| distill-lightgbm tgt=teacher | LiSSA (teacher) | 0.719 | 0.624 |
| distill-lightgbm | BoostIn (учитель) | 0.708 | 0.651 |
| distill-lightgbm | Data-OOB | 0.873 | 0.626 |
| distill-lightgbm | LossHigh (студент) | 0.915 | 0.605 |
| distill-catboost | Influence (true_labels) | 0.423 | 0.644 |
| distill-catboost tgt=teacher | Influence (teacher) | 0.413 | 0.639 |
| distill-catboost | CatBoost LFC (учитель) | 0.684 | 0.652 |
| models-lightgbm | BoostIn | 0.708 | 0.658 |
| models-lightgbm | LossHigh | 0.842 | 0.617 |
| models-catboost | CatBoost LFC | 0.684 | 0.666 |
| models-catboost | LossHigh | 0.845 | 0.636 |

Baseline F1: учитель LightGBM 0.610, CatBoost 0.649. Один сид и n=400 — только проверка работоспособности.
BoostIn на n_train=1500 (1 сид): adult AUC 0.81 (0.7 с), covertype 0.91 (6 с), housing 0.53 (0.2 с).

## Время полного прогона

`estimate-ext` новые блоки не считает (их нет в `results/pilot_ext`): EXT 22.2 ч как и было. Ручная оценка прироста:
BoostIn ≤ 6 с значений на блок + дешёвые кривые LightGBM (~24 блока) ≈ +0.1 ч; distill: +DataOOB/BoostIn/LFC
(~48 запусков, стоимость ≈ кривая LossHigh) и tgtteacher (48 запусков Influence/LiSSA + 24 baseline) — примерно
удвоение секции distill (0.58 → ~1.2–1.5 ч). Итого **+0.7–1 ч** (< 3 ч, урезание не нужно). Точнее — после
`run_study.py pilot`-ext на новых секциях.

## Оговорки

* Teacher-target influence на пилоте не лучше true_labels (direct 0.38 — антидетекция: студент воспроизводит
  учителя, градиент по «чужой» цели на шумной точке мал). Это ожидаемо и само по себе результат: для детекции шума
  в метках нужен true_labels-вариант; teacher-вариант отвечает на вопрос «какие точки формируют функцию студента».
* BoostIn с balanced весами: train-градиенты взвешены нами (пакет весов не знает); без весов — точное совпадение с пакетом.
* LiSSA пишет «max residual nan» — было и раньше (pyDVL-лог), значения конечны.
* CatBoost BoostIn возможен только при `leaf_estimation_iterations=1` (другая модель) — не включал, можно отдельной опцией.
