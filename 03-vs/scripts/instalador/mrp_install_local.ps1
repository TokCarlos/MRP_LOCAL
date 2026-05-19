param(
    [string]$InstallRoot = "$env:ProgramData\MRP_LOCAL",
    [switch]$InstallTask,
    [switch]$OpenFirewall
)
$ErrorActionPreference = "Stop"

# Instalador local inicial. Ainda nao copia runtime portable; prepara a pasta e aciona scripts existentes.
# Regra: instalador prepara ambiente; regra de negocio continua desacoplada.
$sourceRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
if (-not (Test-Path -LiteralPath $InstallRoot)) { New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null }
robocopy $sourceRoot $InstallRoot /E /XD .git .codex /XF Thumbs.db desktop.ini *.log | Out-Null
$env:MRP_LOCAL_ROOT = $InstallRoot
& "$InstallRoot\03-vs\scripts\instalador\mrp_precheck_instalacao.ps1"
if ($OpenFirewall) { & "$InstallRoot\03-vs\scripts\servicos\mrp_firewall_8765.ps1" }
if ($InstallTask) { & "$InstallRoot\03-vs\scripts\servicos\mrp_frontend_task_install.ps1" }
Write-Host "Instalacao local preparada em: $InstallRoot"
