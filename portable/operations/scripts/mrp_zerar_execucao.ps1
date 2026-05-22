$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$tmp = Join-Path $root "tmp"
$logs = Join-Path $root "logs"
if (Test-Path -LiteralPath $tmp) {
    Get-ChildItem -LiteralPath $tmp -Force -File | Remove-Item -Force -ErrorAction SilentlyContinue
}
Write-Host "[OK] Limpeza de execucao concluida em $tmp"
Write-Host "[INFO] Logs preservados em $logs"
exit 0

