# 🎯 LUP PROJECT - OPERATIONS & MAINTENANCE GUIDE

This guide covers how to operate, maintain, and scale your LUP application once it's running.

---

## 📊 MONITORING & HEALTH CHECKS

### Health Check Endpoint
```bash
curl http://localhost:8000/health/
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "timestamp": "2026-01-28T00:00:00Z"
}
```

### Service Status Checks (Docker)
```bash
# Check all services
docker-compose ps

# Check service logs
docker-compose logs web        # Django app
docker-compose logs db         # PostgreSQL
docker-compose logs redis      # Redis cache
docker-compose logs celery     # Background tasks
```

### System Resource Monitoring
```bash
# View container resource usage
docker stats

# View disk usage
docker system df

# Clean up unused resources
docker system prune -a
```

---

## 🗄️ DATABASE MANAGEMENT

### Backups

**Daily Automated Backup (Recommended)**

Add to cron/task scheduler:
```bash
#!/bin/bash
BACKUP_DIR="/backups/lup"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup
docker-compose exec -T db pg_dump -U lup_user lup_db | \
  gzip > "$BACKUP_DIR/lup_db_$TIMESTAMP.sql.gz"

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

**Manual Backup**
```bash
docker-compose exec db pg_dump -U lup_user lup_db > backup.sql
```

**Restore from Backup**
```bash
docker-compose exec -T db psql -U lup_user lup_db < backup.sql
```

### Running Migrations

```bash
# Create new migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Show migration history
docker-compose exec web python manage.py showmigrations

# Reverse migration
docker-compose exec web python manage.py migrate app_name 0001
```

### Database Maintenance

```bash
# Create database backups
docker-compose exec db vacuumdb -U lup_user lup_db

# Analyze tables for query optimization
docker-compose exec db analyzedb -U lup_user lup_db

# Reindex (if data is corrupted)
docker-compose exec db reindexdb -U lup_user lup_db
```

---

## 🔍 SEARCH ENGINE (ELASTICSEARCH)

### Rebuild Search Index

```bash
# Rebuild all indexes
docker-compose exec web python manage.py rebuild_index --noinput

# Clear and rebuild specific app
docker-compose exec web python manage.py clear_index --noinput
docker-compose exec web python manage.py rebuild_index --noinput
```

### Check Elasticsearch Health

```bash
# Check cluster status
curl http://localhost:9200/_cluster/health

# View indices
curl http://localhost:9200/_cat/indices

# Check specific index
curl http://localhost:9200/lup/_stats
```

### Troubleshooting Search

```bash
# If search not working, rebuild index:
docker-compose restart elasticsearch
docker-compose exec web python manage.py rebuild_index --noinput

# Check logs
docker-compose logs elasticsearch
```

---

## 💼 BACKGROUND TASKS (CELERY)

### Monitor Tasks

```bash
# Check Celery worker logs
docker-compose logs celery

# Check beat scheduler logs
docker-compose logs celery-beat

# View pending tasks (in Redis)
redis-cli KEYS "celery*"
```

### Restart Task Workers

```bash
# Restart Celery worker
docker-compose restart celery

# Restart beat scheduler
docker-compose restart celery-beat

# Restart both
docker-compose restart celery celery-beat
```

### Clear Task Queue

```bash
# Purge all pending tasks
docker-compose exec redis redis-cli FLUSHDB

# Warning: This will delete all cached data!
```

---

## ⚙️ APPLICATION UPDATES

### Deploy New Code

```bash
# 1. Stop services
docker-compose down

# 2. Pull latest code
git pull origin main

# 3. Rebuild containers
docker-compose build --no-cache

# 4. Start services
docker-compose up -d

# 5. Run migrations
docker-compose exec web python manage.py migrate

# 6. Rebuild search index
docker-compose exec web python manage.py rebuild_index --noinput

# 7. Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# 8. Verify health
curl http://localhost:8000/health/
```

### Zero-Downtime Updates (Advanced)

```bash
# Using multiple containers:
docker-compose up -d --scale web=2

# Update code on running container
docker-compose exec web git pull

# Restart services one at a time
docker-compose restart web
```

---

## 🔐 SECURITY MAINTENANCE

### Update Dependencies

```bash
# Update Python packages
docker-compose exec web pip list --outdated

# Update specific package
docker-compose exec web pip install --upgrade django

# Rebuild image with new dependencies
docker-compose build --no-cache web
```

### SSL/TLS Certificate Management

For production with Let's Encrypt:

```bash
# Install certbot in container or host
certbot certonly --standalone -d yourdomain.com

