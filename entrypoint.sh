#!/bin/sh

set -e

echo "Starting entrypoint..."

echo "Waiting for database..."

python << END
import os
import time
import sys

import django
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SSW_Backend_Django.settings")

django.setup()

connection = connections["default"]

max_attempts = 30
delay = 2

for attempt in range(1, max_attempts + 1):
    try:
        connection.cursor()
        print("Database is available.")
        sys.exit(0)
    except OperationalError:
        print(f"Database is unavailable. Attempt {attempt}/{max_attempts}...")
        time.sleep(delay)

print("Database is still unavailable after waiting.")
sys.exit(1)
END

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if required..."

python << END
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SSW_Backend_Django.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email or "",
            password=password
        )
        print(f"Superuser '{username}' created.")
    else:
        print(f"Superuser '{username}' already exists.")
else:
    print("Superuser credentials are not set. Skipping superuser creation.")
END

if [ -f "initial_data.json" ]; then
    echo "Loading initial_data.json..."
    python manage.py loaddata initial_data.json
else
    echo "No initial_data.json found. Skipping fixture loading."
fi

if [ "$RUN_SEED_DATA" = "true" ]; then
    echo "Running seed_data command..."
    python manage.py seed_data
else
    echo "RUN_SEED_DATA is not true. Skipping seed_data command."
fi

echo "Starting Gunicorn..."

exec gunicorn SSW_Backend_Django.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
