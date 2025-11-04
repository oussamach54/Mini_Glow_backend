# backend/Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Only runtime libs; no build-essential needed when using psycopg2-binary
RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq5 curl wget \
 && rm -rf /var/lib/apt/lists/*

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Expose your Django app on port 8000 via Gunicorn
# IMPORTANT: change the module below if your WSGI path differs
CMD ["gunicorn", "my_project.wsgi:application", "--bind", "0.0.0.0:8000"]
