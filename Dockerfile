# syntax=docker/dockerfile:1

FROM python:3.11-slim

# Install any system deps you need (e.g. for google-cloud libraries)
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend
COPY backend ./backend
COPY frontend_simple ./frontend_simple

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "backend.server:app", "--host", "0.0.0.0", "--port", "8000"]
