@echo off
setlocal

set PORT=5006
set PYTHONPATH=%~dp0libs;%PYTHONPATH%

echo Starting DeepSeek Multilingual Studio (COPY VERSION)...

rem Detect Python command (prefer py on Windows)
where py >nul 2>nul
if %ERRORLEVEL%==0 (
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo Using Python: %PYTHON_CMD%

echo Checking Python environment...
%PYTHON_CMD% --version

echo Checking Flask...
%PYTHON_CMD% -c "import flask; print(f'Flask {flask.__version__} OK')" 2>nul || (
  echo WARNING: Flask not found. Basic dependencies should be installed.
  echo For full functionality, run: pip install -r requirements.txt
)

echo Starting backend server on port %PORT%...
echo A new window named "DeepSeek Server" will open for the backend.
echo Please keep that server window OPEN while using the website.
echo If the server fails to start, error messages will appear in that window.

start "DeepSeek Server" cmd /k "cd /d %~dp0 && set PORT=%PORT% && set PYTHONPATH=%PYTHONPATH% && %PYTHON_CMD% app.py"

echo Waiting for server to start (5 seconds)...
ping 127.0.0.1 -n 6 >nul

echo Opening website in your default browser...
start "" http://127.0.0.1:%PORT%/

echo If the browser does not open, copy this URL manually:
echo   http://127.0.0.1:%PORT%/

pause
