@echo off
chcp 65001 >nul
setlocal EnableExtensions
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"
set "PS=powershell.exe -NoProfile -ExecutionPolicy Bypass"

echo ========================================================
echo MRP_LOCAL - PRECHECK PC DO TRABALHO
echo ========================================================
echo Raiz detectada: %ROOT%
echo Destino esperado: X:\PCP\09_Sistema
echo.

if not exist "%ROOT%\01-mrp\front_end\index.html" (
  echo [CRITICO] Frontend nao encontrado: %ROOT%\01-mrp\front_end\index.html
  exit /b 1
)
if not exist "%ROOT%\03-vs\scripts\servicos\mrp_frontend_start.ps1" (
  echo [CRITICO] Script start nao encontrado.
  exit /b 1
)

where py >nul 2>nul
if %errorlevel% equ 0 (
  echo [OK] py.exe detectado.
) else (
  where python >nul 2>nul
  if %errorlevel% equ 0 (
    echo [OK] python.exe detectado.
  ) else (
    if exist "%ROOT%\01-mrp\runtime\python\python.exe" (
      echo [OK] Python portable detectado.
    ) else (
      echo [CRITICO] Python nao detectado. Instale Python ou configure runtime portable futuro.
      exit /b 1
    )
  )
)

echo.
echo Validando porta 8765...
netstat -ano | findstr :8765 | findstr LISTENING >nul 2>nul
if %errorlevel% equ 0 (
  echo [OPCIONAL] Porta 8765 ja esta em uso. Se for o MRP, isso pode estar OK. Rode status para confirmar.
) else (
  echo [OK] Porta 8765 livre.
)

echo.
echo Validando Tailscale, se existir...
where tailscale >nul 2>nul
if %errorlevel% equ 0 (
  tailscale status --peers=false >nul 2>nul
  if %errorlevel% equ 0 (
    echo [OK] Tailscale detectado e respondendo.
    for /f "delims=" %%A in ('tailscale ip -4 2^>nul') do echo IP_TAILSCALE=%%A
  ) else (
    echo [RECOMENDADO] Tailscale detectado, mas nao respondeu status. Validar login/conexao.
  )
) else (
  echo [RECOMENDADO] Tailscale nao encontrado no PATH. Necessario apenas para acesso remoto.
)

echo.
echo Rodando precheck passivo interno...
%PS% -File "%ROOT%\01-mrp\install\precheck_instalacao.ps1"
if errorlevel 1 (
  echo.
  echo [FALHA] Precheck interno encontrou pendencia critica.
  exit /b 1
)

echo.
echo PRECHECK_TRABALHO=OK_SEM_BLOQUEIO_CRITICO
echo Proximo passo: executar MRP_MENU_SISTEMA.bat e escolher opcao 1.
exit /b 0
