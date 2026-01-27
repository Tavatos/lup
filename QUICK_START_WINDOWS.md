# 🚀 LUP PROJECT - GETTING STARTED GUIDE

## ⚠️ CURRENT ISSUE

**Error**: `psycopg2.OperationalError: password authentication failed for user "postgres"`

**Root Cause**: PostgreSQL database isn't running or isn't properly configured on your system.

---

## ✅ SOLUTION OPTIONS

### Option 1: Use Docker for Everything (RECOMMENDED ⭐)

This is the **easiest and most reliable** approach for development.

**Step 1: Ensure Docker is installed**
```powershell
docker --version
docker-compose --version
```

**Step 2: Start all services with Docker**
```powershell
cd C:\Users\Thys\Dev\lup
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Elasticsearch (port 9200)

**Step 3: Verify services are running**
```powershell
docker-compose ps
# Should show all containers "Up"
```

**Step 4: Run migrations and create user**
```powershell
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser (admin account)
docker-compose exec web python manage.py createsuperuser

# Build search index (Elasticsearch)
docker-compose exec web python manage.py rebuild_index --noinput
```

**Step 5: Access the application**
```
Web App: http://localhost:8000
Admin Panel: http://localhost:8000/admin
```

---

### Option 2: Local PostgreSQL Installation

If you want to run Django locally in VSCode (requires more setup):

**Step 1: Install PostgreSQL on Windows**

Download from: https://www.postgresql.org/download/windows/

During installation:
- Set password for `postgres` user to: `postgres` (or update in `.env`)
- Enable PostGIS extension during setup

**Step 2: Verify PostgreSQL is running**
```powershell
# Check if service is running
Get-Service | Select-Object Name, Status | Where-Object {$_.Name -like '*Post*'}

# Connect to test
psql -U postgres
# Type password when prompted
# Type \q to exit
```

**Step 3: Create database**
```sql
CREATE DATABASE lup_db;
CREATE USER lup_user WITH PASSWORD 'lup_password';
ALTER ROLE lup_user SET client_encoding TO 'utf8';
ALTER ROLE lup_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE lup_user SET default_transaction_deferrable TO on;
ALTER ROLE lup_user SET default_transaction_read_committed TO on;
GRANT ALL PRIVILEGES ON DATABASE lup_db TO lup_user;
```

**Step 4: Update `.env` file**
```env
DB_USER=lup_user
DB_PASSWORD=lup_password
DB_NAME=lup_db
```

**Step 5: Install Redis locally** (optional for dev)
```powershell
# Download from: https://github.com/microsoftarchive/redis/releases
# Or use Windows Subsystem for Linux (WSL)
```

---

## 🐳 RECOMMENDED: Docker Setup (Step by Step)

### Why Docker?
- ✅ Works identically everywhere (local, Docker, production)
- ✅ No need to install PostgreSQL locally
- ✅ Easy cleanup (just `docker-compose down`)
- ✅ Perfect for team collaboration
- ✅ Mirrors production environment

### Complete Docker Workflow

**1. Start Services**
```powershell
cd C:\Users\Thys\Dev\lup
docker-compose up -d
```

**2. Verify Running**
```powershell
docker-compose ps
```

Expected output:
```
CONTAINER ID   IMAGE                    STATUS
xxx            postgres:15              Up 2 minutes
xxx            redis:7-alpine           Up 2 minutes
xxx            elasticsearch:7.17.0     Up 2 minutes
xxx            lup_web                  Up 2 minutes
```

**3. Run Setup Commands**
```powershell
# Create database tables
docker-compose exec web python manage.py migrate

# Create admin user (follow prompts)
docker-compose exec web python manage.py createsuperuser

# Build search index
docker-compose exec web python manage.py rebuild_index --noinput

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

**4. Access Application**
```
Open browser: http://localhost:8000
```

**5. View Logs (for troubleshooting)**
```powershell
# See all service logs
docker-compose logs -f

# See specific service
docker-compose logs -f web
docker-compose logs -f db

# Exit logs: Ctrl+C
```

**6. Stop Everything**
```powershell
docker-compose down
```

**7. Start Fresh (if needed)**
```powershell
# Stop and remove everything (including data!)
docker-compose down -v

# Rebuild and start
docker-compose up -d
```

---

## 📝 Troubleshooting

### Port Already in Use
```powershell
# Find and kill process on port 8000
Get-Process | Where-Object {$_.ProcessName -match "python|gunicorn"} | Stop-Process

# Or in Docker:
docker-compose down
```

### Database Won't Connect
```powershell
# Check database service
docker-compose logs db

# Restart database
docker-compose restart db
docker-compose exec web python manage.py migrate
```

### Search Not Working
```powershell
# Check Elasticsearch
docker-compose logs elasticsearch

# Rebuild search index
docker-compose exec web python manage.py rebuild_index --noinput
```

### Memory Issues
```powershell
# Increase Docker memory in Docker Desktop settings
# Settings > Resources > Memory (increase to 4-8GB)
```

---

## 🔄 Development Workflow

### Normal Development Days
```powershell
# Morning: Start services
docker-compose up -d

# Work on code...
# Services auto-reload for most changes

# Evening: Stop services
docker-compose down
```

### Making Code Changes
Most changes reload automatically:
- ✅ Template changes - instant reload
- ✅ View changes - instant reload
- ✅ Static files - rebuild with `collectstatic`
- ✅ Database models - run migrations

### Running Django Commands
```powershell
# Any Django command:
docker-compose exec web python manage.py <command>

# Examples:
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py test
```

---

## 🚀 Next Steps

1. **Choose approach**: Option 1 (Docker) recommended
2. **Start services**: `docker-compose up -d`
3. **Run setup**: Follow setup commands above
4. **Access app**: Open http://localhost:8000
5. **Read** [DEPLOYMENT.md](./DEPLOYMENT.md) for production info
