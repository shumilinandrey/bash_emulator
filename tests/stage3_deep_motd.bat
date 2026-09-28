@echo off
chcp 65001 >nul
cd /d "%~dp0.."
python src\main.py -vfs vfs/deep_motd.json
pause