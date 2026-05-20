$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$vbsPath = Join-Path $repoRoot "MRP_PAINEL_SERVIDOR.vbs"
$iconPrimary = Join-Path $repoRoot "01-mrp\assets\icons\windows\ico\mrp_mrp_dark.ico"
$iconFallback = Join-Path $repoRoot "01-mrp\assets\icons\windows\ico\mrp_pcp_light.ico"

if (!(Test-Path -LiteralPath $vbsPath)) {
    Write-Host "ERRO: launcher VBS nao encontrado: $vbsPath"
    exit 1
}

$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "MRP_LOCAL - Painel do Servidor.lnk"

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $vbsPath
$shortcut.WorkingDirectory = $repoRoot
if (Test-Path -LiteralPath $iconPrimary) {
    $shortcut.IconLocation = $iconPrimary
    Write-Host "Icone definido: $iconPrimary"
} elseif (Test-Path -LiteralPath $iconFallback) {
    $shortcut.IconLocation = $iconFallback
    Write-Warning "Icone principal ausente. Usando fallback: $iconFallback"
} else {
    $shortcut.IconLocation = "$env:WINDIR\System32\imageres.dll,15"
    Write-Warning "Icones oficiais nao encontrados. Usando icone padrao do Windows."
}
$shortcut.Description = "Launcher do Painel Administrativo Local do MRP_LOCAL"
$shortcut.Save()

Write-Host "Atalho criado:"
Write-Host $shortcutPath
exit 0
