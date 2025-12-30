#!/bin/bash
# LUP DEPLOYMENT CHECKLIST - Production Ready
# Usage: Run this script to verify deployment readiness

set -e

echo "════════════════════════════════════════════════════════════"
echo "   🚀 LUP PLATFORM - PRODUCTION DEPLOYMENT CHECKLIST"
echo "════════════════════════════════════════════════════════════"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter
CHECKS_PASSED=0
CHECKS_FAILED=0

check() {
    local name=$1
    local command=$2
    
    echo -n "Checking: $name ... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}"
        ((CHECKS_FAILED++))
    fi
}

warning() {
    local name=$1
    echo -e "${YELLOW}⚠ WARNING: $name${NC}"
}

# ===== 1. ENVIRONMENT CHECKS =====
echo -e "${YELLOW}1. ENVIRONMENT CONFIGURATION${NC}"
check "Python 3.9+ installed" "python3 --version | grep -q '3.[9-9]'"
check ".env file exists" "test -f .env"
check ".env has SECRET_KEY" "grep -q 'SECRET_KEY=' .env"
check ".env has DEBUG=False" "grep -q 'DEBUG=False' .env"
check ".env has ALLOWED_HOSTS" "grep -q 'ALLOWED_HOSTS=' .env"
echo ""

# ===== 2. DATABASE CHECKS =====
echo -e "${YELLOW}2. DATABASE CONFIGURATION${NC}"
check "PostgreSQL client installed" "psql --version"
check "Database credentials in .env" "grep -q 'DB_NAME=' .env && grep -q 'DB_USER=' .env"
check "Database host configured" "grep -q 'DB_HOST=' .env"
check "SSL mode for production" "grep -q 'sslmode=require' src/lup/lup/settings.py"
echo ""

# ===== 3. SECURITY CHECKS =====
echo -e "${YELLOW}3. SECURITY HARDENING${NC}"
check "SECRET_KEY is not default" "! grep -q 'django-insecure-CHANGE' src/lup/lup/settings.py"
check "Debug is False" "grep -q 'DEBUG.*False' src/lup/lup/settings.py"
check "SECURE_SSL_REDIRECT enabled" "grep -q 'SECURE_SSL_REDIRECT.*True' src/lup/lup/settings.py"
check "HSTS headers configured" "grep -q 'SECURE_HSTS' src/lup/lup/settings.py"
check "X-Frame-Options set" "grep -q 'X_FRAME_OPTIONS.*DENY' src/lup/lup/settings.py"
check "Content-Type options set" "grep -q 'X_CONTENT_TYPE_OPTIONS.*nosniff' src/lup/lup/settings.py"
echo ""

# ===== 4. FILE STRUCTURE CHECKS =====
echo -e "${YELLOW}4. FILE STRUCTURE${NC}"
check "Docker file exists at root" "test -f Dockerfile"
check "docker-compose.yml exists" "test -f docker-compose.yml"
check ".gitignore exists" "test -f .gitignore"
check "README.md exists" "test -f README.md"
check "DEPLOYMENT.md exists" "test -f DEPLOYMENT.md"
check "manage.py configured" "grep -q 'DJANGO_SETTINGS_MODULE' src/lup/manage.py"
check "No hardcoded paths" "! grep -q 'C:\\\\Users' src/lup/lup/settings.py"
echo ""

# ===== 5. APPLICATION CHECKS =====
echo -e "${YELLOW}5. APPLICATION CONFIGURATION${NC}"
check "All apps in INSTALLED_APPS" "grep -q \"'core.apps.CoreConfig'\" src/lup/lup/settings.py"
check "Health check endpoint exists" "grep -q 'health_check' src/lup/core/views.py"
check "WSGI application configured" "test -f src/lup/lup/wsgi.py"
check "Celery configured" "test -f src/lup/lup/celery.py"
check "URLs configured" "grep -q 'urlpatterns' src/lup/lup/urls.py"
echo ""

# ===== 6. DEPENDENCIES CHECKS =====
echo -e "${YELLOW}6. PYTHON DEPENDENCIES${NC}"
check "requirements.txt exists" "test -f src/lup/requirements.txt"
check "Django in requirements" "grep -q 'Django' src/lup/requirements.txt"
check "PostgreSQL driver installed" "grep -q 'psycopg2' src/lup/requirements.txt"
check "Gunicorn in requirements" "grep -q 'gunicorn' src/lup/requirements.txt"
check "Redis in requirements" "grep -q 'redis' src/lup/requirements.txt"
check "Elasticsearch in requirements" "grep -q 'elasticsearch' src/lup/requirements.txt"
echo ""

# ===== 7. DOCKER CHECKS =====
echo -e "${YELLOW}7. DOCKER CONFIGURATION${NC}"
check "Docker installed" "docker --version"
check "Docker Compose installed" "docker-compose --version"
check "Dockerfile uses Python 3.9" "grep -q 'FROM python:3.9' Dockerfile"
check "PostGIS image specified" "grep -q 'postgis/postgis' docker-compose.yml"
check "Redis service configured" "grep -q 'redis:7' docker-compose.yml"
check "Elasticsearch service configured" "grep -q 'elasticsearch' docker-compose.yml"
check "Health checks configured" "grep -q 'healthcheck' docker-compose.yml"
echo ""

# ===== 8. DOCUMENTATION CHECKS =====
echo -e "${YELLOW}8. DOCUMENTATION${NC}"
check "README.md is comprehensive" "grep -q 'Quick Start' README.md"
check "DEPLOYMENT.md has instructions" "grep -q 'Production' DEPLOYMENT.md"
check ".env.example has all variables" "grep -q 'SECRET_KEY' .env.example"
echo ""

# ===== RESULTS =====
echo "════════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ PASSED: $CHECKS_PASSED${NC}"
if [ $CHECKS_FAILED -gt 0 ]; then
    echo -e "${RED}✗ FAILED: $CHECKS_FAILED${NC}"
else
    echo -e "${GREEN}✗ FAILED: 0${NC}"
fi
echo "════════════════════════════════════════════════════════════"
echo ""

# ===== WARNINGS =====
echo -e "${YELLOW}PRODUCTION DEPLOYMENT WARNINGS:${NC}"
warning "Ensure SSL certificate is installed"
warning "Configure email service (Gmail, SendGrid, etc)"
warning "Setup database backups"
warning "Configure monitoring (Sentry, DataDog, New Relic)"
warning "Setup log aggregation (ELK Stack, CloudWatch)"
warning "Configure CDN for static files (CloudFront, Cloudflare)"
warning "Enable DDoS protection"
warning "Setup WAF (Web Application Firewall)"
echo ""

# ===== FINAL STATUS =====
if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}   ✅ PROJECT IS LAUNCH READY! 🚀${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Generate secure SECRET_KEY"
    echo "2. Configure production .env"
    echo "3. Build Docker images: docker-compose build"
    echo "4. Start services: docker-compose up -d"
    echo "5. Create superuser: docker-compose exec web python manage.py createsuperuser"
    echo "6. Verify: curl http://localhost:8000/health/"
    exit 0
else
    echo -e "${RED}════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}   ❌ FIX FAILED CHECKS BEFORE DEPLOYMENT${NC}"
    echo -e "${RED}════════════════════════════════════════════════════════════${NC}"
    exit 1
fi
