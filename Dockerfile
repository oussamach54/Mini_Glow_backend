FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    DJANGO_SETTINGS_MODULE=my_project.settings \
    PORT=8000

# Pillow deps + Postgres headers + curl (Coolify) + netcat for DB wait
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev libjpeg62-turbo-dev zlib1g-dev \
    curl netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install -r requirements.txt

# Project files
COPY . /app

# Entrypoint: fix Windows CRLF + UTF-8 BOM & make executable
COPY docker/entrypoint.sh /entrypoint.sh
RUN sed -i '1s/^\xEF\xBB\xBF//' /entrypoint.sh && sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

EXPOSE 8000

# Run through sh to avoid shebang issues
ENTRYPOINT ["sh", "/entrypoint.sh"]
