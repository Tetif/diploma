import time
import json
import pickle
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np


class ExperimentLogger:
    """Класс для логирования эксперимента и сохранения результатов"""

    def __init__(self, base_dir="experiments", experiment_name=None):
        self.start_time = time.time()
        self.experiment_dir = self._create_experiment_dir(base_dir, experiment_name)
        self.log_file = self.experiment_dir / "experiment_log.txt"
        self.results_file = self.experiment_dir / "results.pkl"
        self.config_file = self.experiment_dir / "config.json"
        self.timings = {}

        print(f"Experiment directory: {self.experiment_dir}")

    def _create_experiment_dir(self, base_dir, experiment_name):
        """Создает вложенную структуру папок: дата/время/название"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M-%S")

        if experiment_name:
            experiment_dir = Path(base_dir) / date_str / time_str / experiment_name
        else:
            experiment_dir = Path(base_dir) / date_str / time_str

        experiment_dir.mkdir(parents=True, exist_ok=True)
        return experiment_dir

    def log_message(self, message):
        """Записывает сообщение в лог-файл и выводит на экран"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')

        print(log_entry)

    def start_timing(self, method_name):
        """Начинает замер времени для метода"""
        self.timings[method_name] = {
            'start': time.time(),
            'end': None,
            'duration': None
        }

    def end_timing(self, method_name):
        """Заканчивает замер времени для метода"""
        if method_name in self.timings:
            self.timings[method_name]['end'] = time.time()
            self.timings[method_name]['duration'] = (
                    self.timings[method_name]['end'] - self.timings[method_name]['start']
            )

    def save_plot(self, plt, plot_name):
        """Сохраняет график в папку эксперимента"""
        plot_path = self.experiment_dir / f"{plot_name}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        self.log_message(f"Plot saved: {plot_name}.png")

    def save_results(self, results, scores, scores_raw, n_remove_list):
        """Сохраняет результаты в pickle файл"""
        data_to_save = {
            'results': results,
            'scores': scores,
            'scores_raw': scores_raw,
            'n_remove_list': n_remove_list,
            'timestamp': pd.Timestamp.now(),
            'experiment_dir': str(self.experiment_dir),
            'timings': self.timings
        }

        with open(self.results_file, 'wb') as f:
            pickle.dump(data_to_save, f)

        self.log_message(f"Results saved: {self.results_file}")

    def save_config(self, config):
        """Сохраняет конфигурацию эксперимента в JSON"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        self.log_message(f"Config saved: {self.config_file}")

    def _calculate_total_experiment_time(self):
        """Вычисляет общее время эксперимента как сумму всех этапов"""
        total_time = 0.0
        valid_timings = []

        for method_name, timing in self.timings.items():
            if timing['duration'] is not None:
                total_time += timing['duration']
                valid_timings.append((method_name, timing['duration']))

        return total_time, valid_timings

    def generate_summary(self, config, model_metrics, influence_stats, scores, scores_raw):
        """Генерирует итоговый отчет с сырыми и нормализованными значениями"""
        summary_file = self.experiment_dir / "experiment_summary.txt"

        total_experiment_time, valid_timings = self._calculate_total_experiment_time()
        wall_clock_time = time.time() - self.start_time

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("EXPERIMENT SUMMARY\n")
            f.write("=" * 80 + "\n\n")

            f.write("TIMING INFORMATION:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total experiment duration (sum of all stages): {total_experiment_time:.2f} seconds\n")
            f.write(f"Wall clock time: {wall_clock_time:.2f} seconds\n")
            f.write(f"Efficiency: {(total_experiment_time / wall_clock_time * 100):.1f}%\n\n")

            sorted_timings = sorted(valid_timings, key=lambda x: x[1], reverse=True)

            f.write("Detailed timing breakdown:\n")
            for method_name, duration in sorted_timings:
                percentage = (duration / total_experiment_time * 100) if total_experiment_time > 0 else 0
                f.write(f"  {method_name}: {duration:.2f} seconds ({percentage:.1f}%)\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("EXPERIMENT CONFIGURATION:\n")
            f.write("-" * 40 + "\n")
            for key, value in config.items():
                if isinstance(value, dict):
                    f.write(f"{key}:\n")
                    for sub_key, sub_value in value.items():
                        f.write(f"  {sub_key}: {sub_value}\n")
                else:
                    f.write(f"{key}: {value}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("MODEL PERFORMANCE:\n")
            f.write("-" * 40 + "\n")
            for key, value in model_metrics.items():
                f.write(f"{key}: {value}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("INFLUENCE METHOD STATISTICS:\n")
            f.write("-" * 40 + "\n")
            for method_name, stats in influence_stats.items():
                f.write(f"\n{method_name}:\n")
                for stat_name, stat_value in stats.items():
                    f.write(f"  {stat_name}: {stat_value}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("DETAILED SCORE STATISTICS:\n")
            f.write("-" * 40 + "\n")

            f.write("\nSCORES:\n")
            for method_name, values in scores.items():
                if len(values) > 0:
                    f.write(f"\n{method_name}:\n")
                    f.write(f"  Min: {np.min(values):.8f}\n")
                    f.write(f"  Max: {np.max(values):.8f}\n")
                    f.write(f"  Mean: {np.mean(values):.8f}\n")
                    f.write(f"  Median: {np.median(values):.8f}\n")
                    f.write(f"  Std: {np.std(values):.8f}\n")
                    f.write(f"  Q1: {np.percentile(values, 25):.8f}\n")
                    f.write(f"  Q3: {np.percentile(values, 75):.8f}\n")
                    f.write(f"  Non-zero: {np.sum(values != 0)}/{len(values)}\n")

            f.write("\n\nRAW SCORES (original scale):\n")
            for method_name, values in scores_raw.items():
                if len(values) > 0:
                    f.write(f"\n{method_name}:\n")
                    f.write(f"  Min: {np.min(values):.10f}\n")
                    f.write(f"  Max: {np.max(values):.10f}\n")
                    f.write(f"  Mean: {np.mean(values):.10f}\n")
                    f.write(f"  Median: {np.median(values):.10f}\n")
                    f.write(f"  Std: {np.std(values):.10f}\n")
                    f.write(f"  Q1: {np.percentile(values, 25):.10f}\n")
                    f.write(f"  Q3: {np.percentile(values, 75):.10f}\n")
                    f.write(f"  Range: {np.max(values) - np.min(values):.10f}\n")
                    f.write(f"  Non-zero: {np.sum(values != 0)}/{len(values)}\n")

                    positive_vals = values[values > 0]
                    negative_vals = values[values < 0]
                    zero_vals = values[values == 0]

                    f.write(f"  Positive values: {len(positive_vals)}/{len(values)}\n")
                    f.write(f"  Negative values: {len(negative_vals)}/{len(values)}\n")
                    f.write(f"  Zero values: {len(zero_vals)}/{len(values)}\n")

                    if len(positive_vals) > 0:
                        f.write(f"  Positive stats - Min: {np.min(positive_vals):.10f}, "
                                f"Max: {np.max(positive_vals):.10f}, Mean: {np.mean(positive_vals):.10f}\n")

                    if len(negative_vals) > 0:
                        f.write(f"  Negative stats - Min: {np.min(negative_vals):.10f}, "
                                f"Max: {np.max(negative_vals):.10f}, Mean: {np.mean(negative_vals):.10f}\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("EXPERIMENT DIRECTORY:\n")
            f.write("-" * 40 + "\n")
            f.write(f"{self.experiment_dir}\n")

        self.log_message(f"Summary saved: {summary_file}")

    def get_experiment_dir(self):
        """Возвращает путь к папке эксперимента"""
        return self.experiment_dir


def debug_print(*args, **kwargs):
    from config.settings import DEBUG_MODE
    if DEBUG_MODE:
        print("[DEBUG]", *args, **kwargs)