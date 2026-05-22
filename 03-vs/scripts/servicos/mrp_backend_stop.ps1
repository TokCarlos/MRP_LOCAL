$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$backendRootDir = Join-Path $root "01-mrp\back_end"
$stateDir = Join-Path $env:LOCALAPPDATA "MRP_LOCAL\backend"
$pidFile = Join-Path $stateDir "backend.pid"
$port = 8876

function Get-PortPids([int]$Port) {
    try {
        return @(Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $_.LocalPort -eq $Port } | Select-Object -ExpandProperty OwningProcess -Unique)
    } catch { return @() }
}

$stopped = 0
if (!(Test-Path -LiteralPath $backendRootDir)) {
    Write-Host "ERRO: backend oficial inexistente: $backendRootDir"
    exit 2
}

$listeners = Get-PortPids -Port $port
if ($listeners.Count -eq 0) {
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
    Write-Host "Backend parado. Porta $port livre."
    exit 0
}

Write-Host "Porta $port ocupada. Encerrando somente processo dono da porta."
foreach ($listenerPid in $listeners) {
    try {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $listenerPid" -ErrorAction SilentlyContinue
        $name = if ($proc) { $proc.Name } else { "desconhecido" }
        Write-Host "Encerrando PID=$listenerPid Processo=$name"
        Stop-Process -Id $listenerPid -Force -ErrorAction Stop
        $stopped++
    } catch {
        Write-Host "ERRO: falha ao encerrar PID=${listenerPid}: $($_.Exception.Message)"
    }
}

if (Test-Path -LiteralPath $pidFile) {
    $pidText = Get-Content -Path $pidFile -ErrorAction SilentlyContinue
    if ($pidText -match "^\d+$") {
        $pidNumber = [int]$pidText
        if ($listeners -contains $pidNumber) {
            Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
        }
    }
}

Start-Sleep -Milliseconds 800
$after = Get-PortPids -Port $port
if ($after.Count -gt 0) {
    Write-Host "ERRO: porta $port ainda em LISTEN. PIDs=$([string]::Join(', ', $after))"
    exit 2
}

Write-Host "Backend parado. Processos encerrados: $stopped"
exit 0
