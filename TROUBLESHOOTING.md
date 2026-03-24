# 🆘 LUP PROJECT - EMERGENCY TROUBLESHOOTING

**Your immediate error**: PostgreSQL password authentication failed

---

## ✅ QUICK FIX (Right Now)

### FASTEST SOLUTION: Use Docker (2 minutes)

```powershell
# Step 1: Go to project directory
cd C:\Users\Thys\Dev\lup

# Step 2: Start all services with Docker
docker-compose up -d

# Step 3: Wait 30 seconds for database to initialize

# Step 4: Run migrations
docker-compose exec web python manage.py migrate

# Step 5: Create admin user
docker-compose exec web python manage.py createsuperuser

# Step 6: Open browser to http://localhost:8000
```

**Done!** Your site should now be loading.

---

## 🔍 IF THAT DIDN'T WORK

### Check 1: Is Docker Running?

```powershell
# Check if Docker daemon is running
docker --version
docker-compose --version

# If error: Start Docker Desktop from taskbar or Programs
# Wait 30 seconds for it to start
```

### Check 2: Are Containers Running?

```powershell
# List all containers
docker-compose ps

# You should see:
#   lup_db           postgres:15      Up
#   lup_redis        redis:7          Up
#   lup_elasticsearch elasticsearch:7  Up
#   lup_web          lup_web:latest   Up

# If not Up: Check logs
docker-compose logs db
docker-compose logs web
```

### Check 3: Fix Port Conflicts

If you see "port already in use" error:

```powershell
# Windows: Find and kill process using port 8000
netstat -ano | findstr :8000
# Example: PID 1234 is using port 8000
taskkill /PID 1234 /F

# OR just stop and restart
docker-compose down
docker-compose up -d
```

### Check 4: Database Connection Issue

```powershell
# Check database logs
docker-compose logs db

# Try to connect manually
docker-compose exec db psql -U lup_user -d lup_db

# If authentication fails: Restart database
docker-compose restart db
docker-compose exec web python manage.py migrate
```

### Check 5: Clean Rebuild

If containers are corrupted:

```powershell
# WARNING: This deletes all data!
docker-compose down -v

# Rebuild from scratch
docker-compose up -d

# Run setup
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 📋 TROUBLESHOOTING FLOWCHART

```
Site not loading?
│
├─ Is Docker running?
│  ├─ NO → Start Docker Desktop
│  └─ YES ↓
│
├─ Are containers running?
│  ├─ NO → docker-compose up -d
│  └─ YES ↓
│
├─ Check service status
│  ├─ docker-compose ps
│  └─ All showing "Up"? ↓
│
├─ Try accessing site
│  ├─ http://localhost:8000
│  ├─ YES → Success! ✅
│  └─ NO ↓
│
├─ Check web service logs
│  ├─ docker-compose logs web
│  └─ See error? ↓
│
├─ Check database logs
│  ├─ docker-compose logs db
│  └─ See error? ↓
│
└─ Last resort:
   docker-compose down -v
   docker-compose up -d
   (Rebuilds everything)
```

---

## 🔧 COMMON ERRORS & FIXES

### "Connection refused"
```powershell
# Database hasn't started yet. Wait 10 seconds
docker-compose logs db
# If "Database system was shut down"
docker-compose restart db
docker-compose exec web python manage.py migrate
```

### "Port 8000 already in use"
```powershell
# Kill the process using the port
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or map to different port in docker-compose.yml
# Change: "8000:8000" to "8001:8000"
docker-compose up -d
# Then access: http://localhost:8001
```

### "Module 'django' not found"
```powershell
# Web container failed to build
docker-compose build --no-cache web
docker-compose up -d
```

### "Database 'lup_db' does not exist"
```powershell
# Create database and run migrations
docker-compose exec db psql -U postgres
# Then type: CREATE DATABASE lup_db;
# Then: \q

# OR just run migrations
docker-compose exec web python manage.py migrate
```

### "Could not connect to server"
```powershell
# Network issue. Check docker network
docker network ls
docker-compose exec web ping db

# If ping fails, recreate network
docker-compose down
docker-compose up -d
```

---

## 📞 GETTING HELP

If you're still stuck:

1. **Collect diagnostic information:**
   ```powershell
   docker-compose ps > ps.txt
   docker-compose logs > logs.txt
   docker system df > system.txt
   docker images > images.txt
   ```

2. **Check the documentation:**
   - [QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md)
   - [OPERATIONS_GUIDE.md](OPERATIONS_GUIDE.md)
   - [README.md](README.md)

3. **Search the error message:**
   - Copy full error message
   - Search GitHub issues
   - Check Docker documentation

4. **Provide context when asking for help:**
   - Operating system: Windows
   - Docker version: `docker --version`
   - Full error message (from logs)
   - What you were trying to do
   - Steps you've already taken

---

## ⚡ COMMANDS CHEAT SHEET

```powershell
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# View all containers
docker-compose ps

# View logs
docker-compose logs -f          # All services
docker-compose logs -f web      # Specific service

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Enter container
docker-compose exec web bash

# Database commands
docker-compose exec db psql -U lup_user -d lup_db

# Restart specific service
docker-compose restart web
docker-compose restart db

# View resource usage
docker stats

# Clean everything
docker-compose down -v          # With data deletion
docker system prune -a          # Remove unused images

# Check if ports are in use
netstat -ano | findstr :8000
netstat -ano | findstr :5432
netstat -ano | findstr :6379
```

---

## ✨ NEXT STEPS

Once your site is running:

1. **Access the site**: http://localhost:8000
2. **Admin panel**: http://localhost:8000/admin
   - Login with superuser credentials you created
3. **Read the guides**:
   - [QUICK_START_WINDOWS.md](QUICK_START_WINDOWS.md) - More detail
   - [OPERATIONS_GUIDE.md](OPERATIONS_GUIDE.md) - Day-to-day operations
   - [PRODUCTION_DEPLOYMENT.md](PRODUCTION_DEPLOYMENT.md) - Going live

4. **Understand the architecture**: Check [README.md](README.md)

---

**You've got this!** 💪 The most common issue is just Docker not being started. If it still doesn't work, provide the output of `docker-compose logs web` and `docker-compose logs db` and we can dig deeper.
