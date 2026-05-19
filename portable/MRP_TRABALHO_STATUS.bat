@echo off
chcp 65001 >nul
setlocal EnableExtensions
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "PS=powershell.exe -NoProfile -ExecutionPolicy Bypass"
%PS% -File "%ROOT%\03-vs\scripts\servicos\mrp_frontend_status.ps1"
echo.
pause
