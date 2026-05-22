@echo off
chcp 65001 >nul
setlocal EnableExtensions

:MENU
cls
echo ========================================================
echo                MRP_LOCAL - MENU PORTABLE
echo ========================================================
echo.
echo 1 - Iniciar sistema
echo 2 - Parar sistema
echo 3 - Status do sistema
echo 4 - Healthcheck
echo 5 - Abrir painel do servidor
echo 6 - Criar atalho do painel na area de trabalho
echo 7 - Sair
echo.
choice /C 1234567 /N /M "Escolha [1-7]: "
if errorlevel 7 exit /b 0
if errorlevel 6 call "%~dp0CRIAR_ATALHO_PAINEL_SERVIDOR.bat" & pause & goto MENU
if errorlevel 5 call "%~dp0MRP_PAINEL_SERVIDOR.cmd" & pause & goto MENU
if errorlevel 4 call "%~dp0healthcheck_mrp.bat" & pause & goto MENU
if errorlevel 3 call "%~dp0status_mrp.bat" & pause & goto MENU
if errorlevel 2 call "%~dp0stop_mrp.bat" & pause & goto MENU
if errorlevel 1 call "%~dp0start_mrp.bat" & pause & goto MENU
goto MENU
