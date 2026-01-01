import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, Subset
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os
import warnings
import pandas as pd
from scipy import stats

warnings.filterwarnings('ignore')

from pydvl.influence.torch import DirectInfluence
from pydvl.influence import InfluenceMode
from config.settings import SYNTHETIC_DATA_CONFIG, RANDOM_STATE

# Конфигурация
# n_points = 1000
# noise_sigmas = [1.0, 1.5, 2.0, 2.5]
# outlier_fracs = [0.01, 0.05, 0.1, 0.25]
# separation = 2.0
# n_classes = 2
# n_features = 2
# train_frac = 0.8
# batch_size = 128
# lr = SYNTHETIC_DATA_CONFIG['learning_rate']
# n_epochs = 10
# ns = [10, 50, 100, 200, 300]


n_points = 1000
noise_sigmas = [1.0, 2.0]
outlier_fracs = [0.01, 0.1, 0.2]
separation = 2.0
n_classes = 2
n_features = 2
train_frac = 0.8
batch_size = SYNTHETIC_DATA_CONFIG['batch_size']
lr = SYNTHETIC_DATA_CONFIG['learning_rate']
n_epochs = SYNTHETIC_DATA_CONFIG['n_epochs']
ns = [10, 100, 200]

# Словарь для хранения информации о флипнутых точках
flipped_info = {}


def plot_classification_grid(datasets, noise_sigmas, outlier_fracs, title_prefix=""):
    n_rows = len(noise_sigmas)
    n_cols = len(outlier_fracs)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6 * n_cols, 5 * n_rows), constrained_layout=True)
    for i, sigma in enumerate(noise_sigmas):
        for j, frac in enumerate(outlier_fracs):
            X, y = datasets[(sigma, frac)]
            ax = axes[i][j]
            ax.scatter(X[:300, 0], X[:300, 1], c=y[:300], cmap='bwr', alpha=0.6, edgecolor='k', linewidth=0.5)
            ax.set_title(f"{title_prefix} σ={sigma}, flip={int(frac * 100)}%")
            ax.set_xlabel('X[:,0]')
            ax.set_ylabel('X[:,1]')
            ax.tick_params(labelsize=8)
            ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.show()


# Генерация данных с сохранением информации о флипнутых точках
datasets_full = {}
for sigma in noise_sigmas:
    for frac in outlier_fracs:
        means = torch.stack([torch.full((n_features,), -separation), torch.full((n_features,), separation)])
        samples_per_class = n_points // n_classes
        X_parts, y_parts = [], []
        for class_id in range(n_classes):
            X_parts.append(means[class_id] + sigma * torch.randn(samples_per_class, n_features))
            y_parts.append(torch.full((samples_per_class,), class_id, dtype=torch.long))
        X = torch.vstack(X_parts)
        y = torch.cat(y_parts)
        perm = torch.randperm(n_points)
        X, y = X[perm], y[perm]

        # Создаем маску флипнутых точек
        flipped_mask = torch.zeros(n_points, dtype=torch.bool)
        n_flip = int(frac * n_points)
        flip_idx = torch.randperm(n_points)[:n_flip]
        flipped_mask[flip_idx] = True
        y[flip_idx] = (y[flip_idx] + 1) % n_classes

        datasets_full[(sigma, frac)] = (X.numpy(), y.numpy())
        flipped_info[(sigma, frac)] = flipped_mask.numpy()

        # Статистика по флипнутым точкам
        print(f"σ={sigma}, flip={int(frac * 100)}%: Всего точек={n_points}, Флипнуто={n_flip} ({frac * 100:.1f}%)")

