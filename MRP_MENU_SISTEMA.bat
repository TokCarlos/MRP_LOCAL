@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "SERVICOS=%ROOT%\03-vs\scripts\servicos"
set "PAINEL_LAUNCHER_CMD=%ROOT%\MRP_PAINEL_SERVIDOR.cmd"
set "PS=powershell.exe -NoProfile -ExecutionPolicy Bypass"

if exist "%PAINEL_LAUNCHER_CMD%" (
    call "%PAINEL_LAUNCHER_CMD%"
    if %errorlevel% equ 0 exit /b 0
    echo.
    echo Launcher do painel retornou erro. Entrando no fallback CMD...
    echo.
)

if not exist "%SERVICOS%\mrp_frontend_start.ps1" goto ERRO_ESTRUTURA
if not exist "%SERVICOS%\mrp_frontend_stop.ps1" goto ERRO_ESTRUTURA
if not exist "%SERVICOS%\mrp_frontend_status.ps1" goto ERRO_ESTRUTURA

:MENU
cls
echo ========================================================
echo         MRP_LOCAL - FALLBACK MINIMO ^(SEM PYTHON^)
echo ========================================================
echo Raiz: %ROOT%
echo.
echo 1 - Iniciar Sistema
echo 2 - Desativar Sistema
echo 3 - Ver Status
echo 4 - Sair
echo.
choice /C 1234 /N /M "Escolha uma opcao [1-4]: "
if errorlevel 4 goto SAIR
if errorlevel 3 goto STATUS
if errorlevel 2 goto DESATIVAR
if errorlevel 1 goto INICIAR
goto MENU

:INICIAR
cls
echo Iniciando sistema...
%PS% -File "%SERVICOS%\mrp_frontend_start.ps1"
echo.
pause
goto MENU

:DESATIVAR
cls
echo Desativando sistema...
%PS% -File "%SERVICOS%\mrp_frontend_stop.ps1"
echo.
pause
goto MENU

:STATUS
cls
echo Consultando status...
%PS% -File "%SERVICOS%\mrp_frontend_status.ps1"
echo.
pause
goto MENU

:ERRO_ESTRUTURA
echo ERRO: estrutura esperada nao encontrada.
echo Esperado: %SERVICOS%
pause
exit /b 1

:SAIR
exit /b 0
