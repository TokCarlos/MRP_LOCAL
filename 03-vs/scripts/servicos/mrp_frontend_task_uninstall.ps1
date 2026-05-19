$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
schtasks /End /TN $ctx.TaskName > $null 2>&1
schtasks /Delete /TN $ctx.TaskName /F > $null 2>&1
Write-Host "Tarefa removida/desativada se existia: $($ctx.TaskName)"
