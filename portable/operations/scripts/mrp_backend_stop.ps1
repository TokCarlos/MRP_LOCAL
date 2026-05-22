$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
& (Join-Path $root "stop_mrp.bat")
exit $LASTEXITCODE

