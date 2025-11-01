# =========================
# Base image (Option A)
# =========================
FROM python:3.10-slim

# Env de base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# (Optionnel) variables runtime par défaut
# Vous pouvez override via docker run -e ou docker compose
ENV DJANGO_SETTINGS_MODULE=core.settings \
    PORT=8000

# Dépendances système (Pillow, Postgres/psycopg2)
# - build-essential + libpq-dev pour compiler les wheels si nécessaire
# - libjpeg + zlib pour Pillow
# - curl & netcat-traditional utiles en debug/healthchecks (facultatif)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    curl \
    netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

# Répertoire d’app
WORKDIR /app

# D’abord requirements pour profiter du cache
COPY requirements.txt /app/requirements.txt

# Mettre pip/setuptools/wheel à jour puis installer deps
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install -r requirements.txt

# Copier le code
COPY . /app

# (Optionnel) créer un utilisateur non-root
# RUN adduser --disabled-password --gecos '' appuser \
#  && chown -R appuser:appuser /app
# USER appuser

# Expose le port (informative)
EXPOSE 8000

# (Optionnel) collectstatic au build si vos settings le permettent
# RUN python manage.py collectstatic --noinput

# CMD de prod : Gunicorn
# Adaptez core.wsgi si votre module diffère (ex: config.wsgi)
CMD ["gunicorn", "my_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]


