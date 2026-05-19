$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"

try {
    $ctx = Get-MrpServiceContext
    $log = Join-Path $ctx.LogsDir "frontend.stop.log"

    Add-MrpLogLine -LogFile $log -Origem "stop" -Status "INICIO" -Detalhe "Porta=$($ctx.Port) Root=$($ctx.Root)"

    $killedByPort = Stop-MrpHttpServerOnPort -Port $ctx.Port -LogFile $log -ForceAll
    $killedWatchdog = Stop-MrpRelatedWatchdogs -ProjectRoot $ctx.Root -LogFile $log
    $totalKilled = $killedByPort + $killedWatchdog

    Start-Sleep -Milliseconds 800

    $remainingProcessIds = @(Get-MrpPortListenerPids -Port $ctx.Port)

    if ($remainingProcessIds.Count -gt 0) {
        $remainingText = [string]::Join(", ", $remainingProcessIds)
        Add-MrpLogLine -LogFile $log -Origem "stop" -Status "FALHA_PORTA_OCUPADA" -Detalhe "Porta=$($ctx.Port) PIDs=$remainingText"

        Write-Host "ERRO: ainda existem processos em LISTENING na porta $($ctx.Port): $remainingText"
        exit 2
    }

    if ($totalKilled -eq 0) {
        Add-MrpLogLine -LogFile $log -Origem "stop" -Status "NENHUM_PROCESSO" -Detalhe "Porta=$($ctx.Port)"
    } else {
        Add-MrpLogLine -LogFile $log -Origem "stop" -Status "OK" -Detalhe "Encerrados=$totalKilled Porta=$($ctx.Port)"
    }

    Write-Host "Sistema parado. Processos encerrados: $totalKilled"
    exit 0
} catch {
    Write-Host "ERRO ao desativar MRP_LOCAL: $($_.Exception.Message)"
    exit 1
}
