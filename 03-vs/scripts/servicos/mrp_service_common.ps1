$ErrorActionPreference = "Stop"
$script:MrpServiceCommonDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }

function Get-MrpRepoRoot {
    if ($env:MRP_LOCAL_ROOT -and (Test-Path -LiteralPath $env:MRP_LOCAL_ROOT)) {
        return (Resolve-Path -LiteralPath $env:MRP_LOCAL_ROOT).Path
    }

    $dir = $script:MrpServiceCommonDir
    $candidate = Join-Path $dir "..\..\.."
    if (Test-Path -LiteralPath $candidate) {
        return (Resolve-Path -LiteralPath $candidate).Path
    }

    throw "Nao foi possivel resolver a raiz do MRP_LOCAL. Defina MRP_LOCAL_ROOT ou execute o script dentro do projeto."
}

function Read-MrpConfig {
    $root = Get-MrpRepoRoot
    $configPath = Join-Path $root "01-mrp\config\mrp_local.env.json"
    if (-not (Test-Path -LiteralPath $configPath)) {
        throw "Config nao encontrada: $configPath"
    }
    $json = Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 | ConvertFrom-Json
    return [pscustomobject]@{ Root = $root; Path = $configPath; Data = $json }
}

function Join-MrpPath {
    param([string]$Root, [string]$RelativePath)
    return Join-Path $Root ($RelativePath -replace "/", "\")
}

function Write-Utf8NoBomFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Text,
        [switch]$Append
    )
    $dir = Split-Path -Parent $Path
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    $enc = [System.Text.UTF8Encoding]::new($false)
    if ($Append -and (Test-Path -LiteralPath $Path)) {
        [System.IO.File]::AppendAllText($Path, $Text, $enc)
    } else {
        [System.IO.File]::WriteAllText($Path, $Text, $enc)
    }
}

function Add-MrpLogLine {
    param(
        [Parameter(Mandatory = $true)][string]$LogFile,
        [Parameter(Mandatory = $true)][string]$Origem,
        [Parameter(Mandatory = $true)][string]$Status,
        [string]$Detalhe = ""
    )
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | Origem=$Origem | Status=$Status | Detalhe=$Detalhe`n"
    Write-Utf8NoBomFile -Path $LogFile -Text $line -Append
}

function Get-MrpServiceContext {
    $cfg = Read-MrpConfig
    $root = $cfg.Root
    $data = $cfg.Data
    $frontendDir = Join-MrpPath -Root $root -RelativePath $data.frontend.relative_dir
    $indexFile = Join-Path $frontendDir $data.frontend.index_file
    $logsDir = Join-MrpPath -Root $root -RelativePath $data.logs.relative_dir
    $scriptsDir = Join-Path $root "03-vs\scripts\servicos"
    New-Item -ItemType Directory -Force -Path $logsDir | Out-Null
    return [pscustomobject]@{
        Root = $root
        Config = $data
        ConfigPath = $cfg.Path
        FrontendDir = $frontendDir
        IndexFile = $indexFile
        LogsDir = $logsDir
        ScriptsDir = $scriptsDir
        Port = [int]$data.frontend.port
        Bind = [string]$data.frontend.bind
        HealthUrl = "http://127.0.0.1:$([int]$data.frontend.port)$([string]$data.frontend.health_path)"
        TaskName = [string]$data.windows_task.name
    }
}

function Test-PortListening {
    param([int]$Port)
    try {
        $conn = @(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction Stop)
        return ($conn.Count -gt 0)
    } catch {
        try {
            $client = New-Object Net.Sockets.TcpClient
            $iar = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
            $ok = $iar.AsyncWaitHandle.WaitOne(500, $false)
            $client.Close()
            return $ok
        } catch { return $false }
    }
}

function Test-MrpHttpOk {
    param([string]$Url, [int]$TimeoutSec = 2)
    try {
        $resp = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec $TimeoutSec
        return ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 400)
    } catch { return $false }
}

function Resolve-MrpPython {
    param($Context)
    $candidates = @()
    if ($Context.Config.python.preferred_relative_exe) {
        $candidates += (Join-MrpPath -Root $Context.Root -RelativePath ([string]$Context.Config.python.preferred_relative_exe))
    }
    if ($env:MRP_PYTHON_EXE) { $candidates += $env:MRP_PYTHON_EXE }
    if ($Context.Config.python.allow_py_launcher) { $candidates += "py.exe" }
    if ($Context.Config.python.allow_python_path) { $candidates += "python.exe" }

    foreach ($cmd in $candidates) {
        if (-not $cmd) { continue }
        if ($cmd -match "[\\/]") {
            if (Test-Path -LiteralPath $cmd) { return $cmd }
        } else {
            $found = Get-Command $cmd -ErrorAction SilentlyContinue
            if ($found) { return $found.Source }
        }
    }
    throw "Python nao encontrado. Configure MRP_PYTHON_EXE, instale Python ou forneca runtime portable em 01-mrp/runtime/python/python.exe."
}
