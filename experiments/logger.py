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

    def save_results(self, results, scores, scores_raw, n_remove_list, random_run_results=None):
        """Сохраняет результаты в pickle файл"""
        data_to_save = {
            'results': results,
            'scores': scores,
            'scores_raw': scores_raw,
            'n_remove_list': n_remove_list,
            'random_run_results': random_run_results,
            'timestamp': pd.Timestamp.now(),
            'experiment_dir': str(self.experiment_dir),
            'timings': self.timings
        }

        with open(self.results_file, 'wb') as f:
            pickle.dump(data_to_save, f)

        self.log_message(f"Results saved: {self.results_file}")

    def save_config(self, config):
        """
        Сохраняет конфигурацию эксперимента в JSON без дублирования.
        Нормализует структуру конфига, чтобы избежать повторений.
        """
        # Нормализованный конфиг без дублирования
        normalized_config = self._normalize_config(config)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(normalized_config, f, indent=2, ensure_ascii=False)

        self.log_message(f"Config saved: {self.config_file}")

    def _normalize_config(self, config):
        """
        Нормализует конфиг, удаляя дублирование и стандартизируя структуру.
        
        Правило: каждый параметр сохраняется ОДИН раз в нужной секции.
        """
        normalized = {
            'metadata': {
                'experiment_dir': str(self.experiment_dir),
                'timestamp': pd.Timestamp.now().isoformat(),
            },
            'environment': {
                'debug_mode': config.get('debug_mode', False),
                'device': config.get('model_params', {}).get('device', 'cpu'),
            },
            'versions': {
                'pydvl': config.get('pyDVL_version'),
                'torch': config.get('torch_version'),
                'cuda': config.get('cuda_version'),
            },
            'dataset': config.get('dataset', {}),
            'model': {},
            'training': {},
            'data_processing': {},
        }

        # Обработка model_params - извлекаем только необходимое
        model_params = config.get('model_params', {})
        normalized['model'] = {
            'type': model_params.get('model_type'),
            'architecture': model_params.get('model_architecture'),
            'input_size': model_params.get('input_size'),
            'device': model_params.get('device'),
        }

        # Параметры дистилляции - только если используется
        if model_params.get('use_distillation'):
            normalized['model']['distillation'] = {
                'enabled': True,
                'epochs': model_params.get('distillation_epochs'),
                'temperature': model_params.get('temperature'),
                'student_architecture': model_params.get('student_architecture'),
            }

        # Обработка training_params - убираем дублирование
        training_params = config.get('training_params', {})
        
        # Определяем removal strategy - берем из одного источника
        removal_strategy = training_params.get('removal_strategy') or \
                         training_params.get('removal_strategies', [None])[0] or \
                         'remove_lowest_influence'
        
        # Определяем n_remove_list - берем один список, не оба
        n_remove_list = training_params.get('n_remove_list') or \
                       training_params.get('n_remove_percentages') or []
        
        normalized['training'] = {
            'test_size': training_params.get('test_size'),
            'val_size': training_params.get('val_size'),
            'epochs': training_params.get('n_epochs'),
            'cv_folds': training_params.get('cv_folds'),
            'sample_size_percentage': training_params.get('sample_size_percentage'),
            'removal': {
                'strategy': removal_strategy,
                'sample_counts': n_remove_list,
                'count': len(n_remove_list) if n_remove_list else 0,
            } if n_remove_list else None
        }

        # Информация о данных
        data_info = config.get('data_info', {})
        if data_info:
            normalized['data_processing'] = {
                'original_rows': data_info.get('original_rows'),
                'final_training_rows': data_info.get('final_training_rows'),
                'features': {
                    'numeric': data_info.get('numeric_columns'),
                    'categorical': data_info.get('categorical_columns'),
                    'total': data_info.get('total_features'),
                }
            }

        # Добавляем расширенные параметры методов если они есть
        if 'pydvl_config' in config or 'influence_params' in config:
            normalized['methods_config'] = config.get('pydvl_config') or config.get('influence_params')

        return self._clean_none_values(normalized)

    def _clean_none_values(self, d):
        """Удаляет пустые значения из словаря рекурсивно"""
        if isinstance(d, dict):
            return {k: self._clean_none_values(v) for k, v in d.items() if v is not None and v != {}}
        elif isinstance(d, list):
            return [self._clean_none_values(item) for item in d if item is not None]
        return d

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
        """
        Генерирует итоговый отчет с результатами эксперимента.
        Не дублирует информацию из config.json - ссылается на него.
        Фокусируется на результатах, метриках и статистике.
        """
        summary_file = self.experiment_dir / "experiment_summary.txt"

        total_experiment_time, valid_timings = self._calculate_total_experiment_time()
        wall_clock_time = time.time() - self.start_time

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("EXPERIMENT SUMMARY\n")
            f.write("=" * 80 + "\n\n")

            f.write("REFERENCE:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Full configuration: config.json\n")
            f.write(f"Experiment directory: {self.experiment_dir}\n")
            f.write(f"Results: results.pkl\n\n")

            # === TIMING INFORMATION ===
            f.write("=" * 80 + "\n")
            f.write("TIMING INFORMATION:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total experiment duration (sum of all stages): {total_experiment_time:.2f} seconds\n")
            f.write(f"Wall clock time: {wall_clock_time:.2f} seconds\n")
            if wall_clock_time > 0:
                efficiency = (total_experiment_time / wall_clock_time * 100)
                f.write(f"Parallel efficiency: {efficiency:.1f}%\n\n")
            else:
                f.write(f"Parallel efficiency: N/A\n\n")

            sorted_timings = sorted(valid_timings, key=lambda x: x[1], reverse=True)
            f.write("Detailed timing breakdown (top 10):\n")
            for method_name, duration in sorted_timings[:10]:
                percentage = (duration / total_experiment_time * 100) if total_experiment_time > 0 else 0
                f.write(f"  {method_name:<35} {duration:>10.2f}s  ({percentage:>5.1f}%)\n")

            # === MODEL PERFORMANCE ===
            f.write("\n" + "=" * 80 + "\n")
            f.write("MODEL PERFORMANCE METRICS:\n")
            f.write("-" * 40 + "\n")
            if model_metrics:
                for key, value in sorted(model_metrics.items()):
                    if isinstance(value, float):
                        f.write(f"  {key:<40} {value:.10f}\n")
                    else:
                        f.write(f"  {key:<40} {value}\n")
            else:
                f.write("No model metrics available.\n")

            # === INFLUENCE METHOD STATISTICS ===
            f.write("\n" + "=" * 80 + "\n")
            f.write("INFLUENCE METHOD STATISTICS (NORMALIZED VALUES):\n")
            f.write("-" * 40 + "\n")
            if influence_stats:
                for method_name, stats in sorted(influence_stats.items()):
                    f.write(f"\n{method_name}:\n")
                    for stat_name, stat_value in sorted(stats.items()):
                        if isinstance(stat_value, float):
                            f.write(f"  {stat_name:<35} {stat_value:.10f}\n")
                        else:
                            f.write(f"  {stat_name:<35} {stat_value}\n")
            else:
                f.write("No influence statistics available.\n")

            # === DETAILED SCORE STATISTICS ===
            f.write("\n" + "=" * 80 + "\n")
            f.write("DETAILED SCORE STATISTICS:\n")
            f.write("-" * 40 + "\n")

            # Normalized scores
            f.write("\nNORMALIZED SCORES (0-1 range):\n")
            for method_name, values in sorted(scores.items()):
                if len(values) > 0:
                    f.write(f"\n{method_name}:\n")
                    self._write_score_statistics(f, values)
                else:
                    f.write(f"\n{method_name}: [No data]\n")

            # Raw scores
            f.write("\n" + "-" * 40 + "\n")
            f.write("RAW SCORES (original scale):\n")
            for method_name, values in sorted(scores_raw.items()):
                if len(values) > 0:
                    f.write(f"\n{method_name}:\n")
                    self._write_score_statistics(f, values, raw=True)
                else:
                    f.write(f"\n{method_name}: [No data]\n")

            # === SUMMARY STATISTICS ===
            f.write("\n" + "=" * 80 + "\n")
            f.write("SUMMARY STATISTICS:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Number of influence methods evaluated: {len(influence_stats)}\n")
            f.write(f"Number of scores per method: {len(list(scores.values())[0]) if scores else 0}\n")
            f.write(f"Total experiment time: {wall_clock_time:.2f} seconds (~{wall_clock_time/60:.2f} minutes)\n")
            f.write(f"Experiment date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        self.log_message(f"Summary saved: {summary_file}")

    def _write_score_statistics(self, f, values, raw=False):
        """Вспомогательный метод для вывода статистики по scores"""
        f.write(f"  Data points: {len(values)}\n")
        f.write(f"  Min:       {np.min(values):.10f}\n")
        f.write(f"  Max:       {np.max(values):.10f}\n")
        f.write(f"  Mean:      {np.mean(values):.10f}\n")
        f.write(f"  Median:    {np.median(values):.10f}\n")
        f.write(f"  Std Dev:   {np.std(values):.10f}\n")
        f.write(f"  Q1 (25%):  {np.percentile(values, 25):.10f}\n")
        f.write(f"  Q3 (75%):  {np.percentile(values, 75):.10f}\n")
        
        if raw:
            f.write(f"  Range:     {np.max(values) - np.min(values):.10f}\n")
            
            positive_vals = values[values > 0]
            negative_vals = values[values < 0]
            zero_vals = values[values == 0]
            
            f.write(f"  Sign distribution:\n")
            f.write(f"    Positive: {len(positive_vals):4d}/{len(values)}  ({len(positive_vals)/len(values)*100:5.1f}%)\n")
            f.write(f"    Negative: {len(negative_vals):4d}/{len(values)}  ({len(negative_vals)/len(values)*100:5.1f}%)\n")
            f.write(f"    Zero:     {len(zero_vals):4d}/{len(values)}  ({len(zero_vals)/len(values)*100:5.1f}%)\n")
            
            if len(positive_vals) > 0:
                f.write(f"  Positive - Min: {np.min(positive_vals):.10f}, "
                        f"Max: {np.max(positive_vals):.10f}, Mean: {np.mean(positive_vals):.10f}\n")
            if len(negative_vals) > 0:
                f.write(f"  Negative - Min: {np.min(negative_vals):.10f}, "
                        f"Max: {np.max(negative_vals):.10f}, Mean: {np.mean(negative_vals):.10f}\n")
        else:
            f.write(f"  Non-zero: {np.sum(values != 0)}/{len(values)}\n")

    def get_experiment_dir(self):
        """Возвращает путь к папке эксперимента"""
        return self.experiment_dir


def debug_print(*args, **kwargs):
    from config.settings import DEBUG_MODE
    if DEBUG_MODE:
        print("[DEBUG]", *args, **kwargs)