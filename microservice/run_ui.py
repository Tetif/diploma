#!/usr/bin/env python
"""Start only Streamlit interface"""
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    microservice_dir = Path(__file__).parent
    
    print("🎨 Starting Streamlit interface...")
    print("  URL: http://localhost:8501")
    print("\nMake sure FastAPI is running on localhost:8000!")
    print("Press Ctrl+C to stop...\n")
    
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8501"],
        cwd=str(microservice_dir)
    )
