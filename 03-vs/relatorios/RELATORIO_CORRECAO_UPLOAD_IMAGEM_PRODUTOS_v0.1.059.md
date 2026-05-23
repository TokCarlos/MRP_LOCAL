# RELATORIO - Correcao upload imagem Produtos v0.1.059

## Problema

O upload de imagem estava gravando arquivo, mas a imagem nao era trocada na tela. A causa foi divergencia de raiz:

- destino anterior: `assets/images/produtos`;
- resolucao DEV anterior: `01-mrp/app/frontend/assets`;
- frontend ativo real: `01-mrp/front_end`;
- banco guardava caminho relativo que nao era servido de forma estavel.

## Correcao

- Upload real agora salva em `01-mrp/data/media/produtos`.
- Banco salva `media/produtos/{arquivo}`.
- Backend serve midia runtime em `/media`.
- Frontend resolve `media/...` usando a origem do backend na porta `8876`.
- Imagens oficiais do seed continuam em `01-mrp/front_end/img/produtos`.

## Regra definida

Dados estruturados:

`01-mrp/data/db`

Seeds:

`01-mrp/data/seed`

Midia runtime enviada pelo usuario:

`01-mrp/data/media/produtos`

Imagens oficiais do catalogo:

`01-mrp/front_end/img/produtos`

## Estado local corrigido

O produto ID 110 foi migrado de:

`assets/images/produtos/aco_cimasp_029_2025_item_057.png`

para:

`media/produtos/aco_cimasp_029_2025_item_057.png`

O arquivo fisico foi copiado para `01-mrp/data/media/produtos`.

## Validacao

- Backend real reiniciado na porta `8876` com versao `v0.1.059`.
- `/api/status` confirmou backend ativo em `01-mrp/back_end`.
- `/media/produtos/aco_cimasp_029_2025_item_057.png` respondeu HTTP 200.
- `mrp_backend_status.ps1` retornou `STATUS_BACKEND=OK`.
- `mrp_backend_healthcheck.ps1` retornou `HEALTHCHECK_BACKEND=OK`.

## Pendencias

- Validacao manual final no navegador pelo usuario.
- Definir politica de limpeza de midia antiga quando houver substituicao por outra extensao.
- Criar teste automatizado de upload com banco temporario em etapa posterior.
