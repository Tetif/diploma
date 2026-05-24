import re
import time
import json
import pickle
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
from config import settings as settings_module
from config.settings import METRIC_METADATA


def _process_rss_bytes():
    """Текущий RSS процесса (байт). Без psutil — None."""
    try:
        import psutil
        return int(psutil.Process().memory_info().rss)
    except Exception:
        return None


def _reset_cuda_peak_memory_stats():
    try:
        import torch
        if not torch.cuda.is_available():
            return
        for i in range(torch.cuda.device_count()):
            torch.cuda.reset_peak_memory_stats(i)
    except Exception:
        pass


def _cuda_peak_allocated_bytes_sum():
    """Сумма пиков выделенной памяти по всем CUDA-устройствам за интервал после reset."""
    try:
        import torch
        if not torch.cuda.is_available():
            return None
        total = 0
        for i in range(torch.cuda.device_count()):
            total += int(torch.cuda.max_memory_allocated(i))
        return total
    except Exception:
        return None


def _parse_cuda_oom_tried_allocate_mb(message: str):
    """
    Из сообщения CUDA OOM (PyTorch) достаёт размер неудачного выделения, в МБ (2**20 байт).
    Пример: 'Tried to allocate 16.63 GiB. GPU 0 has a total capacity of...'
    """
    if not message:
        return None
    m = re.search(
        r"Tried to allocate\s+([\d.]+)\s*(GiB|MiB|KiB|GB|MB)\b",
        message,
        flags=re.IGNORECASE,
    )
    if not m:
        return None
    val = float(m.group(1))
    unit = m.group(2).lower()
    # Как и для gpu_peak_mb: МБ = байт / (1024**2)
    if unit in ("gib", "gb"):
        return val * (1024.0**3) / (1024.0**2)
    if unit in ("mib", "mb"):
        return val
    if unit in ("kib",):
        return val / 1024.0
    return None


