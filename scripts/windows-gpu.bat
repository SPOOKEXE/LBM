@echo off

echo Entering Directory
cd /d "%~dp0\\.."

echo Creating the virtual environment
py -m venv venv

echo Entering Virtual Environment
call venv.bat

echo Installing requirements
pip install --upgrade pip
pip install -r scripts\requirements.txt
pip install -r scripts\windows-nvidia-gpu.txt
