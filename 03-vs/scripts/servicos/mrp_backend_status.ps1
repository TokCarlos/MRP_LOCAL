$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$backendRootDir = Join-Path $root "01-mrp\back_end"
$backendHost = "127.0.0.1"
$port = 8876
$healthUrl = "http://$backendHost`:$port/health"

function Test-PortListening([int]$Port) {
    try {
        $c = Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $_.LocalPort -eq $Port }
        return $c
    } catch { return @() }
}

Write-Host "MRP_BACKEND STATUS"
Write-Host "BackendRoot=$backendRootDir"
Write-Host "Porta=$port"
Write-Host "Health=$healthUrl"

if (!(Test-Path -LiteralPath $backendRootDir)) {
    Write-Host "ERRO: backend oficial inexistente."
    exit 2
}

$listeners = @(Test-PortListening -Port $port)
if ($listeners.Count -eq 0) {
    Write-Host "LISTEN=NAO"
} else {
    Write-Host "LISTEN=SIM"
    $pids = $listeners | Select-Object -ExpandProperty OwningProcess -Unique
    Write-Host "PIDs=$([string]::Join(', ', $pids))"
}

try {
    $resp = Invoke-WebRequest -UseBasicParsing -TimeoutSec 3 -Uri $healthUrl
    if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 300) {
        Write-Host "HEALTH=OK"
        exit 0
    }
    Write-Host "HEALTH=FAIL HTTP=$($resp.StatusCode)"
    exit 1
} catch {
    Write-Host "HEALTH=FAIL"
    exit 1
}
