import numpy as np
import pandas as pd
import torch
from torch.utils.data import TensorDataset, DataLoader
from joblib import parallel_config
from scipy.stats import rankdata

from pydvl.valuation.dataset import Dataset
from pydvl.valuation.utility import ModelUtility
from pydvl.valuation.scorers import SupervisedScorer
from pydvl.valuation.methods import (
    LOOValuation, ShapleyValuation, BetaShapleyValuation,
    BanzhafValuation, TMCShapleyValuation, KNNShapleyValuation,
    DataOOBValuation, LeastCoreValuation
)
from pydvl.valuation.samplers import PermutationSampler
from pydvl.valuation.stopping import HistoryDeviation, MaxUpdates
from pydvl.influence.torch import (
    DirectInfluence, ArnoldiInfluence, CgInfluence,
    LissaInfluence, NystroemSketchInfluence
)
from pydvl.influence import InfluenceMode

from experiments.logger import debug_print
from config.settings import PYDVL_CONFIG, N_JOBS
from .scorers import ScorerFactory


class InfluenceMethods:
    """Класс для работы с методами оценки влияния"""

    def __init__(self, logger=None):
        self.logger = logger
        self.methods = {}

    def setup_methods(self, pipeline, X_train, y_train, X_val, y_val,
                      preprocessor, methods_to_use=None):
        """
        Подготавливает методы оценки влияния
        """
        if self.logger:
            self.logger.log_message("\n" + "=" * 60)
            self.logger.log_message("SETTING UP INFLUENCE METHODS")
            self.logger.log_message("=" * 60)
        else:
            debug_print("Setting up influence methods...")

        # Подготовка данных
        X_train_t = preprocessor.transform(X_train)
        X_val_t = preprocessor.transform(X_val)

        if hasattr(X_train_t, 'toarray'):
            X_train_t = X_train_t.toarray()
            X_val_t = X_val_t.toarray()

        X_train_t = np.asarray(X_train_t)
        X_val_t = np.asarray(X_val_t)
        y_train_1d = np.asarray(y_train).reshape(-1)
        y_val_1d = np.asarray(y_val).reshape(-1)

        # Создание Dataset
        n_features = X_train_t.shape[1]
        feature_names = [f"x{i + 1}" for i in range(n_features)]

        X_train_df = pd.DataFrame(X_train_t, columns=feature_names)
        X_val_df = pd.DataFrame(X_val_t, columns=feature_names)
        y_train_series = pd.Series(y_train_1d, name="y")
        y_val_series = pd.Series(y_val_1d, name="y")

        try:
            val_dataset = Dataset(X_train_df, y_train_series, X_val_df, y_val_series)
        except Exception as e:
            debug_print(f"DataFrame Dataset failed: {e}, trying array interface")
            val_dataset = Dataset(X_train_t, y_train_1d.reshape(-1, 1), X_val_t, y_val_1d.reshape(-1, 1))

        # Создание скорера
        scorer_callable = ScorerFactory.create_scorer('neg_mae')
        model_wrapper = pipeline.named_steps['model']

        # Проверяем, что модель обучена перед созданием scorer
        if hasattr(model_wrapper, 'estimators_'):
            if model_wrapper.estimators_ is None or len(model_wrapper.estimators_) == 0:
                self.logger.log_message("WARNING: RandomForest model not properly fitted before creating scorer!")
                # Попытка переобучить модель на тренировочных данных
                if self.logger:
                    self.logger.log_message("Attempting to refit model on training data...")
                try:
                    model_wrapper.fit(X_train_t, y_train_1d)
                    if self.logger:
                        self.logger.log_message("Model refitted successfully")
                except Exception as e:
                    if self.logger:
                        self.logger.log_message(f"Failed to refit model: {e}")

        supervised_scorer = SupervisedScorer(
            scoring=scorer_callable,
            test_data=val_dataset,
            default=float(-1e6),
            range=None
        )

        utility = ModelUtility(
            model=model_wrapper,
            scorer=supervised_scorer,
            show_warnings=True,
            clone_before_fit=True  # Изменено на True для клонирования модели перед каждым fit
        )

        # Определение методов для использования
        if methods_to_use is None:
            methods_to_use = [
                'LOO'
                # , 'DataShapley'
                # , 'BetaShapley'
                , 'Banzhaf'
                , 'TMCShapley'
                # , 'KNNShapley'  # Только для классификации
                # , 'DataOOB'     # Требует специальной настройки
                # , 'LeastCore'
                              ]  # Добавлены новые методы для тестирования

            # Проверяем, является ли модель PyTorch моделью или дистиллированной
            is_pytorch = (hasattr(model_wrapper, 'model') and isinstance(getattr(model_wrapper, 'model', None), torch.nn.Module)) or \
                         (hasattr(model_wrapper, 'student_model') and isinstance(getattr(model_wrapper, 'student_model', None), torch.nn.Module))
            if is_pytorch:
                methods_to_use.extend([
                    'Influence',
                    'ArnoldiInfluence',
                    # 'CgInfluence',
                    'LissaInfluence',
                    # 'NystroemSketchInfluence'
                ])

            # Добавляем Shapley методы только если не дистилляция (слишком медленно)
            is_distilled = hasattr(model_wrapper, 'student_model')
            # if not is_distilled:
            #     methods_to_use.extend(['DataShapley', 'BetaShapley'])

        # Инициализация методов - каждый метод в отдельном try-except блоке
        with parallel_config(backend="threading", n_jobs=N_JOBS):
            for method_name in methods_to_use:
                try:
                    if method_name == 'LOO':
                        if self.logger:
                            self.logger.start_timing("LOO_setup")
                        self.methods['LOO'] = LOOValuation(
                            utility=utility,
                            progress=True
                        )
                        if self.logger:
                            self.logger.end_timing("LOO_setup")

                    elif method_name == 'DataShapley':
                        if self.logger:
                            self.logger.start_timing("DataShapley_setup")
                        self.methods['DataShapley'] = ShapleyValuation(
                            utility=utility,
                            sampler=PermutationSampler(truncation=None, seed=42),
                            is_done=HistoryDeviation(n_steps=PYDVL_CONFIG['n_steps'],
                                                     rtol=PYDVL_CONFIG['rtol']) | MaxUpdates(
                                PYDVL_CONFIG['max_updates']),
                            progress=True
                        )
                        if self.logger:
                            self.logger.end_timing("DataShapley_setup")

                    elif method_name == 'BetaShapley':
                        if self.logger:
                            self.logger.start_timing("BetaShapley_setup")
                        self.methods['BetaShapley'] = BetaShapleyValuation(
                            utility=utility,
                            sampler=PermutationSampler(truncation=None, seed=42),
                            is_done=HistoryDeviation(n_steps=PYDVL_CONFIG['n_steps'],
                                                     rtol=PYDVL_CONFIG['rtol']) | MaxUpdates(
                                PYDVL_CONFIG['max_updates']),
                            alpha=PYDVL_CONFIG['beta_shapley_params']['alpha'],
                            beta=PYDVL_CONFIG['beta_shapley_params']['beta'],
                            progress=True
                        )
                        if self.logger:
                            self.logger.end_timing("BetaShapley_setup")

                    elif method_name == 'Banzhaf':
                        if self.logger:
                            self.logger.start_timing("Banzhaf_setup")
                        self.methods['Banzhaf'] = BanzhafValuation(
                            utility=utility,
                            sampler=PermutationSampler(truncation=None, seed=42),
                            is_done=MaxUpdates(PYDVL_CONFIG['banzhaf_params']['n_samples']),
                            progress=True
                        )
                        if self.logger:
                            self.logger.end_timing("Banzhaf_setup")

                    elif method_name == 'TMCShapley':
                        if self.logger:
                            self.logger.start_timing("TMCShapley_setup")
                        self.methods['TMCShapley'] = TMCShapleyValuation(
                            utility=utility,
                            is_done=MaxUpdates(PYDVL_CONFIG['tmc_shapley_params']['n_samples']),
                            progress=True
                        )
                        if self.logger:
                            self.logger.end_timing("TMCShapley_setup")

                    elif method_name == 'KNNShapley':
                        # KNNShapleyValuation требует KNeighborsClassifier, пропускаем для регрессии
                        if self.logger:
                            self.logger.log_message("KNNShapley skipped - requires KNeighborsClassifier (classification only)")
                        continue

                    elif method_name == 'DataOOB':
                        # DataOOBValuation требует BaggingModel, сложно настроить для произвольных моделей
                        if self.logger:
                            self.logger.log_message("DataOOB skipped - requires BaggingModel setup")
                        continue

                    elif method_name == 'LeastCore':
                        if self.logger:
                            self.logger.start_timing("LeastCore_setup")
                        self.methods['LeastCore'] = LeastCoreValuation(
                            utility=utility,
                            epsilon=PYDVL_CONFIG['least_core_params']['epsilon'],
                            n_samples=PYDVL_CONFIG['least_core_params']['n_samples'],
                            progress=True
                        )
                        if self.logger:
                            self.logger.end_timing("LeastCore_setup")

                    elif method_name == 'Influence':
                        if self.logger:
                            self.logger.start_timing("Influence_setup")

                        # Для дистиллированных моделей используем student_model
                        influence_model = getattr(model_wrapper, "student_model", None)
                        if influence_model is None:
                            # Для обычных PyTorch моделей используем model
                            influence_model = getattr(model_wrapper, "model", model_wrapper)

                        # Переключаем модель в eval режим для избежания случайных операций
                        if hasattr(influence_model, 'eval'):
                            influence_model.eval()

                        self.methods['Influence'] = DirectInfluence(
                            influence_model,
                            getattr(model_wrapper, "criterion", torch.nn.MSELoss()),
                            regularization=1e-6
                        )
                        if self.logger:
                            self.logger.end_timing("Influence_setup")

                    elif method_name == 'ArnoldiInfluence':
                        if self.logger:
                            self.logger.start_timing("ArnoldiInfluence_setup")

                        influence_model = getattr(model_wrapper, "student_model", None)
                        if influence_model is None:
                            influence_model = getattr(model_wrapper, "model", model_wrapper)

                        if hasattr(influence_model, 'eval'):
                            influence_model.eval()

                        self.methods['ArnoldiInfluence'] = ArnoldiInfluence(
                            influence_model,
                            getattr(model_wrapper, "criterion", torch.nn.MSELoss()),
                            rank=PYDVL_CONFIG['influence_params']['arnoldi_params']['rank'],
                            regularization=PYDVL_CONFIG['influence_params']['regularization']
                        )
                        if self.logger:
                            self.logger.end_timing("ArnoldiInfluence_setup")

                    elif method_name == 'CgInfluence':
                        if self.logger:
                            self.logger.start_timing("CgInfluence_setup")

                        influence_model = getattr(model_wrapper, "student_model", None)
                        if influence_model is None:
                            influence_model = getattr(model_wrapper, "model", model_wrapper)

                        if hasattr(influence_model, 'eval'):
                            influence_model.eval()

                        self.methods['CgInfluence'] = CgInfluence(
                            influence_model,
                            getattr(model_wrapper, "criterion", torch.nn.MSELoss()),
                            maxiter=PYDVL_CONFIG['influence_params']['cg_params']['maxiter'],
                            tolerance=PYDVL_CONFIG['influence_params']['cg_params']['tolerance'],
                            regularization=PYDVL_CONFIG['influence_params']['regularization']
                        )
                        if self.logger:
                            self.logger.end_timing("CgInfluence_setup")

                    elif method_name == 'LissaInfluence':
                        if self.logger:
                            self.logger.start_timing("LissaInfluence_setup")

                        influence_model = getattr(model_wrapper, "student_model", None)
                        if influence_model is None:
                            influence_model = getattr(model_wrapper, "model", model_wrapper)

                        if hasattr(influence_model, 'eval'):
                            influence_model.eval()

                        self.methods['LissaInfluence'] = LissaInfluence(
                            influence_model,
                            getattr(model_wrapper, "criterion", torch.nn.MSELoss()),
                            scale=PYDVL_CONFIG['influence_params']['lissa_params']['scale'],
                            dampen=PYDVL_CONFIG['influence_params']['lissa_params']['damping'],
                            regularization=PYDVL_CONFIG['influence_params']['regularization']
                        )
                        if self.logger:
                            self.logger.end_timing("LissaInfluence_setup")

                    elif method_name == 'NystroemSketchInfluence':
                        if self.logger:
                            self.logger.start_timing("NystroemSketchInfluence_setup")

                        influence_model = getattr(model_wrapper, "student_model", None)
                        if influence_model is None:
                            influence_model = getattr(model_wrapper, "model", model_wrapper)

                        if hasattr(influence_model, 'eval'):
                            influence_model.eval()

                        self.methods['NystroemSketchInfluence'] = NystroemSketchInfluence(
                            influence_model,
                            getattr(model_wrapper, "criterion", torch.nn.MSELoss()),
                            rank=PYDVL_CONFIG['influence_params']['nystroem_params']['rank'],
                            regularization=PYDVL_CONFIG['influence_params']['regularization']
                        )
                        if self.logger:
                            self.logger.end_timing("NystroemSketchInfluence_setup")

                except Exception as e:
                    if self.logger:
                        self.logger.log_message(f"ERROR initializing {method_name}: {type(e).__name__}: {e}")
                        import traceback
                        self.logger.log_message(f"Traceback for {method_name}: {traceback.format_exc()}")
                    else:
                        debug_print(f"Error initializing {method_name}: {e}")
                        import traceback
                        debug_print(traceback.format_exc())

        if self.logger:
            self.logger.log_message("Methods initialization completed!")

        return self.methods, scorer_callable

    def compute_scores(self, methods, X_train, y_train, preprocessor, X_val, y_val, pipeline):
        """Вычисление influence scores с сохранением сырых значений"""
        from .utils import _extract_numeric_values_from_result

        if self.logger:
            self.logger.log_message("\n" + "=" * 60)
            self.logger.log_message("COMPUTING INFLUENCE SCORES")
            self.logger.log_message("=" * 60)

        # Трансформация данных
        X_train_t = preprocessor.transform(X_train)
        X_val_t = preprocessor.transform(X_val)

        if hasattr(X_train_t, 'toarray'):
            X_train_t = X_train_t.toarray()
            X_val_t = X_val_t.toarray()

        X_train_t = np.asarray(X_train_t)
        X_val_t = np.asarray(X_val_t)
        y_train_arr = np.asarray(y_train).reshape(-1)
        y_val_arr = np.asarray(y_val).reshape(-1)

        # Создание Dataset
        n_features = X_train_t.shape[1]
        feature_names = [f"x{i + 1}" for i in range(n_features)]

        X_train_df = pd.DataFrame(X_train_t, columns=feature_names)
        X_val_df = pd.DataFrame(X_val_t, columns=feature_names)
        y_train_series = pd.Series(y_train_arr, name="y")
        y_val_series = pd.Series(y_val_arr, name="y")

        try:
            train_dataset = Dataset(X_train_df, y_train_series, X_val_df, y_val_series)
        except Exception as e:
            train_dataset = Dataset(X_train_t, y_train_arr.reshape(-1, 1), X_val_t, y_val_arr.reshape(-1, 1))

        scores = {}
        scores_raw = {}

        for name, method in methods.items():
            if self.logger:
                self.logger.start_timing(f"{name}_computation")
                self.logger.log_message(f"\n--- Computing {name} scores ---")

            try:
                if name in ['Influence', 'ArnoldiInfluence', 'CgInfluence', 'LissaInfluence', 'NystroemSketchInfluence']:
                    # Вычисление влияния для PyTorch моделей
                    train_loader = DataLoader(
                        TensorDataset(
                            torch.FloatTensor(X_train_t),
                            torch.FloatTensor(y_train_arr.reshape(-1, 1))
                        ),
                        batch_size=1,
                        shuffle=False
                    )

                    # Log loader/model diagnostics
                    if self.logger:
                        try:
                            n_train = len(train_loader.dataset)
                            n_batches = len(train_loader)
                            batch_size = train_loader.batch_size
                            self.logger.log_message(
                                f"Influence: train loader - {n_train} samples, {n_batches} batches, batch_size={batch_size}"
                            )
                            # model parameter count if available
                            wrapped_model = getattr(pipeline.named_steps.get('model', {}), 'model', pipeline.named_steps.get('model', None))
                            if hasattr(wrapped_model, 'parameters'):
                                param_count = sum(p.numel() for p in wrapped_model.parameters())
                                self.logger.log_message(f"Influence: model parameter count = {param_count}")
                        except Exception as e:
                            debug_print(f"Failed to log loader/model diagnostics: {e}")

                    infl = method.fit(train_loader)
                    if self.logger:
                        self.logger.log_message("Influence: DirectInfluence.fit completed")

                    zf = infl.influence_factors(
                        torch.FloatTensor(X_val_t),
                        torch.FloatTensor(y_val_arr.reshape(-1, 1))
                    )

                    # Diagnostics for influence factors
                    try:
                        zf_np = zf.detach().cpu().numpy() if hasattr(zf, 'detach') else np.asarray(zf)
                        if self.logger:
                            self.logger.log_message(
                                f"Influence: influence_factors shape={getattr(zf_np, 'shape', 'unknown')}, "
                                f"dtype={zf_np.dtype if hasattr(zf_np, 'dtype') else 'unknown'}"
                            )
                            nan_count = np.isnan(zf_np).sum()
                            inf_count = np.isinf(zf_np).sum()
                            self.logger.log_message(f"Influence: zf NaN={nan_count}, Inf={inf_count}")
                            if zf_np.size > 0:
                                self.logger.log_message(
                                    f"Influence factors stats - min={np.nanmin(zf_np):.6g}, max={np.nanmax(zf_np):.6g}, mean={np.nanmean(zf_np):.6g}, std={np.nanstd(zf_np):.6g}"
                                )
                    except Exception as e:
                        debug_print(f"Failed to analyze influence_factors: {e}")

                    scores_raw_val = infl.influences_from_factors(
                        zf,
                        torch.FloatTensor(X_train_t),
                        torch.FloatTensor(y_train_arr.reshape(-1, 1)),
                        mode=InfluenceMode.Up
                    ).cpu().numpy()

                    # Агрегирование влияний
                    if scores_raw_val.ndim == 2:
                        per_train = np.abs(scores_raw_val).sum(axis=0)
                    elif scores_raw_val.ndim > 2:
                        per_train = np.abs(scores_raw_val).sum(axis=tuple(range(scores_raw_val.ndim - 1)))
                    else:
                        per_train = np.abs(scores_raw_val).flatten()

                    # Diagnostics for raw influence values
                    try:
                        if self.logger:
                            self.logger.log_message(
                                f"Influence: raw influences shape={scores_raw_val.shape}, aggregated per-train length={len(per_train)}"
                            )
                            nan_count = np.isnan(per_train).sum()
                            inf_count = np.isinf(per_train).sum()
                            self.logger.log_message(f"Influence: per_train NaN={nan_count}, Inf={inf_count}")

                            if per_train.size > 0:
                                self.logger.log_message(
                                    f"Influence RAW stats - min={np.min(per_train):.6g}, max={np.max(per_train):.6g}, mean={np.mean(per_train):.6g}, std={np.std(per_train):.6g}"
                                )
                                # Top / bottom indices for quick inspection
                                idx_sorted = np.argsort(per_train)
                                top_idx = idx_sorted[-5:][::-1]
                                bot_idx = idx_sorted[:5]
                                self.logger.log_message(
                                    f"Top 5 influences (idx:value): {[(int(i), float(per_train[i])) for i in top_idx]}"
                                )
                                self.logger.log_message(
                                    f"Bottom 5 influences (idx:value): {[(int(i), float(per_train[i])) for i in bot_idx]}"
                                )
                    except Exception as e:
                        debug_print(f"Failed to log raw influence diagnostics: {e}")

                    scores_raw[name] = per_train.copy()
                    scores[name] = per_train.copy()

                else:
                    # Вычисление для valuation методов
                    with parallel_config(backend="threading", n_jobs=N_JOBS):
                        try:
                            result = method.fit(train_dataset)
                            if result is None:
                                if self.logger:
                                    self.logger.log_message(f"WARNING: {name} method returned None result")
                                scores[name] = np.zeros(len(X_train_t))
                                scores_raw[name] = np.zeros(len(X_train_t))
                                continue
                        except Exception as fit_e:
                            if self.logger:
                                self.logger.log_message(f"ERROR: Failed to fit {name} method: {fit_e}")
                            scores[name] = np.zeros(len(X_train_t))
                            scores_raw[name] = np.zeros(len(X_train_t))
                            continue

                    values_arr = _extract_numeric_values_from_result(result)

                    # Проверяем, что получили правильное количество значений
                    if len(values_arr) == 0:
                        if self.logger:
                            self.logger.log_message(f"WARNING: {name} method returned no values")
                        scores[name] = np.zeros(len(X_train_t))
                        scores_raw[name] = np.zeros(len(X_train_t))
                        continue

                    expected_len = len(X_train_t)
                    if len(values_arr) != expected_len:
                        if self.logger:
                            self.logger.log_message(f"WARNING: {name} returned {len(values_arr)} values, expected {expected_len}")
                            if len(values_arr) < expected_len:
                                # Дополняем нулями
                                padding = np.zeros(expected_len - len(values_arr))
                                values_arr = np.concatenate([values_arr, padding])
                            else:
                                # Обрезаем до нужной длины
                                values_arr = values_arr[:expected_len]

                    # Diagnostic logging about extracted values
                    try:
                        if self.logger:
                            self.logger.log_message(f"{name}: extracted {values_arr.size} values")
                            if values_arr.size > 0:
                                finite_mask = np.isfinite(values_arr)
                                n_finite = int(np.sum(finite_mask))
                                n_nonfinite = int(np.sum(~finite_mask))
                                n_unique = int(np.unique(values_arr[finite_mask]).size) if n_finite > 0 else 0
                                pcts = np.percentile(values_arr[finite_mask], [1,5,25,50,75,95,99]) if n_finite > 0 else []
                                self.logger.log_message(
                                    f"{name}: finite={n_finite}, non-finite={n_nonfinite}, unique={n_unique}, percentiles (1,5,25,50,75,95,99)={list(pcts)}"
                                )
                                if n_finite > 0:
                                    idx_sorted = np.argsort(values_arr[finite_mask])
                                    # map back indices to original array
                                    finite_idx = np.where(finite_mask)[0]
                                    top_idx = finite_idx[idx_sorted[-5:]][::-1]
                                    bot_idx = finite_idx[idx_sorted[:5]]
                                    self.logger.log_message(f"{name} top 5 (idx:value): {[(int(i), float(values_arr[i])) for i in top_idx]}")
                                    self.logger.log_message(f"{name} bottom 5 (idx:value): {[(int(i), float(values_arr[i])) for i in bot_idx]}")
                    except Exception as e:
                        debug_print(f"Failed to log extracted values diagnostics for {name}: {e}")

                    if values_arr.size == 0:
                        debug_print(f"WARNING: No values extracted for {name}, using zeros")
                        scores[name] = np.zeros(len(X_train_t))
                        scores_raw[name] = np.array([])
                        continue

                    scores_raw[name] = values_arr.copy()

                    # Обработка неконечных значений
                    finite_mask = np.isfinite(values_arr)
                    if not finite_mask.all():
                        debug_print(f"WARNING: Non-finite values in {name}: {np.sum(~finite_mask)}/{len(values_arr)}")
                        if self.logger:
                            bad_indices = np.where(~finite_mask)[0][:10]
                            self.logger.log_message(f"{name}: non-finite indices sample: {list(bad_indices)}")
                        finite_vals = values_arr[finite_mask]
                        fill_val = np.median(finite_vals) if finite_vals.size > 0 else 0.0
                        values_arr[~finite_mask] = fill_val

                    scores[name] = values_arr.copy()

                # Логирование результатов
                if self.logger:
                    final_scores = scores[name]
                    raw_scores = scores_raw[name]
                    self.logger.log_message(
                        f"{name} scores - min: {final_scores.min():.6f}, max: {final_scores.max():.6f}, "
                        f"mean: {final_scores.mean():.6f}, std: {final_scores.std():.6f}"
                    )
                    if len(raw_scores) > 0:
                        self.logger.log_message(
                            f"{name} raw scores - min: {raw_scores.min():.6f}, max: {raw_scores.max():.6f}, "
                            f"mean: {raw_scores.mean():.6f}, std: {raw_scores.std():.6f}"
                        )

            except Exception as e:
                if self.logger:
                    self.logger.log_message(f"ERROR computing {name} scores: {type(e).__name__}: {e}")
                    import traceback
                    self.logger.log_message(traceback.format_exc())

                # В случае ошибки используем нули
                scores[name] = np.zeros(len(X_train_t))
                scores_raw[name] = np.zeros(len(X_train_t))

            if self.logger:
                self.logger.end_timing(f"{name}_computation")

        return scores, scores_raw