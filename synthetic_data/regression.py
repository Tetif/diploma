import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, Subset
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
from pydvl.valuation.dataset import Dataset
from pydvl.valuation.utility import ModelUtility
from pydvl.valuation.scorers import SupervisedScorer
from pydvl.valuation.methods.loo import LOOValuation
from pydvl.valuation.methods.shapley import ShapleyValuation
from pydvl.valuation.methods.beta_shapley import BetaShapleyValuation
from pydvl.valuation.samplers import PermutationSampler
from pydvl.valuation.stopping import HistoryDeviation, MaxUpdates
from pydvl.influence.torch import DirectInfluence
from pydvl.influence import InfluenceMode
from joblib import parallel_config
import os
from config.settings import SYNTHETIC_DATA_CONFIG, RANDOM_STATE
from scipy.stats import rankdata
import warnings

warnings.filterwarnings('ignore')

# Настройки
np.set_printoptions(precision=6, suppress=True)
torch.manual_seed(42)
np.random.seed(42)

DEBUG_MODE = False


def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print("[DEBUG]", *args, **kwargs)


# Параметры данных
n_points = 1000
noise_sigmas = [0.5, 2.0]
outlier_fracs = [0.01, 0.5]
outlier_sigma = 10.0
x_range = (-10, 10)
train_frac = 0.8
batch_size = SYNTHETIC_DATA_CONFIG['batch_size']
lr = SYNTHETIC_DATA_CONFIG['learning_rate']
n_epochs = SYNTHETIC_DATA_CONFIG['n_epochs']
ns = [10, 100, 500]


class RegressionNN(nn.Module):
    def __init__(self, input_size=1, hidden_size=50):
        super(RegressionNN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1)
        )

    def forward(self, x):
        return self.network(x)


class PyTorchRegressionModel:
    def __init__(self, input_size=1, device='cpu'):
        self.device = device
        self.model = RegressionNN(input_size).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def fit(self, X, y, epochs=10):
        X_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).reshape(-1, 1).to(self.device)

        self.model.train()
        total_loss = 0
        for epoch in range(epochs):
            self.optimizer.zero_grad()
            predictions = self.model(X_tensor)
            loss = self.criterion(predictions, y_tensor)
            loss.backward()
            self.optimizer.step()
            total_loss += loss.item()
        return total_loss / epochs

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X).to(self.device)
            return self.model(X_tensor).cpu().numpy()

    def named_parameters(self):
        return self.model.named_parameters()


def generate_regression_data():
    """Генерация данных для регрессии"""
    datasets_full = {}
    for sigma in noise_sigmas:
        for frac in outlier_fracs:
            x = np.random.uniform(x_range[0], x_range[1], size=n_points)
            y = x + np.random.normal(0, sigma, size=n_points)
            n_outliers = int(n_points * frac)
            out_idx = np.random.choice(n_points, size=n_outliers, replace=False)
            mask = np.ones(n_points, dtype=bool)
            mask[out_idx] = False
            signs = np.where(np.random.rand(n_outliers) < 0.5, -1, +1)
            y[out_idx] = x[out_idx] + signs * np.random.exponential(scale=outlier_sigma, size=n_outliers)
            datasets_full[(sigma, frac)] = (x, y, mask)

    # Разделение на train/test
    datasets_train, datasets_test = {}, {}
    for key, (x, y, mask) in datasets_full.items():
        n = len(x)
        perm = np.random.permutation(n)
        split = int(train_frac * n)
        train_idx, test_idx = perm[:split], perm[split:]
        datasets_train[key] = (x[train_idx], y[train_idx], mask[train_idx])
        datasets_test[key] = (x[test_idx], y[test_idx], mask[test_idx])

    return datasets_full, datasets_train, datasets_test


def plot_regression_data(datasets, noise_sigmas, outlier_fracs, title_prefix=""):
    """Визуализация данных регрессии"""
    n_rows = len(noise_sigmas)
    n_cols = len(outlier_fracs)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 4 * n_rows), squeeze=False)
    for i, sigma in enumerate(noise_sigmas):
        for j, frac in enumerate(outlier_fracs):
            x, y, mask = datasets[(sigma, frac)]
            ax = axes[i][j]
            # Отображаем выбросы красным
            outlier_indices = np.where(~mask)[0]
            ax.scatter(x[mask], y[mask], s=5, alpha=0.5, label='Inliers')
            ax.scatter(x[outlier_indices], y[outlier_indices], s=5, alpha=0.5, color='red', label='Outliers')
            ax.set_title(f"{title_prefix} σ={sigma}, outliers={int(frac * 100)}%")
            ax.set_xlim(x_range)
            ax.set_ylim(x_range)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            if i == 0 and j == 0:
                ax.legend()
    plt.tight_layout()
    plt.show()


