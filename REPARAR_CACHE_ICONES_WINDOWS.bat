@echo off
chcp 65001 >nul
setlocal EnableExtensions

set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "PS_SCRIPT=%ROOT%\03-vs\scripts\icons\reparar_cache_icones_windows.ps1"

if not exist "%PS_SCRIPT%" (
  echo ERRO: script nao encontrado.
  echo %PS_SCRIPT%
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%"
set "RC=%errorlevel%"
if not "%RC%"=="0" (
  echo Falha ao reparar cache de icones. Codigo: %RC%
  pause
)
exit /b %RC%
