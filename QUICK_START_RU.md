# Быстрый старт микросервиса

## Установка

```bash
pip install -r microservice/requirements_microservice.txt
```

## Запуск

**API и UI вместе:**

```bash
python microservice/run_services.py
```

**Только API:**

```bash
python microservice/run_api.py
```

**Только UI** (API уже на порту 8000):

```bash
python microservice/run_ui.py
```

По умолчанию: API http://localhost:8000, документация `/docs`, UI http://localhost:8501.

Переменные окружения (опционально): см. [.env.example](.env.example).

## Docker

```bash
docker compose up --build
```

Подробнее: [microservice/README.md](microservice/README.md).