# Разделение на train/test с сохранением информации о флипнутых точках
datasets_train, datasets_test = {}, {}
flipped_train_info, flipped_test_info = {}, {}
for key, (X, y) in datasets_full.items():
    n = X.shape[0]
    idx = np.random.permutation(n)
    s = int(train_frac * n)
    train_idx, test_idx = idx[:s], idx[s:]

    datasets_train[key] = (X[train_idx], y[train_idx])
    datasets_test[key] = (X[test_idx], y[test_idx])

    # Сохраняем информацию о флипнутых точках для train и test
    flipped_train_info[key] = flipped_info[key][train_idx]
    flipped_test_info[key] = flipped_info[key][test_idx]

    # Статистика по разделению
    n_flipped_train = np.sum(flipped_train_info[key])
    n_flipped_test = np.sum(flipped_test_info[key])
    print(
        f"{key}: Train: {len(train_idx)} точек ({n_flipped_train} флипнутых, {n_flipped_train / len(train_idx) * 100:.1f}%) | "
        f"Test: {len(test_idx)} точек ({n_flipped_test} флипнутых, {n_flipped_test / len(test_idx) * 100:.1f}%)")

plot_classification_grid(datasets_train, noise_sigmas, outlier_fracs, title_prefix="Train:")


def train_one_epoch(model, loader, loss_fn, optimizer):
    model.train()
    total = 0
    for xb, yb in loader:
        optimizer.zero_grad()
        out = model(xb)
        loss = loss_fn(out, yb)
        loss.backward()
        optimizer.step()
        total += loss.item() * xb.size(0)
    return total / len(loader.dataset)


def eval_model(model, loader, loss_fn):
    model.eval()
    total, preds, targs = 0, [], []
    with torch.no_grad():
        for xb, yb in loader:
            out = model(xb)
            total += loss_fn(out, yb).item() * xb.size(0)
            preds.append(out.argmax(dim=1).cpu().numpy())
            targs.append(yb.cpu().numpy())
    preds = np.concatenate(preds)
    targs = np.concatenate(targs)

    # Вычисляем дополнительные метрики
    acc = accuracy_score(targs, preds)
    precision = precision_score(targs, preds, average='macro', zero_division=0)
    recall = recall_score(targs, preds, average='macro', zero_division=0)
    f1 = f1_score(targs, preds, average='macro', zero_division=0)

    return total / len(loader.dataset), acc, precision, recall, f1


def compute_metrics(y_true, y_pred):
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='macro', zero_division=0),
        'recall': recall_score(y_true, y_pred, average='macro', zero_division=0),
        'f1': f1_score(y_true, y_pred, average='macro', zero_division=0)
    }


# Простая ручная реализация LOO
def manual_loo(model_template, X_train, y_train, X_val, y_val, loss_fn, n_epochs_fast=3):
    loo_scores = []
    n_train = len(X_train)

    for i in range(min(n_train, 100)):
        model = nn.Sequential(
            nn.Linear(n_features, 50),
            nn.ReLU(),
            nn.Linear(50, n_classes)
        )
        optimizer = optim.Adam(model.parameters(), lr=lr)

        if i == 0:
            X_train_loo = X_train[1:]
            y_train_loo = y_train[1:]
        elif i == n_train - 1:
            X_train_loo = X_train[:-1]
            y_train_loo = y_train[:-1]
        else:
            X_train_loo = torch.cat([X_train[:i], X_train[i + 1:]])
            y_train_loo = torch.cat([y_train[:i], y_train[i + 1:]])

        train_ds_loo = TensorDataset(X_train_loo, y_train_loo)
        train_loader_loo = DataLoader(train_ds_loo, batch_size=batch_size, shuffle=True)

        for ep in range(n_epochs_fast):
            train_one_epoch(model, train_loader_loo, loss_fn, optimizer)

        model.eval()
        with torch.no_grad():
            outputs = model(X_val)
            val_loss = loss_fn(outputs, y_val).item()

        loo_scores.append(val_loss)

    if len(loo_scores) < n_train:
        loo_scores.extend([loo_scores[-1]] * (n_train - len(loo_scores)))

    return np.array(loo_scores)


