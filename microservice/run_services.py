#!/usr/bin/env python
"""Script to start both API and Streamlit servers"""
import subprocess
import sys
import os
import time
from pathlib import Path

def main():
    """Start both API and Streamlit servers"""
    
    # Get the microservice directory
    microservice_dir = Path(__file__).parent.parent
    
    print("🚀 Starting Influence Functions Microservice...")
    print("=" * 60)
    
    # Start FastAPI server
    print("\n📡 Starting FastAPI server on http://localhost:8000...")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "microservice.api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(microservice_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait a bit for API to start
    time.sleep(3)
    
    # Start Streamlit
    print("🎨 Starting Streamlit interface on http://localhost:8501...")
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "microservice/app.py", "--server.port", "8501"],
        cwd=str(microservice_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("\n" + "=" * 60)
    print("✓ Both services started!")
    print("  📡 API:       http://localhost:8000")
    print("  🎨 Streamlit: http://localhost:8501")
    print("  📚 API Docs:  http://localhost:8000/docs")
    print("=" * 60)
    print("\nPress Ctrl+C to stop both servers...\n")
    
    try:
        # Keep both processes running
        while True:
            time.sleep(1)
            if api_process.poll() is not None:
                print("❌ API process terminated!")
                break
            if streamlit_process.poll() is not None:
                print("❌ Streamlit process terminated!")
                break
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        api_process.terminate()
        streamlit_process.terminate()
        
        try:
            api_process.wait(timeout=5)
            streamlit_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            api_process.kill()
            streamlit_process.kill()
        
        print("✓ All services stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()
