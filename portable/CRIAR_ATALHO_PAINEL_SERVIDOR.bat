@echo off
chcp 65001 >nul
setlocal EnableExtensions

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$root=(Resolve-Path -LiteralPath '%~dp0').Path; $desktop=[Environment]::GetFolderPath('Desktop'); $lnk=Join-Path $desktop 'MRP_LOCAL - Painel do Servidor.lnk'; $target=Join-Path $root 'MRP_PAINEL_SERVIDOR.vbs'; $icon=Join-Path $root 'assets\icons\windows\ico\mrp_mrp_dark.ico'; $w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut($lnk); $s.TargetPath='wscript.exe'; $s.Arguments='""'+$target+'""'; $s.WorkingDirectory=$root; if(Test-Path -LiteralPath $icon){$s.IconLocation=$icon}; $s.Save(); Write-Host '[OK] Atalho criado em: ' + $lnk"
set "RC=%errorlevel%"
if not "%RC%"=="0" (
  echo ERRO: falha ao criar atalho.
)
exit /b %RC%

