@echo off
echo ================================================
echo   STRCrosshair  --  Build to .exe
echo ================================================

echo [1/3] Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

echo [2/3] Building executable (onedir)...
pyinstaller ^
  --onedir ^
  --windowed ^
  --name STRCrosshair ^
  --add-data "crosshair_engine.py;." ^
  --add-data "settings_window.py;." ^
  --add-data "config_manager.py;." ^
  --add-data "tray_manager.py;." ^
  --add-data "crosshair_overlay.py;." ^
  --hidden-import pygame ^
  --hidden-import pystray ^
  --hidden-import PIL ^
  --hidden-import keyboard ^
  main.py

echo [3/3] Done!
echo.
echo Output: dist\STRCrosshair\STRCrosshair.exe
echo.
pause
