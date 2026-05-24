#!/usr/bin/env python
"""Запуск API и Streamlit вместе."""
import subprocess
import sys
import time
from pathlib import Path

def main():
    """Поднимает uvicorn (cwd — корень репозитория) и Streamlit (cwd — папка microservice)."""
    project_root = Path(__file__).resolve().parent.parent
    microservice_pkg = Path(__file__).resolve().parent

    print("Микросервис influence: запуск API и UI")
    print("=" * 60)

    print("\nFastAPI: http://localhost:8000")
    # Не перенаправлять stdout/stderr в PIPE: буфер забивается и дочерние процессы зависают,
    # плюс ошибки (занятый порт, импорты) не видны в консоли.
    api_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "microservice.api:app",
            "--reload",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
        cwd=str(project_root),
    )

    time.sleep(3)

    print("Streamlit: http://localhost:8501")
    streamlit_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.port",
            "8501",
            "--server.headless",
            "true",
        ],
        cwd=str(microservice_pkg),
    )
    
    print("\n" + "=" * 60)
    print("Сервисы запущены. API: http://localhost:8000  UI: http://localhost:8501")
    print("Документация API: http://localhost:8000/docs")
    print("=" * 60)
    print("\nОстановка обоих: Ctrl+C\n")
    
    def _stop_other(other: subprocess.Popen, name: str) -> None:
        if other.poll() is None:
            print(f"Останавливаем {name}…")
            other.terminate()
            try:
                other.wait(timeout=5)
            except subprocess.TimeoutExpired:
                other.kill()

    try:
        while True:
            time.sleep(1)
            if api_process.poll() is not None:
                print("Процесс API завершился.")
                _stop_other(streamlit_process, "Streamlit")
                break
            if streamlit_process.poll() is not None:
                print("Процесс Streamlit завершился.")
                _stop_other(api_process, "API")
                break
    except KeyboardInterrupt:
        print("\n\nОстановка серверов…")
        api_process.terminate()
        streamlit_process.terminate()
        
        try:
            api_process.wait(timeout=5)
            streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()
            streamlit_process.kill()
        
        print("Сервисы остановлены.")
        sys.exit(0)


if __name__ == "__main__":
    main()
