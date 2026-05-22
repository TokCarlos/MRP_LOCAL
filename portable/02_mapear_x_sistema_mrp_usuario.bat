@echo off
setlocal

set "SHARE=\\HOME-MACHINE\system_jpl"

echo [INFO] Removendo mapeamento anterior de X:, se existir.
net use X: /delete /y >nul 2>nul

echo [INFO] Mapeando X: para %SHARE%
net use X: "%SHARE%" /persistent:yes
if errorlevel 1 (
  echo [ERRO] Falha ao mapear X: para %SHARE%.
  exit /b 1
)

if not exist X:\ (
  echo [ERRO] X:\ nao ficou acessivel apos o mapeamento.
  exit /b 1
)

echo [OK] X: mapeado para %SHARE%.
exit /b 0
