param(
    [Parameter(Mandatory = $true)]
    [string]$Versao,

    [Parameter(Mandatory = $true)]
    [string]$Mensagem,

    [switch]$Auto
)

$ErrorActionPreference = "Stop"

function Stop-ComAviso {
    param([string]$MensagemErro)
    Write-Host "ERRO: $MensagemErro" -ForegroundColor Red
    exit 1
}

function Get-CaminhosVersionaveis {
    $arquivos = @()
    $arquivos += git ls-files -o --exclude-standard
    $arquivos += git diff --name-only
    $arquivos += git diff --cached --name-only
    return $arquivos | Where-Object { $_ } | Sort-Object -Unique
}

function Test-ArquivoProibido {
    param([string]$Caminho)

    $normalizado = $Caminho -replace "\\", "/"
    $nome = [System.IO.Path]::GetFileName($normalizado)

    if ($normalizado -match "(^|/)\.env($|\.)") { return $true }
    if ($normalizado -match "(^|/)\.venv(/|$)") { return $true }
    if ($normalizado -match "(^|/)node_modules(/|$)") { return $true }
    if ($normalizado -match "(^|/)__pycache__(/|$)") { return $true }
    if ($normalizado -match "(^|/)\.codex(/|$)") { return $true }
    if ($nome -like "*.db") { return $true }
    if ($nome -like "*.sqlite") { return $true }
    if ($nome -like "*.tmp") { return $true }
    if ($nome -like "*.bak") { return $true }
    if ($nome -match "(?i)(credential|credentials|secret|secrets|senha|senhas|token|tokens)") { return $true }

    if ($nome -like "*.log") {
        if (Test-Path -LiteralPath $Caminho) {
            $item = Get-Item -LiteralPath $Caminho -ErrorAction SilentlyContinue
            if ($item -and $item.Length -gt 5MB) { return $true }
        }
    }

    return $false
}

Set-Location X:\

git status

$versionaveis = Get-CaminhosVersionaveis
$proibidos = @($versionaveis | Where-Object { Test-ArquivoProibido $_ })

if ($proibidos.Count -gt 0) {
    Write-Host "Arquivos proibidos versionaveis encontrados. Commit cancelado:" -ForegroundColor Red
    $proibidos | ForEach-Object { Write-Host $_ }
    Stop-ComAviso "Remova, mova ou ignore corretamente os itens proibidos antes de fechar a versao."
}

git add .

$staged = git diff --cached --name-only
if (-not $staged) {
    Write-Host "Nada para commitar" -ForegroundColor Yellow
    git status
    exit 0
}

git commit -m "$Versao - $Mensagem"

git pull --rebase

$tagExiste = git tag --list $Versao
if ($tagExiste) {
    Write-Host "Tag $Versao ja existe. Nao sera recriada." -ForegroundColor Yellow
} else {
    git tag $Versao
}

git push

git push origin $Versao

git status