def train_and_evaluate_model_with_history(X_train, y_train, X_val, y_val, n_epochs=10):
    """Обучение и оценка модели регрессии с полной историей"""
    # Преобразуем данные в тензоры
    X_train_tensor = torch.FloatTensor(X_train.reshape(-1, 1))
    y_train_tensor = torch.FloatTensor(y_train.reshape(-1, 1))
    X_val_tensor = torch.FloatTensor(X_val.reshape(-1, 1))
    y_val_tensor = torch.FloatTensor(y_val.reshape(-1, 1))

    # Создаем DataLoader'ы
    train_ds = TensorDataset(X_train_tensor, y_train_tensor)
    val_ds = TensorDataset(X_val_tensor, y_val_tensor)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    # Создаем и обучаем модель
    model = RegressionNN(input_size=1)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    def train_one_epoch():
        model.train()
        total_loss = 0
        for xb, yb in train_loader:
            optimizer.zero_grad()
            pred = model(xb)
            loss = criterion(pred, yb)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * xb.size(0)
        return total_loss / len(train_loader.dataset)

    def evaluate():
        model.eval()
        total_loss = 0
        predictions, targets = [], []
        with torch.no_grad():
            for xb, yb in val_loader:
                pred = model(xb)
                total_loss += criterion(pred, yb).item() * xb.size(0)
                predictions.append(pred.numpy())
                targets.append(yb.numpy())

        predictions = np.vstack(predictions).flatten()
        targets = np.vstack(targets).flatten()

        mse = total_loss / len(val_loader.dataset)
        r2 = r2_score(targets, predictions)

        return mse, r2

    history = {'val_mse': [], 'val_r2': [], 'train_loss': []}
    for epoch in range(n_epochs):
        train_loss = train_one_epoch()
        mse, r2 = evaluate()
        history['val_mse'].append(mse)
        history['val_r2'].append(r2)
        history['train_loss'].append(train_loss)
        debug_print(f"Epoch {epoch + 1}/{n_epochs}: Train Loss: {train_loss:.4f}, Val MSE: {mse:.4f}, Val R²: {r2:.4f}")

    return history, model


class ModelWrapper:
    """Wrapper для модели с методами, которые ожидает pyDVL"""

    def __init__(self, model):
        self.model = model
        self.criterion = nn.MSELoss()

    def fit(self, X, y):
        """Dummy fit method для совместимости с pyDVL"""
        # В pyDVL для utility вычислений нам не нужно переобучать модель
        # Мы используем предобученную модель
        pass

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            if hasattr(X, 'values'):
                X = X.values
            X_tensor = torch.FloatTensor(X.reshape(-1, 1))
            output = self.model(X_tensor)
            return output.numpy().flatten()


def make_regression_scorer(fail_score=-1e6):
    """Scorer для задачи регрессии с улучшенной обработкой"""

    def regression_scorer(model, x, y):
        try:
            debug_print(
                f"Scorer called with x: {x.shape if hasattr(x, 'shape') else 'unknown'}, y: {y.shape if hasattr(y, 'shape') else 'unknown'}")

            # Конвертируем данные
            if hasattr(x, 'values'):
                x_np = x.values
            else:
                x_np = np.asarray(x)

            if hasattr(y, 'values'):
                y_np = y.values
            else:
                y_np = np.asarray(y)

            y_np = y_np.reshape(-1)
            debug_print(f"Converted to numpy - x: {x_np.shape}, y: {y_np.shape}")

            # Получаем предсказания
            if hasattr(model, "predict"):
                y_pred = model.predict(x_np)
                debug_print("Used model.predict()")
            else:
                # Прямой вызов torch модели
                model_module = getattr(model, "model", model)
                if hasattr(model_module, "eval"):
                    model_module.eval()
                with torch.no_grad():
                    device = next(model_module.parameters()).device
                    tx = torch.FloatTensor(x_np).to(device)
                    out = model_module(tx)
                    y_pred = out.cpu().numpy()
                    debug_print("Used direct torch model forward pass")

            # Конвертируем предсказания
            if torch.is_tensor(y_pred):
                y_pred = y_pred.detach().cpu().numpy()
            y_pred = np.asarray(y_pred).reshape(-1)

            debug_print(
                f"Prediction stats - min: {y_pred.min():.6f}, max: {y_pred.max():.6f}, mean: {y_pred.mean():.6f}")
            debug_print(f"True stats - min: {y_np.min():.6f}, max: {y_np.max():.6f}, mean: {y_np.mean():.6f}")

            # Проверяем размеры
            min_len = min(len(y_np), len(y_pred))
            if min_len == 0:
                debug_print("ERROR: Zero length arrays!")
                return float(fail_score)

            y_true = y_np[:min_len]
            y_pred = y_pred[:min_len]

            # Проверяем на NaN/Inf
            if not np.isfinite(y_pred).all():
                debug_print("ERROR: Non-finite values in predictions!")
                return float(fail_score)
            if not np.isfinite(y_true).all():
                debug_print("ERROR: Non-finite values in true values!")
                return float(fail_score)

            # Вычисляем отрицательный MSE (чтобы больше = лучше)
            mse = float(np.mean((y_pred - y_true) ** 2))
            score = -mse

            debug_print(f"Computed MSE: {mse:.6f}, Score: {score:.6f}")

            if not np.isfinite(score):
                debug_print("ERROR: Non-finite score!")
                return float(fail_score)

            # Ограничиваем и возвращаем значение
            score = float(np.clip(score, -1e9, 0.0))
            debug_print(f"Final score: {score:.6f}")

            return score

        except Exception as e:
            debug_print(f"ERROR in regression scorer: {type(e).__name__}: {e}")
            import traceback
            debug_print(traceback.format_exc())
            return float(fail_score)

    return regression_scorer


