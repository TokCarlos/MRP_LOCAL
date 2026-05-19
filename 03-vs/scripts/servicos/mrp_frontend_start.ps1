$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$log = Join-Path $ctx.LogsDir "frontend.start.log"
$outLog = Join-Path $ctx.LogsDir "frontend.out.log"
$errLog = Join-Path $ctx.LogsDir "frontend.err.log"

try {
    if (-not (Test-Path -LiteralPath $ctx.FrontendDir)) { throw "front_end inexistente: $($ctx.FrontendDir)" }
    if (-not (Test-Path -LiteralPath $ctx.IndexFile)) { throw "index.html inexistente: $($ctx.IndexFile)" }

    if ((Test-PortListening -Port $ctx.Port) -and (Test-MrpHttpOk -Url $ctx.HealthUrl)) {
        Add-MrpLogLine -LogFile $log -Origem "start" -Status "JA_ATIVO" -Detalhe "Porta=$($ctx.Port) URL=$($ctx.HealthUrl)"
        Write-Host "Servidor ja esta ativo na porta $($ctx.Port)."
        exit 0
    }

    $python = Resolve-MrpPython -Context $ctx
    $args = @("-m", "http.server", "$($ctx.Port)", "--bind", $ctx.Bind, "--directory", $ctx.FrontendDir)
    $proc = Start-Process -FilePath $python -ArgumentList $args -RedirectStandardOutput $outLog -RedirectStandardError $errLog -WindowStyle Hidden -PassThru
    Add-MrpLogLine -LogFile $log -Origem "start" -Status "INICIADO" -Detalhe "PID=$($proc.Id) Porta=$($ctx.Port) Bind=$($ctx.Bind) Python=$python"
    Write-Host "Servidor iniciado. PID=$($proc.Id) Porta=$($ctx.Port)"
    exit 0
} catch {
    Add-MrpLogLine -LogFile $log -Origem "start" -Status "ERRO" -Detalhe $_.Exception.Message
    Write-Error $_.Exception.Message
    exit 1
}
