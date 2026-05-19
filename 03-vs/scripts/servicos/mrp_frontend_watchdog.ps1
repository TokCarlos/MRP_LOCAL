param([switch]$Once)
$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$log = Join-Path $ctx.LogsDir "frontend.watchdog.log"
$health = Join-Path $ctx.ScriptsDir "mrp_frontend_healthcheck.ps1"
$start = Join-Path $ctx.ScriptsDir "mrp_frontend_start.ps1"
$interval = [int]$ctx.Config.watchdog.interval_seconds
$maxRestarts = [int]$ctx.Config.watchdog.max_restarts_per_hour
$cooldown = [int]$ctx.Config.watchdog.restart_cooldown_seconds
$restartTimes = New-Object System.Collections.Generic.List[datetime]
Add-MrpLogLine -LogFile $log -Origem "watchdog" -Status "INICIADO" -Detalhe "Once=$Once Interval=$interval"
while ($true) {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $health | Out-Null
    $hc = $LASTEXITCODE
    if ($hc -eq 0) { Add-MrpLogLine -LogFile $log -Origem "watchdog" -Status "OK" -Detalhe "Healthcheck OK"; if ($Once) { exit 0 } }
    else {
        $now = Get-Date
        for ($i = $restartTimes.Count - 1; $i -ge 0; $i--) { if (($now - $restartTimes[$i]).TotalMinutes -gt 60) { $restartTimes.RemoveAt($i) } }
        if ($restartTimes.Count -ge $maxRestarts) { Add-MrpLogLine -LogFile $log -Origem "watchdog" -Status "COOLDOWN" -Detalhe "Limite de $maxRestarts restarts/hora atingido."; Start-Sleep -Seconds $cooldown }
        else { Add-MrpLogLine -LogFile $log -Origem "watchdog" -Status "RESTART" -Detalhe "Healthcheck falhou. Tentando iniciar."; & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $start | Out-Null; $restartTimes.Add((Get-Date)); Start-Sleep -Seconds 3 }
        if ($Once) { & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $health | Out-Null; exit $LASTEXITCODE }
    }
    Start-Sleep -Seconds $interval
}
