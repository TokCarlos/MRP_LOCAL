$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$vbsPath = Join-Path $repoRoot "MRP_PAINEL_SERVIDOR.vbs"
$iconsDll = Join-Path $repoRoot "01-mrp\assets\icons\windows\MRP_ICONS.dll"

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
if (Test-Path -LiteralPath $iconsDll) {
    $shortcut.IconLocation = "$iconsDll,0"
    Write-Host "Icone definido pela DLL: $iconsDll,0"
} else {
    $shortcut.IconLocation = "$env:WINDIR\System32\imageres.dll,15"
    Write-Warning "DLL de icones nao encontrada. Usando icone padrao do Windows."
}
$shortcut.Description = "Launcher do Painel Administrativo Local do MRP_LOCAL"
$shortcut.Save()

Write-Host "Atalho criado:"
Write-Host $shortcutPath
exit 0
