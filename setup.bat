@echo off
setlocal

REM 1. Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Downloading and installing Python 3.10...
    call install_python
)

REM 2. Check the Python version
for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)
echo Found Python version %MAJOR%.%MINOR%
if %MAJOR% lss 3 (
    echo Python version is less than 3.10. Downloading and installing Python 3.10...
    goto install_python
) else if %MAJOR%==3 if %MINOR% lss 10 (
    echo Python version is less than 3.10. Downloading and installing Python 3.10...
    goto install_python
) else (
    echo Python 3.10 or newer is already installed.
)

REM 3. INSTALLING MODULES
pip install pillow
pip install pynput
pip install pystray
timeout 10
exit /b 0







:install_python
REM Download Python 3.10 installer
set PYTHON_INSTALLER=python-3.10.11-amd64.exe
echo Downloading %PYTHON_INSTALLER%...
powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.11/%PYTHON_INSTALLER% -OutFile %PYTHON_INSTALLER%"

REM Install Python 3.10
echo Installing Python 3.10...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1

REM Clean up installer
del %PYTHON_INSTALLER%
exit /b 0

