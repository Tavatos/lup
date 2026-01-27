# 🚀 LUP PROJECT - PRODUCTION DEPLOYMENT GUIDE

Complete step-by-step guide for deploying LUP to production on cloud platforms.

---

## 📋 DEPLOYMENT CHECKLIST

### Pre-Deployment (Weeks Before)

- [ ] Configure production database backups
- [ ] Set up SSL/TLS certificates (Let's Encrypt)
- [ ] Configure domain DNS records
- [ ] Set up monitoring and alerting (DataDog, New Relic, Sentry)
- [ ] Plan capacity (estimate users, traffic patterns)
- [ ] Perform security audit
- [ ] Load testing with production data
- [ ] Disaster recovery plan documented
- [ ] Update all dependencies to latest secure versions
- [ ] Prepare deployment runbook

### Pre-Deployment (Day Before)

- [ ] Database backup created and tested
- [ ] All code committed and pushed to main branch
- [ ] All tests passing: `docker-compose exec web python manage.py test`
- [ ] Production environment variables in secure vault
- [ ] Monitoring dashboards set up
- [ ] Log aggregation configured (ELK, Splunk, etc.)
- [ ] DNS propagation verified
- [ ] SSL certificate valid and installed
- [ ] Rollback plan ready

### Deployment Day

- [ ] Team notified of deployment window
- [ ] Maintenance page prepared
- [ ] Database migrations tested in staging
- [ ] Feature flags configured for gradual rollout
- [ ] Deployment approved by lead

### Post-Deployment (First 24 Hours)

- [ ] Monitor error rates and logs closely
- [ ] Verify all major features working
- [ ] Check database performance
- [ ] Monitor resource usage
- [ ] Collect user feedback
- [ ] Have rollback plan ready

---

## 🌐 CLOUD PLATFORM OPTIONS

### Option 1: AWS (Amazon Web Services)

**Infrastructure:**
- ECS (Elastic Container Service) for Docker containers
- RDS (Relational Database Service) for PostgreSQL
- ElastiCache for Redis
- S3 for static files and media
- CloudFront for CDN
- Route 53 for DNS
- CloudWatch for monitoring

**Setup Steps:**

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name lup-web

# 2. Build and push image
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag lup:latest <account>.dkr.ecr.us-east-1.amazonaws.com/lup-web:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/lup-web:latest

# 3. Create RDS PostgreSQL database
# Via AWS Console or CLI:
aws rds create-db-instance \
  --db-instance-identifier lup-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.3 \
  --master-username lup_user \
  --allocated-storage 20
```

**Estimated Costs (Monthly):**
- ECS: $10-20 (small instances)
- RDS: $15-30 (db.t3.micro)
- ElastiCache: $10-15 (cache.t3.micro)
- S3: $1-5 (storage)
- Data transfer: $5-10
- **Total: $40-80/month for small deployment**

---

### Option 2: DigitalOcean (Recommended for Small Teams ⭐)

**Simpler, cheaper, developer-friendly**

**Infrastructure:**
- App Platform (managed Docker deployment)
- Managed PostgreSQL database
- Redis database
- Spaces (S3-compatible object storage)
- Load balancers
- Managed Kubernetes (optional)

**Setup Steps:**

```bash
# 1. Create app.yaml for App Platform
cat > app.yaml << 'EOF'
name: lup-platform
services:
  - name: web
    github:
      repo: your-username/lup
      branch: main
    build_command: docker-compose build
    run_command: gunicorn lup.wsgi:application --bind 0.0.0.0:8080
    envs:
      - key: DEBUG
        value: "False"
      - key: DATABASE_URL
        scope: RUN_AND_BUILD_TIME
        value: ${db.connection_string}
databases:
  - name: lup_postgres
    engine: PG
    version: "15"
    production: true
  - name: lup_redis
    engine: REDIS
    version: "7"
    production: true
EOF

# 2. Deploy
doctl apps create --spec app.yaml
```

**Estimated Costs (Monthly):**
- App Platform: $5-12 (starter to professional)
- PostgreSQL: $12-50 (1GB to 4GB)
- Redis: $5-15
- Spaces: $1-5 (object storage)
- **Total: $25-80/month**

---

### Option 3: Heroku

**Most beginner-friendly, higher cost**

```bash
# 1. Install Heroku CLI
# 2. Login
heroku login

# 3. Create app
heroku create lup-app

# 4. Add PostgreSQL
heroku addons:create heroku-postgresql:standard-0

# 5. Add Redis
heroku addons:create heroku-redis:premium-0

# 6. Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-very-secret-key
heroku config:set ALLOWED_HOSTS=lup-app.herokuapp.com

# 7. Deploy
git push heroku main

# 8. Run migrations
heroku run python manage.py migrate

# 9. Create superuser
heroku run python manage.py createsuperuser
```

**Estimated Costs (Monthly):**
- Dyno: $50+ (production tier)
- PostgreSQL: $50+ (standard tier)
- Redis: $30+ (premium tier)
- **Total: $130+/month minimum**

---

## 🏗️ RECOMMENDED: DigitalOcean Setup

### Step 1: Prepare Repository

Add production Dockerfile and docker-compose.yml:

```bash
# Ensure your repo has:
- Dockerfile (optimized)
- docker-compose.yml
- .env.example
- requirements.txt
- All code committed to main branch
```

### Step 2: Create DigitalOcean Account

1. Sign up at https://www.digitalocean.com
2. Link GitHub account
3. Create personal access token

### Step 3: Create Managed Databases

**PostgreSQL:**
```bash
1. Console > Databases > Create Database
2. Select PostgreSQL 15
3. Select Premium ($12/month minimum)
4. Region: Close to users
5. Create
```

**Redis:**
```bash
1. Console > Databases > Create Database
2. Select Redis
3. Select Premium Tier ($5/month)
4. Create
```

### Step 4: Create App Platform Deployment

```bash
1. Console > Apps > Create App
2. Select "GitHub" source
3. Authorize GitHub
4. Select your lup repository
5. Select "main" branch
6. Configure resources:
   - Web service: Basic ($5/month)
   - Buildpack: Docker
7. Set environment variables (from .env but with production values):
   DEBUG=False
   SECRET_KEY=<generate-new>
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   DATABASE_URL=<auto-filled from PostgreSQL>
   REDIS_URL=<auto-filled from Redis>
   ELASTICSEARCH_URL=<managed or external>
8. Create
```

### Step 5: Configure Domain

```bash
1. Console > Networking > Domains
2. Add domain
3. Update domain DNS:
   - Add A record pointing to App Platform IP
   - Or use DigitalOcean's nameservers
```

### Step 6: Enable HTTPS/SSL

```bash
1. In App settings
2. Enable "Auto TLS"
3. Certificate auto-renewed yearly
```

### Step 7: Run Setup Commands

```bash
# Via App Console or SSH:
doctl apps exec <app-id> -- python manage.py migrate
doctl apps exec <app-id> -- python manage.py createsuperuser
doctl apps exec <app-id> -- python manage.py collectstatic --noinput
doctl apps exec <app-id> -- python manage.py rebuild_index --noinput
```

---

## 🔒 PRODUCTION CONFIGURATION

### Update Settings for Production

```python
# In settings.py or separate settings_production.py:

DEBUG = False
ENVIRONMENT = 'production'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Allowed hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Static/Media files
STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

# Database SSL
DATABASES = {
    'default': {
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '<sendgrid-api-key>'

# Error tracking
SENTRY_DSN = '<your-sentry-dsn>'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'sentry': {
            'class': 'sentry_sdk.integrations.logging.SentryHandler',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console', 'sentry'],
        'level': 'INFO',
    },
}
```

### Environment Variables for Production

```bash
# Core
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=<generate-50-char-random-string>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
DB_SSLMODE=require

# Redis/Cache
REDIS_URL=redis://:password@host:6379/0
CELERY_BROKER_URL=redis://:password@host:6379/1

# Search
ELASTICSEARCH_URL=https://elasticsearch-host:9200
ELASTICSEARCH_API_KEY=<api-key>

# Email (SendGrid recommended for production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=<sendgrid-api-key>

# Monitoring
SENTRY_DSN=<your-sentry-dsn>
DATADOG_API_KEY=<datadog-key>

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

---

## 📊 MONITORING & LOGGING

### Set Up Error Tracking (Sentry)

```bash
# 1. Sign up at https://sentry.io
# 2. Create Django project
# 3. Get your DSN
# 4. Add to settings.py:

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="<your-sentry-dsn>",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False,
    environment="production"
)

# 5. All errors now logged to Sentry dashboard
```

### Set Up Performance Monitoring (DataDog)

```bash
# 1. Sign up at https://www.datadoghq.com
# 2. Install DataDog agent
# 3. Configure Django integration
# 4. Set up dashboards and alerts
```

### Configure Log Aggregation

```bash
# ELK Stack (Elasticsearch, Logstash, Kibana)
# OR
# Splunk
# OR
# Cloudflare
# OR
# Datadog

# All methods: Ship logs to centralized service
# Query and analyze logs from single dashboard
```

---

## 🔄 CONTINUOUS DEPLOYMENT

### GitHub Actions Setup

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run tests
        run: docker-compose exec web python manage.py test
      
      - name: Deploy to DigitalOcean
        run: doctl apps update <app-id> --source-repo-branch main
      
      - name: Run migrations
        run: doctl apps exec <app-id> -- python manage.py migrate
      
      - name: Notify Slack
        if: success()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d 'text=LUP deployed successfully!'
```

---

## 🚨 SCALING STRATEGY

### Stage 1: Initial Launch (0-1000 users)
- Single web container
- Shared database
- Basic caching
- Cost: ~$30-50/month

### Stage 2: Growth (1000-10000 users)
- Multiple web containers (load balanced)
- Separate read replicas for database
- Dedicated Redis instance
- CDN for static files
- Cost: ~$100-200/month

### Stage 3: Scale (10000+ users)
- Kubernetes cluster
- Database sharding
- Multi-region deployment
- Advanced caching strategies
- Cost: $500+/month

---

## 🔐 SECURITY HARDENING

### SSL/TLS Setup

```bash
# Auto-renewed Let's Encrypt (via DigitalOcean, Heroku, etc.)
# Or manual:
certbot certonly --standalone -d yourdomain.com
# Renew: certbot renew --quiet
```

### Firewall Rules

```bash
# Allow only necessary traffic:
- Port 80: HTTP (redirect to HTTPS)
- Port 443: HTTPS (application)
- Port 5432: PostgreSQL (VPC only)
- Port 6379: Redis (VPC only)
```

### Database Security

```bash
# Use strong passwords
# Enable SSL connections
# Regular backups to secure location
# Restrict database access to app servers only
```

### Application Security

```bash
# Run Django security check
docker-compose exec web python manage.py check --deploy

# Output should show no errors

# Regular dependency updates
pip install --upgrade -r requirements.txt
```

---

## 📈 DISASTER RECOVERY

### Backup Strategy

**Daily automated backups:**
```bash
# Database backup every 6 hours
# 30-day retention
# Geographic replication (different region)
# Weekly manual verification test
```

**Recovery Time Objectives:**
- RTO (Recovery Time): 1 hour
- RPO (Recovery Point): 6 hours

**Restore Procedure:**
```bash
# 1. Restore database from backup
# 2. Restore application code (from git)
# 3. Run migrations
# 4. Rebuild search indices
# 5. Verify functionality
```

---

## 📞 SUPPORT & RESOURCES

**DigitalOcean:**
- Docs: https://docs.digitalocean.com/
- Community: https://www.digitalocean.com/community/

**Django:**
- Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/

**Docker:**
- Reference: https://docs.docker.com/

---

**Last Updated**: January 28, 2026  
**Author**: LUP Development Team  
**Version**: 1.0.0
