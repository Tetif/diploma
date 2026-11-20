# archive/

Код и материалы, которые **не используются текущим пайплайном** (`run_study.py`, `run_overnight.ps1`, `plot_results.py`, `paired_stats.py`), но могут пригодиться для текста диплома или как история. Удалять не стали, перенесли через `git mv`.

| Путь | Что это |
|---|---|
| `scripts/check_overfitting.py` | диагностика переобучения моделей старого пайплайна (`main.py`); запускать из корня: `python archive/scripts/check_overfitting.py --list` |
| `scripts/plot_removal_from_weights.py` | кривые удаления по сохранённым influence-весам из `experiment_logs/` (старый пайплайн) |
| `visualization/graph_plot_from_pkl.py`, `visualization/timing_analysis.py` | графики и тайминги по pkl-логам старого пайплайна |
| `synthetic_data/` | синтетические эксперименты (pyDVL 0.10 API, в study не участвуют) |
| `notebooks/eda_{cifar10,electric,imdb,mnist,zillow}.ipynb` | EDA датасетов, которые не вошли в итоговое исследование (оно идёт на wine, housing, adult, covertype) |

Удалены (`git rm`, восстановить можно из истории git): `scripts/legacy/*` (одноразовые скрипты до аудита), `scripts/check_distillation.py`, `scripts/check_mlp_epochs.py`, `QUICK_START_RU.md` (дубль `microservice/README.md`).
