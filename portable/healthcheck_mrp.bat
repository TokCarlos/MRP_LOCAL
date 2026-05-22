@echo off
setlocal EnableExtensions
set "PORT_FRONT=8765"
set "PORT_BACK=8876"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "try { $r=Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:%PORT_FRONT%/index.html' -TimeoutSec 3; if($r.StatusCode -ge 200 -and $r.StatusCode -lt 400){ Write-Host '[OK] Frontend respondeu'; exit 0 } else { Write-Host '[ERRO] Frontend status invalido'; exit 1 } } catch { Write-Host '[ERRO] Frontend indisponivel'; exit 1 }"
set "FRONT_STATUS=%ERRORLEVEL%"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "try { $r=Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:%PORT_BACK%/health' -TimeoutSec 3; if($r.StatusCode -ge 200 -and $r.StatusCode -lt 400){ Write-Host '[OK] Backend respondeu'; exit 0 } else { Write-Host '[WARN] Backend status invalido'; exit 0 } } catch { Write-Host '[INFO] Backend nao respondeu (opcional para frontend estatico)'; exit 0 }"

exit /b %FRONT_STATUS%