def get_influence_methods(model_wrapper, X_train, y_train, X_val, y_val):
    """Подготовка методов оценки влияния для регрессии"""
    print("\n" + "=" * 60)
    print("SETTING UP INFLUENCE METHODS FOR REGRESSION")
    print("=" * 60)

    # Создаем Dataset
    X_train_arr = np.asarray(X_train).reshape(-1, 1)
    X_val_arr = np.asarray(X_val).reshape(-1, 1)
    y_train_arr = np.asarray(y_train).reshape(-1)
    y_val_arr = np.asarray(y_val).reshape(-1)

    # Создаем DataFrame
    X_train_df = pd.DataFrame(X_train_arr, columns=['x'])
    X_val_df = pd.DataFrame(X_val_arr, columns=['x'])
    y_train_series = pd.Series(y_train_arr, name='y')
    y_val_series = pd.Series(y_val_arr, name='y')

    debug_print("Creating Dataset...")
    try:
        val_dataset = Dataset(X_train_df, y_train_series, X_val_df, y_val_series)
        debug_print("Dataset created successfully")
    except Exception as e:
        debug_print(f"Dataset creation failed: {e}")
        val_dataset = Dataset(X_train_arr, y_train_arr.reshape(-1, 1), X_val_arr, y_val_arr.reshape(-1, 1))

    # Создаем scorer для регрессии
    scorer_callable = make_regression_scorer()

    # Тестируем scorer
    debug_print("Testing scorer on validation data...")
    val_score = scorer_callable(model_wrapper, X_val_arr, y_val_arr)
    debug_print(f"Scorer on validation data: {val_score}")

    debug_print("Testing scorer on training data...")
    train_score = scorer_callable(model_wrapper, X_train_arr, y_train_arr)
    debug_print(f"Scorer on training data: {train_score}")

    supervised_scorer = SupervisedScorer(
        scoring=scorer_callable,
        test_data=val_dataset,
        default=float(-1e6),
        range=None
    )

    utility = ModelUtility(
        model=model_wrapper,
        scorer=supervised_scorer,
        show_warnings=True
    )

    # Тестируем utility на разных подмножествах
    debug_print("Testing utility on different subsets...")
    try:
        # Тест на полном наборе
        full_mask = [True] * len(X_train_arr)
        full_score = utility(full_mask)
        debug_print(f"Utility full set score: {full_score}")

        # Тест на пустом наборе
        empty_mask = [False] * len(X_train_arr)
        empty_score = utility(empty_mask)
        debug_print(f"Utility empty set score: {empty_score}")

        # Тест на частичном наборе
        if len(X_train_arr) > 10:
            subset_mask = [True] * 5 + [False] * (len(X_train_arr) - 5)
            subset_score = utility(subset_mask)
            debug_print(f"Utility subset (5 samples) score: {subset_score}")

            # Тест на другом подмножестве
            subset2_mask = [False] * 5 + [True] * 5 + [False] * (len(X_train_arr) - 10)
            subset2_score = utility(subset2_mask)
            debug_print(f"Utility subset2 (different 5 samples) score: {subset2_score}")

            # Проверяем, что scores разные (это важно!)
            if abs(subset_score - subset2_score) < 1e-6:
                debug_print("WARNING: Utility returns same scores for different subsets!")
            else:
                debug_print("GOOD: Utility returns different scores for different subsets")

    except Exception as e:
        debug_print(f"Utility test failed: {e}")
        import traceback
        debug_print(traceback.format_exc())

    # Инициализация методов
    methods = {}

    try:
        with parallel_config(backend="threading", n_jobs=SYNTHETIC_DATA_CONFIG['n_jobs']):
            debug_print("Initializing LOO...")
            methods['LOO'] = LOOValuation(
                utility=utility,
                progress=True
            )

            debug_print("Initializing DataShapley...")
            methods['DataShapley'] = ShapleyValuation(
                utility=utility,
                sampler=PermutationSampler(truncation=None, seed=42),
                is_done=HistoryDeviation(n_steps=10, rtol=0.1) | MaxUpdates(50),  # Уменьшили для тестирования
                progress=True
            )

            debug_print("Initializing BetaShapley...")
            methods['BetaShapley'] = BetaShapleyValuation(
                utility=utility,
                sampler=PermutationSampler(truncation=None, seed=42),
                is_done=HistoryDeviation(n_steps=10, rtol=0.1) | MaxUpdates(100),  # Уменьшили для тестирования
                alpha=0.1, beta=0.1,
                progress=True
            )

            debug_print("Initializing Influence...")
            methods['Influence'] = DirectInfluence(
                getattr(model_wrapper, "model", model_wrapper),
                nn.MSELoss(),
                regularization=1e-4
            )
    except Exception as e:
        debug_print(f"Error initializing methods: {e}")
        import traceback
        debug_print(traceback.format_exc())

    print("Methods initialization completed!")
    return methods


