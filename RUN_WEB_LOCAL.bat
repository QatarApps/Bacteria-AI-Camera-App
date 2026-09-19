@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Setting up virtual environment...
    py -3.13 -m venv .venv
    .\.venv\Scripts\pip.exe install -r requirements.txt flask Pillow
)
echo ==========================================
echo Starting Bacteria AI Web Application
echo Opening http://localhost:5000 in browser...
echo Close this window to stop the server.
echo ==========================================
start http://localhost:5000
.\.venv\Scripts\python.exe web_app.py
pause
