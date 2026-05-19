$ErrorActionPreference = "Stop"
$root = if ($env:MRP_LOCAL_ROOT) { $env:MRP_LOCAL_ROOT } else { (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path }
$config = Join-Path $root "01-mrp\config\mrp_local.env.json"
$frontend = Join-Path $root "01-mrp\front_end\index.html"
$ps = $PSVersionTable.PSVersion.ToString()
$pythonCandidates = @("$root\01-mrp\runtime\python\python.exe", $env:MRP_PYTHON_EXE, "py.exe", "python.exe") | Where-Object { $_ }
$pythonOk = $false
foreach ($p in $pythonCandidates) {
    if ($p -match "[\\/]") { if (Test-Path -LiteralPath $p) { $pythonOk = $true; break } }
    else { if (Get-Command $p -ErrorAction SilentlyContinue) { $pythonOk = $true; break } }
}
Write-Host "MRP_LOCAL_PRECHECK"
Write-Host "ROOT=$root"
Write-Host "POWERSHELL=$ps"
Write-Host "CONFIG_OK=$((Test-Path -LiteralPath $config))"
Write-Host "FRONTEND_OK=$((Test-Path -LiteralPath $frontend))"
Write-Host "PYTHON_OK=$pythonOk"
if (-not (Test-Path -LiteralPath $config)) { exit 1 }
if (-not (Test-Path -LiteralPath $frontend)) { exit 1 }
if (-not $pythonOk) { exit 2 }
exit 0
