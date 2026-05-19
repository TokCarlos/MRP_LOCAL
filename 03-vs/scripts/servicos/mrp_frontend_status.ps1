$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"

$ctx = Get-MrpServiceContext

Write-Host "MRP_LOCAL STATUS"
Write-Host "Raiz=$($ctx.Root)"
Write-Host "Frontend=$($ctx.FrontendDir)"
Write-Host "Porta=$($ctx.Port)"
Write-Host "HealthUrl=$($ctx.HealthUrl)"

$listenerProcessIds = @(Get-MrpPortListenerPids -Port $ctx.Port)

if ($listenerProcessIds.Count -eq 0) {
    Write-Host "Porta: livre"
} else {
    Write-Host "Porta: ocupada por PID(s): $([string]::Join(', ', $listenerProcessIds))"

    foreach ($listenerProcessId in $listenerProcessIds) {
        $processInfo = Get-MrpProcessInfo -ProcessId $listenerProcessId

        if ($processInfo) {
            Write-Host "PID=$listenerProcessId Name=$($processInfo.Name) CMD=$($processInfo.CommandLine)"
        }
    }
}

if (Test-MrpHttpOk -Url $ctx.HealthUrl -TimeoutSec 2) {
    Write-Host "HTTP=OK"
    exit 0
} else {
    Write-Host "HTTP=FAIL"
    exit 1
}
