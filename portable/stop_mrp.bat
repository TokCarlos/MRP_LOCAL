@echo off
setlocal EnableExtensions
set "ROOT=%~dp0"
set "TMP_DIR=%ROOT%tmp"

if exist "%TMP_DIR%\backend.pid" (
  for /f "usebackq delims=" %%P in ("%TMP_DIR%\backend.pid") do (
    if not "%%P"=="" (
      taskkill /PID %%P /T /F >nul 2>nul
      echo [INFO] Backend PID %%P encerrado.
    )
  )
  del /q "%TMP_DIR%\backend.pid" >nul 2>nul
)

if exist "%TMP_DIR%\frontend.pid" (
  for /f "usebackq delims=" %%P in ("%TMP_DIR%\frontend.pid") do (
    if not "%%P"=="" (
      taskkill /PID %%P /T /F >nul 2>nul
      echo [INFO] Frontend PID %%P encerrado.
    )
  )
  del /q "%TMP_DIR%\frontend.pid" >nul 2>nul
)

exit /b 0
