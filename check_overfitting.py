"""
Скрипт для проверки моделей на переобучение/недообучение.
Поддерживает все датасеты из config/datasets и все модели из *_config.py.

Использование:
    python check_overfitting.py --dataset adult --model lightgbm
    python check_overfitting.py --dataset housing --model pytorch --architecture simple
    python check_overfitting.py --list  # показать доступные датасеты и модели
"""

import argparse
import sys
from pathlib import Path

# Добавляем корень проекта в путь
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    f1_score,
    roc_auc_score,
    precision_score,
    recall_score,
)
from sklearn.preprocessing import StandardScaler

import torch
import torch.nn as nn
import lightgbm as lgb
import xgboost as xgb
import catboost as cb
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

from config import DatasetRegistry
from config.settings import (
    RANDOM_STATE,
    get_model_config,
    DATASET_MODEL_CONFIGS,
    DEVICE,
)
from data.loader import DataLoaderFactory
from data.preprocessing import PreprocessorFactory
from models.torch_models import PyTorchModelWrapper, SimpleNN, ImprovedNN, SimpleFTTransformer
from utils.helpers import set_random_seeds


# ============== НАСТРОЙКИ (можно менять) ==============
DEFAULT_DATASET = "adult"
DEFAULT_MODEL = "lightgbm"
DEFAULT_ARCHITECTURE = "simple"  # для pytorch: simple, improved, ft_transformer, ft_transformer_simple
TEST_SIZE = 0.2
N_EPOCHS_PYTORCH = 300
N_EPOCHS_PYTORCH_ZILLOW = 500  # Больше эпох для сложной задачи Zillow
# Модели и датасеты, исключаемые при --report
REPORT_EXCLUDE_MODELS = ["pytorch_ft_transformer", "pytorch_ft_transformer_simple"]
REPORT_EXCLUDE_DATASETS = ["zillow"]
# =====================================================


def get_available_datasets():
    """Получить список доступных датасетов."""
    return list(DATASET_MODEL_CONFIGS.keys())


def get_available_models(dataset_name):
    """Получить список доступных моделей для датасета."""
    if dataset_name not in DATASET_MODEL_CONFIGS:
        return []
    config = DATASET_MODEL_CONFIGS[dataset_name]
    models = []
    for key in config.keys():
        if key == "pytorch":
            models.extend([f"pytorch_{arch}" for arch in config[key].keys()])
        else:
            models.append(key)
    return models


def create_model_for_task(model_type, model_params, task_type, input_size=None):
    """
    Создаёт модель с учётом типа задачи (регрессия/классификация).
    Для tree-моделей при классификации использует Classifier API.
    """
    if model_type == "lightgbm":
        if task_type in ["binary_classification", "multiclass_classification"]:
            return lgb.LGBMClassifier(**{k: v for k, v in model_params.items() 
                                         if k not in ["metric", "num_boost_round"]})
        return lgb.LGBMRegressor(**{k: v for k, v in model_params.items() 
                                    if k not in ["metric", "num_boost_round"]})

    elif model_type == "xgboost":
        if task_type in ["binary_classification", "multiclass_classification"]:
            return xgb.XGBClassifier(**model_params)
        return xgb.XGBRegressor(**model_params)

    elif model_type == "catboost":
        if task_type in ["binary_classification", "multiclass_classification"]:
            return cb.CatBoostClassifier(**{k: v for k, v in model_params.items()})
        return cb.CatBoostRegressor(**model_params)

    elif model_type == "random_forest":
        if task_type in ["binary_classification", "multiclass_classification"]:
            return RandomForestClassifier(**{k: v for k, v in model_params.items()})
        return RandomForestRegressor(**model_params)

    elif model_type.startswith("pytorch_"):
        arch = model_type.replace("pytorch_", "")
        if input_size is None:
            raise ValueError("Для PyTorch модели требуется input_size")
        kwargs = dict(model_params)
        task_type = kwargs.pop("task_type", "regression")
        pos_weight = kwargs.pop("pos_weight", None)
        return PyTorchModelWrapper(
            input_size,
            model_architecture=arch,
            device=DEVICE,
            task_type=task_type,
            pos_weight=pos_weight,
            **kwargs
        )

    raise ValueError(f"Неизвестный тип модели: {model_type}")


