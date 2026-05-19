$ErrorActionPreference = "Stop"
Write-Host "MRP_LOCAL PRECHECK INSTALACAO"
Write-Host "PowerShell=$($PSVersionTable.PSVersion)"
try { Get-Command python.exe -ErrorAction Stop | Out-Null; Write-Host "python.exe=OK" } catch { Write-Host "python.exe=NAO_ENCONTRADO" }
try { Get-Command py.exe -ErrorAction Stop | Out-Null; Write-Host "py.exe=OK" } catch { Write-Host "py.exe=NAO_ENCONTRADO" }
Write-Host "Precheck informativo. Instalador definitivo ainda e etapa futura."
