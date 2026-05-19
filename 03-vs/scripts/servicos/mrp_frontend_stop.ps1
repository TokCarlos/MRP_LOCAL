$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$log = Join-Path $ctx.LogsDir "frontend.stop.log"
$frontPattern = ($ctx.FrontendDir -replace "\\", "\\")
$killed = 0

$procs = Get-CimInstance Win32_Process | Where-Object {
    ($_.Name -match "^(python|py)(\.exe)?$") -and
    ($_.CommandLine -like "*http.server*") -and
    ($_.CommandLine -like "*$($ctx.Port)*") -and
    (($_.CommandLine -like "*$($ctx.FrontendDir)*") -or ($_.CommandLine -like "*$frontPattern*"))
}

foreach ($p in $procs) {
    Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    $killed++
    Add-MrpLogLine -LogFile $log -Origem "stop" -Status "PROCESSO_ENCERRADO" -Detalhe "PID=$($p.ProcessId)"
}

if ($killed -eq 0) {
    Add-MrpLogLine -LogFile $log -Origem "stop" -Status "NENHUM_PROCESSO" -Detalhe "Porta=$($ctx.Port)"
}
Write-Host "Processos encerrados: $killed"
