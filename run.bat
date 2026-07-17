@echo off
REM ===== MU Auto Bai - chay app =====
REM Nen chay bang quyen Administrator de hotkey toan cuc & gui phim vao game hoat dong.
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo [!] Chua cai Python. Tai tai https://www.python.org/downloads/ (nho tick "Add to PATH").
  pause
  exit /b 1
)

if not exist ".installed" (
  echo [i] Cai dat thu vien lan dau...
  python -m pip install -r requirements.txt
  if errorlevel 1 (
    echo [!] Cai thu vien loi. Xem thong bao ben tren.
    pause
    exit /b 1
  )
  echo done> .installed
)

python muauto.py
pause
