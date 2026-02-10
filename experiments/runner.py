import copy
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

from experiments.logger import debug_print
from config.settings import EXPERIMENT_CONFIG, RANDOM_STATE
from models.factory import ModelFactory
from influence.methods import InfluenceMethods


class ExperimentRunner:
    """Класс для запуска экспериментов"""

    def __init__(self, logger=None):
        self.logger = logger
        self.results = {}

    def train_and_evaluate(self, preprocessor, model_params, X_train, y_train, X_test, y_test, X_val, y_val, n_epochs=50):
        """Обучение и оценка модели"""
        if self.logger:
            self.logger.start_timing("model_training")

        # Подготовка данных
        # Если preprocessor еще не fitted, fitted его. Иначе используем как есть
        if not preprocessor.is_fitted:
            preprocessor.fit(X_train)
        X_train_transformed = preprocessor.transform(X_train)
        X_test_transformed = preprocessor.transform(X_test)

        if hasattr(X_train_transformed, 'toarray'):
            X_train_transformed = X_train_transformed.toarray()
            X_test_transformed = X_test_transformed.toarray()

        # Поддержка K-fold кросс-валидации для оценки
        cv_folds = int(model_params.get('cv_folds', 1)) if model_params.get('cv_folds', None) is not None else 1
        cv_results = None
        if cv_folds and cv_folds > 1:
            if self.logger:
                self.logger.log_message(f"Running {cv_folds}-fold cross-validation for model evaluation...")

            # Выбираем стратегию разделения: Stratified для классификации
            use_stratified = model_params.get('task_type', '').lower() in ['binary_classification', 'multiclass_classification']
            if use_stratified:
                splitter = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=RANDOM_STATE)
            else:
                splitter = KFold(n_splits=cv_folds, shuffle=True, random_state=RANDOM_STATE)

            val_scores = []
            fold_idx = 0
            for train_idx, val_idx in splitter.split(X_train, y_train if use_stratified else None):
                fold_idx += 1
                X_tr_fold, X_val_fold = X_train.iloc[train_idx], X_train.iloc[val_idx]
                y_tr_fold, y_val_fold = y_train.iloc[train_idx], y_train.iloc[val_idx]

                # Копируем предобработчик и подгоняем только на трейне фолда
                preproc_fold = copy.deepcopy(preprocessor)
                preproc_fold.fit(X_tr_fold)
                X_tr_t = preproc_fold.transform(X_tr_fold)
                X_val_t = preproc_fold.transform(X_val_fold)
                if hasattr(X_tr_t, 'toarray'):
                    X_tr_t = X_tr_t.toarray()
                    X_val_t = X_val_t.toarray()

                # Создаем модель для фолда
                model_fold = ModelFactory.create_model(**model_params)

                # Обучаем модель (не используем X_test здесь, только фолд)
                if model_params.get('model_type') == 'pytorch':
                    # Простая обучающая петля для PyTorch -- один прогон эпох
                    for epoch in range(n_epochs):
                        model_fold.fit(X_tr_t, y_tr_fold.values, epochs=1)
                    y_pred = model_fold.predict(X_val_t)
                else:
                    if model_params.get('model_type') == 'lightgbm' or model_params.get('use_distillation', False):
                        model_fold.fit(X_tr_t, y_tr_fold.values, X_val=X_val_t, y_val=y_val_fold.values)
                    else:
                        model_fold.fit(X_tr_t, y_tr_fold.values)
                    y_pred = model_fold.predict(X_val_t)

                val_mae = mean_absolute_error(y_val_fold, y_pred)
                val_scores.append(val_mae)
                if self.logger:
                    self.logger.log_message(f"  Fold {fold_idx}/{cv_folds} - Val MAE: {val_mae:.4f}")

            cv_results = {'mean_val_mae': float(np.mean(val_scores)), 'std_val_mae': float(np.std(val_scores)), 'folds': val_scores}
            if self.logger:
                self.logger.log_message(f"CV results - Mean MAE: {cv_results['mean_val_mae']:.4f}, Std: {cv_results['std_val_mae']:.4f}")

        # Создание модели (финальная подгонка на всем X_train)
        model = ModelFactory.create_model(**model_params)

        history = {'train': [], 'val': [], 'best_epoch': 0, 'best_val_mae': float('inf')}

        # Обучение модели
        if model_params.get('model_type') == 'pytorch':
            best_model_weights = None
            patience = 30  # Early stopping patience
            patience_counter = 0

            for epoch in range(n_epochs):
                train_loss = model.fit(X_train_transformed, y_train.values, epochs=1)
                history['train'].append(train_loss)

                y_pred_test = model.predict(X_test_transformed)
                val_mae = mean_absolute_error(y_test, y_pred_test)
                history['val'].append(val_mae)
                
                # Update learning rate scheduler based on validation loss
                if hasattr(model, 'scheduler'):
                    model.scheduler.step(val_mae)

                if val_mae < history['best_val_mae']:
                    history['best_val_mae'] = val_mae
                    history['best_epoch'] = epoch
                    patience_counter = 0  # Reset patience counter

                    if hasattr(model, 'model'):
                        best_model_weights = {
                            name: param.clone() for name, param in model.model.state_dict().items()
                        }
                else:
                    patience_counter += 1

                if (epoch + 1) % 10 == 0 and self.logger:
                    self.logger.log_message(
                        f"Epoch {epoch + 1}/{n_epochs} - Train Loss: {train_loss:.4f} - Val MAE: {val_mae:.4f} "
                        f"(Best: {history['best_val_mae']:.4f} at epoch {history['best_epoch'] + 1})")

                # Early stopping
                if patience_counter >= patience:
                    if self.logger:
                        self.logger.log_message(f"Early stopping at epoch {epoch + 1} (patience {patience} exceeded)")
                    break

            if best_model_weights is not None and hasattr(model, 'model'):
                model.model.load_state_dict(best_model_weights)
                if self.logger:
                    self.logger.log_message(f"Loaded best PyTorch model from epoch {history['best_epoch'] + 1}")

        else:
            # Для tree-based моделей и дистиллированных моделей
            if model_params.get('model_type') == 'lightgbm' or model_params.get('use_distillation', False):
                train_loss = model.fit(X_train_transformed, y_train.values,
                                       X_val=X_test_transformed, y_val=y_test.values)
            else:
                train_loss = model.fit(X_train_transformed, y_train.values)

            history['train'].append(train_loss)

            y_pred_test = model.predict(X_test_transformed)
            test_mae = mean_absolute_error(y_test, y_pred_test)
            history['val'].append(test_mae)
            history['best_val_mae'] = test_mae
            history['best_epoch'] = 0

        # Финальная оценка на валидационном множестве
        X_final_transformed = preprocessor.transform(X_val)
        if hasattr(X_final_transformed, 'toarray'):
            X_final_transformed = X_final_transformed.toarray()
        y_pred_final = model.predict(X_final_transformed)
        history['final_mae'] = mean_absolute_error(y_val, y_pred_final)

        if self.logger:
            self.logger.end_timing("model_training")

        return history, model

    def run_experiments(self, X_train, y_train, X_test, y_test, X_val, y_val,
                        preprocessor, model_params,
                        n_remove_list=None,
                        n_epochs=50,
                        dataset_config=None
                        ):
        """Запуск экспериментов с удалением данных"""
        if self.logger:
            self.logger.log_message("Starting experiments...")

        if n_remove_list is None:
            n_remove_list = EXPERIMENT_CONFIG['n_remove_list']


        history, model = self.train_and_evaluate(preprocessor, model_params,
                                                 X_train, y_train, X_test, y_test, X_val, y_val, n_epochs)
        self.results['orig'] = history

        pipeline = Pipeline([
            ('preproc', preprocessor),
            ('model', model)
        ])
        removal_strategy = model_params['removal_strategy']
        # Настройка методов влияния
        influence_methods = InfluenceMethods(self.logger, dataset_config=dataset_config)
        methods, _ = influence_methods.setup_methods(pipeline, X_train, y_train,
                                                     X_test, y_test, preprocessor)

        # Вычисление influence scores
        scores, scores_raw = influence_methods.compute_scores(methods, X_train, y_train,
                                                              preprocessor, X_test, y_test, pipeline)

        # Эксперименты с удалением данных
        for method, vals in scores.items():
            if self.logger:
                self.logger.log_message(f"\nProcessing method: {method}")

            self.results[f'{method}_0'] = self.results['orig']  # 0% удаления - baseline

            # Выбираем стратегию удаления в зависимости от типа метода
            # Для influence методов удаляем наиболее влиятельные (highest influence)
            # Для остальных методов удаляем наименее влиятельные (lowest influence)
            is_influence_method = method in ['Influence', 'ArnoldiInfluence', 'CgInfluence', 'LissaInfluence', 'NystroemSketchInfluence']

            if is_influence_method:
                # Для influence методов: удаляем наиболее влиятельные (самые высокие значения)

                if removal_strategy == 'remove_lowest_influence':
                    idx_sorted = np.argsort(vals)[::-1]
                    if self.logger:
                        self.logger.log_message(f"  Using remove_lowest_influence strategy for {method}")
                elif removal_strategy == 'remove_highest_influence':
                    idx_sorted = np.argsort(vals)
                    if self.logger:
                        self.logger.log_message(f"  Using remove_highest_influence strategy for {method}")

                # idx_sorted = np.argsort(vals)[::-1]
                # if self.logger:
                #     self.logger.log_message(f"  Using remove_highest_influence strategy for {method}")


            else:
                # Для остальных методов: удаляем наименее влиятельные (самые низкие значения)
                idx_sorted = np.argsort(vals)
                if self.logger:
                    self.logger.log_message(f"  Using remove_lowest_influence strategy for {method}")

            for pct in n_remove_list:

                n_to_remove = int(len(X_train) * pct / 100)
                n_to_remove = max(1, n_to_remove)
                n_to_remove = min(n_to_remove, len(X_train) - 10)

                remove_idx = idx_sorted[:n_to_remove]
                keep_mask = np.ones(len(X_train), dtype=bool)
                keep_mask[remove_idx] = False

                X_sub, y_sub = X_train.iloc[keep_mask], y_train.iloc[keep_mask]

                if len(X_sub) < 10:
                    if self.logger:
                        self.logger.log_message(f"  Skipping - only {len(X_sub)} samples left (min 10 required)")
                    continue

                # Check if target has only one class for classification tasks
                if dataset_config and dataset_config.task_type in ['binary_classification', 'multiclass_classification']:
                    unique_classes = y_sub.nunique()
                    if unique_classes < 2:
                        if self.logger:
                            self.logger.log_message(f"  Skipping - only {unique_classes} class(es) remaining (need at least 2 for classification)")
                        continue

                key = f'{method}_{pct}pct'
                history, _ = self.train_and_evaluate(preprocessor, model_params,
                                                     X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs)
                self.results[key] = history

        # Случайное удаление - запускаем 5 раз для получения доверительных интервалов
        if self.logger:
            self.logger.log_message("Processing random removal")

        n_random_runs = EXPERIMENT_CONFIG['n_random_runs']
        random_run_results = {}  # Словарь для хранения результатов всех запусков
        
        for run_idx in range(n_random_runs):
            if self.logger:
                self.logger.log_message(f"  Random removal run {run_idx + 1}/{n_random_runs}...")
            
            for pct in n_remove_list:
                n_to_remove = int(len(X_train) * pct / 100)
                n_to_remove = max(1, n_to_remove)
                n_to_remove = min(n_to_remove, len(X_train) - 10)

                # Используем разные random seeds для каждого запуска
                np.random.seed(RANDOM_STATE + run_idx)
                remove_idx = np.random.choice(len(X_train), size=n_to_remove, replace=False)
                keep_mask = np.ones(len(X_train), dtype=bool)
                keep_mask[remove_idx] = False
                X_sub, y_sub = X_train.iloc[keep_mask], y_train.iloc[keep_mask]

                if len(X_sub) < 10:
                    continue

                # Check if target has only one class for classification tasks
                if dataset_config and dataset_config.task_type in ['binary_classification', 'multiclass_classification']:
                    unique_classes = y_sub.nunique()
                    if unique_classes < 2:
                        continue

                # Сохраняем результаты каждого запуска
                key = f'random_{pct}pct_run{run_idx}'
                history, _ = self.train_and_evaluate(preprocessor, model_params,
                                                     X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs)
                self.results[key] = history
                
                # Также сохраняем для вычисления статистики
                if pct not in random_run_results:
                    random_run_results[pct] = []
                random_run_results[pct].append(history['final_mae'])
        
        # Вычисляем и сохраняем статистику для random метода
        self.random_run_results = random_run_results  # Сохраняем для использования в plot
        
        # Сохраняем медианные результаты как основные результаты random метода
        for pct, mae_values in random_run_results.items():
            if mae_values:
                median_mae = np.median(mae_values)
                key = f'random_{pct}pct'
                # Создаём history с медианным значением
                self.results[key] = {'final_mae': median_mae}

        if self.logger:
            self.logger.log_message("All experiments completed!")

        return self.results, scores, scores_raw

    def run_single_experiment(self, X_train, y_train, X_val, y_val,
                              preprocessor, model_params,
                              removal_percentage=0,
                              removal_strategy='remove_lowest_influence',
                              influence_scores=None,
                              n_epochs=50):

        if removal_percentage > 0:
            if influence_scores is None:
                raise ValueError("Influence scores required for non-zero removal")

            n_to_remove = int(len(X_train) * removal_percentage / 100)
            n_to_remove = max(1, n_to_remove)
            n_to_remove = min(n_to_remove, len(X_train) - 10)

            if removal_strategy == 'remove_lowest_influence':
                idx_sorted = np.argsort(influence_scores)
                remove_idx = idx_sorted[:n_to_remove]
            elif removal_strategy == 'remove_highest_influence':
                idx_sorted = np.argsort(influence_scores)
                remove_idx = idx_sorted[::-1][:n_to_remove]
            else:
                raise ValueError(f"Unknown removal strategy: {removal_strategy}")

            keep_mask = np.ones(len(X_train), dtype=bool)
            keep_mask[remove_idx] = False
            X_train = X_train.iloc[keep_mask]
            y_train = y_train.iloc[keep_mask]

        history, model = self.train_and_evaluate(preprocessor, model_params,
                                                 X_train, y_train, X_val, y_val, n_epochs)

        return history, model