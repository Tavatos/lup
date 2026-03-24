FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including PostGIS and GDAL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GDAL_CONFIG=/usr/bin/gdal-config \
    LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Copy requirements and install Python packages
COPY src/lup/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/lup /app

# Create necessary directories
RUN mkdir -p /app/logs /app/media /app/staticfiles && \
    chmod -R 755 /app/logs /app/media /app/staticfiles

# Collect static files (non-critical, won't fail if it errors)
RUN python manage.py collectstatic --noinput --clear || true

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run application
CMD ["gunicorn", "lup.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]
