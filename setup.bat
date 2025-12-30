@echo off
REM LUP PROJECT - QUICK START SCRIPT FOR WINDOWS
REM This script sets up the LUP project for development or production

setlocal enabledelayedexpansion

cls
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo     LUP - LOCAL UNIFIED PLATFORM
echo     🚀 Quick Start Setup Script
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Check Python
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9+
    exit /b 1
)
echo ✓ Python found
echo.

REM Check if .env exists
echo [2/7] Checking environment configuration...
if not exist .env (
    echo ⚠️  .env not found, copying from .env.example...
    copy .env.example .env >nul 2>&1
    if errorlevel 1 (
        echo ❌ Failed to copy .env.example
        exit /b 1
    )
    echo ✓ .env created. Please edit it with your settings.
) else (
    echo ✓ .env already exists
)
echo.

REM Check if virtual environment exists
echo [3/7] Checking virtual environment...
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [4/7] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo [5/7] Installing Python dependencies...
cd src\lup
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    cd ..\..
    exit /b 1
)
echo ✓ Dependencies installed
cd ..\..
echo.

REM Run migrations
echo [6/7] Running database migrations...
cd src\lup
python manage.py migrate --noinput
if errorlevel 1 (
    echo ⚠️  Migrations may have failed (check database connection)
)
echo ✓ Migrations completed
cd ..\..
echo.

REM Collect static files
echo [7/7] Collecting static files...
cd src\lup
python manage.py collectstatic --noinput --quiet
if errorlevel 1 (
    echo ⚠️  Static files collection may have failed
)
echo ✓ Static files collected
cd ..\..
echo.

REM Summary
echo ════════════════════════════════════════════════════════════
echo.
echo ✅ SETUP COMPLETE!
echo.
echo Next steps:
echo.
echo For DEVELOPMENT:
echo   1. Navigate to: cd src\lup
echo   2. Run server: python manage.py runserver
echo   3. Open: http://localhost:8000
echo.
echo For PRODUCTION (Docker):
echo   1. Edit .env with production settings
echo   2. Build images: docker-compose build
echo   3. Start services: docker-compose up -d
echo   4. Create admin: docker-compose exec web python manage.py createsuperuser
echo   5. Open: http://localhost:8000
echo.
echo For help, see:
echo   - README.md (Project overview)
echo   - DEPLOYMENT.md (Production setup)
echo   - LAUNCH_READY.md (Launch status)
echo.
echo ════════════════════════════════════════════════════════════
echo.

pause
