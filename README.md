# MRP_LOCAL

Sistema local-first para PCP/MRP em desenvolvimento controlado.

## Leitura obrigatoria

Antes de alterar o projeto, ler:

1. `02-docs/REGRAS_ATUAIS_MRP.txt`
2. `02-docs/LOG_PROGRESSO_MRP.txt`
3. `COMO_CRIAR_COMANDOS_CODEX.txt`, quando for criar comando para Codex/revisao.

## Estado atual

- Frontend oficial atual: `01-mrp/front_end`.
- Backend oficial atual: `01-mrp/back_end`.
- Frontend roda na porta `8765`.
- Backend FastAPI roda na porta `8876`.
- Produtos e o primeiro modulo backend real.
- Produtos usa SQLite DEV quando o banco runtime e criado em `01-mrp/data/db/mrp_local_dev.sqlite`.
- Endpoints minimos validados em DEV: `/health`, `/api/status`, `/api/produtos`, `/api/produtos/bases`.
- Upload de imagem de usuario em Produtos usa `01-mrp/data/media/produtos` e URL publica `/media/produtos/...`.
- Imagens oficiais/seed continuam em `01-mrp/front_end/img/produtos`.
- Portable esta pausado para evolucao; nao e o foco atual.
- Sistema ainda nao esta homologado/blindado.

## Regras criticas

- Nunca tocar na pasta `C:\Users\carlo\Desktop\PCP SERVIDOR\PCP`.
- Nao usar raiz direta em `C:\` como raiz do MRP_LOCAL.
- Nao fazer commit/push sem ordem explicita.
- Alterar `01-mrp` ou `.git` exige chave `LIBERADO`.
- `.git` nao deve ser alterado internamente.
- Nao versionar runtime, logs reais, cache, venv, banco SQLite runtime ou credenciais.

## Estrutura principal

```text
01-mrp/     sistema funcional
02-docs/    documentacao, regras, progresso e historico
03-vs/      scripts, relatorios, patches e pacotes
portable/   pacote/apoio operacional separado
```

## Estrutura ativa atual

```text
01-mrp/front_end          frontend ativo
01-mrp/back_end           backend ativo
01-mrp/data/media         uploads de usuario/runtime
01-mrp/data/db            banco SQLite runtime DEV
01-mrp/runtime            venv/runtime local ignorado pelo Git
01-mrp/logs               logs locais ignorados pelo Git
```

A estrutura `01-mrp/app`, `core`, `infrastructure` e `operations` existe como estrutura-alvo parcial, mas `front_end` e `back_end` continuam ativos nesta fase.

## Operacao DEV

Backend:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_backend_start.ps1
```

Frontend:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_start.ps1
```

Painel local:

```text
MRP_PAINEL_SERVIDOR.vbs
```

## Proximas frentes

1. Consolidar documentos atuais e remover divergencias restantes em lotes controlados.
2. Validar manualmente CRUD Produtos/BOM/Upload no navegador.
3. Preparar commit seletivo da etapa atual.
4. Depois, evoluir backend Produtos com paginacao, filtros no backend e persistencia mais robusta.
