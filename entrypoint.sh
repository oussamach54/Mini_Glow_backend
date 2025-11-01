#!/usr/bin/env bash
set -e

# Allow overriding settings via Coolify env
: "${DJANGO_SETTINGS_MODULE:=my_project.settings}"
export DJANGO_SETTINGS_MODULE

# Optional: wait for Postgres if DATABASE_URL is postgres://
if [[ "${DATABASE_URL:-}" == postgres* ]]; then
  echo "Waiting for Postgres..."
  for i in {1..30}; do
    nc -z 127.0.0.1 5432 && break || sleep 1
  done || echo "Postgres wait timed out (continuing anyway)"
fi

# Safe admin tasks — ignore failures in first boot
python - <<'PY'
import os, sys, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE","my_project.settings"))
try:
    from django.core.management import execute_from_command_line
    execute_from_command_line(["manage.py","migrate","--noinput"])
    execute_from_command_line(["manage.py","collectstatic","--noinput"])
except Exception as e:
    print("Startup admin tasks warning:", e, file=sys.stderr)
PY

# Launch Gunicorn with the CORRECT module
exec gunicorn my_project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 60
