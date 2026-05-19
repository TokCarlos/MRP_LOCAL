$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$vbsPath = Join-Path $repoRoot "MRP_PAINEL_SERVIDOR.vbs"

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
$shortcut.IconLocation = "$env:WINDIR\System32\imageres.dll,15"
$shortcut.Description = "Launcher do Painel Administrativo Local do MRP_LOCAL"
$shortcut.Save()

Write-Host "Atalho criado:"
Write-Host $shortcutPath
exit 0

