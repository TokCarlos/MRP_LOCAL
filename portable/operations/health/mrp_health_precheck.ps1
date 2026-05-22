$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$MrpRoot = Resolve-Path (Join-Path $ScriptDir "..")
$RepoRoot = Resolve-Path (Join-Path $MrpRoot "..")
$Port = 8765

$RequiredDirs = @(
    "config", "runtime", "tools", "data", "db", "logs", "tmp", "backups",
    "front_end", "back_end", "engine", "adapters", "install", "health", "docs_runtime"
)

$Errors = New-Object System.Collections.Generic.List[string]
$Warnings = New-Object System.Collections.Generic.List[string]

function Test-WriteAccess {
    param([string]$Dir)
    $probe = Join-Path $Dir (".write_test_" + [guid]::NewGuid().ToString("N") + ".tmp")
    try {
        [System.IO.File]::WriteAllText($probe, "ok", [System.Text.UTF8Encoding]::new($false))
        Remove-Item -LiteralPath $probe -Force
        return $true
    } catch {
        return $false
    }
}

foreach ($dir in $RequiredDirs) {
    $path = Join-Path $MrpRoot $dir
    if (!(Test-Path $path)) { $Errors.Add("Diretorio ausente: $dir") }
}

$index = Join-Path $MrpRoot "front_end\index.html"
if (!(Test-Path $index)) { $Errors.Add("front_end/index.html ausente") }

$config = Join-Path $MrpRoot "config\mrp_local.env.json"
if (!(Test-Path $config)) {
    $Warnings.Add("config/mrp_local.env.json ausente")
} else {
    try { Get-Content $config -Raw | ConvertFrom-Json | Out-Null } catch { $Errors.Add("config/mrp_local.env.json invalido: $($_.Exception.Message)") }
}

foreach ($dir in @("logs", "tmp", "backups")) {
    $path = Join-Path $MrpRoot $dir
    if ((Test-Path $path) -and !(Test-WriteAccess -Dir $path)) { $Errors.Add("Sem permissao de escrita em: $dir") }
}

$pyOk = $false
try {
    $cmd = Get-Command py -ErrorAction Stop
    if ($cmd) { $pyOk = $true }
} catch {}

$runtimePython = Join-Path $MrpRoot "runtime\python\python.exe"
if (!$pyOk -and !(Test-Path $runtimePython)) {
    $Warnings.Add("Python nao encontrado via py e runtime portatil ainda ausente")
}

$tcp = Test-NetConnection -ComputerName "127.0.0.1" -Port $Port -WarningAction SilentlyContinue
if ($tcp.TcpTestSucceeded) {
    $Warnings.Add("Porta $Port esta ocupada/respondendo")
} else {
    $Warnings.Add("Porta $Port livre ou sem resposta local")
}

$forbidden = @()
$forbidden += Get-ChildItem -Path $RepoRoot -Recurse -Force -File -ErrorAction SilentlyContinue |
    Where-Object {
        $_.FullName -notmatch "\\.git(\\|$)" -and
        ($_.Name -eq "Thumbs.db" -or $_.Name -eq "desktop.ini" -or $_.Extension -in @(".pyc", ".tmp", ".temp", ".log"))
    } |
    Select-Object -ExpandProperty FullName

if ($forbidden.Count -gt 0) {
    foreach ($f in $forbidden) { $Warnings.Add("Arquivo operacional encontrado: $f") }
}

Write-Host "MRP_HEALTH_PRECHECK"
Write-Host "MRP_ROOT=$MrpRoot"
Write-Host "REPO_ROOT=$RepoRoot"
Write-Host "PORT=$Port"
Write-Host "ERRORS=$($Errors.Count)"
Write-Host "WARNINGS=$($Warnings.Count)"

foreach ($w in $Warnings) { Write-Host "WARN: $w" }
foreach ($e in $Errors) { Write-Host "ERROR: $e" }

if ($Errors.Count -gt 0) { exit 1 }
exit 0