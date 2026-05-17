param(
    [Parameter(Mandatory = $true)]
    [string]$Versao,

    [Parameter(Mandatory = $true)]
    [string]$Mensagem
)

$ErrorActionPreference = "Stop"

function Stop-ComAviso {
    param([string]$MensagemErro)
    Write-Host "ERRO: $MensagemErro" -ForegroundColor Red
    exit 1
}

function Get-ArquivosProibidos {
    $raiz = (Get-Location).Path
    $itens = Get-ChildItem -LiteralPath $raiz -Force -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch "\\.git(\\|$)" }

    $proibidos = @()

    $proibidos += $itens | Where-Object { $_.Name -eq ".env" }
    $proibidos += $itens | Where-Object { $_.Name -like ".env.*" }
    $proibidos += $itens | Where-Object { $_.PSIsContainer -and $_.Name -eq ".venv" }
    $proibidos += $itens | Where-Object { $_.PSIsContainer -and $_.Name -eq "node_modules" }
    $proibidos += $itens | Where-Object { $_.PSIsContainer -and $_.Name -eq "__pycache__" }
    $proibidos += $itens | Where-Object { $_.PSIsContainer -and $_.Name -eq ".codex" }
    $proibidos += $itens | Where-Object { -not $_.PSIsContainer -and $_.Name -like "*.db" }
    $proibidos += $itens | Where-Object { -not $_.PSIsContainer -and $_.Name -like "*.sqlite" }
    $proibidos += $itens | Where-Object { -not $_.PSIsContainer -and $_.Name -like "*.tmp" }
    $proibidos += $itens | Where-Object { -not $_.PSIsContainer -and $_.Name -like "*.bak" }
    $proibidos += $itens | Where-Object { -not $_.PSIsContainer -and $_.Name -like "*.log" -and $_.Length -gt 5MB }
    $proibidos += $itens | Where-Object { $_.Name -match "(?i)(credential|credentials|secret|secrets|senha|senhas|token|tokens)" }

    return $proibidos | Sort-Object FullName -Unique
}

Set-Location X:\

git status

git pull --rebase

$arquivosProibidos = Get-ArquivosProibidos
if ($arquivosProibidos.Count -gt 0) {
    Write-Host "Arquivos proibidos encontrados. Commit cancelado:" -ForegroundColor Red
    $arquivosProibidos | ForEach-Object { Write-Host $_.FullName }
    Stop-ComAviso "Remova ou exclua corretamente os itens proibidos antes de fechar a versao."
}

$alteracoes = git status --porcelain
if (-not $alteracoes) {
    Write-Host "Nenhuma alteracao real encontrada. Commit vazio nao sera criado." -ForegroundColor Yellow
    git status
    exit 0
}

git add .

git commit -m "$Versao - $Mensagem"

$tagExiste = git tag --list $Versao
if ($tagExiste) {
    Write-Host "Tag $Versao ja existe. Nao sera recriada." -ForegroundColor Yellow
} else {
    git tag $Versao
}

git push

if (-not $tagExiste) {
    git push origin $Versao
}

git status
