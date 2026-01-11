FROM python:3.12-slim

# Define build-time variable for the port
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$${API_PORT}/health || exit 1

# Start FastAPI using the dynamic port
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${API_PORT}"]