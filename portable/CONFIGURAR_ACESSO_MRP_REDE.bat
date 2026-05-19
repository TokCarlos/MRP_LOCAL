@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul

REM ============================================================
REM CONFIGURAR_ACESSO_MRP_REDE.bat
REM Preparar PC cliente da rede para acessar o MRP_LOCAL.
REM Servidor MRP LAN: 192.168.1.71:8765
REM Servidor MRP Tailscale: 100.117.224.127:8765
REM ============================================================

set "MRP_HOST_LAN=192.168.1.71"
set "MRP_HOST_TS=100.117.224.127"
set "MRP_PORT=8765"
set "MRP_URL_LAN=http://%MRP_HOST_LAN%:%MRP_PORT%/index.html"
set "MRP_URL_TS=http://%MRP_HOST_TS%:%MRP_PORT%/index.html"

set "LOG_DIR=%LOCALAPPDATA%\MRP_LOCAL\access_setup"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%" >nul 2>&1
set "LOG_FILE=%LOG_DIR%\configurar_acesso_mrp_rede.log"

echo ============================================================
echo CONFIGURAR ACESSO MRP_LOCAL - PC CLIENTE DA REDE
echo ============================================================
echo Data/Hora: %date% %time%
echo URL LAN: %MRP_URL_LAN%
echo URL Tailscale: %MRP_URL_TS%
echo Log: %LOG_FILE%
echo.

>> "%LOG_FILE%" echo ============================================================
>> "%LOG_FILE%" echo CONFIGURAR ACESSO MRP_LOCAL - PC CLIENTE DA REDE
>> "%LOG_FILE%" echo ============================================================
>> "%LOG_FILE%" echo Data/Hora: %date% %time%
>> "%LOG_FILE%" echo URL LAN: %MRP_URL_LAN%
>> "%LOG_FILE%" echo URL Tailscale: %MRP_URL_TS%
>> "%LOG_FILE%" echo.

echo [1/8] Conferindo proxy WinHTTP...
>> "%LOG_FILE%" echo [1/8] Conferindo proxy WinHTTP...
netsh winhttp show proxy
netsh winhttp show proxy >> "%LOG_FILE%" 2>&1
echo.

echo [2/8] Conferindo proxy do usuario/navegador...
>> "%LOG_FILE%" echo [2/8] Conferindo proxy do usuario/navegador...
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable >> "%LOG_FILE%" 2>&1
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer >> "%LOG_FILE%" 2>&1
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride >> "%LOG_FILE%" 2>&1
echo.

echo [3/8] Atualizando excecoes de proxy do usuario...
>> "%LOG_FILE%" echo [3/8] Atualizando excecoes de proxy do usuario...

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$key='HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings';" ^
 "$backupDir=Join-Path $env:LOCALAPPDATA 'MRP_LOCAL\access_setup';" ^
 "New-Item -ItemType Directory -Force -Path $backupDir | Out-Null;" ^
 "$backup=Join-Path $backupDir 'proxy_override_backup.txt';" ^
 "$current=(Get-ItemProperty -Path $key -Name ProxyOverride -ErrorAction SilentlyContinue).ProxyOverride;" ^
 "if($null -eq $current){$current=''};" ^
 "[System.IO.File]::WriteAllText($backup,$current,[System.Text.UTF8Encoding]::new($false));" ^
 "$items=@();" ^
 "if($current.Trim().Length -gt 0){$items += ($current -split ';')}" ^
 "$items += @('localhost','127.0.0.1','%MRP_HOST_LAN%','192.168.*','10.*','172.16.*','172.17.*','172.18.*','172.19.*','172.20.*','172.21.*','172.22.*','172.23.*','172.24.*','172.25.*','172.26.*','172.27.*','172.28.*','172.29.*','172.30.*','172.31.*','%MRP_HOST_TS%','100.*','100.64.*','100.117.*','<local>');" ^
 "$merged=($items | Where-Object { $_ -and $_.Trim().Length -gt 0 } | ForEach-Object { $_.Trim() } | Select-Object -Unique) -join ';';" ^
 "Set-ItemProperty -Path $key -Name ProxyOverride -Value $merged;" ^
 "Write-Host 'ProxyOverride atualizado:';" ^
 "Write-Host $merged;" >> "%LOG_FILE%" 2>&1

if errorlevel 1 (
    echo ERRO: Falha ao atualizar ProxyOverride. Veja o log.
    >> "%LOG_FILE%" echo ERRO: Falha ao atualizar ProxyOverride.
) else (
    echo ProxyOverride atualizado com excecoes para MRP.
    >> "%LOG_FILE%" echo ProxyOverride atualizado com excecoes para MRP.
)
echo.

echo [4/8] Testando porta LAN %MRP_HOST_LAN%:%MRP_PORT%...
>> "%LOG_FILE%" echo [4/8] Testando porta LAN %MRP_HOST_LAN%:%MRP_PORT%...

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$r=Test-NetConnection '%MRP_HOST_LAN%' -Port %MRP_PORT% -WarningAction SilentlyContinue;" ^
 "Write-Host ('TcpTestSucceeded=' + $r.TcpTestSucceeded);" ^
 "if(-not $r.TcpTestSucceeded){ exit 2 }" >> "%LOG_FILE%" 2>&1

