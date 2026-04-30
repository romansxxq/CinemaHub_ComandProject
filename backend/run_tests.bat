@echo off
REM Test Runner для CinemaHub Backend на Windows

cd /d "%~dp0"

REM Запуск pytest
python -m pytest tests/ -v --tb=short %*

pause
