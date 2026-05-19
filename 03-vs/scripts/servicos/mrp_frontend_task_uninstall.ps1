$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
schtasks /Query /TN $ctx.TaskName > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tarefa nao encontrada: $($ctx.TaskName)"
    exit 0
}
schtasks /Delete /TN $ctx.TaskName /F | Out-Null
Write-Host "Tarefa removida: $($ctx.TaskName)"
