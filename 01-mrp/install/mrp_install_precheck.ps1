$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$MrpRoot = Resolve-Path (Join-Path $ScriptDir "..")
$RepoRoot = Resolve-Path (Join-Path $MrpRoot "..")
$HealthScript = Join-Path $MrpRoot "health\mrp_health_precheck.ps1"

Write-Host "MRP_INSTALL_PRECHECK"
Write-Host "Este script nao instala dependencias, nao cria banco e nao inicia backend."
Write-Host "MRP_ROOT=$MrpRoot"
Write-Host "REPO_ROOT=$RepoRoot"

if (!(Test-Path $HealthScript)) {
    Write-Host "ERROR: health/mrp_health_precheck.ps1 ausente"
    exit 1
}

& powershell -NoProfile -ExecutionPolicy Bypass -File $HealthScript
$healthExit = $LASTEXITCODE

Write-Host "HEALTH_EXIT=$healthExit"
if ($healthExit -ne 0) { exit $healthExit }

Write-Host "INSTALL_PRECHECK=OK"
exit 0