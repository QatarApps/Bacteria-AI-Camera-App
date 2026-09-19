@echo off
echo ==========================================
echo Starting Bacteria AI Classifier in Docker
echo ==========================================

docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop on your PC and try again.
    pause
    exit /b 1
)

echo Building and starting Docker container...
docker compose up -d --build

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ==========================================
    echo Container started successfully!
    echo Opening browser at http://localhost:5000
    echo ==========================================
    start http://localhost:5000
) else (
    echo [ERROR] Failed to start Docker container.
)

pause
