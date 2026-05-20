$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$pyScript = Join-Path $repoRoot "03-vs\scripts\icons\gerar_icones_oficiais.py"
$sourceDir = Join-Path $repoRoot "01-mrp\assets\icons\source"

if (!(Test-Path -LiteralPath $pyScript)) {
    Write-Host "ERRO: script Python nao encontrado: $pyScript"
    exit 1
}

$required = @(
    "mrp_pcp_light.png",
    "mrp_jpl_dark.png",
    "mrp_mrp_light.png",
    "mrp_mrp_dark.png"
)

foreach ($file in $required) {
    $full = Join-Path $sourceDir $file
    if (!(Test-Path -LiteralPath $full)) {
        Write-Host "ERRO: imagem fonte ausente: $full"
        exit 1
    }
}

if (Get-Command python -ErrorAction SilentlyContinue) {
    $py = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $py = "py"
} else {
    Write-Host "ERRO: Python nao encontrado no PATH."
    exit 1
}

& $py $pyScript
$rc = $LASTEXITCODE
if ($rc -ne 0) {
    Write-Host "ERRO: falha na geracao dos icones oficiais. Codigo: $rc"
    exit $rc
}

Write-Host "Geracao dos icones oficiais concluida."
exit 0
