#!/bin/sh

echo "Waiting for database..."

# Ждём БД
python manage.py migrate --noinput

echo "Collecting static..."
python manage.py collectstatic --noinput

echo "Starting server..."
exec gunicorn SSW_Backend_Django.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
