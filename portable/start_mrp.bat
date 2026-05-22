@echo off
setlocal EnableExtensions
set "ROOT=%~dp0"
set "PORT_FRONT=8765"
set "PORT_BACK=8876"
set "FRONT_DIR=%ROOT%app\frontend"
set "BACK_DIR=%ROOT%app\backend"
set "LOG_DIR=%ROOT%logs"
set "TMP_DIR=%ROOT%tmp"
set "RUN_DIR=%ROOT%runtime"
set "PY_CMD=python"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
if not exist "%TMP_DIR%" mkdir "%TMP_DIR%"
if not exist "%RUN_DIR%" mkdir "%RUN_DIR%"

if not exist "%FRONT_DIR%\index.html" (
  echo [ERRO] Frontend nao encontrado em %FRONT_DIR%\index.html
  exit /b 1
)

where %PY_CMD% >nul 2>nul
if errorlevel 1 (
  echo [ERRO] Python nao encontrado no PATH. Necessario para iniciar o portable.
  exit /b 1
)

echo [INFO] Iniciando frontend na porta %PORT_FRONT%
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "if ($env:PATH -and $env:Path) { Remove-Item Env:PATH -ErrorAction SilentlyContinue }; $p = Start-Process -FilePath '%PY_CMD%' -ArgumentList '-m http.server %PORT_FRONT% --bind 0.0.0.0 --directory ""%FRONT_DIR%""' -PassThru -WindowStyle Hidden -RedirectStandardOutput '%LOG_DIR%\frontend.out.log' -RedirectStandardError '%LOG_DIR%\frontend.err.log'; Set-Content -LiteralPath '%TMP_DIR%\frontend.pid' -Value $p.Id -Encoding ascii"

if not exist "%BACK_DIR%\app\main.py" (
  echo [WARN] Backend nao encontrado em %BACK_DIR%\app\main.py. Fluxo segue com frontend.
  exit /b 0
)

echo [INFO] Validando dependencias backend (fastapi/uvicorn)
%PY_CMD% -c "import fastapi,uvicorn" >nul 2>nul
if errorlevel 1 (
  echo [WARN] Backend nao iniciado: fastapi/uvicorn indisponiveis no Python atual.
  exit /b 0
)

echo [INFO] Iniciando backend na porta %PORT_BACK%
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "if ($env:PATH -and $env:Path) { Remove-Item Env:PATH -ErrorAction SilentlyContinue }; $p = Start-Process -FilePath '%PY_CMD%' -ArgumentList '-m uvicorn app.main:app --host 0.0.0.0 --port %PORT_BACK% --app-dir ""%BACK_DIR%""' -PassThru -WindowStyle Hidden -RedirectStandardOutput '%LOG_DIR%\backend.out.log' -RedirectStandardError '%LOG_DIR%\backend.err.log'; Set-Content -LiteralPath '%TMP_DIR%\backend.pid' -Value $p.Id -Encoding ascii"

exit /b 0
