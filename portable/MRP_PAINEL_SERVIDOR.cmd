@echo off
chcp 65001 >nul
setlocal EnableExtensions

set "ROOT=%~dp0"
set "PANEL=%ROOT%operations\painel\mrp_painel_controle.py"
set "LOGDIR=%ROOT%logs\admin"
set "LOGFILE=%LOGDIR%\launcher_painel.log"

if not exist "%LOGDIR%" mkdir "%LOGDIR%" >nul 2>nul
if not exist "%PANEL%" (
  echo ERRO: painel nao encontrado em %PANEL%
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
  echo ERRO: Python nao encontrado no PATH.
  exit /b 2
)

>>"%LOGFILE%" echo [%date% %time%] [INFO] Iniciando painel portable
"%PY_CMD%" "%PANEL%"
set "RC=%errorlevel%"
>>"%LOGFILE%" echo [%date% %time%] [INFO] Painel finalizado rc=%RC%
exit /b %RC%

