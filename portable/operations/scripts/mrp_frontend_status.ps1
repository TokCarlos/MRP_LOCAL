$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
& (Join-Path $root "status_mrp.bat")
exit $LASTEXITCODE

