$ErrorActionPreference = "Stop"
. "$PSScriptRoot\mrp_service_common.ps1"
$ctx = Get-MrpServiceContext
$log = Join-Path $ctx.LogsDir "frontend.health.log"
$ok = $true
$errors = New-Object System.Collections.Generic.List[string]

if (-not (Test-Path -LiteralPath $ctx.Root)) { $ok = $false; $errors.Add("Raiz inexistente: $($ctx.Root)") }
if (-not (Test-Path -LiteralPath $ctx.ConfigPath)) { $ok = $false; $errors.Add("Config inexistente: $($ctx.ConfigPath)") }
if (-not (Test-Path -LiteralPath $ctx.FrontendDir)) { $ok = $false; $errors.Add("front_end inexistente: $($ctx.FrontendDir)") }
if (-not (Test-Path -LiteralPath $ctx.IndexFile)) { $ok = $false; $errors.Add("index.html inexistente: $($ctx.IndexFile)") }

try { $null = Resolve-MrpPython -Context $ctx } catch { $ok = $false; $errors.Add($_.Exception.Message) }

$isListening = Test-PortListening -Port $ctx.Port
if (-not $isListening) { $ok = $false; $errors.Add("Porta $($ctx.Port) nao esta escutando") }

$httpOk = Test-MrpHttpOk -Url $ctx.HealthUrl
if (-not $httpOk) { $ok = $false; $errors.Add("HTTP nao respondeu com sucesso em $($ctx.HealthUrl)") }

$detail = "OK=$ok LISTEN=$isListening HTTP=$httpOk ERRORS=$([string]::Join('; ', $errors))"
Add-MrpLogLine -LogFile $log -Origem "healthcheck" -Status $(if ($ok) { "OK" } else { "FALHA" }) -Detalhe $detail

if ($ok) {
    Write-Host "HEALTHCHECK=OK"
    exit 0
}

Write-Host "HEALTHCHECK=FAIL"
foreach ($e in $errors) { Write-Host " - $e" }
exit 1
