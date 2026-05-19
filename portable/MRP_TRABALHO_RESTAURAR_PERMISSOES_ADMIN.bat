@echo off
chcp 65001 >nul
setlocal EnableExtensions
set "ROOT=%~dp0"
set "ROOT=%ROOT:~0,-1%"

echo ========================================================
echo MRP_LOCAL - RESTAURAR PERMISSOES DA PASTA
echo ========================================================
echo Este script deve ser executado como Administrador.
echo Raiz: %ROOT%
echo.
pause

icacls "%ROOT%" /inheritance:e /T /C
icacls "%ROOT%" /grant:r "%USERDOMAIN%\%USERNAME%:(OI)(CI)F" /T /C
attrib -H "%ROOT%\03-vs" 2>nul

echo.
echo PERMISSOES_RESTAURADAS_COM_HERANCA.
echo.
pause