if errorlevel 2 (
    echo ALERTA: A porta LAN nao respondeu. Pode ser firewall, IP errado ou servidor MRP desligado.
    >> "%LOG_FILE%" echo ALERTA: Porta LAN falhou.
    set "LAN_PORT_OK=0"
) else (
    echo Porta LAN respondeu OK.
    >> "%LOG_FILE%" echo Porta LAN respondeu OK.
    set "LAN_PORT_OK=1"
)
echo.

echo [5/8] Testando HTTP LAN sem proxy...
>> "%LOG_FILE%" echo [5/8] Testando HTTP LAN sem proxy...
curl --noproxy "*" -I "%MRP_URL_LAN%"
curl --noproxy "*" -I "%MRP_URL_LAN%" >> "%LOG_FILE%" 2>&1

if errorlevel 1 (
    echo ALERTA: HTTP LAN sem proxy falhou.
    >> "%LOG_FILE%" echo ALERTA: HTTP LAN sem proxy falhou.
    set "LAN_HTTP_OK=0"
) else (
    echo HTTP LAN sem proxy respondeu.
    >> "%LOG_FILE%" echo HTTP LAN sem proxy respondeu.
    set "LAN_HTTP_OK=1"
)
echo.

echo [6/8] Testando Tailscale como fallback, se houver rota...
>> "%LOG_FILE%" echo [6/8] Testando Tailscale como fallback...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$r=Test-NetConnection '%MRP_HOST_TS%' -Port %MRP_PORT% -WarningAction SilentlyContinue;" ^
 "Write-Host ('TcpTestSucceeded=' + $r.TcpTestSucceeded);" >> "%LOG_FILE%" 2>&1

curl --noproxy "*" -I "%MRP_URL_TS%" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo Tailscale nao respondeu neste PC. Normal se este PC nao tiver Tailscale.
    >> "%LOG_FILE%" echo Tailscale nao respondeu neste PC.
) else (
    echo Tailscale respondeu neste PC.
    >> "%LOG_FILE%" echo Tailscale respondeu neste PC.
)
echo.

echo [7/8] Criando atalho na Area de Trabalho...
>> "%LOG_FILE%" echo [7/8] Criando atalho na Area de Trabalho...

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "$desktop=[Environment]::GetFolderPath('Desktop');" ^
 "$url='%MRP_URL_LAN%';" ^
 "$shortcutPath=Join-Path $desktop 'MRP_LOCAL.url';" ^
 "$content='[InternetShortcut]' + [Environment]::NewLine + 'URL=' + $url + [Environment]::NewLine;" ^
 "[System.IO.File]::WriteAllText($shortcutPath,$content,[System.Text.UTF8Encoding]::new($false));" ^
 "Write-Host ('Atalho criado: ' + $shortcutPath);" >> "%LOG_FILE%" 2>&1

if errorlevel 1 (
    echo ALERTA: Nao foi possivel criar atalho.
    >> "%LOG_FILE%" echo ALERTA: Nao foi possivel criar atalho.
) else (
    echo Atalho criado na Area de Trabalho: MRP_LOCAL.url
    >> "%LOG_FILE%" echo Atalho criado na Area de Trabalho.
)
echo.

echo [8/8] Abrindo MRP_LOCAL no navegador padrao...
>> "%LOG_FILE%" echo [8/8] Abrindo MRP_LOCAL no navegador padrao.
start "" "%MRP_URL_LAN%"
echo.

echo ============================================================
echo RESULTADO
echo ============================================================
echo URL principal: %MRP_URL_LAN%
echo URL Tailscale:  %MRP_URL_TS%
echo Log salvo em: %LOG_FILE%

>> "%LOG_FILE%" echo ============================================================
>> "%LOG_FILE%" echo RESULTADO
>> "%LOG_FILE%" echo URL principal: %MRP_URL_LAN%
>> "%LOG_FILE%" echo URL Tailscale: %MRP_URL_TS%
>> "%LOG_FILE%" echo Log salvo em: %LOG_FILE%

if "%LAN_PORT_OK%"=="1" (
    echo Porta LAN: OK
    >> "%LOG_FILE%" echo Porta LAN: OK
) else (
    echo Porta LAN: FALHOU
    >> "%LOG_FILE%" echo Porta LAN: FALHOU
)

if "%LAN_HTTP_OK%"=="1" (
    echo HTTP LAN sem proxy: OK
    >> "%LOG_FILE%" echo HTTP LAN sem proxy: OK
) else (
    echo HTTP LAN sem proxy: FALHOU
    >> "%LOG_FILE%" echo HTTP LAN sem proxy: FALHOU
)

echo.
echo Se o navegador ainda der erro de proxy, feche Chrome/Edge e abra novamente.
echo Se continuar falhando, envie o log:
echo %LOG_FILE%
echo.
pause
endlocal
exit /b 0
