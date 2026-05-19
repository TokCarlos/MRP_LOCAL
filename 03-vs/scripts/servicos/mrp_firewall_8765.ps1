$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$ruleName = "MRP_LOCAL_FRONTEND_$($ctx.Port)"
$exists = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
if ($exists) {
    Write-Host "Regra ja existe: $ruleName"
    exit 0
}
New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Profile Private -Action Allow -Protocol TCP -LocalPort $ctx.Port | Out-Null
Write-Host "Regra criada: $ruleName"