def _extract_numeric_values_from_result(result):
    """Расширенная диагностика извлечения значений из результатов pyDVL"""
    debug_print(f"Extracting values from result type: {type(result)}")

    # Пробуем разные методы извлечения
    extraction_methods = [
        ('values()', lambda: result.values()),
        ('dict values', lambda: list(result.values()) if hasattr(result, 'values') else None),
        ('iteration', lambda: list(result)),
        ('direct access', lambda: [v for v in result] if hasattr(result, '__iter__') else None)
    ]

    for method_name, method in extraction_methods:
        try:
            items = method()
            if items is not None:
                print(
                    f"Success with {method_name}, got {len(list(items)) if hasattr(items, '__len__') else 'unknown'} items")
                items_list = list(items) if hasattr(items, '__iter__') and not isinstance(items, (int, float)) else [
                    items]
                break
        except Exception as e:
            print(f"Failed {method_name}: {e}")
            continue
    else:
        print("All extraction methods failed, returning zeros")
        return np.array([])

    numeric = []
    debug_print(f"Processing {len(items_list)} items...")

    for i, v in enumerate(items_list):
        if v is None:
            numeric.append(0.0)
            continue

        # Пробуем разные способы извлечения числового значения
        value_extractors = [
            ('direct', lambda x: float(x)),
            ('.value', lambda x: float(x.value)),
            ('.val', lambda x: float(x.val)),
            ('dict value', lambda x: float(x.get('value', 0)) if isinstance(x, dict) else None),
            ('dict val', lambda x: float(x.get('val', 0)) if isinstance(x, dict) else None),
        ]

        extracted = None
        for extractor_name, extractor in value_extractors:
            try:
                extracted = extractor(v)
                if i < 5:  # Выводим только первые 5 значений для отладки
                    debug_print(f"Item {i}: successfully extracted value {extracted} using {extractor_name}")
                break
            except (AttributeError, TypeError, ValueError, KeyError):
                continue

        if extracted is None:
            if i < 5:  # Выводим только первые 5 ошибок для отладки
                debug_print(f"Item {i}: failed to extract value from {type(v)}: {v}")
            numeric.append(0.0)
        else:
            numeric.append(extracted)

    result_array = np.asarray(numeric)

    # ДЕТАЛЬНАЯ СТАТИСТИКА ПЕРЕД ЛЮБЫМИ ПРЕОБРАЗОВАНИЯМИ
    if len(result_array) > 0:
        # Ищем реальные диапазоны, игнорируя выбросы
        finite_mask = np.isfinite(result_array)
        if np.any(finite_mask):
            finite_vals = result_array[finite_mask]

            # Используем процентили чтобы отсечь выбросы
            p1 = np.percentile(finite_vals, 1)
            p99 = np.percentile(finite_vals, 99)
            median = np.median(finite_vals)
            mean = np.mean(finite_vals)

            print(f"RAW VALUES BEFORE PROCESSING:")
            print(f"  Min: {np.min(finite_vals):.10f}")
            print(f"  Max: {np.max(finite_vals):.10f}")
            print(f"  Mean: {mean:.10f}")
            print(f"  Median: {median:.10f}")
            print(f"  P1: {p1:.10f}")
            print(f"  P99: {p99:.10f}")
            print(f"  Std: {np.std(finite_vals):.10f}")

            # Проверяем, не все ли значения одинаковые
            if np.max(finite_vals) - np.min(finite_vals) < 1e-10:
                debug_print("WARNING: All values are essentially the same!")
            else:
                debug_print(f"Value range: {np.max(finite_vals) - np.min(finite_vals):.10f}")

            # Проверяем, не слишком ли маленькие значения
            abs_vals = np.abs(finite_vals)
            if np.max(abs_vals) < 1e-6:
                debug_print("WARNING: Values are very small, might be rounded to zero")

        else:
            debug_print("WARNING: No finite values found!")

    return result_array


