$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$backendRootDir = Join-Path $root "01-mrp\back_end"
$venvPython = Join-Path $root "01-mrp\runtime\venv_backend\Scripts\python.exe"
$stateDir = Join-Path $env:LOCALAPPDATA "MRP_LOCAL\backend"
$pidFile = Join-Path $stateDir "backend.pid"
$backendHost = "0.0.0.0"
$port = 8876

function Test-PortListening([int]$Port) {
    try {
        $c = Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $_.LocalPort -eq $Port }
        if ($null -ne $c) {
            return $true
        }
    } catch { }

    try {
        $client = New-Object System.Net.Sockets.TcpClient
        $connect = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
        $ok = $connect.AsyncWaitHandle.WaitOne(500, $false)
        if ($ok) {
            $client.EndConnect($connect)
        }
        $client.Close()
        return $ok
    } catch {
        return $false
    }
}

if (!(Test-Path -LiteralPath $backendRootDir)) {
    Write-Host "ERRO: backend oficial inexistente: $backendRootDir"
    exit 1
}

if (Test-PortListening -Port $port) {
    Write-Host "Backend ja ativo na porta $port."
    exit 0
}

$pythonCandidates = @()

if (Test-Path -LiteralPath $venvPython) {
    $pythonCandidates += [pscustomobject]@{
        Nome = "venv_backend"
        Comando = $venvPython
        BaseArgs = @()
    }
} else {
    Write-Host "Aviso: venv_backend ausente em $venvPython"
}

$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if ($pythonPath) {
    $pythonCandidates += [pscustomobject]@{
        Nome = "python PATH"
        Comando = $pythonPath.Source
        BaseArgs = @()
    }
}

$pyLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($pyLauncher) {
    $pythonCandidates += [pscustomobject]@{
        Nome = "py launcher"
        Comando = $pyLauncher.Source
        BaseArgs = @()
    }
}

if ($pythonCandidates.Count -eq 0) {
    Write-Host "ERRO: Python nao encontrado."
    exit 1
}

$pythonSelecionado = $null
foreach ($candidate in $pythonCandidates) {
    try {
        & $candidate.Comando @($candidate.BaseArgs + @("-c", "import fastapi, uvicorn, pydantic, python_multipart")) | Out-Null
        $pythonSelecionado = $candidate
        break
    } catch {
        Write-Host "Aviso: dependencias ausentes em $($candidate.Nome)."
    }
}

if ($null -eq $pythonSelecionado) {
    Write-Host "ERRO: Dependencias do backend ausentes. Rode 03-vs/scripts/backend/setup_backend_dev_env.ps1"
    exit 1
}

if ($pythonSelecionado.Nome -ne "venv_backend") {
    Write-Host "Aviso: usando $($pythonSelecionado.Nome). Recomenda-se venv_backend."
}

Write-Host "Python backend selecionado: $($pythonSelecionado.Nome)"

New-Item -ItemType Directory -Force -Path $stateDir | Out-Null
$args = @($pythonSelecionado.BaseArgs + @(
    "-m",
    "uvicorn",
    "app.main:app",
    "--host",
    $backendHost,
    "--port",
    [string]$port,
    "--app-dir",
    $backendRootDir
))
$argLine = ($args | ForEach-Object {
    $arg = [string]$_
    if ($arg -match "\s") {
        '"' + ($arg -replace '"', '\"') + '"'
    } else {
        $arg
    }
}) -join " "

$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $pythonSelecionado.Comando
$psi.Arguments = $argLine
$psi.WorkingDirectory = $backendRootDir
$psi.UseShellExecute = $true
$psi.CreateNoWindow = $true
$psi.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
$proc = New-Object System.Diagnostics.Process
$proc.StartInfo = $psi
[void]$proc.Start()
Set-Content -Path $pidFile -Value $proc.Id -Encoding UTF8

for ($i = 1; $i -le 15; $i++) {
    Start-Sleep -Seconds 1
    if (Test-PortListening -Port $port) {
        Write-Host "Backend iniciado. PID=$($proc.Id) URL=http://127.0.0.1`:$port/health"
        exit 0
    }
}

Write-Host "ERRO: backend nao entrou em LISTEN na porta $port."
exit 1
