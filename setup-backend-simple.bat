@echo off
cd /d "c:\Users\Admin\OneDrive - uni-pr.edu\Desktop\projekti_ndryshimi\schedule-builder\backend"
python -m venv venv
call venv\Scripts\activate.bat
pip install fastapi uvicorn python-multipart pandas openpyxl xlrd pydantic sqlalchemy alembic python-jose passlib python-dotenv