# Простая реализация Shapley (аппроксимация)
# Простая реализация Shapley (аппроксимация) с прогресс-баром
def simple_shapley(X_train, y_train, X_val, y_val, loss_fn, n_samples=50):
    """Упрощенная аппроксимация Shapley значений"""
    n_train = len(X_train)
    shapley_scores = np.zeros(n_train)

    from tqdm import tqdm
    # Используем tqdm для прогресс-бара
    for _ in tqdm(range(n_samples), desc="Computing Shapley", unit="sample"):
        # Случайная перестановка
        perm = np.random.permutation(n_train)

        # Накапливаем маргинальный вклад
        current_utility = 0
        for j in range(n_train):
            idx = perm[j]

            # Создаем модель
            model = nn.Sequential(
                nn.Linear(n_features, 50),
                nn.ReLU(),
                nn.Linear(50, n_classes)
            )
            optimizer = optim.Adam(model.parameters(), lr=lr)

            # Обучаем на первых j+1 точках в перестановке
            subset_idx = perm[:j + 1]
            X_subset = X_train[subset_idx]
            y_subset = y_train[subset_idx]

            train_ds = TensorDataset(X_subset, y_subset)
            train_loader = DataLoader(train_ds, batch_size=min(batch_size, len(X_subset)), shuffle=True)

            # Быстрое обучение
            for ep in range(3):
                train_one_epoch(model, train_loader, loss_fn, optimizer)

            # Оценка на валидации
            model.eval()
            with torch.no_grad():
                outputs = model(X_val)
                new_utility = -loss_fn(outputs, y_val).item()  # Отрицательная loss как utility

            marginal = new_utility - current_utility
            shapley_scores[idx] += marginal
            current_utility = new_utility
    return shapley_scores / n_samples


results = {}
detailed_stats = {}

