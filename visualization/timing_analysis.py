#!/usr/bin/env python3
"""
Timing Analysis Tool for Influence Methods

This script analyzes and visualizes the execution time of different influence methods
from experiment summary files.

Usage:
    python timing_analysis.py [experiment_path]

    experiment_path: Path to experiment directory (optional)
                    If not provided, uses default: experiment_logs/2025-12-24/02-31-40
                    Can be relative to project root or absolute path

Examples:
    python timing_analysis.py
    python timing_analysis.py experiment_logs/2025-12-24/00-09-02
    python timing_analysis.py /full/path/to/experiment

The script will display a bar chart showing execution times for all influence methods
found in the experiment_summary.txt file.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import re
import sys
from pathlib import Path


def parse_experiment_summary(experiment_path):
    """
    Парсит файл experiment_summary.txt и извлекает время выполнения методов

    Args:
        experiment_path: путь к папке эксперимента

    Returns:
        dict: словарь с временами выполнения методов {method_name: time_seconds}
    """
    summary_file = Path(experiment_path) / "experiment_summary.txt"

    if not summary_file.exists():
        raise FileNotFoundError(f"Файл experiment_summary.txt не найден в {experiment_path}")

    timing_data = {}

    with open(summary_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ищем секцию "Detailed timing breakdown:"
    timing_section = re.search(r'Detailed timing breakdown:(.*?)(?=\n\n|\n=)', content, re.DOTALL)

    if timing_section:
        timing_lines = timing_section.group(1).strip().split('\n')

        for line in timing_lines:
            line = line.strip()
            if line and '_computation:' in line:
                # Парсим строку вида "Method_computation: 123.45 seconds (78.9%)"
                match = re.match(r'(\w+)_computation:\s*([\d.]+)\s*seconds', line)
                if match:
                    method_name = match.group(1)
                    time_seconds = float(match.group(2))
                    timing_data[method_name] = time_seconds

    return timing_data


def plot_timing_comparison(experiment_paths, experiment_names=None, save_path=None):
    """
    Строит столбчатую диаграмму сравнения времени выполнения методов

    Args:
        experiment_paths: список путей к папкам экспериментов
        experiment_names: список имен экспериментов (опционально)
        save_path: путь для сохранения графика (опционально)
    """
    if experiment_names is None:
        experiment_names = [f"Exp_{i+1}" for i in range(len(experiment_paths))]

    # Собираем данные по всем экспериментам
    all_methods = set()
    timing_data = {}

    for exp_path, exp_name in zip(experiment_paths, experiment_names):
        try:
            exp_timing = parse_experiment_summary(exp_path)
            timing_data[exp_name] = exp_timing
            all_methods.update(exp_timing.keys())
        except Exception as e:
            print(f"Ошибка при обработке {exp_path}: {e}")
            continue

    if not timing_data:
        print("Не удалось загрузить данные ни из одного эксперимента")
        return

    # Сортируем методы по общему времени выполнения
    all_methods = sorted(all_methods)

    # Создаем график
    fig, ax = plt.subplots(figsize=(12, 6))

    # Настройки позиций
    n_experiments = len(timing_data)
    n_methods = len(all_methods)
    bar_width = 0.8 / n_experiments

    # Цвета для разных экспериментов
    colors = plt.cm.tab10(np.linspace(0, 1, n_experiments))

    for i, (exp_name, exp_data) in enumerate(timing_data.items()):
        # Получаем времена для всех методов (0 если метод не использовался)
        times = [exp_data.get(method, 0) for method in all_methods]

        # Позиции столбцов
        positions = np.arange(n_methods) + i * bar_width - (n_experiments - 1) * bar_width / 2

        bars = ax.bar(positions, times, bar_width, label=exp_name, color=colors[i], alpha=0.8)

        # Добавляем значения над столбцами
        for bar, time in zip(bars, times):
            if time > 0:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + max(times) * 0.01,
                       f'{time:.1f}s', ha='center', va='bottom', fontsize=8, rotation=90)

    # Настройки графика
    ax.set_xlabel('Методы влияния')
    ax.set_ylabel('Время выполнения (секунды)')
    ax.set_title('Сравнение времени выполнения методов влияния')
    ax.set_xticks(np.arange(n_methods))
    ax.set_xticklabels(all_methods, rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend()

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен в: {save_path}")

    return plt


def plot_single_experiment_timing(experiment_path, save_path=None):
    """
    Строит столбчатую диаграмму времени выполнения методов для одного эксперимента

    Args:
        experiment_path: путь к папке эксперимента
        save_path: путь для сохранения графика (опционально)
    """
    try:
        timing_data = parse_experiment_summary(experiment_path)
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    if not timing_data:
        print("Не удалось извлечь данные о времени выполнения")
        return

    # Сортируем по времени выполнения (по убыванию)
    sorted_methods = sorted(timing_data.items(), key=lambda x: x[1], reverse=True)
    methods, times = zip(*sorted_methods)

    # Создаем график
    fig, ax = plt.subplots(figsize=(10, 6))

    # Цвета для столбцов
    colors = plt.cm.viridis(np.linspace(0, 1, len(methods)))

    bars = ax.bar(methods, times, color=colors, alpha=0.8)

    # Добавляем значения над столбцами
    for bar, time in zip(bars, times):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(times) * 0.01,
               f'{time:.1f}s', ha='center', va='bottom', fontsize=9)

    # Настройки графика
    ax.set_xlabel('Методы влияния')
    ax.set_ylabel('Время выполнения (секунды)')
    ax.set_title(f'Время выполнения методов влияния')
    ax.grid(True, alpha=0.3, axis='y')

    # Поворачиваем подписи если они длинные
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"График сохранен в: {save_path}")

    return plt


if __name__ == "__main__":
    # Получаем путь к корневой директории проекта относительно текущего файла
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Если передан аргумент командной строки, используем его
    if len(sys.argv) > 1:
        experiment_path_arg = sys.argv[1]
        # Если путь относительный, делаем его абсолютным относительно корня проекта
        if not Path(experiment_path_arg).is_absolute():
            experiment_path = project_root / experiment_path_arg
        else:
            experiment_path = Path(experiment_path_arg)
    else:
        # Пример использования для одного эксперимента (по умолчанию)
        experiment_path = project_root / "experiment_logs" / "2025-12-24" / "00-09-02"

    print(f"Анализ эксперимента: {experiment_path}")
    plot_single_experiment_timing(str(experiment_path))
    plt.show()
