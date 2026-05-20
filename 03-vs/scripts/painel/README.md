# Painel Admin Local - MRP_LOCAL (v0.1.049 fix launcher)

Painel administrativo local separado do `index.html` (frontend de usuario final).

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

## Icone do atalho

- local oficial da DLL: `01-mrp/assets/icons/windows/MRP_ICONS.dll`
- indice principal usado no atalho: `MRP_ICONS.dll,0`
- se a DLL nao existir, o script usa icone padrao do Windows sem quebrar.
