$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$desktop = [Environment]::GetFolderPath("Desktop")
$zipPath = Join-Path $desktop "system_jpl.zip"
$stageDir = Join-Path $env:TEMP ("mrp_local_stage_" + [guid]::NewGuid().ToString("N"))

$excludeDirs = @(
    ".git",
    ".codex",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "release",
    "01-mrp\\logs",
    "01-mrp\\config\\local",
    "01-mrp\\runtime\\python"
)

$excludeFiles = @("*.pyc", "*.pyo", "Thumbs.db", "*.log", "*.bak*", "*.tmp", "*.zip")

Write-Host "Repo: $repoRoot"
Write-Host "Destino ZIP: $zipPath"

if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}
New-Item -ItemType Directory -Path $stageDir | Out-Null

try {
    $xd = ($excludeDirs | ForEach-Object { "/XD `"$repoRoot\\$_`"" }) -join " "
    $xf = ($excludeFiles | ForEach-Object { "/XF $_" }) -join " "
    $cmd = "robocopy `"$repoRoot`" `"$stageDir`" /E /NFL /NDL /NJH /NJS /NP $xd $xf"
    cmd /c $cmd | Out-Null

    Compress-Archive -Path (Join-Path $stageDir "*") -DestinationPath $zipPath -CompressionLevel Optimal
    Write-Host "Pacote limpo gerado:"
    Write-Host $zipPath
    exit 0
} catch {
    Write-Host "ERRO ao gerar pacote limpo: $($_.Exception.Message)"
    exit 1
} finally {
    if (Test-Path -LiteralPath $stageDir) {
        Remove-Item -LiteralPath $stageDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
