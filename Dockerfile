# ---- Base image ----
FROM python:3.11-slim

# ---- System deps ----
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- Workdir ----
WORKDIR /app

# ---- Install deps ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project ----
COPY . .

# ---- Env ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Collect static ----
RUN python manage.py collectstatic --noinput

# ---- Expose ----
EXPOSE 8000

# ---- Start ----
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
