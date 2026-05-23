$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$backendRootDir = Join-Path $root "01-mrp\back_end"
$backendHost = "127.0.0.1"
$port = 8876
$healthUrl = "http://$backendHost`:$port/health"
$statusUrl = "http://$backendHost`:$port/api/status"

function Get-PortListeners([int]$Port) {
    try {
        $listeners = @(Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $_.LocalPort -eq $Port })
        if ($listeners.Count -gt 0) {
            return $listeners
        }
    } catch {
    }

    $netstatRows = @(netstat -ano | Select-String ":$Port\s+.*LISTENING")
    return @($netstatRows | ForEach-Object {
        $parts = ($_.Line.Trim() -split "\s+")
        [pscustomobject]@{
            LocalAddress = $parts[1]
            LocalPort = $Port
            OwningProcess = [int]$parts[-1]
        }
    })
}

function Test-HttpEndpoint([string]$Url) {
    try {
        $resp = Invoke-WebRequest -UseBasicParsing -TimeoutSec 3 -Uri $Url
        if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 300) {
            Write-Host "$Url = OK HTTP $($resp.StatusCode)"
            return $true
        }
        Write-Host "$Url = FALHOU HTTP $($resp.StatusCode)"
        return $false
    } catch {
        Write-Host "$Url = FALHOU $($_.Exception.Message)"
        return $false
    }
}

Write-Host "MRP_BACKEND STATUS"
Write-Host "BackendRoot=$backendRootDir"
Write-Host "Porta=$port"

if (!(Test-Path -LiteralPath $backendRootDir)) {
    Write-Host "ERRO: backend oficial inexistente: $backendRootDir"
    exit 2
}

$listeners = @(Get-PortListeners -Port $port)
if ($listeners.Count -eq 0) {
    Write-Host "Backend parado"
    Write-Host "LISTEN=NAO"
    exit 1
}

Write-Host "Backend rodando"
Write-Host "LISTEN=SIM"
$pids = @($listeners | Select-Object -ExpandProperty OwningProcess -Unique)
Write-Host "PIDs=$([string]::Join(', ', $pids))"
foreach ($listenerPid in $pids) {
    $proc = $null
    try {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $listenerPid" -ErrorAction SilentlyContinue
    } catch {
        $proc = $null
    }
    if ($proc) {
        Write-Host "PID=$listenerPid Processo=$($proc.Name) Comando=$($proc.CommandLine)"
    } else {
        $basicProc = Get-Process -Id $listenerPid -ErrorAction SilentlyContinue
        if ($basicProc) {
            Write-Host "PID=$listenerPid Processo=$($basicProc.ProcessName)"
        }
    }
}

$healthOk = Test-HttpEndpoint -Url $healthUrl
$statusOk = Test-HttpEndpoint -Url $statusUrl

if ($healthOk -and $statusOk) {
    Write-Host "STATUS_BACKEND=OK"
    exit 0
}

Write-Host "STATUS_BACKEND=FALHOU"
exit 1
