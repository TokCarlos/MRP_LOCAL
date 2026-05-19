@echo off
chcp 65001 >nul
setlocal EnableExtensions
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"

echo ========================================================
echo MRP_LOCAL - PROTEGER PASTA DO TESTE
echo ========================================================
echo Este script deve ser executado como Administrador.
echo Raiz: %ROOT%
echo.
echo AVISO: isto nao impede copia por Administrador/IT, mas remove acesso amplo.
echo.
pause

icacls "%ROOT%" /inheritance:r /T /C
icacls "%ROOT%" /grant:r "%USERDOMAIN%\%USERNAME%:(OI)(CI)F" /T /C
icacls "%ROOT%" /grant:r *S-1-5-32-544:(OI)(CI)F /T /C
icacls "%ROOT%" /grant:r *S-1-5-18:(OI)(CI)F /T /C
icacls "%ROOT%" /remove:g *S-1-1-0 *S-1-5-11 *S-1-5-32-545 /T /C
attrib +H "%ROOT%\00-manual-dev" 2>nul
attrib +H "%ROOT%\02-docs" 2>nul
attrib +H "%ROOT%\03-vs" 2>nul

echo.
echo PROTECAO_APLICADA.
echo Valide o sistema com MRP_TRABALHO_PRECHECK.bat e MRP_MENU_SISTEMA.bat.
echo.
pause
