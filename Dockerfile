FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY microservice/requirements_microservice.txt .
COPY requirements.txt ./requirements_base.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements_microservice.txt

# Copy application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV API_BASE_URL="http://localhost:8000"

# Expose ports
EXPOSE 8000 8501

# Run services
CMD ["python", "microservice/run_services.py"]
