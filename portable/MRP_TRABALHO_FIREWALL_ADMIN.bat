@echo off
chcp 65001 >nul
setlocal EnableExtensions
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "PS=powershell.exe -NoProfile -ExecutionPolicy Bypass"

echo ========================================================
echo MRP_LOCAL - FIREWALL PC DO TRABALHO
echo ========================================================
echo Este script precisa ser executado como Administrador.
echo Ele libera entrada TCP na porta configurada do MRP_LOCAL.
echo.
%PS% -File "%ROOT%\03-vs\scripts\servicos\mrp_firewall_8765.ps1"
echo.
pause
