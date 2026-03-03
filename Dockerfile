# -------------------------
# Base image
# -------------------------
FROM python:3.11-slim

# -------------------------
# System dependencies
# -------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# -------------------------
# Environment
# -------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -------------------------
# Workdir
# -------------------------
WORKDIR /app

# -------------------------
# Install dependencies
# -------------------------
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -------------------------
# Copy project
# -------------------------
COPY . .

# -------------------------
# Create non-root user
# -------------------------
RUN useradd -m appuser
USER appuser

# -------------------------
# Expose port
# -------------------------
EXPOSE 8000

# -------------------------
# Start server
# -------------------------
CMD gunicorn SSW_Backend_Django.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120
