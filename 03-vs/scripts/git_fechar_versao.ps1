param(
    [Parameter(Mandatory = $true)][string]$Versao,
    [Parameter(Mandatory = $true)][string]$Mensagem,
    [switch]$Auto,
    [switch]$NoPush
)
$ErrorActionPreference = "Stop"

function Stop-ComAviso { param([string]$MensagemErro) Write-Host "ERRO: $MensagemErro" -ForegroundColor Red; exit 1 }
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..\..")).Path
Set-Location $repoRoot

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Stop-ComAviso "Git nao encontrado no PATH." }

& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repoRoot "03-vs\scripts\validar_encoding.ps1") -Modo Ativo
if ($LASTEXITCODE -ne 0) { Stop-ComAviso "Encoding invalido. Commit bloqueado." }

git diff --check
if ($LASTEXITCODE -ne 0) { Stop-ComAviso "git diff --check falhou. Corrija whitespace/encoding antes do commit." }

$versionaveis = @()
$versionaveis += git ls-files -o --exclude-standard
$versionaveis += git diff --name-only
$versionaveis += git diff --cached --name-only
$versionaveis = $versionaveis | Where-Object { $_ } | Sort-Object -Unique
$proibidos = @()
foreach ($a in $versionaveis) {
    $n = $a -replace "\\", "/"
    $base = [System.IO.Path]::GetFileName($n)
    if ($n -match "(^|/)\.codex(/|$)" -or $n -match "(^|/)\.env($|\.)" -or $n -match "(^|/)node_modules(/|$)" -or $n -match "(^|/)__pycache__(/|$)" -or $base -match "(?i)^(Thumbs\.db|desktop\.ini)$" -or $base -match "(?i)\.(log|tmp|bak|backup|pyc|db|sqlite|sqlite3)$" -or $base -match "(?i)(credential|secret|senha|token)") {
        $proibidos += $a
    }
}
if ($proibidos.Count -gt 0) {
    Write-Host "Arquivos proibidos versionaveis encontrados:" -ForegroundColor Red
    $proibidos | ForEach-Object { Write-Host " - $_" }
    Stop-ComAviso "Commit bloqueado."
}

git status --short
if (-not $Auto) {
    Write-Host "Use -Auto para confirmar commit automatico. Nenhuma alteracao foi commitada."
    exit 0
}

git add -A
git commit -m "$Versao - $Mensagem"
if ($LASTEXITCODE -ne 0) { Stop-ComAviso "Falha no git commit." }
git tag $Versao
if ($LASTEXITCODE -ne 0) { Stop-ComAviso "Falha ao criar tag $Versao." }
if (-not $NoPush) {
    git push
    if ($LASTEXITCODE -ne 0) { Stop-ComAviso "Falha no git push." }
    git push origin $Versao
    if ($LASTEXITCODE -ne 0) { Stop-ComAviso "Falha no git push da tag." }
}
Write-Host "Fechamento concluido: $Versao"
