@echo off
chcp 65001 >nul
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "PANEL=%ROOT%\03-vs\scripts\painel\mrp_painel_controle.py"
set "LOGDIR=%ROOT%\01-mrp\logs\admin"
set "LOGFILE=%LOGDIR%\launcher_painel.log"

if not exist "%LOGDIR%" mkdir "%LOGDIR%" >nul 2>nul

call :LOG INICIO "Launcher iniciado"
call :LOG INFO "ROOT=%ROOT%"

if not exist "%PANEL%" (
  call :LOG ERRO "Painel nao encontrado em %PANEL%"
  echo ERRO: painel nao encontrado.
  echo Esperado: %PANEL%
  pause
  exit /b 1
)

set "PY_CMD="
where python >nul 2>nul
if %errorlevel% equ 0 set "PY_CMD=python"
if not defined PY_CMD (
  where py >nul 2>nul
  if %errorlevel% equ 0 set "PY_CMD=py"
)

if not defined PY_CMD (
  call :LOG ERRO "Python nao encontrado (python/py)"
  echo ERRO: Python nao encontrado.
  echo Instale Python ou configure py launcher.
  pause
  exit /b 2
)

call :LOG INFO "Executando painel com %PY_CMD%"
"%PY_CMD%" "%PANEL%"
set "EXITCODE=%errorlevel%"
call :LOG FIM "Painel finalizado exit=%EXITCODE%"

if not "%EXITCODE%"=="0" (
  echo O painel retornou erro ^(exit=%EXITCODE%^).
  echo Verifique o log: %LOGFILE%
  pause
)

exit /b %EXITCODE%

:LOG
set "LV=%~1"
set "MSG=%~2"
>>"%LOGFILE%" echo [%date% %time%] [%LV%] %MSG%
exit /b 0