def compute_influence_scores(methods, X_train, y_train, X_val, y_val):
    """Вычисление influence scores для регрессии с улучшенной обработкой"""
    print("\n" + "=" * 60)
    print("COMPUTING INFLUENCE SCORES FOR REGRESSION")
    print("=" * 60)

    X_train_arr = np.asarray(X_train).reshape(-1, 1)
    X_val_arr = np.asarray(X_val).reshape(-1, 1)
    y_train_arr = np.asarray(y_train).reshape(-1)
    y_val_arr = np.asarray(y_val).reshape(-1)

    # Создаем Dataset для обучения
    X_train_df = pd.DataFrame(X_train_arr, columns=['x'])
    X_val_df = pd.DataFrame(X_val_arr, columns=['x'])
    y_train_series = pd.Series(y_train_arr, name='y')
    y_val_series = pd.Series(y_val_arr, name='y')

    try:
        train_dataset = Dataset(X_train_df, y_train_series, X_val_df, y_val_series)
        debug_print("Training dataset created successfully with DataFrame")
    except Exception as e:
        debug_print(f"DataFrame training dataset failed: {e}, using arrays")
        train_dataset = Dataset(X_train_arr, y_train_arr.reshape(-1, 1), X_val_arr, y_val_arr.reshape(-1, 1))

    scores = {}
    scores_pre = {}

    for name, method in methods.items():
        print(f"\n--- Computing {name} scores ---")
        try:
            if name == 'Influence':
                debug_print("Using DirectInfluence method...")

                train_loader = DataLoader(
                    TensorDataset(
                        torch.FloatTensor(X_train_arr),
                        torch.FloatTensor(y_train_arr.reshape(-1, 1))
                    ),
                    batch_size=32,
                    shuffle=False
                )

                debug_print("Fitting influence model...")
                infl = method.fit(train_loader)

                debug_print("Computing influence factors...")
                zf = infl.influence_factors(
                    torch.FloatTensor(X_val_arr),
                    torch.FloatTensor(y_val_arr.reshape(-1, 1))
                )

                debug_print("Computing influences from factors...")
                scores_raw = infl.influences_from_factors(
                    zf,
                    torch.FloatTensor(X_train_arr),
                    torch.FloatTensor(y_train_arr.reshape(-1, 1)),
                    mode=InfluenceMode.Up
                ).cpu().numpy()

                debug_print(f"Raw influence scores shape: {scores_raw.shape}")

                # Агрегируем влияния
                if scores_raw.ndim == 2:
                    per_train = np.abs(scores_raw).sum(axis=0)
                else:
                    per_train = np.abs(scores_raw).flatten()

                debug_print(
                    f"Aggregated scores stats - min: {per_train.min()}, max: {per_train.max()}, mean: {per_train.mean()}")

                # Сохраняем сырые значения
                scores_pre[name] = per_train.copy()

                if per_train.max() > per_train.min():
                    scaled = (per_train - per_train.min()) / (per_train.max() - per_train.min() + 1e-10)
                else:
                    scaled = np.ones_like(per_train) * 0.5
                    debug_print("All influence scores are equal, using uniform")

                scores[name] = scaled

            else:
                # Для Shapley методов
                debug_print(f"Using {name} method with utility...")
                with parallel_config(backend="threading", n_jobs=SYNTHETIC_DATA_CONFIG['n_jobs']):
                    debug_print("Fitting valuation method...")
                    result = method.fit(train_dataset)
                    debug_print(f"Result type: {type(result)}")

                # Извлекаем значения с улучшенной диагностикой
                values_arr = _extract_numeric_values_from_result(result)
                debug_print(f"Extracted {len(values_arr)} values for {name}")

                if values_arr.size == 0:
                    debug_print(f"WARNING: No values extracted for {name}, using uniform")
                    scores[name] = np.ones(len(X_train_arr)) * 0.5
                    scores_pre[name] = np.array([])
                    continue

                # Сохраняем сырые значения
                scores_pre[name] = values_arr.copy()

                # УЛУЧШЕННАЯ ОБРАБОТКА МАСШТАБОВ
                finite_mask = np.isfinite(values_arr)
                if not finite_mask.all():
                    debug_print(f"WARNING: Non-finite values in {name}: {np.sum(~finite_mask)}/{len(values_arr)}")
                    finite_vals = values_arr[finite_mask]
                    fill_val = np.median(finite_vals) if finite_vals.size > 0 else 0.0
                    values_arr[~finite_mask] = fill_val

                # СПЕЦИАЛЬНАЯ ОБРАБОТКА ДЛЯ ОЧЕНЬ МАЛЕНЬКИХ ЗНАЧЕНИЙ
                abs_vals = np.abs(values_arr)
                max_abs = np.max(abs_vals) if len(abs_vals) > 0 else 1.0

                if max_abs < 1e-10:
                    debug_print(f"WARNING: All values for {name} are near zero, using uniform distribution")
                    scores[name] = np.ones(len(values_arr)) * 0.5
                    continue
                elif max_abs < 1e-6:
                    debug_print(f"WARNING: Values for {name} are very small, scaling up for better precision")
                    scale_factor = 1e6 / max_abs if max_abs > 0 else 1e6
                    values_arr = values_arr * scale_factor
                    debug_print(f"Scaled values by {scale_factor:.2f}")

                # РАЗДЕЛЬНАЯ ОБРАБОТКА ПОЛОЖИТЕЛЬНЫХ И ОТРИЦАТЕЛЬНЫХ ЗНАЧЕНИЙ
                positive_vals = values_arr[values_arr > 0]
                negative_vals = values_arr[values_arr < 0]
                zero_vals = values_arr[values_arr == 0]

                debug_print(
                    f"Value distribution: {len(positive_vals)} positive, {len(negative_vals)} negative, {len(zero_vals)} zero")

                if len(positive_vals) > 0 and len(negative_vals) > 0:
                    debug_print("Mixed positive/negative values - using signed rank normalization")
                    signed_ranks = rankdata(np.abs(values_arr), method="average") * np.sign(values_arr)
                    min_rank = np.min(signed_ranks)
                    max_rank = np.max(signed_ranks)
                    if max_rank > min_rank:
                        scaled = (signed_ranks - min_rank) / (max_rank - min_rank)
                    else:
                        scaled = np.ones_like(signed_ranks) * 0.5
                else:
                    try:
                        ranks = rankdata(values_arr, method="average")
                        if len(values_arr) > 1:
                            scaled = (ranks - 1) / (len(values_arr) - 1)
                        else:
                            scaled = np.ones_like(ranks) * 0.5
                        debug_print(f"Standard rank normalization successful for {name}")
                    except Exception as e:
                        debug_print(f"Rank normalization failed for {name}: {e}, using winsorized min-max")
                        lo = np.percentile(values_arr, 5)
                        hi = np.percentile(values_arr, 95)
                        vals_clip = np.clip(values_arr, lo, hi)
                        if hi > lo:
                            scaled = (vals_clip - lo) / (hi - lo)
                        else:
                            scaled = np.ones_like(vals_clip) * 0.5

                scores[name] = scaled

            # Финальная статистика
            final_scores = scores[name]
            raw_scores = scores_pre[name] if name in scores_pre else np.array([])

            print(f"FINAL {name} - min: {final_scores.min():.6f}, max: {final_scores.max():.6f}, "
                  f"mean: {final_scores.mean():.6f}, std: {final_scores.std():.6f}")

            if raw_scores.size > 0:
                print(f"RAW {name} - min: {raw_scores.min():.6f}, max: {raw_scores.max():.6f}, "
                      f"mean: {raw_scores.mean():.6f}, std: {raw_scores.std():.6f}")

            if np.allclose(final_scores, 0.5, atol=0.01):
                debug_print(f"WARNING: All {name} scores are ~0.5 - this indicates a problem!")

        except Exception as e:
            print(f"ERROR computing {name} scores: {type(e).__name__}: {e}")
            import traceback
            print(traceback.format_exc())
            scores[name] = np.ones(len(X_train_arr)) * 0.5
            scores_pre[name] = np.zeros(len(X_train_arr))

    return scores, scores_pre


