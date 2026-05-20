$ErrorActionPreference = "Stop"

Write-Warning "Este script e manual/diagnostico. Use somente se o Windows mantiver icone antigo/branco."
Write-Host "Acao: encerrar/reiniciar Explorer e limpar cache local de icones."
$confirm = Read-Host "Confirmar execucao? (S/N)"
if ($confirm -notin @("S", "s")) {
    Write-Host "Operacao cancelada."
    exit 0
}

try {
    Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1

    $cacheDb = Join-Path $env:LOCALAPPDATA "IconCache.db"
    if (Test-Path -LiteralPath $cacheDb) {
        Remove-Item -LiteralPath $cacheDb -Force -ErrorAction SilentlyContinue
    }

    $explorerCache = Join-Path $env:LOCALAPPDATA "Microsoft\Windows\Explorer"
    if (Test-Path -LiteralPath $explorerCache) {
        Get-ChildItem -Path $explorerCache -Filter "iconcache*" -ErrorAction SilentlyContinue |
            Remove-Item -Force -ErrorAction SilentlyContinue
    }

    Start-Process explorer.exe
    Write-Host "Cache de icones atualizado. Se necessario, aguarde alguns segundos e atualize a area de trabalho."
    exit 0
} catch {
    Write-Host "ERRO ao reparar cache de icones: $($_.Exception.Message)"
    exit 1
}
