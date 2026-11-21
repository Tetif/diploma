#!/usr/bin/env python
"""Start only the Streamlit UI."""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    microservice_dir = Path(__file__).parent

    print("Streamlit: http://localhost:8501")
    print("Make sure the API is available at http://localhost:8000")
    print("Stop: Ctrl+C\n")
    
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
        cwd=str(microservice_dir)
    )