class ExperimentLogger:
    """Класс для логирования эксперимента и сохранения результатов"""

    def __init__(self, base_dir="experiments", experiment_name=None):
        self.start_time = time.time()
        self.experiment_dir = self._create_experiment_dir(base_dir, experiment_name)
        self.log_file = self.experiment_dir / "experiment_log.txt"
        self.results_file = self.experiment_dir / "results.pkl"
        self.config_file = self.experiment_dir / "config.json"
        self.timings = {}

        print(f"Каталог эксперимента: {self.experiment_dir}")

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
        _reset_cuda_peak_memory_stats()
        self.timings[method_name] = {
            'start': time.time(),
            'end': None,
            'duration': None,
            'ram_rss_start_bytes': _process_rss_bytes(),
        }

    def end_timing(self, method_name):
        """Заканчивает замер времени для метода"""
        if method_name in self.timings:
            self.timings[method_name]['end'] = time.time()
            self.timings[method_name]['duration'] = (
                    self.timings[method_name]['end'] - self.timings[method_name]['start']
            )
            rss_end = _process_rss_bytes()
            rss_start = self.timings[method_name].get('ram_rss_start_bytes')
            self.timings[method_name]['ram_rss_end_bytes'] = rss_end
            if rss_start is not None and rss_end is not None:
                self.timings[method_name]['ram_peak_mb'] = max(rss_start, rss_end) / (1024.0 ** 2)
            elif rss_end is not None:
                self.timings[method_name]['ram_peak_mb'] = rss_end / (1024.0 ** 2)
            elif rss_start is not None:
                self.timings[method_name]['ram_peak_mb'] = rss_start / (1024.0 ** 2)
            else:
                self.timings[method_name]['ram_peak_mb'] = None

            gpu_b = _cuda_peak_allocated_bytes_sum()
            self.timings[method_name]['gpu_peak_mb'] = (
                gpu_b / (1024.0 ** 2) if gpu_b is not None else None
            )

    def record_cuda_oom_if_applicable(self, method_name, exc):
        """
        После end_timing: если было CUDA OOM, из текста исключения читается «Tried to allocate …».
        Сохраняет gpu_oom_requested_mb и gpu_memory_max_wanted_mb = max(peak, запрос).
        """
        if method_name not in self.timings or exc is None:
            return
        msg = str(exc)
        req_mb = _parse_cuda_oom_tried_allocate_mb(msg)
        if req_mb is None:
            return
        t = self.timings[method_name]
        t['gpu_oom_requested_mb'] = req_mb
        peak = t.get('gpu_peak_mb')
        if peak is None:
            peak = 0.0
        t['gpu_memory_max_wanted_mb'] = max(float(peak), float(req_mb))
        try:
            self.log_message(
                f"CUDA OOM parsed: stage={method_name}, requested_alloc≈{req_mb:.2f} MB, "
                f"peak_allocated={peak:.2f} MB, max_wanted≈{t['gpu_memory_max_wanted_mb']:.2f} MB"
            )
        except Exception:
            pass

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

    def save_influence_weights_to_experiment_dir(
        self,
        scores_raw,
        dataset_name: str,
        n_train: int,
        n_remove_list: list,
    ):
        """
        Save influence weights to experiment dir as influence_weights.pkl
        for later reuse (e.g. plot_removal_from_weights.py).
        """
        from influence.io import save_influence_weights
        from datetime import datetime
        metadata = {
            'dataset_name': dataset_name,
            'n_train': n_train,
            'n_remove_list': n_remove_list,
            'methods': list(scores_raw.keys()),
            'timestamp': datetime.now().isoformat(),
        }
        path = self.experiment_dir / "influence_weights.pkl"
        save_influence_weights(scores_raw, metadata, path)
        self.log_message(f"Influence weights saved: {path}")

    def save_config(self, config):
        """
        Сохраняет конфигурацию эксперимента в JSON без дублирования.
        Нормализует структуру конфига, чтобы избежать повторений.
        """
        # Нормализованный конфиг без дублирования
        normalized_config = self._normalize_config(config)

        # Снимок всех ключевых настроек из config/settings.py,
        # чтобы в config.json всегда сохранялась полная конфигурация.
        normalized_config["settings_snapshot"] = self._get_settings_snapshot()

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(normalized_config, f, indent=2, ensure_ascii=False)

        self.log_message(f"Config saved: {self.config_file}")

        # Попытаться создать diff с предыдущим конфигом (если он существует)
        try:
            prev_config_path = self._find_previous_config_path()
            if prev_config_path and prev_config_path.exists():
                with open(prev_config_path, 'r', encoding='utf-8') as pf:
                    prev_config = json.load(pf)
                diff_lines = self._generate_config_diff(prev_config, normalized_config)
                if diff_lines:
                    diff_path = self.experiment_dir / "diff.txt"
                    with open(diff_path, 'w', encoding='utf-8') as df:
                        df.write("\n".join(diff_lines))
                    self.log_message(f"Config diff saved: {diff_path}")
        except Exception as e:
            # Diff не критичен для работы эксперимента, поэтому ошибки здесь не фатальны
            self.log_message(f"Warning: failed to generate config diff: {e}")

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
        
        # Берем фактически используемую стратегию из model_params, затем fallback к training_params.
        removal_strategy = model_params.get('removal_strategy') or \
                         training_params.get('removal_strategy') or \
                         training_params.get('removal_strategies', [None])[0] or \
                         'remove_lowest_influence'
        
        # Определяем n_remove_list - берем один список, не оба.
        # Приоритет: явные проценты из experiment_params, затем legacy-поля.
        n_remove_list = (
            training_params.get('n_remove_percentages')
            or config.get('experiment_params', {}).get('n_remove_percentages')
            or training_params.get('n_remove_list')
            or config.get('experiment_params', {}).get('n_remove_list')
            or []
        )
        loss_removal_methods = training_params.get('loss_removal_methods') or \
                              config.get('experiment_params', {}).get('loss_removal_methods') or []
        
        normalized['training'] = {
            'test_size': training_params.get('test_size'),
            'val_size': training_params.get('val_size'),
            'epochs': training_params.get('n_epochs'),
            'cv_folds': training_params.get('cv_folds'),
            'sample_size_percentage': training_params.get('sample_size_percentage'),
            'removal': {
                'strategy': removal_strategy,
                'loss_methods': loss_removal_methods,
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

    def _get_settings_snapshot(self):
        """
        Возвращает JSON-сериализуемый снимок всех основных конфигов из config/settings.py.
        Здесь собираются только примитивы и словари/списки, чтобы json.dump не падал.
        """
        snapshot = {
            "CURRENT_DATASET": settings_module.CURRENT_DATASET,
            "DEBUG_MODE": settings_module.DEBUG_MODE,
            "EXPERIMENTS_BASE_DIR": settings_module.EXPERIMENTS_BASE_DIR,
            "CACHE_DIR": settings_module.CACHE_DIR,
            "USE_CACHE": settings_module.USE_CACHE,
            "DEVICE": settings_module.DEVICE,
            "N_JOBS": settings_module.N_JOBS,
            "RANDOM_STATE": settings_module.RANDOM_STATE,
            "MODEL_RUN_CONFIG": settings_module.MODEL_RUN_CONFIG,
            "INFLUENCE_METHODS_CONFIG": settings_module.INFLUENCE_METHODS_CONFIG,
            "EXPERIMENT_CONFIG": settings_module.EXPERIMENT_CONFIG,
            "REMOVAL_STRATEGIES": settings_module.REMOVAL_STRATEGIES,
            "METRIC_CONFIG": settings_module.METRIC_CONFIG,
            "METRIC_METADATA": settings_module.METRIC_METADATA,
            "PYDVL_CONFIG": settings_module.PYDVL_CONFIG,
            "DATASET_INFLUENCE_PARAMS": settings_module.DATASET_INFLUENCE_PARAMS,
            "DISTILLATION_CONFIG": settings_module.DISTILLATION_CONFIG,
            "SYNTHETIC_DATA_CONFIG": settings_module.SYNTHETIC_DATA_CONFIG,
        }
        return snapshot

    def _find_previous_config_path(self) -> Path | None:
        """
        Ищет config.json предыдущего эксперимента в пределах той же даты.
        Ориентируется на структуру experiment_logs/YYYY-MM-DD/HH-MM-SS/.
        """
        try:
            # Ожидаем, что self.experiment_dir = .../YYYY-MM-DD/HH-MM-SS
            date_dir = self.experiment_dir.parent
            if not date_dir.exists():
                return None

            # Собираем все поддиректории с конфигами в этой дате
            candidates = []
            for subdir in date_dir.iterdir():
                if subdir.is_dir():
                    cfg_path = subdir / "config.json"
                    if cfg_path.exists():
                        candidates.append(cfg_path)

            # Отсортировать по имени директории (времени) и выбрать предыдущий
            candidates_sorted = sorted(
                candidates,
                key=lambda p: p.parent.name
            )

            previous = None
            for cfg_path in candidates_sorted:
                if cfg_path.parent == self.experiment_dir:
                    break
                previous = cfg_path
            return previous
        except Exception:
            return None

    def _generate_config_diff(self, old_cfg: dict, new_cfg: dict):
        """
        Генерирует человекочитаемый diff между двумя конфигами.
        Формат строк: path.to.key: old_value -> new_value
        """

        def _walk(old, new, path_prefix=""):
            lines = []
            if isinstance(old, dict) and isinstance(new, dict):
                keys = sorted(set(old.keys()) | set(new.keys()))
                for key in keys:
                    new_path = f"{path_prefix}.{key}" if path_prefix else str(key)
                    if key not in old:
                        lines.append(f"{new_path}: [added] -> {repr(new[key])}")
                    elif key not in new:
                        lines.append(f"{new_path}: {repr(old[key])} -> [removed]")
                    else:
                        lines.extend(_walk(old[key], new[key], new_path))
            elif isinstance(old, list) and isinstance(new, list):
                if old != new:
                    lines.append(f"{path_prefix}: {repr(old)} -> {repr(new)}")
            else:
                if old != new:
                    lines.append(f"{path_prefix}: {repr(old)} -> {repr(new)}")
            return lines

        return _walk(old_cfg, new_cfg)

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

    @staticmethod
    def _format_run_metadata_block(_config) -> str:
        """
        Короткий блок для experiment_summary: датасет и sample_size_percentage,
        если они есть в dict конфигурации (main, API saved_config, скрипты).
        """
        if not isinstance(_config, dict):
            return ""
        dataset = None
        d = _config.get("dataset")
        if isinstance(d, dict):
            dataset = d.get("name")
        if dataset is None:
            dataset = _config.get("dataset_name")
        pct = _config.get("sample_size_percentage")
        if pct is None:
            tp = _config.get("training_params")
            if isinstance(tp, dict):
                pct = tp.get("sample_size_percentage")
        if pct is None:
            tr = _config.get("training")
            if isinstance(tr, dict):
                pct = tr.get("sample_size_percentage")
        model_type = None
        mp = _config.get("model_params")
        if isinstance(mp, dict):
            model_type = mp.get("model_type")
        if model_type is None:
            m = _config.get("model")
            if isinstance(m, dict):
                model_type = m.get("type")
        lines = []
        if dataset is not None:
            lines.append(f"dataset: {dataset}")
        if pct is not None:
            lines.append(f"sample_size_percentage: {pct}")
        if model_type is not None:
            lines.append(f"model_type: {model_type}")
        if not lines:
            return ""
        return (
            "=" * 80 + "\n"
            "RUN METADATA\n"
            "-" * 40 + "\n"
            + "\n".join(lines) + "\n\n"
        )

    def generate_summary(
        self,
        _config,
        model_metrics,
        influence_stats,
        _scores,
        scores_raw,
        removal_results=None,
        n_remove_list=None,
    ):
        """
        Краткий итог эксперимента: время, память по этапам, метрики модели,
        сводная таблица по сырым influence-scores. Полная конфигурация — в config.json.
        _config — опционально даёт блок RUN METADATA в summary (dataset, sample_size_percentage, model_type).
        _scores — для совместимости вызовов (в файл не пишутся).
        removal_results / n_remove_list — опционально: площадь под кривой removal (AUC) по методам.
        """
        summary_file = self.experiment_dir / "experiment_summary.txt"

        total_experiment_time, valid_timings = self._calculate_total_experiment_time()
        wall_clock_time = time.time() - self.start_time

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("EXPERIMENT SUMMARY\n")
            f.write("=" * 80 + "\n\n")

            f.write("REFERENCE\n")
            f.write("-" * 40 + "\n")
            f.write(f"config.json  |  {self.experiment_dir}\n")
            f.write(f"results.pkl\n\n")

            meta_block = ExperimentLogger._format_run_metadata_block(_config)
            if meta_block:
                f.write(meta_block)

            sorted_timings = sorted(valid_timings, key=lambda x: x[1], reverse=True)

            f.write("=" * 80 + "\n")
            f.write("TIMING INFORMATION\n")
            f.write("-" * 40 + "\n")
            f.write(
                f"Total experiment duration (sum of all stages): {total_experiment_time:.2f} seconds\n"
            )
            f.write(f"Wall clock time: {wall_clock_time:.2f} seconds\n")
            if wall_clock_time > 0:
                eff = total_experiment_time / wall_clock_time * 100
                f.write(f"Parallel efficiency: {eff:.1f}%\n\n")
            else:
                f.write("Parallel efficiency: N/A\n\n")

            f.write("Detailed timing breakdown (all stages):\n")
            for method_name, duration in sorted_timings:
                pct = (
                    (duration / total_experiment_time * 100) if total_experiment_time > 0 else 0.0
                )
                f.write(f"  {method_name:<40} {duration:>10.2f}s  ({pct:>5.1f}%)\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("STAGES: duration and memory\n")
            f.write("-" * 40 + "\n")
            f.write(
                "Только этапы с суффиксом _computation. "
                "%total — доля от суммарного времени этих этапов.\n"
                "RAM_MB: RSS (max of start/end snapshot). VRAM_MB: PyTorch CUDA peak allocated per stage; "
                "N/A if no GPU.\n"
                "max_wanted_MB: max(VRAM_MB, failed alloc from CUDA OOM text if any); on OOM peak is often "
                "far below the size PyTorch tried to allocate.\n\n"
            )
            comp_sorted = [
                (mn, dur)
                for mn, dur in sorted_timings
                if str(mn).endswith("_computation")
            ]
            comp_time_sum = sum(d for _, d in comp_sorted)
            mem_rows = []
            for mn, dur in comp_sorted:
                tinfo = self.timings.get(mn, {})
                ram = tinfo.get('ram_peak_mb')
                vram = tinfo.get('gpu_peak_mb')
                max_w = tinfo.get('gpu_memory_max_wanted_mb')
                if max_w is None:
                    max_w = vram
                ram_s = f"{ram:.2f}" if ram is not None else "N/A"
                if vram is None:
                    vram_s = "N/A"
                elif vram <= 0:
                    vram_s = "0.00"
                else:
                    vram_s = f"{vram:.2f}"
                if max_w is None:
                    max_w_s = "N/A"
                elif max_w <= 0:
                    max_w_s = "0.00"
                else:
                    max_w_s = f"{max_w:.2f}"
                pct = (dur / comp_time_sum * 100) if comp_time_sum > 0 else 0.0
                mem_rows.append((mn, dur, pct, ram_s, vram_s, max_w_s))
            name_w = max((len(r[0]) for r in mem_rows), default=28)
            name_w = max(name_w, 18)
            if not mem_rows:
                f.write("  (no *_computation stages in timings)\n")
            else:
                f.write(
                    f"  {'stage':<{name_w}}  {'s':>8}  {'%total':>7}  "
                    f"{'RAM_MB':>10}  {'VRAM_MB':>10}  {'max_wanted_MB':>14}\n"
                )
                f.write(
                    f"  {'-' * name_w}  {'-' * 8}  {'-' * 7}  "
                    f"{'-' * 10}  {'-' * 10}  {'-' * 14}\n"
                )
                for mn, dur, pct, ram_s, vram_s, max_w_s in mem_rows:
                    f.write(
                        f"  {mn:<{name_w}}  {dur:>8.2f}  {pct:>6.1f}%  "
                        f"{ram_s:>10}  {vram_s:>10}  {max_w_s:>14}\n"
                    )

            f.write("\n" + "=" * 80 + "\n")
            f.write("MODEL\n")
            f.write("-" * 40 + "\n")
            if model_metrics:
                for key, value in sorted(model_metrics.items()):
                    if isinstance(value, float):
                        f.write(f"  {key:<36} {value:.6g}\n")
                    else:
                        f.write(f"  {key:<36} {value}\n")
            else:
                f.write("  (no metrics)\n")

            if (
                removal_results is not None
                and n_remove_list
                and isinstance(removal_results, dict)
            ):
                from visualization.plots import (
                    compute_removal_curve_aucs,
                    removal_curve_rank_scores,
                )

                aucs = compute_removal_curve_aucs(removal_results, n_remove_list)
                if aucs:
                    mn = None
                    if model_metrics:
                        mn = model_metrics.get("metric_name")
                    if not mn and isinstance(removal_results.get("orig"), dict):
                        mn = removal_results["orig"].get("metric_name")
                    if not mn:
                        mn = "f1"
                    rank_by_m = removal_curve_rank_scores(aucs, mn, METRIC_METADATA)
                    order = sorted(
                        aucs.keys(),
                        key=lambda m: (
                            float("-inf")
                            if not np.isfinite(rank_by_m.get(m, float("nan")))
                            else rank_by_m.get(m, float("-inf")),
                        ),
                        reverse=True,
                    )
                    places = {}
                    p = 0
                    last_rs = object()
                    for m in order:
                        rs = rank_by_m.get(m, float("nan"))
                        if not np.isfinite(rs):
                            places[m] = "—"
                            continue
                        if rs != last_rs:
                            p += 1
                            last_rs = rs
                        places[m] = p

                    f.write("\n" + "=" * 80 + "\n")
                    f.write("REMOVAL CURVES (AUC-style integral)\n")
                    f.write("-" * 40 + "\n")
                    f.write(
                        "  ∫ y dx: y — метрика на тесте, x — доля удалённых от train, x∈[0,1] "
                        "(как на графике removal / removal_metrics.csv).\n"
                    )
                    f.write(
                        "  rank_score: для сравнения кривых (больше = лучше); "
                        "для метрик «чем меньше тем лучше» rank_score = −AUC.\n"
                    )
                    f.write(f"  metric: {mn}\n\n")
                    name_w = max(len(m) for m in aucs.keys())
                    name_w = max(name_w, 12)
                    f.write(
                        f"  {'method':<{name_w}}  {'AUC':>14}  {'rank_score':>14}  {'rank':>5}\n"
                    )
                    f.write(
                        f"  {'-' * name_w}  {'-' * 14}  {'-' * 14}  {'-' * 5}\n"
                    )
                    for m in order:
                        a = aucs.get(m, float("nan"))
                        rs = rank_by_m.get(m, float("nan"))
                        pl = places.get(m, "—")
                        a_s = f"{a:.6g}" if np.isfinite(a) else "N/A"
                        rs_s = f"{rs:.6g}" if np.isfinite(rs) else "N/A"
                        pl_s = str(pl) if pl != "—" else "—"
                        f.write(
                            f"  {m:<{name_w}}  {a_s:>14}  {rs_s:>14}  {pl_s:>5}\n"
                        )

            f.write("\n" + "=" * 80 + "\n")
            f.write("INFLUENCE SCORES (raw; one row per method)\n")
            f.write("-" * 40 + "\n")
            if influence_stats:
                hdr = (
                    f"  {'method':<34} {'n':>6}  {'min':>14}  {'max':>14}  "
                    f"{'mean':>14}  {'std':>14}  {'pos%':>6}  {'neg%':>6}  {'zero%':>6}\n"
                )
                f.write(hdr)
                f.write(
                    f"  {'-' * 34} {'-' * 6}  {'-' * 14}  {'-' * 14}  "
                    f"{'-' * 14}  {'-' * 14}  {'-' * 6}  {'-' * 6}  {'-' * 6}\n"
                )
                for method_name in sorted(influence_stats.keys()):
                    st = influence_stats[method_name]
                    n = int(st.get('total_count', 0))
                    raw_v = scores_raw.get(method_name)
                    if raw_v is not None and len(raw_v) > 0:
                        v = np.asarray(raw_v).ravel()
                        n_pos = int(np.sum(v > 0))
                        n_neg = int(np.sum(v < 0))
                        n_z = int(np.sum(v == 0))
                        p_pct = 100.0 * n_pos / len(v)
                        neg_pct = 100.0 * n_neg / len(v)
                        z_pct = 100.0 * n_z / len(v)
                    else:
                        p_pct = neg_pct = z_pct = float("nan")
                    f.write(
                        f"  {method_name:<34} {n:>6}  "
                        f"{st['min']:>14.6g}  {st['max']:>14.6g}  "
                        f"{st['mean']:>14.6g}  {st['std']:>14.6g}  "
                    )
                    if raw_v is not None and len(raw_v) > 0:
                        f.write(f"{p_pct:>5.1f}%  {neg_pct:>5.1f}%  {z_pct:>5.1f}%\n")
                    else:
                        f.write(f"{'N/A':>6}  {'N/A':>6}  {'N/A':>6}\n")
            else:
                f.write("  (no influence runs)\n")

            f.write(f"\nGenerated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        self.log_message(f"Summary saved: {summary_file}")

    def log_top_bottom_influence(self, scores_raw, X_train, y_train, n=10):
        """
        Логирует N примеров с наибольшими и наименьшими influence-весами.
        Для каждого метода:
          - CSV со всеми фичами, таргетом, influence score и группой (top/bottom)
          - CSV со сравнением распределений (dataset vs top-N vs bottom-N)
          - Текстовый отчёт в консоль и лог
        """
        if not n or n <= 0:
            return

        X_df = X_train if isinstance(X_train, pd.DataFrame) else pd.DataFrame(X_train)
        y_arr = np.asarray(y_train.values if hasattr(y_train, 'values') else y_train).ravel()
        target_col = y_train.name if hasattr(y_train, 'name') and y_train.name else 'target'
        feature_cols = list(X_df.columns)

        numeric_cols = X_df.select_dtypes(include=[np.number]).columns.tolist()
        # Sparse-колонки (например TF-IDF от IMDB) нужно привести к dense перед agg
        X_numeric = X_df[numeric_cols]
        sparse_cols = [c for c in numeric_cols
                       if hasattr(X_numeric[c], 'dtype') and hasattr(X_numeric[c].dtype, 'subtype')]
        if sparse_cols:
            X_numeric = X_numeric.copy()
            for c in sparse_cols:
                X_numeric[c] = X_numeric[c].sparse.to_dense()
        dataset_stats = X_numeric.agg(['mean', 'std', 'min', 'max', 'median']).T
        dataset_stats.columns = [f'dataset_{c}' for c in dataset_stats.columns]
        dataset_target_stats = {
            'dataset_mean': float(np.mean(y_arr)),
            'dataset_std': float(np.std(y_arr)),
            'dataset_min': float(np.min(y_arr)),
            'dataset_max': float(np.max(y_arr)),
            'dataset_median': float(np.median(y_arr)),
        }

        lines = []
        sep = "=" * 100
        lines.append(sep)
        lines.append(f"TOP-{n} AND BOTTOM-{n} INFLUENCE EXAMPLES (full features + distribution comparison)")
        lines.append(sep)

        for method_name, vals in sorted(scores_raw.items()):
            vals = np.asarray(vals).ravel()
            if vals.size == 0:
                continue

            actual_n = min(n, len(vals))
            sorted_indices = np.argsort(vals)
            bottom_idx = sorted_indices[:actual_n]
            top_idx = sorted_indices[-actual_n:][::-1]

            # --- CSV с полными данными примеров ---
            rows = []
            for rank, idx in enumerate(top_idx, 1):
                row = {'group': 'top', 'rank': rank, 'train_index': int(idx),
                       'influence_score': vals[idx], target_col: y_arr[idx]}
                for col in feature_cols:
                    row[col] = X_df.iloc[idx][col] if hasattr(X_df, 'iloc') else X_df[col].iloc[idx]
                rows.append(row)
            for rank, idx in enumerate(bottom_idx, 1):
                row = {'group': 'bottom', 'rank': rank, 'train_index': int(idx),
                       'influence_score': vals[idx], target_col: y_arr[idx]}
                for col in feature_cols:
                    row[col] = X_df.iloc[idx][col] if hasattr(X_df, 'iloc') else X_df[col].iloc[idx]
                rows.append(row)

            examples_df = pd.DataFrame(rows)
            csv_path = self.experiment_dir / f"top_bottom_{method_name}.csv"
            examples_df.to_csv(csv_path, index=False, float_format='%.6f')

            # --- CSV со сравнением распределений ---
            top_data = X_df.iloc[top_idx] if hasattr(X_df, 'iloc') else X_df[top_idx]
            bottom_data = X_df.iloc[bottom_idx] if hasattr(X_df, 'iloc') else X_df[bottom_idx]

            comparison_rows = []
            for col in numeric_cols:
                row = {'feature': col}
                row['dataset_mean'] = dataset_stats.loc[col, 'dataset_mean']
                row['dataset_std'] = dataset_stats.loc[col, 'dataset_std']
                row['dataset_median'] = dataset_stats.loc[col, 'dataset_median']
                top_vals_col = top_data[col].values.astype(float)
                bottom_vals_col = bottom_data[col].values.astype(float)
                row['top_mean'] = float(np.mean(top_vals_col))
                row['top_std'] = float(np.std(top_vals_col))
                row['top_median'] = float(np.median(top_vals_col))
                row['bottom_mean'] = float(np.mean(bottom_vals_col))
                row['bottom_std'] = float(np.std(bottom_vals_col))
                row['bottom_median'] = float(np.median(bottom_vals_col))
                ds_mean = row['dataset_mean']
                if abs(ds_mean) > 1e-9:
                    row['top_mean_diff_%'] = (row['top_mean'] - ds_mean) / abs(ds_mean) * 100
                    row['bottom_mean_diff_%'] = (row['bottom_mean'] - ds_mean) / abs(ds_mean) * 100
                else:
                    row['top_mean_diff_%'] = 0.0
                    row['bottom_mean_diff_%'] = 0.0
                comparison_rows.append(row)

            target_row = {'feature': f'[TARGET] {target_col}'}
            target_row['dataset_mean'] = dataset_target_stats['dataset_mean']
            target_row['dataset_std'] = dataset_target_stats['dataset_std']
            target_row['dataset_median'] = dataset_target_stats['dataset_median']
            top_y = y_arr[top_idx].astype(float)
            bottom_y = y_arr[bottom_idx].astype(float)
            target_row['top_mean'] = float(np.mean(top_y))
            target_row['top_std'] = float(np.std(top_y))
            target_row['top_median'] = float(np.median(top_y))
            target_row['bottom_mean'] = float(np.mean(bottom_y))
            target_row['bottom_std'] = float(np.std(bottom_y))
            target_row['bottom_median'] = float(np.median(bottom_y))
            ds_mean_t = target_row['dataset_mean']
            if abs(ds_mean_t) > 1e-9:
                target_row['top_mean_diff_%'] = (target_row['top_mean'] - ds_mean_t) / abs(ds_mean_t) * 100
                target_row['bottom_mean_diff_%'] = (target_row['bottom_mean'] - ds_mean_t) / abs(ds_mean_t) * 100
            else:
                target_row['top_mean_diff_%'] = 0.0
                target_row['bottom_mean_diff_%'] = 0.0
            comparison_rows.append(target_row)

            comp_df = pd.DataFrame(comparison_rows)
            comp_csv_path = self.experiment_dir / f"distribution_comparison_{method_name}.csv"
            comp_df.to_csv(comp_csv_path, index=False, float_format='%.6f')

            # --- Текстовый отчёт ---
            lines.append(f"\n{'='*100}")
            lines.append(f"METHOD: {method_name}")
            lines.append(f"{'='*100}")

            lines.append(f"\n  Top-{actual_n} (наибольшие influence-веса):")
            lines.append(f"  {'Rank':<5} {'Idx':<8} {'Score':<20} {target_col:<14} | features (first 5)")
            lines.append(f"  {'-'*5} {'-'*8} {'-'*20} {'-'*14} {'-'*40}")
            show_features = feature_cols[:5]
            for rank, idx in enumerate(top_idx, 1):
                feat_vals = "  ".join(f"{X_df.iloc[idx][c]:.4f}" if isinstance(X_df.iloc[idx][c], (int, float, np.floating, np.integer)) else str(X_df.iloc[idx][c])[:10] for c in show_features)
                lines.append(f"  {rank:<5} {idx:<8} {vals[idx]:<20.6f} {y_arr[idx]:<14} | {feat_vals}")

            lines.append(f"\n  Bottom-{actual_n} (наименьшие influence-веса):")
            lines.append(f"  {'Rank':<5} {'Idx':<8} {'Score':<20} {target_col:<14} | features (first 5)")
            lines.append(f"  {'-'*5} {'-'*8} {'-'*20} {'-'*14} {'-'*40}")
            for rank, idx in enumerate(bottom_idx, 1):
                feat_vals = "  ".join(f"{X_df.iloc[idx][c]:.4f}" if isinstance(X_df.iloc[idx][c], (int, float, np.floating, np.integer)) else str(X_df.iloc[idx][c])[:10] for c in show_features)
                lines.append(f"  {rank:<5} {idx:<8} {vals[idx]:<20.6f} {y_arr[idx]:<14} | {feat_vals}")

            lines.append(f"\n  Сравнение распределений (числовые фичи с наибольшим отклонением от среднего):")
            lines.append(f"  {'Feature':<25} {'Dataset mean':>14} {'Top mean':>14} {'Diff%':>8} {'Bottom mean':>14} {'Diff%':>8}")
            lines.append(f"  {'-'*25} {'-'*14} {'-'*14} {'-'*8} {'-'*14} {'-'*8}")

            sorted_comp = sorted(comparison_rows, key=lambda r: abs(r.get('top_mean_diff_%', 0)) + abs(r.get('bottom_mean_diff_%', 0)), reverse=True)
            for row in sorted_comp[:15]:
                feat = row['feature'][:25]
                lines.append(
                    f"  {feat:<25} {row['dataset_mean']:>14.4f} {row['top_mean']:>14.4f} "
                    f"{row['top_mean_diff_%']:>+7.1f}% {row['bottom_mean']:>14.4f} "
                    f"{row['bottom_mean_diff_%']:>+7.1f}%"
                )

            lines.append(f"\n  Полные данные: {csv_path.name}")
            lines.append(f"  Сравнение распределений: {comp_csv_path.name}")

        lines.append("\n" + sep)
        full_text = "\n".join(lines)

        self.log_message(full_text)

        report_path = self.experiment_dir / "top_bottom_influence.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(full_text + "\n")
        self.log_message(f"Top/bottom influence report saved: {report_path}")

    def get_experiment_dir(self):
        """Возвращает путь к папке эксперимента"""
        return self.experiment_dir


def debug_print(*args, **kwargs):
    from config.settings import DEBUG_MODE
    if DEBUG_MODE:
        print("[DEBUG]", *args, **kwargs)