#!/usr/bin/env python
"""Start only FastAPI server"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

if __name__ == "__main__":
    import uvicorn
    
    print("📡 Starting FastAPI server...")
    print("  URL:  http://localhost:8000")
    print("  Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop...\n")
    
    # Use import string for reload mode
    uvicorn.run(
        "microservice.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
