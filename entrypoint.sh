#!/bin/bash
set -e

echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."
until python -c "
import os
import socket
import sys

host = os.environ.get('DB_HOST', 'db')
port = int(os.environ.get('DB_PORT', '5432'))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
try:
    sock.connect((host, port))
except OSError:
    sys.exit(1)
finally:
    sock.close()
"; do
  sleep 1
done

echo "PostgreSQL is ready."

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py init_superuser

exec gunicorn maxway.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --timeout 300 \
  --log-level info
