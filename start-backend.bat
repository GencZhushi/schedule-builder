@echo off
cd /d "c:\Users\Admin\OneDrive - uni-pr.edu\Desktop\projekti_ndryshimi\schedule-builder\backend"
call venv\Scripts\activate.bat
set PYTHONPATH=%cd%
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003