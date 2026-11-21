#!/usr/bin/env python
"""Start only FastAPI (uvicorn)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

if __name__ == "__main__":
    import uvicorn

    print("FastAPI: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    print("Stop: Ctrl+C\n")
    uvicorn.run(
        "microservice.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
