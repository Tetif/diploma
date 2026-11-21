#!/usr/bin/env python
"""Start the API and Streamlit together."""
import subprocess
import sys
import time
from pathlib import Path

def main():
    """Start uvicorn (cwd = repository root) and Streamlit (cwd = microservice folder)."""
    project_root = Path(__file__).resolve().parent.parent
    microservice_pkg = Path(__file__).resolve().parent

    print("Influence microservice: starting the API and UI")
    print("=" * 60)

    print("\nFastAPI: http://localhost:8000")
    # Do not redirect stdout/stderr to PIPE: the buffer fills up and the child processes hang,
    # and errors (busy port, imports) are not visible in the console.
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
    print("Services started. API: http://localhost:8000  UI: http://localhost:8501")
    print("API docs: http://localhost:8000/docs")
    print("=" * 60)
    print("\nStop both: Ctrl+C\n")
    
    def _stop_other(other: subprocess.Popen, name: str) -> None:
        if other.poll() is None:
            print(f"Stopping {name}...")
            other.terminate()
            try:
                other.wait(timeout=5)
            except subprocess.TimeoutExpired:
                other.kill()

    try:
        while True:
            time.sleep(1)
            if api_process.poll() is not None:
                print("The API process exited.")
                _stop_other(streamlit_process, "Streamlit")
                break
            if streamlit_process.poll() is not None:
                print("The Streamlit process exited.")
                _stop_other(api_process, "API")
                break
    except KeyboardInterrupt:
        print("\n\nStopping the servers...")
        api_process.terminate()
        streamlit_process.terminate()
        
        try:
            api_process.wait(timeout=5)
            streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()
            streamlit_process.kill()
        
        print("Services stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