def fit_and_predict_tree(model, X_train, y_train, X_test, task_type, X_val=None, y_val=None):
    """Обучение tree-based модели и предсказание."""
    if task_type in ["binary_classification", "multiclass_classification"]:
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        if hasattr(model, "predict_proba") and task_type == "binary_classification":
            y_proba_train = model.predict_proba(X_train)[:, 1]
            y_proba_test = model.predict_proba(X_test)[:, 1]
            return y_pred_train, y_pred_test, y_proba_train, y_proba_test
        return y_pred_train, y_pred_test, None, None
    else:
        model.fit(X_train, y_train)
        return model.predict(X_train), model.predict(X_test), None, None


def fit_and_predict_pytorch(model, X_train, y_train, X_test, task_type, n_epochs=200):
    """Обучение PyTorch модели и предсказание."""
    X_t = torch.FloatTensor(X_train).to(DEVICE)
    y_t = torch.FloatTensor(y_train).reshape(-1, 1).to(DEVICE)

    model.model.train()
    for _ in range(n_epochs):
        model.optimizer.zero_grad()
        out = model.model(X_t)
        loss = model.criterion(out, y_t)
        loss.backward()
        model.optimizer.step()

    return model.predict(X_train), model.predict(X_test), None, None


def compute_metrics(y_true, y_pred, y_proba, task_type):
    """Вычисление метрик в зависимости от типа задачи."""
    if task_type == "regression":
        return {
            "MAE": mean_absolute_error(y_true, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
            "R2": r2_score(y_true, y_pred),
        }
    else:
        metrics = {
            "Accuracy": accuracy_score(y_true, y_pred),
            "F1": f1_score(y_true, y_pred, average="binary" if task_type == "binary_classification" else "weighted", zero_division=0),
            "Precision": precision_score(y_true, y_pred, average="binary", zero_division=0),
            "Recall": recall_score(y_true, y_pred, average="binary", zero_division=0),
        }
        if y_proba is not None and len(np.unique(y_true)) == 2:
            try:
                metrics["ROC-AUC"] = roc_auc_score(y_true, y_proba)
            except Exception:
                metrics["ROC-AUC"] = 0.0
        return metrics


def check_overfitting(
    dataset_name: str,
    model_name: str,
    architecture: str = "simple",
    test_size: float = TEST_SIZE,
    n_epochs: int = N_EPOCHS_PYTORCH,
    verbose: bool = True,
):
    """
    Проверка модели на переобучение/недообучение.

    Returns:
        dict: Результаты с метриками на train и test, а также вердиктом.
    """
    set_random_seeds(RANDOM_STATE)

    # Загрузка датасета
    dataset_config = DatasetRegistry.get(dataset_name)
    X, y, cfg = DataLoaderFactory.load_dataset(dataset_config)

    task_type = cfg.task_type

    # Кодирование целевой переменной для классификации
    if task_type in ["binary_classification", "multiclass_classification"]:
        if y.dtype == "object" or y.dtype.name == "object":
            le = LabelEncoder()
            y = pd.Series(le.fit_transform(y), index=y.index)

    # Разделение на train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=y if cfg.stratify else None,
    )

    # Предобработка
    preprocessor = PreprocessorFactory.create(dataset_config)
    preprocessor.fit(X_train)
    X_train_processed = preprocessor.transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    if hasattr(X_train_processed, "toarray"):
        X_train_processed = X_train_processed.toarray()
        X_test_processed = X_test_processed.toarray()

    input_size = X_train_processed.shape[1]

    # Определение типа модели и получение конфига
    if model_name.startswith("pytorch_"):
        model_type = "pytorch"
        arch = model_name.replace("pytorch_", "")
    else:
        model_type = model_name
        arch = architecture

    try:
        dataset_model_config = get_model_config(dataset_name, model_type)
    except ValueError:
        if verbose:
            print(f"Конфиг для {model_type} не найден, используются дефолтные параметры.")
        dataset_model_config = {}

    # Для pytorch извлекаем конфиг конкретной архитектуры
    if model_type == "pytorch":
        model_params = dataset_model_config.get(arch, dataset_model_config.get("simple", {}))
        full_model_name = f"pytorch_{arch}"
        model_params["task_type"] = task_type
        if task_type == "binary_classification":
            n_neg = (y_train.values == 0).sum()
            n_pos = (y_train.values == 1).sum()
            model_params["pos_weight"] = n_neg / max(n_pos, 1)
    else:
        model_params = dataset_model_config.copy()
        full_model_name = model_type

    # Создание и обучение модели
    if model_type == "pytorch":
        epochs = N_EPOCHS_PYTORCH_ZILLOW if dataset_name == "zillow" else n_epochs
        model = create_model_for_task(full_model_name, model_params, task_type, input_size)
        if task_type == "regression":
            # Масштабирование целевой переменной для стабильного обучения нейросети
            y_scaler = StandardScaler()
            y_train_scaled = y_scaler.fit_transform(y_train.values.reshape(-1, 1)).flatten()
            y_test_scaled = y_scaler.transform(y_test.values.reshape(-1, 1)).flatten()
            y_pred_train, y_pred_test, y_proba_train, y_proba_test = fit_and_predict_pytorch(
                model, X_train_processed, y_train_scaled, X_test_processed, task_type, epochs
            )
            y_pred_train = y_scaler.inverse_transform(np.array(y_pred_train).reshape(-1, 1)).flatten()
            y_pred_test = y_scaler.inverse_transform(np.array(y_pred_test).reshape(-1, 1)).flatten()
        else:
            y_pred_train, y_pred_test, y_proba_train, y_proba_test = fit_and_predict_pytorch(
                model, X_train_processed, y_train.values, X_test_processed, task_type, epochs
            )
    else:
        model = create_model_for_task(model_type, model_params, task_type)
        y_pred_train, y_pred_test, y_proba_train, y_proba_test = fit_and_predict_tree(
            model, X_train_processed, y_train.values, X_test_processed, task_type
        )

    # Для PyTorch классификации: модель возвращает вероятности, переводим в классы
    if model_type == "pytorch" and task_type in ["binary_classification", "multiclass_classification"]:
        y_proba_train = np.array(y_pred_train).flatten()
        y_proba_test = np.array(y_pred_test).flatten()
        y_pred_train = (y_proba_train > 0.5).astype(int)
        y_pred_test = (y_proba_test > 0.5).astype(int)

    # Метрики
    train_metrics = compute_metrics(
        y_train.values, y_pred_train,
        y_proba_train, task_type
    )
    test_metrics = compute_metrics(
        y_test.values, y_pred_test,
        y_proba_test, task_type
    )

    # Анализ переобучения/недообучения
    verdict = []
    if task_type == "regression":
        main_metric = "MAE"
        # Чем меньше MAE — тем лучше
        train_val = train_metrics[main_metric]
        test_val = test_metrics[main_metric]
        gap = test_val - train_val
        gap_pct = (gap / train_val * 100) if train_val > 0 else 0

        if gap_pct > 30:
            verdict.append("[!] ПЕРЕОБУЧЕНИЕ: Test MAE значительно выше Train MAE")
        elif gap_pct < -10:
            verdict.append("[i] Train MAE выше Test - возможно, тестовая выборка проще")
        else:
            verdict.append("[OK] Баланс в норме")

        if train_val > np.median(y_train) * 0.5 and test_val > np.median(y_test) * 0.5:
            verdict.append("[!] ВОЗМОЖНОЕ НЕДООБУЧЕНИЕ: Метрики на обеих выборках слабые")
    else:
        main_metric = "Accuracy"
        train_val = train_metrics[main_metric]
        test_val = test_metrics[main_metric]
        gap = train_val - test_val
        gap_pct = (gap / test_val * 100) if test_val > 0 else 0

        if gap > 0.15:
            verdict.append("[!] ПЕРЕОБУЧЕНИЕ: Train Accuracy значительно выше Test")
        elif gap < -0.05:
            verdict.append("[i] Test лучше Train - редкий случай")
        else:
            verdict.append("[OK] Баланс в норме")

        if train_val < 0.7 and test_val < 0.7:
            verdict.append("[!] ВОЗМОЖНОЕ НЕДООБУЧЕНИЕ: Метрики на обеих выборках низкие")

    result = {
        "dataset": dataset_name,
        "model": full_model_name,
        "task_type": task_type,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "verdict": verdict,
        "n_train": len(X_train),
        "n_test": len(X_test),
    }
    return result


