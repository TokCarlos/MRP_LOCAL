$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$backendRootDir = Join-Path $root "01-mrp\back_end"
$backendHost = "127.0.0.1"
$port = 8876
$baseUrl = "http://$backendHost`:$port"
$endpoints = @(
    "/health",
    "/api/status",
    "/api/produtos",
    "/api/produtos/bases"
)

$errors = New-Object System.Collections.Generic.List[string]

if (!(Test-Path -LiteralPath $backendRootDir)) {
    $errors.Add("backend oficial inexistente: $backendRootDir")
}

foreach ($endpoint in $endpoints) {
    $url = "$baseUrl$endpoint"
    try {
        $resp = Invoke-WebRequest -UseBasicParsing -TimeoutSec 4 -Uri $url
        if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 300) {
            Write-Host "$endpoint = OK HTTP $($resp.StatusCode)"
        } else {
            $errors.Add("$endpoint HTTP $($resp.StatusCode)")
            Write-Host "$endpoint = FALHOU HTTP $($resp.StatusCode)"
        }
    } catch {
        $errors.Add("$endpoint sem resposta: $($_.Exception.Message)")
        Write-Host "$endpoint = FALHOU $($_.Exception.Message)"
    }
}

if ($errors.Count -eq 0) {
    Write-Host "HEALTHCHECK_BACKEND=OK"
    exit 0
}

Write-Host "HEALTHCHECK_BACKEND=FAIL"
foreach ($e in $errors) {
    Write-Host " - $e"
}
exit 1
