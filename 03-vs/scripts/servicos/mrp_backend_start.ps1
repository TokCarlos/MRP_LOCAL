$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$backendRootDir = Join-Path $root "01-mrp\back_end"
$stateDir = Join-Path $env:LOCALAPPDATA "MRP_LOCAL\backend"
$pidFile = Join-Path $stateDir "backend.pid"
$backendHost = "127.0.0.1"
$port = 8876

function Test-PortListening([int]$Port) {
    try {
        $c = Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $_.LocalPort -eq $Port }
        return ($null -ne $c)
    } catch { return $false }
}

if (!(Test-Path -LiteralPath $backendRootDir)) {
    Write-Host "ERRO: backend oficial inexistente: $backendRootDir"
    exit 1
}

if (Test-PortListening -Port $port) {
    Write-Host "Backend ja ativo na porta $port."
    exit 0
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    $py = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $py = "py"
} else {
    Write-Host "ERRO: Python nao encontrado."
    exit 1
}

try {
    & $py -c "import fastapi,uvicorn" | Out-Null
} catch {
    Write-Host "ERRO: FastAPI/Uvicorn nao disponiveis no ambiente Python atual."
    exit 1
}

New-Item -ItemType Directory -Force -Path $stateDir | Out-Null
$cmd = "pushd `"$backendRootDir`" && `"$py`" -m uvicorn app.main:app --host $backendHost --port $port"
$proc = Start-Process -FilePath "cmd.exe" -ArgumentList @("/d", "/c", $cmd) -WindowStyle Hidden -PassThru
Set-Content -Path $pidFile -Value $proc.Id -Encoding UTF8

Start-Sleep -Seconds 1
if (Test-PortListening -Port $port) {
    Write-Host "Backend iniciado. PID=$($proc.Id) URL=http://$backendHost`:$port/health"
    exit 0
}

Write-Host "ERRO: backend nao entrou em LISTEN na porta $port."
exit 1
