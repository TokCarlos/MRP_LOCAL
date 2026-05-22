$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
& (Join-Path $root "healthcheck_mrp.bat")
exit $LASTEXITCODE

