[CmdletBinding()]
param(
    [switch]$RunInstall
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Resolve-Path (Join-Path $scriptDir "..\..\..")
$backendDir = Join-Path $projectRoot "01-mrp\back_end"
$venvDir = Join-Path $projectRoot ".venv"
$reqDev = Join-Path $backendDir "requirements.dev.txt"

Write-Host "Projeto: $projectRoot"
Write-Host "Backend: $backendDir"
Write-Host "Venv: $venvDir"
Write-Host "Requirements: $reqDev"

if (-not $RunInstall) {
    Write-Warning "Modo planejamento. Nada sera instalado."
    Write-Host "Para executar, rode novamente com -RunInstall."
    exit 0
}

Write-Warning "Instalacao iniciada sob responsabilidade do operador."

if (Get-Command python -ErrorAction SilentlyContinue) {
    $pyCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pyCmd = "py"
} else {
    Write-Error "Python nao encontrado no PATH."
    exit 1
}

& $pyCmd -m venv $venvDir
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$venvPython = Join-Path $venvDir "Scripts\python.exe"
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $venvPython -m pip install -r $reqDev
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& $venvPython -c "import json, pathlib; print('Imports basicos OK')"
exit $LASTEXITCODE
