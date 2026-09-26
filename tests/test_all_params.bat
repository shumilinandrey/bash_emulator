@echo off
chcp 65001 >nul
python src\main.py -vfs vfs.json -s script.txt
pause