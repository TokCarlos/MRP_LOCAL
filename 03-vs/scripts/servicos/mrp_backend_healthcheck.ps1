$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$backendRootDir = Join-Path $root "01-mrp\back_end"
$backendHost = "127.0.0.1"
$port = 8876
$healthUrl = "http://$backendHost`:$port/health"
$statusUrl = "http://$backendHost`:$port/api/status"
$produtosUrl = "http://$backendHost`:$port/api/produtos"

$errors = New-Object System.Collections.Generic.List[string]
if (!(Test-Path -LiteralPath $backendRootDir)) {
    $errors.Add("backend oficial inexistente")
}

try {
    $h = Invoke-WebRequest -UseBasicParsing -TimeoutSec 4 -Uri $healthUrl
    if ($h.StatusCode -lt 200 -or $h.StatusCode -ge 300) { $errors.Add("health HTTP $($h.StatusCode)") }
} catch {
    $errors.Add("health sem resposta")
}

try {
    $s = Invoke-WebRequest -UseBasicParsing -TimeoutSec 4 -Uri $statusUrl
    if ($s.StatusCode -lt 200 -or $s.StatusCode -ge 300) { $errors.Add("status HTTP $($s.StatusCode)") }
} catch {
    $errors.Add("status sem resposta")
}

try {
    $p = Invoke-WebRequest -UseBasicParsing -TimeoutSec 6 -Uri $produtosUrl
    if ($p.StatusCode -lt 200 -or $p.StatusCode -ge 300) { $errors.Add("produtos HTTP $($p.StatusCode)") }
} catch {
    $errors.Add("produtos sem resposta")
}

if ($errors.Count -eq 0) {
    Write-Host "HEALTHCHECK_BACKEND=OK"
    exit 0
}

Write-Host "HEALTHCHECK_BACKEND=FAIL"
foreach ($e in $errors) { Write-Host " - $e" }
exit 1