def run_regression_experiments(datasets_train, datasets_test, noise_sigmas, outlier_fracs, n_epochs=10):
    """Запуск экспериментов для регрессии с исправленной историей"""
    results = {}
    all_scores = {}

    for (sigma, frac), (X_train_np, y_train_np, mask_train) in datasets_train.items():
        print(f"\n{'=' * 50}")
        print(f"Processing dataset: σ={sigma}, outliers={int(frac * 100)}%")
        print(f"{'=' * 50}")

        X_val_np, y_val_np, mask_val = datasets_test[(sigma, frac)]

        # Обучаем baseline модель
        print("Training baseline model...")
        baseline_history, baseline_model = train_and_evaluate_model_with_history(
            X_train_np, y_train_np, X_val_np, y_val_np, n_epochs
        )

        # Создаем wrapper для pyDVL
        model_wrapper = ModelWrapper(baseline_model)

        # Получаем методы влияния
        methods = get_influence_methods(
            model_wrapper, X_train_np, y_train_np, X_val_np, y_val_np
        )

        # Вычисляем scores
        scores, scores_pre = compute_influence_scores(
            methods, X_train_np, y_train_np, X_val_np, y_val_np
        )

        all_scores[(sigma, frac)] = scores

        # Создаем DataLoader для экспериментов с удалением
        X_train_tensor = torch.FloatTensor(X_train_np.reshape(-1, 1))
        y_train_tensor = torch.FloatTensor(y_train_np.reshape(-1, 1))
        train_ds = TensorDataset(X_train_tensor, y_train_tensor)

        # Эксперименты с удалением данных
        train_size = len(X_train_np)
        random_hist, method_hists = {}, {k: {} for k in methods}

        for n_remove in ns:
            print(f"Testing removal of {n_remove} samples...")

            # Случайное удаление
            idxs = np.random.choice(train_size, n_remove, replace=False)
            keep = [i for i in range(train_size) if i not in idxs]

            # Обучаем модель на уменьшенном наборе с полной историей
            history_rand, model_rand = train_and_evaluate_model_with_history(
                X_train_np[keep], y_train_np[keep], X_val_np, y_val_np, n_epochs
            )

            random_hist[n_remove] = history_rand

            # Удаление на основе influence scores
            for name, score_vals in scores.items():
                if len(score_vals) == 0:
                    continue

                worst = np.argsort(score_vals)[:n_remove]
                keep_m = [i for i in range(train_size) if i not in worst]

                # Обучаем модель на уменьшенном наборе с полной историей
                history_method, model_method = train_and_evaluate_model_with_history(
                    X_train_np[keep_m], y_train_np[keep_m], X_val_np, y_val_np, n_epochs
                )

                method_hists[name][n_remove] = history_method

        results[(sigma, frac)] = {
            'orig': baseline_history,
            'random': random_hist,
            **method_hists
        }

    return results, all_scores