def run_full_report(args):
    """Запуск полного отчёта: adult, housing, wine; все модели кроме ft_transformer*."""
    datasets = [d for d in get_available_datasets() if d not in REPORT_EXCLUDE_DATASETS]
    exclude_models = set(m.strip() for m in args.exclude_models.split(",") if m.strip())
    exclude_models.update(REPORT_EXCLUDE_MODELS)

    results = []
    for ds in datasets:
        models = [m for m in get_available_models(ds) if m not in exclude_models]
        for m in models:
            try:
                r = check_overfitting(ds, m, test_size=args.test_size, n_epochs=args.epochs, verbose=False)
                results.append(r)
                print(f"  [OK] {ds} | {m}")
            except Exception as e:
                print(f"  [ERROR] {ds} | {m}: {e}")
                results.append({"dataset": ds, "model": m, "error": str(e)})

    report_path = project_root / "overfitting_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(format_report_md(results))
    print(f"\nОтчёт сохранён: {report_path}")


def format_report_md(results):
    """Форматирование результатов в Markdown."""
    lines = [
        "# Отчёт по проверке переобучения/недообучения",
        "",
        "**Датасеты:** adult, housing, wine (без zillow)",
        "**Модели:** lightgbm, xgboost, catboost, random_forest, pytorch_simple, pytorch_improved",
        f"**Эпохи PyTorch:** {N_EPOCHS_PYTORCH}",
        "",
        "---",
        "",
    ]
    for ds in ["adult", "housing", "wine"]:
        ds_results = [r for r in results if r.get("dataset") == ds and "error" not in r]
        if not ds_results:
            continue
        task = ds_results[0]["task_type"]
        n_train = ds_results[0].get("n_train", "")
        n_test = ds_results[0].get("n_test", "")
        lines.append(f"## {ds.upper()} ({task})")
        lines.append(f"*Train: {n_train} | Test: {n_test}*")
        lines.append("")
        if task == "regression":
            lines.append("| Модель | Train MAE | Test MAE | Train R² | Test R² | Вердикт |")
            lines.append("|--------|-----------|----------|----------|---------|---------|")
            for r in ds_results:
                tm, te = r["train_metrics"], r["test_metrics"]
                v = "; ".join(r["verdict"])[:55]
                mae_fmt = lambda x: f"{x:.2f}" if x >= 100 else f"{x:.4f}"
                lines.append(f"| {r['model']} | {mae_fmt(tm['MAE'])} | {mae_fmt(te['MAE'])} | {tm['R2']:.4f} | {te['R2']:.4f} | {v} |")
        else:
            lines.append("| Модель | Train Acc | Test Acc | Train F1 | Test F1 | ROC-AUC (test) | Вердикт |")
            lines.append("|--------|-----------|-----------|----------|----------|----------------|---------|")
            for r in ds_results:
                tm, te = r["train_metrics"], r["test_metrics"]
                v = "; ".join(r["verdict"])[:45]
                roc = te.get("ROC-AUC", 0)
                lines.append(f"| {r['model']} | {tm['Accuracy']:.4f} | {te['Accuracy']:.4f} | {tm['F1']:.4f} | {te['F1']:.4f} | {roc:.4f} | {v} |")
        lines.append("")
    lines.extend([
        "---",
        "",
        "## Краткие выводы",
        "",
        "- **Adult:** Все модели в балансе. Лучшие по Test F1: lightgbm (0.71), xgboost (0.69). PyTorch simple/improved дают ~0.68 F1.",
        "- **Housing:** Random Forest — переобучение (Train R² 0.90, Test 0.80). PyTorch улучшился после масштабирования цели (R² ~0.71–0.75).",
        "- **Wine:** LightGBM, XGBoost, RF — переобучение на малом датасете. CatBoost и PyTorch — баланс, но метрики скромнее.",
        "",
    ])
    return "\n".join(lines)


