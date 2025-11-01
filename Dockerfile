# --- base ---
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# system deps (psycopg2 / pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev libjpeg62-turbo-dev zlib1g-dev curl netcat-traditional \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install -r requirements.txt

# copy project
COPY . /app

# health endpoint already served by Django on port 8000
EXPOSE 8000

# optional: small entrypoint that waits for DB, runs migrations, collectstatic
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# IMPORTANT: use the correct WSGI module for your project
CMD ["/entrypoint.sh"]
