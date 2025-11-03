@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python -c "from app.app import app; app.run(debug=True, host='127.0.0.1', port=5000)"
pause

