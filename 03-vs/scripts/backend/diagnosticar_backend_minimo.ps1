$ErrorActionPreference = "Stop"

$backendHost = "127.0.0.1"
$port = 8876
$base = "http://$backendHost`:$port"
$urls = @("/health", "/api/status", "/api/produtos")

Write-Host "DIAGNOSTICO BACKEND MINIMO"
Write-Host "Base=$base"

foreach ($u in $urls) {
    $url = "$base$u"
    try {
        $r = Invoke-WebRequest -UseBasicParsing -TimeoutSec 6 -Uri $url
        Write-Host "$u => HTTP $($r.StatusCode)"
    } catch {
        Write-Host "$u => FAIL"
    }
}

try {
    $listeners = Get-NetTCPConnection -State Listen -ErrorAction Stop | Where-Object { $_.LocalPort -eq $port }
    if ($listeners) {
        $pids = $listeners | Select-Object -ExpandProperty OwningProcess -Unique
        Write-Host "LISTENING=SIM PIDs=$([string]::Join(', ', $pids))"
    } else {
        Write-Host "LISTENING=NAO"
    }
} catch {
    Write-Host "LISTENING=DESCONHECIDO"
}
