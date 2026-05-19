@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "SCRIPTS=%ROOT%\03-vs\scripts\servicos"
set "CONFIG=%ROOT%\01-mrp\config\mrp_local.env.json"
set "PS=powershell.exe -NoProfile -ExecutionPolicy Bypass"
set "TASK_NAME=MRP_LOCAL_FRONTEND"

if exist "%CONFIG%" (
    for /f "usebackq delims=" %%T in (`powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "try { $p = '%CONFIG%'; ((Get-Content -Raw -LiteralPath $p) | ConvertFrom-Json).windows_task.name } catch { 'MRP_LOCAL_FRONTEND' }"`) do (
        if not "%%T"=="" set "TASK_NAME=%%T"
    )
)

if not exist "%SCRIPTS%\mrp_frontend_start.ps1" goto ERRO_ESTRUTURA
if not exist "%SCRIPTS%\mrp_frontend_stop.ps1" goto ERRO_ESTRUTURA
if not exist "%SCRIPTS%\mrp_frontend_healthcheck.ps1" goto ERRO_ESTRUTURA

:MENU
cls
echo ========================================================
echo                  MRP_LOCAL - SISTEMA
echo ========================================================
echo Raiz: %ROOT%
echo Tarefa Windows: %TASK_NAME%
echo.
echo 1 - Iniciar Sistema
echo 2 - Desativar Sistema
echo 3 - Reiniciar Sistema
echo 4 - Sair
echo.
choice /C 1234 /N /M "Escolha uma opcao [1-4]: "
if errorlevel 4 goto SAIR
if errorlevel 3 goto REINICIAR
if errorlevel 2 goto DESATIVAR
if errorlevel 1 goto INICIAR
goto MENU

:INICIAR
cls
echo ========================================================
echo Iniciando MRP_LOCAL...
echo ========================================================
echo.
call :HABILITAR_TAREFA
%PS% -File "%SCRIPTS%\mrp_frontend_start.ps1"
echo.
echo Validando healthcheck...
%PS% -File "%SCRIPTS%\mrp_frontend_healthcheck.ps1"
echo.
pause
goto MENU

:DESATIVAR
cls
echo ========================================================
echo Desativando MRP_LOCAL...
echo ========================================================
echo.
echo Encerrando/desabilitando tarefa Windows, se existir...
schtasks /End /TN "%TASK_NAME%" >nul 2>nul
schtasks /Change /TN "%TASK_NAME%" /Disable >nul 2>nul
echo.
echo Parando frontend e watchdog do projeto...
%PS% -File "%SCRIPTS%\mrp_frontend_stop.ps1"
echo.
echo Sistema desativado nesta maquina. Para religar, use a opcao 1.
echo.
pause
goto MENU

:REINICIAR
cls
echo ========================================================
echo Reiniciando MRP_LOCAL...
echo ========================================================
echo.
%PS% -File "%SCRIPTS%\mrp_frontend_stop.ps1"
timeout /t 2 /nobreak >nul
%PS% -File "%SCRIPTS%\mrp_frontend_start.ps1"
echo.
echo Validando healthcheck...
%PS% -File "%SCRIPTS%\mrp_frontend_healthcheck.ps1"
echo.
pause
goto MENU

:HABILITAR_TAREFA
schtasks /Query /TN "%TASK_NAME%" >nul 2>nul
if %errorlevel% equ 0 schtasks /Change /TN "%TASK_NAME%" /Enable >nul 2>nul
exit /b 0

:ERRO_ESTRUTURA
cls
echo ERRO: estrutura do projeto nao encontrada.
echo Este arquivo deve ficar na raiz do projeto MRP_LOCAL.
echo Pasta esperada: %SCRIPTS%
pause
exit /b 1

:SAIR
exit /b 0
