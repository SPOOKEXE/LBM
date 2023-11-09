@echo off

echo Entering Directory
cd /d "%~dp0"

echo Creating the virtual environment
py -m venv venv

echo Entering Virtual Environment
call venv\Scripts\activate.bat

echo Installing requirements
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
