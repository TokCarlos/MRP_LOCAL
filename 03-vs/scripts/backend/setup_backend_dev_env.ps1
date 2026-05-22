[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = (Resolve-Path (Join-Path $scriptDir "..\..\..")).Path
$backendDir = Join-Path $projectRoot "01-mrp\back_end"
$runtimeDir = Join-Path $projectRoot "01-mrp\runtime"
$venvDir = Join-Path $runtimeDir "venv_backend"
$requirementsPath = Join-Path $backendDir "requirements.txt"

if (-not (Test-Path -LiteralPath $requirementsPath)) {
    Write-Error "requirements.txt nao encontrado em $requirementsPath"
    exit 1
}

if (-not (Test-Path -LiteralPath $runtimeDir)) {
    New-Item -ItemType Directory -Path $runtimeDir -Force | Out-Null
}

$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
}

if (-not $pythonCmd) {
    Write-Error "Python nao encontrado no PATH."
    exit 1
}

Write-Host "Criando/ajustando venv: $venvDir"
& $pythonCmd -m venv $venvDir
if ($LASTEXITCODE -ne 0) {
    Write-Error "Falha ao criar venv."
    exit 1
}

$venvPython = Join-Path $venvDir "Scripts\python.exe"
if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Error "Python da venv nao encontrado em $venvPython"
    exit 1
}

Write-Host "Atualizando pip..."
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Error "Falha ao atualizar pip."
    exit 1
}

Write-Host "Instalando dependencias de $requirementsPath"
& $venvPython -m pip install -r $requirementsPath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Falha ao instalar dependencias."
    exit 1
}

Write-Host "Instalando suporte de teste FastAPI TestClient (httpx)"
& $venvPython -m pip install httpx
if ($LASTEXITCODE -ne 0) {
    Write-Error "Falha ao instalar httpx."
    exit 1
}

Write-Host "Validando imports: fastapi, pydantic, uvicorn, python_multipart"
& $venvPython -c "import fastapi, pydantic, uvicorn, python_multipart; print('imports_ok')"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Falha ao importar fastapi/pydantic/uvicorn."
    exit 1
}

Write-Host "Ambiente backend DEV pronto."
exit 0
