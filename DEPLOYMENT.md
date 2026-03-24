# LUP Platform - Deployment Guide

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- PostgreSQL 13+ with PostGIS
- Redis 6+
- Elasticsearch 7.17
- Git

### Setup Steps

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd lup

# 2. Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Copy environment file
cp .env.example .env

# 4. Install dependencies
pip install -r src/lup/requirements.txt

# 5. Run migrations
cd src/lup
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Build search index
python manage.py rebuild_index --noinput

# 8. Run development server
python manage.py runserver
```

Access at: http://localhost:8000

---

## 🐳 Docker Deployment (Production Ready)

### Prerequisites
- Docker & Docker Compose
- `.env` file configured with production values

### Setup Steps

```bash
# 1. Copy and configure environment
cp .env.example .env

# Edit .env with production values:
# - Generate SECRET_KEY
# - Set DEBUG=False
# - Set ENVIRONMENT=production
# - Configure ALLOWED_HOSTS
# - Set database credentials
# - Configure email settings

# 2. Build images
docker-compose build

# 3. Run services
docker-compose up -d

# 4. Check service health
docker-compose ps
docker-compose logs -f web

# 5. Create superuser in container
docker-compose exec web python manage.py createsuperuser

# 6. Verify health check
curl http://localhost:8000/health/
```

---

## 🔧 Environment Configuration

### .env File (Critical Variables)

```bash
# Security (CHANGE THESE!)
DEBUG=False
SECRET_KEY=<generate-with-django-secret-key-generator>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=lup_db
DB_USER=lup_user
DB_PASSWORD=<strong-password>
DB_HOST=localhost  # 'db' in Docker
DB_PORT=5432

# Cache & Queue
REDIS_URL=redis://localhost:6379/0

# Search
ELASTICSEARCH_URL=http://localhost:9200/
SKIP_ELASTICSEARCH_SIGNALS=False

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=<app-password>

# Monitoring
SENTRY_DSN=<your-sentry-dsn>

# SSL/TLS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 🚀 Production Checklist

### Before Deployment

- [ ] Generate secure SECRET_KEY (minimum 50 chars)
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS (no wildcards)
- [ ] Enable SECURE_SSL_REDIRECT=True
- [ ] Set up SSL certificate (Let's Encrypt)
- [ ] Configure database backups
- [ ] Setup monitoring (Sentry, DataDog, etc.)
- [ ] Configure email service (Gmail, SendGrid, etc.)
- [ ] Test health check endpoint
- [ ] Review security headers

### Security Hardening

```bash
# Run Django security checks
python manage.py check --deploy

# Output should show:
# System check identified no issues (with 'deploy' option enabled).
```

### Database Optimization

```bash
# Create indexes
python manage.py migrate

# Analyze performance
python manage.py shell
>>> from django.db import connection
>>> connection.queries  # View SQL queries
```

---

## 📊 Monitoring & Maintenance

### Service Health

```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs -f web
docker-compose logs -f celery
docker-compose logs -f db

# Monitor resources
docker stats

# Health check
curl http://localhost:8000/health/
```

### Database Maintenance

```bash
# Backup
docker-compose exec db pg_dump -U lup_user lup_db > backup.sql

# Restore
docker-compose exec -T db psql -U lup_user lup_db < backup.sql

# Vacuum (optimize)
docker-compose exec db psql -U lup_user lup_db -c "VACUUM FULL;"
```

### Cache Management

```bash
# Clear all cache
docker-compose exec redis redis-cli FLUSHALL

# Monitor
docker-compose exec redis redis-cli INFO
```

---

## 🚨 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL connection
docker-compose exec db pg_isready

# View logs
docker-compose logs db

# Check environment variables
docker-compose config
```

### Elasticsearch Issues

```bash
# Check health
curl http://localhost:9200/_cluster/health

# View indices
curl http://localhost:9200/_cat/indices

# Rebuild index
docker-compose exec web python manage.py rebuild_index --noinput
```

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# In Docker
docker-compose exec web python manage.py collectstatic --noinput
```

### Permission Issues

```bash
# Fix directory permissions
sudo chown -R appuser:appuser media/ logs/ staticfiles/

# In Docker (usually not needed)
docker-compose exec web chown -R appuser:appuser /app
```

---

## 🔄 Backup & Restore

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"

mkdir -p $BACKUP_DIR

# Database backup
docker-compose exec -T db pg_dump -U lup_user lup_db | \
  gzip > "$BACKUP_DIR/db_backup_$DATE.sql.gz"

# Media files backup
tar -czf "$BACKUP_DIR/media_backup_$DATE.tar.gz" ./media

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Restore from Backup

```bash
# Decompress backup
gunzip db_backup_YYYYMMDD_HHMMSS.sql.gz

# Restore
docker-compose exec -T db psql -U lup_user lup_db < db_backup_YYYYMMDD_HHMMSS.sql

# Restore media
tar -xzf media_backup_YYYYMMDD_HHMMSS.tar.gz
```

---

## 📈 Scaling & Performance

### Celery Configuration

```bash
# Increase worker concurrency
celery -A lup worker --concurrency=8

# Monitor tasks
python manage.py shell
>>> from celery.app.control import Inspect
>>> i = Inspect()
>>> i.active()
```

### Database Optimization

```sql
-- Create indexes for frequently queried fields
CREATE INDEX idx_forum_topic_created ON forum_topic(created_at);
CREATE INDEX idx_reporting_report_user ON reporting_report(user_id);
```

### Redis Optimization

```bash
# Monitor memory
redis-cli INFO memory

# Clear old sessions
redis-cli FLUSHDB

# Optimize
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

---

## 🔐 SSL/TLS Setup

### Using Let's Encrypt with Nginx

```nginx
# /etc/nginx/sites-available/lup

server {
    listen 80;
    server_name yourdomain.com;
    
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # Enable HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Proxy to Docker
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 📞 Support & Resources

- **Django Docs**: https://docs.djangoproject.com/
- **Docker Docs**: https://docs.docker.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Elasticsearch Docs**: https://www.elastic.co/guide/
- **Celery Docs**: https://docs.celeryproject.io/

---

**Last Updated**: 2024
**Version**: 1.0.0
**Status**: Production Ready ✅
