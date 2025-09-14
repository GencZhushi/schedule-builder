@echo off
echo Starting Lecture Schedule Preparation System...
echo.

echo Starting backend server...
start "Backend" /min cmd /c ".\start-backend.bat & pause"

echo Starting frontend server...
start "Frontend" /min cmd /c ".\start-frontend.bat & pause"

echo.
echo Both servers are starting in the background.
echo Frontend will be available at http://localhost:3002
echo Backend API will be available at http://localhost:8000
echo API Documentation at http://localhost:8000/docs
echo.
echo Press any key to close this window (servers will continue running)...
pause >nul