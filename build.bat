@echo off
echo ================================================
echo   STRCrosshair  --  Build to .exe
echo ================================================

echo [1/3] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo [2/3] Building executable...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name STRCrosshair ^
  --add-data "*.py;." ^
  main.py

echo [3/3] Done!
echo.
echo Output: dist\STRCrosshair.exe
echo.
pause
