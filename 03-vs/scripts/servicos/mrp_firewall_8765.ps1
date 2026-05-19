$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$rule = "MRP_LOCAL_FRONTEND_$($ctx.Port)"
try { Get-NetFirewallRule -DisplayName $rule -ErrorAction Stop | Out-Null; Write-Host "Regra ja existe: $rule"; exit 0 } catch {}
New-NetFirewallRule -DisplayName $rule -Direction Inbound -Protocol TCP -LocalPort $ctx.Port -Action Allow | Out-Null
Write-Host "Regra de firewall criada: $rule porta $($ctx.Port)"
