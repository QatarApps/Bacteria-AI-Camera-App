@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Setting up virtual environment with Python 3.13...
    py -3.13 -m venv .venv
    .\.venv\Scripts\pip.exe install -r requirements.txt flask Pillow
)
echo ==========================================
echo Starting Bacteria AI Desktop Camera App
echo Press 'Q' inside the camera window to quit
echo ==========================================
.\.venv\Scripts\python.exe camera_app.py
pause
