$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$isListening = Test-PortListening -Port $ctx.Port
$httpOk = Test-MrpHttpOk -Url $ctx.HealthUrl

$ipLocal = (Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -notlike "127.*" -and $_.PrefixOrigin -ne "WellKnown" } |
    Select-Object -First 1 -ExpandProperty IPAddress)
$ipTail = (Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -like "100.*" } |
    Select-Object -First 1 -ExpandProperty IPAddress)

Write-Host "ROOT=$($ctx.Root)"
Write-Host "FRONTEND_DIR=$($ctx.FrontendDir)"
Write-Host "PORTA=$($ctx.Port)"
Write-Host "BIND=$($ctx.Bind)"
Write-Host "PORTA_LISTEN=$isListening"
Write-Host "HTTP_OK=$httpOk"
Write-Host "URL_LOCALHOST=http://localhost:$($ctx.Port)"
if ($ipLocal) { Write-Host "URL_LOCAL=http://${ipLocal}:$($ctx.Port)" }
if ($ipTail) { Write-Host "URL_TAILSCALE=http://${ipTail}:$($ctx.Port)" }