# Configure auto-renewal (cron job)
0 0 * * * certbot renew --quiet
```

### Update Security Settings

```bash
# For production, update .env:
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Restart containers
docker-compose restart web
```

---

## 📈 SCALING & PERFORMANCE

### Increase Web Workers

```bash
# For high traffic, increase Gunicorn workers in docker-compose.yml
# Modify: CMD ["gunicorn", "lup.wsgi:application", "--workers", "8"]
# Recommended: 2-4 workers per CPU core
```

### Optimize Database

```bash
# Add connection pooling in docker-compose.yml
# Use pgBouncer: https://www.pgbouncer.org/

# Connection pool settings in settings.py:
DATABASES = {
    'default': {
        'CONN_MAX_AGE': 600,  # Connection persistence
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}
```

### Enable Caching

```bash
# Redis caching is already configured
# Clear cache if needed
docker-compose exec redis redis-cli FLUSHALL

# Monitor cache
docker-compose exec redis redis-cli INFO stats
```

---

## 🚨 DISASTER RECOVERY

### Complete Service Reset

```bash
# WARNING: This deletes all data!
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Restore from Backup

```bash
# 1. Stop services
docker-compose down

# 2. Restore database
docker-compose up -d db
docker-compose exec -T db psql -U lup_user lup_db < backup.sql

# 3. Start all services
docker-compose up -d

# 4. Verify
docker-compose exec web python manage.py dbshell
```

### Emergency Logs Collection

```bash
# Collect all logs for debugging
docker-compose logs > all_logs.txt
docker system df > system_info.txt
docker ps -a > container_info.txt

# Package for support
zip diagnostic_package.zip all_logs.txt system_info.txt container_info.txt
```

---

## 📅 MAINTENANCE SCHEDULE

### Daily
- [ ] Monitor health check endpoint
- [ ] Check error logs: `docker-compose logs web`
- [ ] Verify database connectivity

### Weekly
- [ ] Backup database
- [ ] Review disk usage: `docker system df`
- [ ] Check security updates: `docker-compose exec web pip list --outdated`

### Monthly
- [ ] Full system health check
- [ ] Update base images: `docker-compose pull`
- [ ] Performance review and optimization
- [ ] Update Python dependencies
- [ ] Test backup restore process

### Quarterly
- [ ] Security audit (review logs for attacks)
- [ ] Capacity planning (prepare for growth)
- [ ] Disaster recovery drill
- [ ] Performance optimization review

---

## 📞 TROUBLESHOOTING

### Site Won't Load

```bash
# 1. Check if containers are running
docker-compose ps

# 2. Check web service logs
docker-compose logs web -f

# 3. Check database connection
docker-compose exec web python manage.py dbshell

# 4. Check if port is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# 5. Restart services
docker-compose restart web db
```

### Database Connection Failed

```bash
# 1. Check database service
docker-compose logs db

# 2. Verify credentials in .env
grep DB_ .env

# 3. Test connection
docker-compose exec db psql -U lup_user -d lup_db

# 4. Restart database
docker-compose restart db
docker-compose exec web python manage.py migrate
```

### Search Not Working

```bash
# 1. Check Elasticsearch
curl http://localhost:9200/_health

# 2. Rebuild index
docker-compose exec web python manage.py rebuild_index --noinput

# 3. Check logs
docker-compose logs elasticsearch
```

### Memory Issues / Crashes

```bash
# 1. Check resource usage
docker stats

# 2. Increase Docker memory limits (Docker Desktop)
# Settings > Resources > Memory: Increase to 4-8GB

# 3. Clean up old data
docker system prune -a

# 4. Rebuild containers
docker-compose down -v
docker-compose up -d
```

---

## 🔗 USEFUL COMMANDS REFERENCE

```bash
# General
docker-compose ps                    # List running containers
docker-compose logs -f               # View logs (all services)
docker-compose logs -f web           # View specific service logs
docker-compose exec web bash         # Enter container shell

# Database
docker-compose exec db psql -U postgres  # Connect to PostgreSQL
docker-compose exec db pg_dump -U lup_user lup_db  # Backup

# Django
docker-compose exec web python manage.py shell  # Django shell
docker-compose exec web python manage.py dbshell  # Database shell
docker-compose exec web python manage.py migrate  # Migrations

# Redis
docker-compose exec redis redis-cli INFO  # Check Redis status
docker-compose exec redis redis-cli FLUSHDB  # Clear cache

# Cleanup
docker system prune                  # Remove unused data
docker-compose down -v               # Stop and remove volumes
docker image rm image_name           # Remove specific image
```

---

## 📚 EXTERNAL RESOURCES

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Elasticsearch Documentation](https://www.elastic.co/guide/index.html)
- [Celery Documentation](https://docs.celeryproject.io/)

---

**Last Updated**: January 28, 2026  
**Maintained By**: LUP Development Team  
**Version**: 1.0.0
