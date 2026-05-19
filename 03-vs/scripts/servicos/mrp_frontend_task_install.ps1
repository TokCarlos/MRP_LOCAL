param(
    [ValidateSet("ONLOGON", "ONSTART")]
    [string]$Schedule = "ONLOGON"
)
$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$log = Join-Path $ctx.LogsDir "frontend.task_install.log"
$watchdog = Join-Path $ctx.ScriptsDir "mrp_frontend_watchdog.ps1"
if (-not (Test-Path -LiteralPath $watchdog)) { throw "Watchdog nao encontrado: $watchdog" }

$action = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$watchdog`""
try {
    schtasks /Query /TN $ctx.TaskName > $null 2>&1
    if ($LASTEXITCODE -eq 0) { schtasks /Delete /TN $ctx.TaskName /F | Out-Null }

    schtasks /Create /TN $ctx.TaskName /SC $Schedule /TR $action /RL LIMITED /F | Out-Null
    schtasks /Query /TN $ctx.TaskName > $null 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Tarefa nao encontrada apos criacao." }

    Add-MrpLogLine -LogFile $log -Origem "task_install" -Status "OK" -Detalhe "Task=$($ctx.TaskName) Schedule=$Schedule Script=$watchdog"
    Write-Host "Tarefa instalada: $($ctx.TaskName) Schedule=$Schedule"
} catch {
    Add-MrpLogLine -LogFile $log -Origem "task_install" -Status "ERRO" -Detalhe $_.Exception.Message
    throw
}
