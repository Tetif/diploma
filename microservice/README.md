# Микросервис influence (FastAPI + Streamlit)

Сервис для запуска экспериментов с функциями влияния (influence), настройкой через API или веб-интерфейс и сохранением артефактов в `microservice_storage/`.

## Установка

```bash
pip install -r requirements_microservice.txt
```

Переменные окружения (необязательно): `API_BASE_URL`, `API_PORT`, `STREAMLIT_PORT`.

## Запуск


| Режим                             | Команда                               |
| --------------------------------- | ------------------------------------- |
| API и UI                          | `python microservice/run_services.py` |
| Только API                        | `python microservice/run_api.py`      |
| Только UI (API уже на порту 8000) | `python microservice/run_ui.py`       |


По умолчанию: API `http://localhost:8000`, документация OpenAPI `http://localhost:8000/docs`, интерфейс `http://localhost:8501`.

## Структура каталога

```
microservice/
├── api/           # FastAPI, модели запросов
├── services/      # логика экспериментов
├── storage/       # сохранение результатов
├── app.py         # Streamlit UI
├── run_services.py / run_api.py / run_ui.py
└── README.md
```

## API (кратко)

- `GET /health`, `GET /info/datasets`, `GET /info/models`, `GET /info/influence-methods`
- `POST /experiments/start` — новый эксперимент
- `GET /experiments/{id}/status`, `GET /experiments/{id}/results`
- `GET /experiments/{id}/influence-weights/{method}`, `GET /experiments/{id}/graph-data`
- `GET /experiments` — список экспериментов
- `DELETE /experiments/{id}` — удаление
- `POST /datasets/upload` — загрузка своих данных (заглушка)

Подробности и примеры тел запросов — в OpenAPI по адресу `/docs`.

## Интерфейс Streamlit

Разделы: рабочая область (новый эксперимент и removal), анализ результатов, настройки.

## Хранение результатов

Каталог эксперимента: `microservice_storage/experiments/{experiment_id}/` — `config.json`, `results.json`, `influence_weights.pkl`, `scores_raw.pkl`, `metadata.json`.