def plot_regression_results(results, noise_sigmas, outlier_fracs, ns, n_epochs=10):
    """Визуализация результатов для регрессии с исправленными данными"""

    epochs = np.arange(1, n_epochs + 1)

    for n_remove in ns:
        # Графики R^2
        fig, axes = plt.subplots(
            len(noise_sigmas), len(outlier_fracs),
            figsize=(5 * len(outlier_fracs), 4 * len(noise_sigmas)),
            constrained_layout=True
        )

        # Обработка разных случаев размерности axes
        if not isinstance(axes, np.ndarray):
            axes = np.array([[axes]])
        elif len(noise_sigmas) == 1 and len(outlier_fracs) == 1:
            axes = np.array([[axes]])
        elif len(noise_sigmas) == 1:
            axes = axes[np.newaxis, :]
        elif len(outlier_fracs) == 1:
            axes = axes[:, np.newaxis]

        for i, sigma in enumerate(noise_sigmas):
            for j, frac in enumerate(outlier_fracs):
                ax = axes[i][j]
                res = results[(sigma, frac)]

                # Проверяем, что у нас есть данные для всех эпох
                if 'val_r2' in res['orig'] and len(res['orig']['val_r2']) == n_epochs:
                    ax.plot(epochs, res['orig']['val_r2'], marker='o', label='Orig', linewidth=2)

                if n_remove in res['random'] and 'val_r2' in res['random'][n_remove] and len(
                        res['random'][n_remove]['val_r2']) == n_epochs:
                    ax.plot(epochs, res['random'][n_remove]['val_r2'], marker='s', label='Random', linewidth=2)

                for name in ['LOO', 'DataShapley', 'BetaShapley', 'Influence']:
                    if (name in res and n_remove in res[name] and
                            'val_r2' in res[name][n_remove] and
                            len(res[name][n_remove]['val_r2']) == n_epochs):
                        ax.plot(epochs, res[name][n_remove]['val_r2'], marker='^', label=name, linewidth=2)

                ax.set_title(f"σ={sigma}, outliers={int(frac * 100)}%")
                ax.set_xlabel('Epoch')
                ax.set_ylabel('R² Score')
                ax.grid(True, alpha=0.3)

                if i == 0 and j == 0:
                    ax.legend(fontsize=8)

        plt.suptitle(f"R² Score (remove={n_remove})")
        plt.show()

        # Графики MSE
        fig, axes = plt.subplots(
            len(noise_sigmas), len(outlier_fracs),
            figsize=(5 * len(outlier_fracs), 4 * len(noise_sigmas)),
            constrained_layout=True
        )

        # Обработка разных случаев размерности axes
        if not isinstance(axes, np.ndarray):
            axes = np.array([[axes]])
        elif len(noise_sigmas) == 1 and len(outlier_fracs) == 1:
            axes = np.array([[axes]])
        elif len(noise_sigmas) == 1:
            axes = axes[np.newaxis, :]
        elif len(outlier_fracs) == 1:
            axes = axes[:, np.newaxis]

        for i, sigma in enumerate(noise_sigmas):
            for j, frac in enumerate(outlier_fracs):
                ax = axes[i][j]
                res = results[(sigma, frac)]

                # Проверяем, что у нас есть данные для всех эпох
                if 'val_mse' in res['orig'] and len(res['orig']['val_mse']) == n_epochs:
                    ax.plot(epochs, res['orig']['val_mse'], marker='o', label='Orig', linewidth=2)

                if n_remove in res['random'] and 'val_mse' in res['random'][n_remove] and len(
                        res['random'][n_remove]['val_mse']) == n_epochs:
                    ax.plot(epochs, res['random'][n_remove]['val_mse'], marker='s', label='Random', linewidth=2)

                for name in ['LOO', 'DataShapley', 'BetaShapley', 'Influence']:
                    if (name in res and n_remove in res[name] and
                            'val_mse' in res[name][n_remove] and
                            len(res[name][n_remove]['val_mse']) == n_epochs):
                        ax.plot(epochs, res[name][n_remove]['val_mse'], marker='^', label=name, linewidth=2)

                ax.set_title(f"σ={sigma}, outliers={int(frac * 100)}%")
                ax.set_xlabel('Epoch')
                ax.set_ylabel('MSE')
                ax.grid(True, alpha=0.3)

                if i == 0 and j == 0:
                    ax.legend(fontsize=8)

        plt.suptitle(f"MSE (remove={n_remove})")
        plt.show()

    # Финальный график изменения R^2 (только последние значения)
    fig, axes = plt.subplots(
        len(noise_sigmas), len(outlier_fracs),
        figsize=(5 * len(outlier_fracs), 4 * len(noise_sigmas)),
        constrained_layout=True
    )

    # Обработка разных случаев размерности axes
    if not isinstance(axes, np.ndarray):
        axes = np.array([[axes]])
    elif len(noise_sigmas) == 1 and len(outlier_fracs) == 1:
        axes = np.array([[axes]])
    elif len(noise_sigmas) == 1:
        axes = axes[np.newaxis, :]
    elif len(outlier_fracs) == 1:
        axes = axes[:, np.newaxis]

    for i, sigma in enumerate(noise_sigmas):
        for j, frac in enumerate(outlier_fracs):
            ax = axes[i][j]
            res = results[(sigma, frac)]

            base = res['orig']['val_r2'][-1] if 'val_r2' in res['orig'] else 0
            delta_rnd = []
            for n in ns:
                if (n in res['random'] and 'val_r2' in res['random'][n] and
                        len(res['random'][n]['val_r2']) > 0):
                    delta_rnd.append(res['random'][n]['val_r2'][-1] - base)
                else:
                    delta_rnd.append(0)

            ax.plot(ns, delta_rnd, marker='^', label='Random', linewidth=2)

            for name in ['LOO', 'DataShapley', 'BetaShapley', 'Influence']:
                if name in res:
                    delta_method = []
                    for n in ns:
                        if (n in res[name] and 'val_r2' in res[name][n] and
                                len(res[name][n]['val_r2']) > 0):
                            delta_method.append(res[name][n]['val_r2'][-1] - base)
                        else:
                            delta_method.append(0)
                    ax.plot(ns, delta_method, marker='s', label=name, linewidth=2)

            ax.axhline(0, linestyle='--', color='gray', alpha=0.7)
            ax.set_xscale('log')
            ax.set_xticks(ns)
            ax.set_title(f"σ={sigma}, outliers={int(frac * 100)}%")
            ax.set_xlabel('n_remove')
            ax.set_ylabel('Δ R² Score')
            ax.grid(True, alpha=0.3)

            if i == 0 and j == 0:
                ax.legend(fontsize=8)

    plt.suptitle("Δ R² Score vs Number of Samples Removed (final epoch)")
    plt.show()


def main():
    """Основная функция для регрессии"""
    print("Starting regression influence analysis...")

    # Генерация данных
    print("Generating regression data...")
    datasets_full, datasets_train, datasets_test = generate_regression_data()

    # Визуализация данных
    print("Plotting data distributions...")
    plot_regression_data(datasets_full, noise_sigmas, outlier_fracs, "Full: ")
    plot_regression_data(datasets_train, noise_sigmas, outlier_fracs, "Train: ")
    plot_regression_data(datasets_test, noise_sigmas, outlier_fracs, "Test: ")

    # Запуск экспериментов
    print("Running influence analysis experiments...")
    results, all_scores = run_regression_experiments(
        datasets_train, datasets_test, noise_sigmas, outlier_fracs, n_epochs
    )

    # Визуализация результатов
    print("Plotting results...")
    plot_regression_results(results, noise_sigmas, outlier_fracs, ns)

    print("Regression analysis completed!")


if __name__ == "__main__":
    main()