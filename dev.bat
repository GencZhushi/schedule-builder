@echo off
cls
echo ==========================================
echo Lecture Schedule Preparation System
echo ==========================================
echo.
echo Starting development environment...
echo.

echo Make sure you have:
echo 1. Python 3.8 or higher installed
echo 2. Node.js installed
echo.
echo Starting servers...
echo.

start "Backend Server" cmd /c ".\start-backend.bat & pause"
start "Frontend Server" cmd /c ".\start-frontend.bat & pause"

echo.
echo Servers are now starting in separate windows:
echo - Frontend: http://localhost:3002
echo - Backend API: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo.
echo Close individual windows to stop servers
echo.
echo Press any key to exit this window...
pause >nul