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
    Write-Host "ERRO: backend oficial inexistente."
    exit 2
}
if (Test-Path -LiteralPath $pidFile) {
    $pidText = Get-Content -Path $pidFile -ErrorAction SilentlyContinue
    if ($pidText -match "^\d+$") {
        try {
            Stop-Process -Id ([int]$pidText) -Force -ErrorAction Stop
            $stopped++
        } catch { }
    }
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue
}

$remaining = Get-PortPids -Port $port
foreach ($pid in $remaining) {
    try {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $pid" -ErrorAction SilentlyContinue
        if ($proc -and $proc.Name -eq "python.exe") {
            Stop-Process -Id $pid -Force -ErrorAction Stop
            $stopped++
        }
    } catch { }
}

Start-Sleep -Milliseconds 800
$after = Get-PortPids -Port $port
if ($after.Count -gt 0) {
    Write-Host "ERRO: porta $port ainda em LISTEN. PIDs=$([string]::Join(', ', $after))"
    exit 2
}

Write-Host "Backend parado. Processos encerrados: $stopped"
exit 0
