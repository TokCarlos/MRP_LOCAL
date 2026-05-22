@echo off
setlocal EnableExtensions
set "ROOT=%~dp0"
set "TMP_DIR=%ROOT%tmp"

echo [INFO] Status do portable

if exist "%TMP_DIR%\frontend.pid" (
  for /f "usebackq delims=" %%P in ("%TMP_DIR%\frontend.pid") do (
    tasklist /FI "PID eq %%P" | find "%%P" >nul 2>nul && echo [OK] Frontend em execucao PID %%P || echo [WARN] Frontend PID salvo mas processo nao esta ativo
  )
) else (
  echo [WARN] Frontend sem PID salvo
)

if exist "%TMP_DIR%\backend.pid" (
  for /f "usebackq delims=" %%P in ("%TMP_DIR%\backend.pid") do (
    tasklist /FI "PID eq %%P" | find "%%P" >nul 2>nul && echo [OK] Backend em execucao PID %%P || echo [WARN] Backend PID salvo mas processo nao esta ativo
  )
) else (
  echo [WARN] Backend sem PID salvo
)

netstat -ano | find ":8765" >nul 2>nul && echo [OK] Porta 8765 em uso || echo [WARN] Porta 8765 sem listener
netstat -ano | find ":8876" >nul 2>nul && echo [INFO] Porta 8876 em uso || echo [INFO] Porta 8876 sem listener

exit /b 0
