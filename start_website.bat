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

echo Checking dependencies...
%PYTHON_CMD% -c "import pkg_resources, sys; reqs = open('requirements.txt').read().splitlines(); missing = [r.split('==')[0] for r in reqs if r and not r.startswith('#') and not pkg_resources.get_distribution(r.split('==')[0]).exists()]; sys.exit(0) if not missing else print(f'Missing: {missing}')" 2>nul || (
  echo Installing missing dependencies from requirements.txt...
  %PYTHON_CMD% -m pip install -r "%~dp0requirements.txt"
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
