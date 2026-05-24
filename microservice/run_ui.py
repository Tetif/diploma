#!/usr/bin/env python
"""Запуск только интерфейса Streamlit."""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    microservice_dir = Path(__file__).parent

    print("Streamlit: http://localhost:8501")
    print("Убедитесь, что API доступен на http://localhost:8000")
    print("Остановка: Ctrl+C\n")
    
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
        cwd=str(microservice_dir)
    )
