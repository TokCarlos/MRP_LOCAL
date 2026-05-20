$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$vbsPath = Join-Path $repoRoot "MRP_PAINEL_SERVIDOR.vbs"
$iconPrimary = Join-Path $repoRoot "01-mrp\assets\icons\windows\ico\mrp_mrp_dark.ico"
$iconFallback = Join-Path $repoRoot "01-mrp\assets\icons\windows\ico\mrp_pcp_light.ico"
$wscriptExe = Join-Path $env:WINDIR "System32\wscript.exe"
$localIconDir = Join-Path $env:LOCALAPPDATA "MRP_LOCAL\icons"
$localIconPath = Join-Path $localIconDir "mrp_painel_servidor.ico"

if (!(Test-Path -LiteralPath $vbsPath)) {
    Write-Host "ERRO: launcher VBS nao encontrado: $vbsPath"
    exit 1
}

if (!(Test-Path -LiteralPath $wscriptExe)) {
    Write-Host "ERRO: wscript.exe nao encontrado: $wscriptExe"
    exit 1
}

$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "MRP_LOCAL - Painel do Servidor.lnk"
$shortcutPathNovo = Join-Path $desktop "MRP_LOCAL - Painel do Servidor NOVO.lnk"

New-Item -ItemType Directory -Force -Path $localIconDir | Out-Null

$iconSource = $null
if (Test-Path -LiteralPath $iconPrimary) {
    $iconSource = $iconPrimary
} elseif (Test-Path -LiteralPath $iconFallback) {
    $iconSource = $iconFallback
    Write-Warning "Icone principal ausente. Usando fallback: $iconFallback"
}

if ($iconSource) {
    Copy-Item -LiteralPath $iconSource -Destination $localIconPath -Force
    Write-Host "Icone local atualizado: $localIconPath"
}

if (Test-Path -LiteralPath $shortcutPath) { Remove-Item -LiteralPath $shortcutPath -Force }
if (Test-Path -LiteralPath $shortcutPathNovo) { Remove-Item -LiteralPath $shortcutPathNovo -Force }

$shell = New-Object -ComObject WScript.Shell
foreach ($lnk in @($shortcutPath, $shortcutPathNovo)) {
    $shortcut = $shell.CreateShortcut($lnk)
    $shortcut.TargetPath = $wscriptExe
    $shortcut.Arguments = "`"$vbsPath`""
    $shortcut.WorkingDirectory = $repoRoot
    if (Test-Path -LiteralPath $localIconPath) {
        $shortcut.IconLocation = "$localIconPath,0"
    } else {
        $shortcut.IconLocation = "$env:WINDIR\System32\imageres.dll,15"
        Write-Warning "Icones oficiais nao encontrados. Usando icone padrao do Windows."
    }
    $shortcut.Description = "Launcher do Painel Administrativo Local do MRP_LOCAL"
    $shortcut.Save()
    Write-Host "Atalho criado/recriado:"
    Write-Host $lnk
}
exit 0
