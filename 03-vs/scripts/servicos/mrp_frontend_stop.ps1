$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$log = Join-Path $ctx.LogsDir "frontend.stop.log"
$killed = Stop-MrpHttpServerOnPort -Port $ctx.Port -LogFile $log
# also stop watchdog powershell started from this project
$rootEsc = [Regex]::Escape($ctx.Root)
$watchdogProcs = Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -ne $PID -and $_.Name -match "^(powershell|pwsh)(\.exe)?$" -and $_.CommandLine -like "*mrp_frontend_watchdog.ps1*" -and $_.CommandLine -match $rootEsc }
foreach ($p in $watchdogProcs) { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue; $killed++; Add-MrpLogLine -LogFile $log -Origem "stop" -Status "WATCHDOG_ENCERRADO" -Detalhe "PID=$($p.ProcessId)" }
if ($killed -eq 0) { Add-MrpLogLine -LogFile $log -Origem "stop" -Status "NENHUM_PROCESSO" -Detalhe "Porta=$($ctx.Port)" }
Write-Host "Processos encerrados: $killed"
exit 0