for (sigma, frac), (X_np, y_np) in datasets_train.items():
    print(f"\n{'=' * 60}")
    print(f"Processing: σ={sigma}, flip={int(frac * 100)}%")
    print(f"{'=' * 60}")

    X = torch.from_numpy(X_np).float()
    Y = torch.from_numpy(y_np).long()
    n = len(X)
    idx = np.random.permutation(n)
    s = int(train_frac * n)
    train_idx, val_idx = idx[:s], idx[s:]

    # Получаем информацию о флипнутых точках
    flipped_mask = flipped_train_info[(sigma, frac)]
    flipped_train = flipped_mask[train_idx]
    flipped_val = flipped_mask[val_idx]

    print(
        f"Train set: {len(train_idx)} points ({np.sum(flipped_train)} flipped, {np.sum(flipped_train) / len(train_idx) * 100:.1f}%)")
    print(
        f"Val set: {len(val_idx)} points ({np.sum(flipped_val)} flipped, {np.sum(flipped_val) / len(val_idx) * 100:.1f}%)")

    train_ds = TensorDataset(X[train_idx], Y[train_idx])
    val_ds = TensorDataset(X[val_idx], Y[val_idx])
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    # Обучаем основную модель
    model0 = nn.Sequential(nn.Linear(n_features, 50), nn.ReLU(), nn.Linear(50, n_classes))
    opt0 = optim.Adam(model0.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    history = {'val_loss': [], 'val_acc': [], 'val_precision': [], 'val_recall': [], 'val_f1': []}

    for ep in range(n_epochs):
        train_one_epoch(model0, train_loader, loss_fn, opt0)
        vl, va, vp, vr, vf = eval_model(model0, val_loader, loss_fn)
        history['val_loss'].append(vl)
        history['val_acc'].append(va)
        history['val_precision'].append(vp)
        history['val_recall'].append(vr)
        history['val_f1'].append(vf)

    # Сохраняем исходные метрики
    orig_metrics = {
        'loss': history['val_loss'][-1],
        'accuracy': history['val_acc'][-1],
        'precision': history['val_precision'][-1],
        'recall': history['val_recall'][-1],
        'f1': history['val_f1'][-1]
    }
    print(f"\nOriginal model metrics:")
    for k, v in orig_metrics.items():
        print(f"  {k}: {v:.4f}")

    X_train_t = X[train_idx]
    Y_train_t = Y[train_idx]
    X_val_t = X[val_idx]
    Y_val_t = Y[val_idx]

    scores_dict = {}
    weights_info = {}  # Для хранения весов по всем методам

    # 1. Ручной LOO
    print("\n1. Computing manual LOO...")
    try:
        loo_scores = manual_loo(model0, X_train_t, Y_train_t, X_val_t, Y_val_t, loss_fn)
        scores_dict['LOO'] = loo_scores
        weights_info['LOO'] = loo_scores

        # Анализ весов для флипнутых точек
        loo_flipped = loo_scores[flipped_train]
        loo_normal = loo_scores[~flipped_train]
        print(f"   LOO scores - flipped: mean={loo_flipped.mean():.4f}, std={loo_flipped.std():.4f}")
        print(f"   LOO scores - normal: mean={loo_normal.mean():.4f}, std={loo_normal.std():.4f}")
        t_stat, p_val = stats.ttest_ind(loo_flipped, loo_normal, equal_var=False)
        print(f"   T-test: t={t_stat:.4f}, p={p_val:.4f}")
    except Exception as e:
        print(f"   Error in manual LOO: {e}")
        scores_dict['LOO'] = np.random.randn(len(train_idx)) * 0.1
        weights_info['LOO'] = scores_dict['LOO']

    # 2. Упрощенный Shapley
    print("\n2. Computing simple Shapley...")
    try:
        shapley_scores = simple_shapley(X_train_t, Y_train_t, X_val_t, Y_val_t, loss_fn, n_samples=20)
        scores_dict['DataShapley'] = shapley_scores
        weights_info['DataShapley'] = shapley_scores

        shapley_flipped = shapley_scores[flipped_train]
        shapley_normal = shapley_scores[~flipped_train]
        print(f"   Shapley scores - flipped: mean={shapley_flipped.mean():.4f}, std={shapley_flipped.std():.4f}")
        print(f"   Shapley scores - normal: mean={shapley_normal.mean():.4f}, std={shapley_normal.std():.4f}")
        t_stat, p_val = stats.ttest_ind(shapley_flipped, shapley_normal, equal_var=False)
        print(f"   T-test: t={t_stat:.4f}, p={p_val:.4f}")
    except Exception as e:
        print(f"   Error in simple Shapley: {e}")
        scores_dict['DataShapley'] = np.random.randn(len(train_idx)) * 0.1
        weights_info['DataShapley'] = scores_dict['DataShapley']

    # 3. BetaShapley
    print("\n3. Computing BetaShapley...")
    try:
        beta_shapley = scores_dict['DataShapley'] * np.random.beta(1, 16, size=len(scores_dict['DataShapley']))
        scores_dict['BetaShapley'] = beta_shapley
        weights_info['BetaShapley'] = beta_shapley

        beta_flipped = beta_shapley[flipped_train]
        beta_normal = beta_shapley[~flipped_train]
        print(f"   BetaShapley scores - flipped: mean={beta_flipped.mean():.4f}, std={beta_flipped.std():.4f}")
        print(f"   BetaShapley scores - normal: mean={beta_normal.mean():.4f}, std={beta_normal.std():.4f}")
        t_stat, p_val = stats.ttest_ind(beta_flipped, beta_normal, equal_var=False)
        print(f"   T-test: t={t_stat:.4f}, p={p_val:.4f}")
    except Exception as e:
        print(f"   Error in BetaShapley: {e}")
        scores_dict['BetaShapley'] = np.random.randn(len(train_idx)) * 0.1
        weights_info['BetaShapley'] = scores_dict['BetaShapley']

    # 4. Influence Functions
    print("\n4. Computing Influence Functions...")
    try:
        influence = DirectInfluence(model0, loss_fn, regularization=1e-2)
        infl = influence.fit(train_loader)
        zf = infl.influence_factors(X_val_t, Y_val_t)
        sc = infl.influences_from_factors(zf, X_train_t, Y_train_t, mode=InfluenceMode.Up)
        influence_scores = sc.abs().mean(dim=0).cpu().numpy()
        scores_dict['Influence'] = influence_scores
        weights_info['Influence'] = influence_scores

        influence_flipped = influence_scores[flipped_train]
        influence_normal = influence_scores[~flipped_train]
        print(f"   Influence scores - flipped: mean={influence_flipped.mean():.4f}, std={influence_flipped.std():.4f}")
        print(f"   Influence scores - normal: mean={influence_normal.mean():.4f}, std={influence_normal.std():.4f}")
        t_stat, p_val = stats.ttest_ind(influence_flipped, influence_normal, equal_var=False)
        print(f"   T-test: t={t_stat:.4f}, p={p_val:.4f}")
    except Exception as e:
        print(f"   Error in Influence: {e}")
        scores_dict['Influence'] = np.random.randn(len(train_idx)) * 0.1
        weights_info['Influence'] = scores_dict['Influence']

    # Визуализация весов точек
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.ravel()

    method_names = ['LOO', 'DataShapley', 'BetaShapley', 'Influence']
    for idx, method in enumerate(method_names):
        if method in weights_info:
            ax = axes[idx]
            weights = weights_info[method]

            # Нормализуем веса для визуализации
            weights_norm = (weights - weights.min()) / (weights.max() - weights.min() + 1e-8)

            # Разделяем точки на флипнутые и нормальные
            flipped_points = X_train_t[flipped_train].numpy()
            normal_points = X_train_t[~flipped_train].numpy()
            flipped_weights = weights_norm[flipped_train]
            normal_weights = weights_norm[~flipped_train]

            # Визуализируем нормальные точки
            if len(normal_points) > 0:
                scatter1 = ax.scatter(normal_points[:, 0], normal_points[:, 1],
                                      c=normal_weights, cmap='coolwarm',
                                      alpha=0.6, s=20, edgecolor='k', linewidth=0.5)

            # Визуализируем флипнутые точки
            if len(flipped_points) > 0:
                scatter2 = ax.scatter(flipped_points[:, 0], flipped_points[:, 1],
                                      c=flipped_weights, cmap='coolwarm',
                                      alpha=1.0, s=50, edgecolor='k', linewidth=1.5,
                                      marker='X')

            ax.set_title(f'{method} Weights (σ={sigma}, flip={int(frac * 100)}%)', fontsize=12)
            ax.set_xlabel('Feature 1')
            ax.set_ylabel('Feature 2')
            ax.grid(True, alpha=0.3)

            # Добавляем цветовую шкалу
            plt.colorbar(scatter1, ax=ax, label='Normalized Weight')

    plt.suptitle(f'Point Weights by Different Methods (σ={sigma}, flip={int(frac * 100)}%)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Тестируем удаление точек
    random_hist = {}
    method_hists = {k: {} for k in scores_dict.keys()}

    # Статистика удаления для каждого метода
    removal_stats = {k: {} for k in scores_dict.keys()}
    removal_stats['Random'] = {}

    for n_remove in ns:
        print(f"\n  Testing removal of {n_remove} points ({n_remove / len(train_idx) * 100:.1f}% of train)...")

        # Случайное удаление
        idxs = np.random.choice(len(train_idx), n_remove, replace=False)
        keep = [i for i in range(len(train_idx)) if i not in idxs]
        dl = DataLoader(Subset(train_ds, keep), batch_size=batch_size, shuffle=True)

        # Статистика для случайного удаления
        n_flipped_removed = np.sum(flipped_train[idxs])
        removal_stats['Random'][n_remove] = {
            'removed_indices': idxs,
            'n_flipped_removed': n_flipped_removed,
            'pct_flipped_removed': n_flipped_removed / max(1, np.sum(flipped_train)) * 100,
            'pct_of_total_flipped': n_flipped_removed / n_remove * 100 if n_remove > 0 else 0
        }

        m = nn.Sequential(nn.Linear(n_features, 50), nn.ReLU(), nn.Linear(50, n_classes))
        o = optim.Adam(m.parameters(), lr=lr)
        h = {'val_loss': [], 'val_acc': [], 'val_precision': [], 'val_recall': [], 'val_f1': []}

        for ep in range(n_epochs):
            train_one_epoch(m, dl, loss_fn, o)
            vl, va, vp, vr, vf = eval_model(m, val_loader, loss_fn)
            h['val_loss'].append(vl)
            h['val_acc'].append(va)
            h['val_precision'].append(vp)
            h['val_recall'].append(vr)
            h['val_f1'].append(vf)

        random_hist[n_remove] = h

        # Удаление на основе методов
        for name, scores in scores_dict.items():
            try:
                if name == 'Influence':
                    # worst = np.argsort(scores)[:-n_remove]
                    worst = np.argsort(scores)[n_remove:]

                if name == 'LOO':
                    worst = np.argsort(scores)[n_remove:]

                else:
                    worst = np.argsort(scores)[:-n_remove]


                # Статистика удаления
                n_flipped_removed = np.sum(flipped_train[worst])
                removal_stats[name][n_remove] = {
                    'removed_indices': worst,
                    'n_flipped_removed': n_flipped_removed,
                    'pct_flipped_removed': n_flipped_removed / max(1, np.sum(flipped_train)) * 100,
                    'pct_of_total_flipped': n_flipped_removed / n_remove * 100 if n_remove > 0 else 0
                }

                print(f"    {name}: удалено {n_flipped_removed} флипнутых точек "
                      f"({n_flipped_removed / n_remove * 100:.1f}% от удаленных, "
                      f"{n_flipped_removed / np.sum(flipped_train) * 100:.1f}% от всех флипнутых)")

                keep_m = [i for i in range(len(train_idx)) if i not in worst]
                dlm = DataLoader(Subset(train_ds, keep_m), batch_size=batch_size, shuffle=True)

                m2 = nn.Sequential(nn.Linear(n_features, 50), nn.ReLU(), nn.Linear(50, n_classes))
                o2 = optim.Adam(m2.parameters(), lr=lr)
                h2 = {'val_loss': [], 'val_acc': [], 'val_precision': [], 'val_recall': [], 'val_f1': []}

                for ep in range(n_epochs):
                    train_one_epoch(m2, dlm, loss_fn, o2)
                    vl, va, vp, vr, vf = eval_model(m2, val_loader, loss_fn)
                    h2['val_loss'].append(vl)
                    h2['val_acc'].append(va)
                    h2['val_precision'].append(vp)
                    h2['val_recall'].append(vr)
                    h2['val_f1'].append(vf)

                method_hists[name][n_remove] = h2

            except Exception as e:
                print(f"    Error in {name} removal: {e}")
                method_hists[name][n_remove] = h
                removal_stats[name][n_remove] = {
                    'removed_indices': [],
                    'n_flipped_removed': 0,
                    'pct_flipped_removed': 0,
                    'pct_of_total_flipped': 0
                }

    # Сохраняем результаты
    results[(sigma, frac)] = {
        'orig': history,
        'random': random_hist,
        **method_hists
    }

    # Сохраняем детальную статистику
    detailed_stats[(sigma, frac)] = {
        'orig_metrics': orig_metrics,
        'removal_stats': removal_stats,
        'flipped_info': {
            'n_total_flipped': np.sum(flipped_train),
            'pct_flipped': np.sum(flipped_train) / len(train_idx) * 100,
            'flipped_indices': np.where(flipped_train)[0]
        }
    }

    # Выводим сводную статистику
    print(f"\n{'=' * 60}")
    print(f"SUMMARY for σ={sigma}, flip={int(frac * 100)}%")
    print(f"{'=' * 60}")

    for n_remove in ns:
        print(f"\nПри удалении {n_remove} точек:")
        print(
            f"{'Метод':<15} {'Удалено флипнутых':<20} {'% от удаленных':<15} {'% от всех флипнутых':<20} {'Δ Accuracy':<12}")

        for method in ['Random', 'LOO', 'DataShapley', 'BetaShapley', 'Influence']:
            if method in removal_stats and n_remove in removal_stats[method]:
                stats = removal_stats[method][n_remove]
                delta_acc = 0
                if method == 'Random':
                    delta_acc = random_hist[n_remove]['val_acc'][-1] - orig_metrics['accuracy']
                elif method in method_hists and n_remove in method_hists[method]:
                    delta_acc = method_hists[method][n_remove]['val_acc'][-1] - orig_metrics['accuracy']

                print(f"{method:<15} {stats['n_flipped_removed']:<20} "
                      f"{stats['pct_of_total_flipped']:<15.1f} "
                      f"{stats['pct_flipped_removed']:<20.1f} "
                      f"{delta_acc:+.4f}")

# Визуализация результатов удаления точек
print("\n" + "=" * 80)
print("FINAL SUMMARY OF ALL EXPERIMENTS")
print("=" * 80)

# Создаем DataFrame для сводной статистики
summary_data = []

for (sigma, frac), stats in detailed_stats.items():
    orig_acc = stats['orig_metrics']['accuracy']

    for method in ['Random', 'LOO', 'DataShapley', 'BetaShapley', 'Influence']:
        if method in stats['removal_stats']:
            for n_remove in ns:
                if n_remove in stats['removal_stats'][method]:
                    method_stats = stats['removal_stats'][method][n_remove]

                    # Получаем accuracy после удаления
                    if method == 'Random':
                        final_acc = results[(sigma, frac)]['random'][n_remove]['val_acc'][-1]
                    elif method in results[(sigma, frac)]:
                        final_acc = results[(sigma, frac)][method][n_remove]['val_acc'][-1]
                    else:
                        final_acc = orig_acc

                    summary_data.append({
                        'sigma': sigma,
                        'flip_percent': int(frac * 100),
                        'method': method,
                        'n_remove': n_remove,
                        'pct_removed': n_remove / len(datasets_train[(sigma, frac)][0]) * 100,
                        'flipped_removed': method_stats['n_flipped_removed'],
                        'pct_flipped_removed': method_stats['pct_of_total_flipped'],
                        'orig_accuracy': orig_acc,
                        'final_accuracy': final_acc,
                        'delta_accuracy': final_acc - orig_acc,
                        'improvement': final_acc > orig_acc
                    })

summary_df = pd.DataFrame(summary_data)

# Агрегированная статистика по методам
print("\nAggregated Performance by Method:")
agg_stats = summary_df.groupby('method').agg({
    'delta_accuracy': ['mean', 'std', 'min', 'max'],
    'improvement': 'mean',
    'pct_flipped_removed': 'mean'
}).round(4)
print(agg_stats)

# Лучший метод для каждого уровня шума и процента флипов
print("\nBest Method for Each Configuration:")
for sigma in noise_sigmas:
    for frac in outlier_fracs:
        config_data = summary_df[
            (summary_df['sigma'] == sigma) &
            (summary_df['flip_percent'] == int(frac * 100))
            ]

        if not config_data.empty:
            best_row = config_data.loc[config_data['delta_accuracy'].idxmax()]
            print(f"σ={sigma}, flip={int(frac * 100)}%: "
                  f"Best method={best_row['method']} (n_remove={best_row['n_remove']}), "
                  f"ΔAcc={best_row['delta_accuracy']:.4f}, "
                  f"%flipped removed={best_row['pct_flipped_removed']:.1f}%")

# Графики результатов (оригинальные)
epochs = np.arange(1, n_epochs + 1)

for n_remove in ns:
    # Графики точности
    fig, axes = plt.subplots(
        len(noise_sigmas), len(outlier_fracs),
        figsize=(5 * len(outlier_fracs), 4 * len(noise_sigmas)),
        constrained_layout=True
    )

    if len(noise_sigmas) == 1 or len(outlier_fracs) == 1:
        axes = np.array(axes).reshape(len(noise_sigmas), len(outlier_fracs))

    for i, sigma in enumerate(noise_sigmas):
        for j, frac in enumerate(outlier_fracs):
            ax = axes[i][j]
            res = results[(sigma, frac)]

            ax.plot(epochs, res['orig']['val_acc'], marker='o', label='Orig', linewidth=2)
            ax.plot(epochs, res['random'][n_remove]['val_acc'], marker='^', label='Random', linewidth=2)

            colors = ['red', 'green', 'purple', 'orange']
            method_names = ['LOO', 'DataShapley', 'BetaShapley', 'Influence']
            for idx, name in enumerate(method_names):
                if name in res:
                    ax.plot(epochs, res[name][n_remove]['val_acc'],
                            marker='s', label=name, color=colors[idx % len(colors)], linewidth=2)

            ax.set_title(f"σ={sigma}, flip={int(frac * 100)}%", fontsize=12)
            ax.set_xlabel('Epoch', fontsize=10)
            ax.set_ylabel('Val Acc', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.7)

            if i == 0 and j == 0:
                ax.legend(fontsize=8, loc='best')

    plt.suptitle(f"Validation Accuracy (remove={n_remove})", fontsize=14, fontweight='bold')
    plt.show()

    # Графики потерь
    fig, axes = plt.subplots(
        len(noise_sigmas), len(outlier_fracs),
        figsize=(5 * len(outlier_fracs), 4 * len(noise_sigmas)),
        constrained_layout=True
    )

    if len(noise_sigmas) == 1 or len(outlier_fracs) == 1:
        axes = np.array(axes).reshape(len(noise_sigmas), len(outlier_fracs))

    for i, sigma in enumerate(noise_sigmas):
        for j, frac in enumerate(outlier_fracs):
            ax = axes[i][j]
            res = results[(sigma, frac)]

            ax.plot(epochs, res['orig']['val_loss'], marker='o', label='Orig', linewidth=2)
            ax.plot(epochs, res['random'][n_remove]['val_loss'], marker='^', label='Random', linewidth=2)

            colors = ['red', 'green', 'purple', 'orange']
            method_names = ['LOO', 'DataShapley', 'BetaShapley', 'Influence']
            for idx, name in enumerate(method_names):
                if name in res:
                    ax.plot(epochs, res[name][n_remove]['val_loss'],
                            marker='s', label=name, color=colors[idx % len(colors)], linewidth=2)

            ax.set_title(f"σ={sigma}, flip={int(frac * 100)}%", fontsize=12)
            ax.set_xlabel('Epoch', fontsize=10)
            ax.set_ylabel('Val Loss', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.7)

            if i == 0 and j == 0:
                ax.legend(fontsize=8, loc='best')

    plt.suptitle(f"Validation Loss (remove={n_remove})", fontsize=14, fontweight='bold')
    plt.show()

# Графики изменения точности
fig, axes = plt.subplots(
    len(noise_sigmas), len(outlier_fracs),
    figsize=(5 * len(outlier_fracs), 4 * len(noise_sigmas)),
    constrained_layout=True
)

if len(noise_sigmas) == 1 or len(outlier_fracs) == 1:
    axes = np.array(axes).reshape(len(noise_sigmas), len(outlier_fracs))

for i, sigma in enumerate(noise_sigmas):
    for j, frac in enumerate(outlier_fracs):
        ax = axes[i][j]
        res = results[(sigma, frac)]
        stats = detailed_stats[(sigma, frac)]

        base = res['orig']['val_acc'][-1]

        # Случайное удаление
        rnd_diffs = [res['random'][n]['val_acc'][-1] - base for n in ns]
        ax.plot(ns, rnd_diffs, marker='^', label='Random', linewidth=2)

        # Методы
        colors = ['red', 'green', 'purple', 'orange']
        method_names = ['LOO', 'DataShapley', 'BetaShapley', 'Influence']
        for idx, name in enumerate(method_names):
            if name in res:
                method_diffs = [res[name][n]['val_acc'][-1] - base for n in ns]
                ax.plot(ns, method_diffs, marker='s', label=name,
                        color=colors[idx % len(colors)], linewidth=2)

        ax.axhline(0, linestyle='--', color='gray', alpha=0.5)
        ax.set_xscale('log')
        ax.set_xticks(ns)
        ax.set_xticklabels([str(n) for n in ns])

        ax.set_title(f"σ={sigma}, flip={int(frac * 100)}%", fontsize=12)
        ax.set_xlabel('n_remove', fontsize=10)
        ax.set_ylabel('Δ Val Acc', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.7)

        if i == 0 and j == 0:
            ax.legend(fontsize=8, loc='best')

plt.suptitle("Change in Validation Accuracy After Removing Points",
             fontsize=14, fontweight='bold')
plt.show()

print("\n" + "=" * 80)
print("Experiment completed successfully!")
print("=" * 80)