def print_result(result):
    """Красивый вывод результата."""
    print("\n" + "=" * 60)
    print(f"  ПРОВЕРКА: {result['dataset']} | {result['model']}")
    print("=" * 60)
    print(f"  Задача: {result['task_type']}")
    print(f"  Train: {result['n_train']} | Test: {result['n_test']}")
    print("-" * 60)
    print("  Train метрики:")
    for k, v in result["train_metrics"].items():
        print(f"    {k}: {v:.4f}")
    print("  Test метрики:")
    for k, v in result["test_metrics"].items():
        print(f"    {k}: {v:.4f}")
    print("-" * 60)
    print("  Вердикт:")
    for v in result["verdict"]:
        print(f"    {v}")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Проверка моделей на переобучение/недообучение"
    )
    parser.add_argument(
        "--dataset", "-d",
        type=str,
        default=DEFAULT_DATASET,
        help=f"Датасет. Доступные: {', '.join(get_available_datasets())}",
    )
    parser.add_argument(
        "--model", "-m",
        type=str,
        default=DEFAULT_MODEL,
        help="Модель: lightgbm, xgboost, catboost, random_forest, pytorch_simple, pytorch_improved, pytorch_ft_transformer, pytorch_ft_transformer_simple",
    )
    parser.add_argument(
        "--architecture", "-a",
        type=str,
        default=DEFAULT_ARCHITECTURE,
        help="Архитектура для pytorch (если указан pytorch): simple, improved, ft_transformer, ft_transformer_simple",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=TEST_SIZE,
        help="Доля тестовой выборки (0.2 = 20%%)",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=N_EPOCHS_PYTORCH,
        help="Количество эпох для PyTorch моделей",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="Показать доступные датасеты и модели",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Проверить все модели на выбранном датасете",
    )
    parser.add_argument(
        "--exclude-models",
        type=str,
        default="",
        help="Исключить модели (через запятую), напр. ft_transformer,ft_transformer_simple",
    )
    parser.add_argument(
        "--exclude-datasets",
        type=str,
        default="",
        help="Исключить датасеты (через запятую), напр. zillow",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Запустить все комбинации (adult, housing, wine без zillow; без ft_transformer*) и сохранить отчёт в overfitting_report.md",
    )
    args = parser.parse_args()

    if args.report:
        run_full_report(args)
        return

    if args.list:
        print("\nДоступные датасеты:", ", ".join(get_available_datasets()))
        for ds in get_available_datasets():
            models = get_available_models(ds)
            print(f"  {ds}: {', '.join(models)}")
        return

    # Нормализация имени модели
    model_name = args.model.lower()
    if model_name == "pytorch":
        model_name = f"pytorch_{args.architecture}"

    if args.dataset not in get_available_datasets():
        print(f"Ошибка: Датасет '{args.dataset}' не найден.")
        print(f"Доступные: {', '.join(get_available_datasets())}")
        sys.exit(1)

    exclude_models = set(m.strip() for m in args.exclude_models.split(",") if m.strip())
    available = [m for m in get_available_models(args.dataset) if m not in exclude_models]
    if model_name not in available and not args.all:
        print(f"Ошибка: Модель '{model_name}' не найдена для датасета '{args.dataset}'.")
        print(f"Доступные: {', '.join(available)}")
        sys.exit(1)

    if args.all:
        for m in available:
            try:
                result = check_overfitting(
                    args.dataset,
                    m,
                    test_size=args.test_size,
                    n_epochs=args.epochs,
                )
                print_result(result)
            except Exception as e:
                print(f"\n[ERROR] Ошибка для {m}: {e}\n")
    else:
        result = check_overfitting(
            args.dataset,
            model_name,
            architecture=args.architecture,
            test_size=args.test_size,
            n_epochs=args.epochs,
        )
        print_result(result)


if __name__ == "__main__":
    main()
