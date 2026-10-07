@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\push_github.ps1"
pause
