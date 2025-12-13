@echo off
echo Starting AML System Services...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Optional: Activate conda only if needed for other scripts
REM call conda.bat activate aml-env
REM if errorlevel 1 (
REM     echo Failed to activate conda environment
REM     pause
REM     exit /b 1
REM )

REM Start Docker Compose services
echo Starting Docker containers...
docker compose -f infra/docker-compose.yml up -d

if errorlevel 1 (
    echo.
    echo Failed to start Docker services!
    pause
    exit /b 1
)

echo.
echo Services started successfully!
echo.
echo To view logs: docker compose -f infra/docker-compose.yml logs -f
echo To stop: docker compose -f infra/docker-compose.yml down
echo.
pause