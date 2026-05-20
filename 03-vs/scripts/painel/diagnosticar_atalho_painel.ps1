$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $scriptDir "..\..\.."))
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "MRP_LOCAL - Painel do Servidor.lnk"
$vbsPath = Join-Path $repoRoot "MRP_PAINEL_SERVIDOR.vbs"
$expectedWscript = (Join-Path $env:WINDIR "System32\wscript.exe")

if (!(Test-Path -LiteralPath $shortcutPath)) {
    Write-Host "ERRO: atalho nao encontrado: $shortcutPath"
    exit 1
}

$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut($shortcutPath)

$iconFile = $sc.IconLocation
if ($iconFile -match "^(.*),\d+$") { $iconFile = $Matches[1] }

Write-Host "ShortcutPath: $shortcutPath"
Write-Host "TargetPath: $($sc.TargetPath)"
Write-Host "Arguments: $($sc.Arguments)"
Write-Host "WorkingDirectory: $($sc.WorkingDirectory)"
Write-Host "IconLocation: $($sc.IconLocation)"
Write-Host "IconFileExists: $([bool](Test-Path -LiteralPath $iconFile))"
Write-Host "IconInLocalAppData: $($iconFile.StartsWith($env:LOCALAPPDATA, [System.StringComparison]::OrdinalIgnoreCase))"
Write-Host "TargetIsWscript: $($sc.TargetPath -ieq $expectedWscript)"

$argTrim = $sc.Arguments.Trim('"')
Write-Host "ArgumentPointsToVbs: $($argTrim -ieq $vbsPath)"

exit 0
