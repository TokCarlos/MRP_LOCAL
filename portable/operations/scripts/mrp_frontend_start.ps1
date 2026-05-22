$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
& (Join-Path $root "start_mrp.bat")
exit $LASTEXITCODE

