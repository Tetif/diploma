"""Configuration for microservice"""
import os
from typing import Optional

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"
API_WORKERS = int(os.getenv("API_WORKERS", 1))

# Streamlit Configuration
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))
STREAMLIT_HOST = os.getenv("STREAMLIT_HOST", "0.0.0.0")

# Storage Configuration
STORAGE_BASE_PATH = os.getenv("STORAGE_BASE_PATH", "microservice_storage")
MAX_EXPERIMENTS = int(os.getenv("MAX_EXPERIMENTS", 100))
AUTO_CLEANUP = os.getenv("AUTO_CLEANUP", "false").lower() == "true"

# Experiment Configuration
MAX_CONCURRENT_EXPERIMENTS = int(os.getenv("MAX_CONCURRENT_EXPERIMENTS", 1))
EXPERIMENT_TIMEOUT = int(os.getenv("EXPERIMENT_TIMEOUT", 3600))  # seconds
CLEANUP_INTERVAL = int(os.getenv("CLEANUP_INTERVAL", 3600))  # seconds

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "microservice.log")

# Database Configuration (future use)
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

# Debug Configuration
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Print configuration on startup
if DEBUG:
    print(f"Microservice Configuration:")
    print(f"  API: {API_HOST}:{API_PORT}")
    print(f"  Streamlit: {STREAMLIT_HOST}:{STREAMLIT_PORT}")
    print(f"  Storage: {STORAGE_BASE_PATH}")
    print(f"  Max Concurrent: {MAX_CONCURRENT_EXPERIMENTS}")
