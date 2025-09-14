@echo off
echo Setting up and starting Lecture Schedule Preparation System...
echo.

echo Installing/Updating Python dependencies...
cd schedule-builder\backend
pip install -r requirements.txt
cd ..\..

echo Installing/Updating Node dependencies...
npm install
cd schedule-builder\frontend
npm install
cd ..\..

echo.
echo Starting both servers...
echo.
start "Backend Server" /min cmd /c ".\start-backend.bat & pause"
start "Frontend Server" /min cmd /c ".\start-frontend.bat & pause"

echo Both servers are starting in separate windows.
echo Frontend will be available at http://localhost:3002
echo Backend API will be available at http://localhost:8000
echo API Documentation at http://localhost:8000/docs
echo.
echo Close the individual server windows to stop the servers.
echo Press any key to continue...
pause >nul