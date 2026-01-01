import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
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
            self.logger.log_message("Preparing data for training...")

        # Подготовка данных
        preprocessor.fit(X_train)
        X_train_transformed = preprocessor.transform(X_train)
        X_val_transformed = preprocessor.transform(X_test)

        if hasattr(X_train_transformed, 'toarray'):
            X_train_transformed = X_train_transformed.toarray()
            X_val_transformed = X_val_transformed.toarray()

        # Создание модели
        model = ModelFactory.create_model(**model_params)

        history = {'train': [], 'val': [], 'best_epoch': 0, 'best_val_mae': float('inf')}

        # Обучение модели
        if model_params.get('model_type') == 'pytorch':
            best_model_weights = None

            for epoch in range(n_epochs):
                train_loss = model.fit(X_train_transformed, y_train.values, epochs=1)
                history['train'].append(train_loss)

                y_pred_val = model.predict(X_val_transformed)
                val_mae = mean_absolute_error(y_test, y_pred_val)
                history['val'].append(val_mae)

                if val_mae < history['best_val_mae']:
                    history['best_val_mae'] = val_mae
                    history['best_epoch'] = epoch

                    if hasattr(model, 'model'):
                        best_model_weights = {
                            name: param.clone() for name, param in model.model.state_dict().items()
                        }

                if (epoch + 1) % 10 == 0 and self.logger:
                    self.logger.log_message(
                        f"Epoch {epoch + 1}/{n_epochs} - Train Loss: {train_loss:.4f} - Val MAE: {val_mae:.4f} "
                        f"(Best: {history['best_val_mae']:.4f} at epoch {history['best_epoch'] + 1})")

            if best_model_weights is not None and hasattr(model, 'model'):
                model.model.load_state_dict(best_model_weights)
                if self.logger:
                    self.logger.log_message(f"Loaded best PyTorch model from epoch {history['best_epoch'] + 1}")

        else:
            # Для tree-based моделей и дистиллированных моделей
            if model_params.get('model_type') == 'lightgbm' or model_params.get('use_distillation', False):
                train_loss = model.fit(X_train_transformed, y_train.values,
                                       X_val=X_val_transformed, y_val=y_test.values)
            else:
                train_loss = model.fit(X_train_transformed, y_train.values)

            history['train'].append(train_loss)

            y_pred_val = model.predict(X_val_transformed)
            val_mae = mean_absolute_error(y_test, y_pred_val)
            history['val'].append(val_mae)
            history['best_val_mae'] = val_mae
            history['best_epoch'] = 0

        # Финальная оценка на валидационном множестве
        X_final_transformed = preprocessor.transform(X_test)
        if hasattr(X_final_transformed, 'toarray'):
            X_final_transformed = X_final_transformed.toarray()
        y_pred_final = model.predict(X_final_transformed)
        history['final_mae'] = mean_absolute_error(y_test, y_pred_final)

        if self.logger:
            self.logger.log_message(f"Final validation MAE: {history['final_mae']:.4f}")
            self.logger.end_timing("model_training")

        return history, model

    def run_experiments(self, X_train, y_train, X_test, y_test, X_val, y_val,
                        preprocessor, model_params,
                        n_remove_list=None,
                        n_epochs=50):
        """Запуск экспериментов с удалением данных"""
        if self.logger:
            self.logger.log_message("Starting experiments...")

        if n_remove_list is None:
            n_remove_list = EXPERIMENT_CONFIG['n_remove_list']

        # Комбинируем train и test для обучения (как просил пользователь)
        # X_combined = pd.concat([X_train, X_test], ignore_index=True)
        # y_combined = pd.concat([y_train, y_test], ignore_index=True)

        # if self.logger:
        #     self.logger.log_message(f"Combined training data: {len(X_combined)} samples")
        #     self.logger.log_message("Training baseline model...")

        history, model = self.train_and_evaluate(preprocessor, model_params,
                                                 X_train, y_train, X_test, y_test, X_val, y_val, n_epochs)
        self.results['orig'] = history

        # Создание пайплайна
        pipeline = Pipeline([
            ('preproc', preprocessor),
            ('model', model)
        ])

        # Настройка методов влияния
        influence_methods = InfluenceMethods(self.logger)
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
                idx_sorted = np.argsort(vals)[::-1]  # descending order
                if self.logger:
                    self.logger.log_message(f"  Using remove_highest_influence strategy for {method}")
            else:
                # Для остальных методов: удаляем наименее влиятельные (самые низкие значения)
                idx_sorted = np.argsort(vals)  # ascending order
                if self.logger:
                    self.logger.log_message(f"  Using remove_lowest_influence strategy for {method}")

            for pct in n_remove_list:
                if self.logger:
                    self.logger.log_message(f"  Removing {pct}% of samples...")

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

                key = f'{method}_{pct}pct'
                history, _ = self.train_and_evaluate(preprocessor, model_params,
                                                     X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs)
                self.results[key] = history

        # Случайное удаление (контрольный эксперимент)
        if self.logger:
            self.logger.log_message("Processing random removal...")

        for pct in n_remove_list:
            if self.logger:
                self.logger.log_message(f"  Randomly removing {pct}% of samples...")

            n_to_remove = int(len(X_train) * pct / 100)
            n_to_remove = max(1, n_to_remove)
            n_to_remove = min(n_to_remove, len(X_train) - 10)

            np.random.seed(RANDOM_STATE)
            remove_idx = np.random.choice(len(X_train), size=n_to_remove, replace=False)
            keep_mask = np.ones(len(X_train), dtype=bool)
            keep_mask[remove_idx] = False
            X_sub, y_sub = X_train.iloc[keep_mask], y_train.iloc[keep_mask]

            if len(X_sub) < 10:
                if self.logger:
                    self.logger.log_message(f"  Skipping - only {len(X_sub)} samples left (min 10 required)")
                continue

            key = f'random_{pct}pct'
            history, _ = self.train_and_evaluate(preprocessor, model_params,
                                                 X_sub, y_sub, X_test, y_test, X_val, y_val, n_epochs)
            self.results[key] = history

        if self.logger:
            self.logger.log_message("All experiments completed!")

        return self.results, scores, scores_raw

    def run_single_experiment(self, X_train, y_train, X_val, y_val,
                              preprocessor, model_params,
                              removal_percentage=0,
                              removal_strategy='remove_lowest_influence',
                              influence_scores=None,
                              n_epochs=50):
        """Запуск одиночного эксперимента"""
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