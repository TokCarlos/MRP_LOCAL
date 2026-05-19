$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$log = Join-Path $ctx.LogsDir "frontend.start.log"
$outLog = Join-Path $ctx.LogsDir "frontend.out.log"
$errLog = Join-Path $ctx.LogsDir "frontend.err.log"
try {
    if (-not (Test-Path -LiteralPath $ctx.FrontendDir)) { throw "front_end inexistente: $($ctx.FrontendDir)" }
    if (-not (Test-Path -LiteralPath $ctx.IndexFile)) { throw "index.html inexistente: $($ctx.IndexFile)" }
    if (Test-MrpHttpOk -Url $ctx.HealthUrl -TimeoutSec 2) {
        Add-MrpLogLine -LogFile $log -Origem "start" -Status "JA_ATIVO" -Detalhe "URL=$($ctx.HealthUrl)"
        Write-Host "Servidor ja esta ativo na porta $($ctx.Port)."
        exit 0
    }
    if (Test-PortListening -Port $ctx.Port) {
        Add-MrpLogLine -LogFile $log -Origem "start" -Status "PORTA_OCUPADA_SEM_HTTP_OK" -Detalhe "Tentando encerrar servidor http.server antigo na porta $($ctx.Port)."
        $k = Stop-MrpHttpServerOnPort -Port $ctx.Port -LogFile $log
        Start-Sleep -Seconds 1
        if ((Test-PortListening -Port $ctx.Port) -and -not (Test-MrpHttpOk -Url $ctx.HealthUrl -TimeoutSec 2)) {
            throw "Porta $($ctx.Port) ocupada por processo que nao responde como MRP. Encerrar manualmente antes de iniciar."
        }
        if ($k -gt 0) { Add-MrpLogLine -LogFile $log -Origem "start" -Status "SERVIDOR_ANTIGO_ENCERRADO" -Detalhe "Processos=$k" }
    }
    $python = Resolve-MrpPython -Context $ctx
    $cmd = "pushd `"$($ctx.FrontendDir)`" && `"$python`" -m http.server $($ctx.Port) --bind $($ctx.Bind)"
    $proc = Start-Process -FilePath "cmd.exe" -ArgumentList @("/d", "/c", $cmd) -RedirectStandardOutput $outLog -RedirectStandardError $errLog -WindowStyle Hidden -PassThru
    Add-MrpLogLine -LogFile $log -Origem "start" -Status "INICIADO" -Detalhe "CMD_PID=$($proc.Id) Porta=$($ctx.Port) Bind=$($ctx.Bind) Frontend=$($ctx.FrontendDir) Python=$python"
    $deadline = (Get-Date).AddSeconds([Math]::Max(2, $ctx.StartupWaitSeconds))
    while ((Get-Date) -lt $deadline) {
        if (Test-MrpHttpOk -Url $ctx.HealthUrl -TimeoutSec 2) {
            Add-MrpLogLine -LogFile $log -Origem "start" -Status "HTTP_OK" -Detalhe "URL=$($ctx.HealthUrl)"
            Write-Host "Servidor iniciado. PID=$($proc.Id) Porta=$($ctx.Port)"
            exit 0
        }
        Start-Sleep -Milliseconds 700
    }
    Write-Host "Servidor iniciado. PID=$($proc.Id) Porta=$($ctx.Port)"
    Write-Host "Aviso: HTTP ainda nao validou dentro da janela de espera. Rode o healthcheck."
    Add-MrpLogLine -LogFile $log -Origem "start" -Status "HTTP_PENDENTE" -Detalhe "URL=$($ctx.HealthUrl)"
    exit 0
} catch {
    Add-MrpLogLine -LogFile $log -Origem "start" -Status "ERRO" -Detalhe $_.Exception.Message
    Write-Error $_.Exception.Message
    exit 1
}
