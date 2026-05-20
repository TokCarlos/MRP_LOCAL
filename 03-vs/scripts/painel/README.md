# Painel Admin Local - MRP_LOCAL (v0.1.049 fix launcher)

Painel administrativo local separado do `index.html` (frontend de usuario final).

Conceito operacional:

- `MRP_PAINEL_SERVIDOR.vbs` e launcher interno.
- o item visual oficial para o usuario e o atalho `.lnk` na Area de Trabalho.
- o icone personalizado deve ficar no `.lnk`, nao no `.vbs`.

## Objetivo

- controlar a operacao local do servidor: start, stop, restart, status, healthcheck;
- preparar base de modo automatico futuro sem ativar watchdog/tarefa nesta etapa.

## Arquivos

- `mrp_painel_controle.py`: painel tkinter local do servidor.
- `mrp_admin_auth_setup.py`: setup de credencial admin local com PBKDF2-HMAC-SHA256.
- `criar_atalho_painel.ps1`: cria atalho na area de trabalho.

Launchers na raiz:

- `MRP_PAINEL_SERVIDOR.vbs` (principal, duplo clique)
- `MRP_PAINEL_SERVIDOR.cmd` (diagnostico com log)
- `CRIAR_ATALHO_PAINEL_SERVIDOR.bat` (opcional para criar atalho)

## Credencial admin local

Arquivo real local (nao versionado):

- `01-mrp/config/local/admin_auth.local.json`

Geracao:

```powershell
python 03-vs/scripts/painel/mrp_admin_auth_setup.py
```

Exemplo versionado:

- `01-mrp/config/admin_auth.example.json`

## Chave de modo automatico local

Arquivo real local (nao versionado):

- `01-mrp/config/local/mrp_auto_mode.local.json`

Exemplo versionado:

- `01-mrp/config/mrp_auto_mode.example.json`

## Integracao com scripts existentes

- Start: `03-vs/scripts/servicos/mrp_frontend_start.ps1`
- Stop: `03-vs/scripts/servicos/mrp_frontend_stop.ps1`
- Status: `03-vs/scripts/servicos/mrp_frontend_status.ps1`
- Healthcheck: `03-vs/scripts/servicos/mrp_frontend_healthcheck.ps1`
- Zerar execucao: `03-vs/scripts/servicos/mrp_zerar_execucao.ps1`

## Regras da etapa

- sem backend novo;
- sem banco novo;
- sem dependencias externas;
- sem expor painel administrativo pelo navegador;
- sem senha em texto puro no Git;
- sem log administrativo real no Git.

## Como abrir por duplo clique

1. Clique em `MRP_PAINEL_SERVIDOR.vbs`.
2. Se Python estiver disponivel (`python` ou `py`), o painel abre.
3. Em caso de erro, verifique `01-mrp/logs/admin/launcher_painel.log`.

## Como criar atalho na area de trabalho

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\painel\criar_atalho_painel.ps1
```

Ou por duplo clique em `CRIAR_ATALHO_PAINEL_SERVIDOR.bat`.

O script cria somente um atalho oficial:

- `MRP_LOCAL - Painel do Servidor.lnk`

O atalho legado `MRP_LOCAL - Painel do Servidor NOVO.lnk`, se existir, e removido automaticamente.

Modelo tecnico do atalho:

- `TargetPath` = `wscript.exe`
- `Arguments` = caminho absoluto do `MRP_PAINEL_SERVIDOR.vbs`
- `IconLocation` = `%LOCALAPPDATA%\MRP_LOCAL\icons\mrp_painel_servidor.ico,0`

Diagnostico:

- use `03-vs/scripts/painel/diagnosticar_atalho_painel.ps1` para validar TargetPath/Arguments/WorkingDirectory/IconLocation.

## Icone do atalho

- padrao atual: `.ico` direto em `01-mrp/assets/icons/windows/ico/mrp_mrp_dark.ico`
- fallback: `01-mrp/assets/icons/windows/ico/mrp_pcp_light.ico`
- se ambos nao existirem, o script usa icone padrao do Windows sem quebrar.
- DLL de icones permanece opcional/futura e nao e padrao de atalho nesta fase.
