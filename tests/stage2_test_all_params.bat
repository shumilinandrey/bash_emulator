@echo off
chcp 65001 >nul
cd /d "%~dp0.."
python src\main.py -vfs vfs/motd_exists.json -s scripts/script.txt
pause