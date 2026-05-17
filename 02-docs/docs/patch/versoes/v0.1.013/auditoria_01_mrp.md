# Auditoria 01-mrp - v0.1.013

Data do registro: 2026-05-17
Status: `01_MRP_AUDITADO_E_ALINHADO_COM_ARQUITETURA_ATUAL`

## Snapshot

Snapshot criado antes da alteracao:

`03-vs/snapshots/antes_v0.1.013/01-mrp`

## Estrutura analisada

### `01-mrp`

Itens encontrados:

- `backend`
- `config`
- `database`
- `front_end`
- `logs`
- `runtime`
- `scripts`

### `01-mrp/front_end`

Itens encontrados:

- `login.html`
- `index.html`
- `acesso_negado.html`
- `css`
- `css/pages`
- `data`
- `img`
- `js`
- `js/pages`
- `pages`

## Arquivos principais analisados

### HTML

- `01-mrp/front_end/index.html`
- `01-mrp/front_end/login.html`
- `01-mrp/front_end/acesso_negado.html`
- `01-mrp/front_end/pages/dashboard.html`
- `01-mrp/front_end/pages/produtos_list.html`

### CSS

- `01-mrp/front_end/css/style.css`
- `01-mrp/front_end/css/pages/dashboard.css`
- `01-mrp/front_end/css/pages/produtos_list.css`
- `01-mrp/front_end/css/pages/aparelho.css`
- `01-mrp/front_end/css/pages/estoque.css`
- `01-mrp/front_end/css/pages/processos.css`

### JavaScript

- `01-mrp/front_end/js/auth.js`
- `01-mrp/front_end/js/api.js`
- `01-mrp/front_end/js/security.js`
- `01-mrp/front_end/js/spa.js`
- `01-mrp/front_end/js/utils.js`
- `01-mrp/front_end/js/pages/dashboard.js`
- `01-mrp/front_end/js/pages/produtos_list.js`

### Assets e dados

- `01-mrp/front_end/img/background_jpl.png`
- `01-mrp/front_end/img/logo_jpl.png`
- `01-mrp/front_end/data/mock_data.json`

## Dependencias antigas verificadas

Busca executada para:

- StackAuth.
- Neon.
- dominios externos.
- URLs de API online.
- JWT online obrigatorio.
- referencias fixas a hospedagem antiga.

Resultado: nenhuma ocorrencia ativa encontrada em `01-mrp/front_end` apos os ajustes.

## Valores fixos indevidos verificados

Busca executada para:

- `HOME-MACHINE`.
- `X:\`.
- `100.108.26.10`.
- `100.90.190.4`.
- `localhost`.
- `8000`.

Resultado: nenhuma ocorrencia encontrada em codigo funcional de `01-mrp/front_end` apos os ajustes.

## Problemas encontrados

- HTML principais nao tinham `meta viewport`.
- Configuracoes de autenticacao local e storage estavam dentro de `auth.js` e `api.js`.
- Nomes legados `neonGET` e `neonINSERT` ainda existiam no adaptador local, mesmo sem chamada Neon real.
- `index.html` carregava apenas `dashboard.css`, apesar de existirem CSS de outras paginas.

## Acoes tomadas

- Criado `js/config.js` para configuracao do front-end.
- `auth.js` passou a usar `APP_CONFIG`.
- `api.js` passou a usar `APP_CONFIG`.
- `dashboard.js` passou a importar `localGET`.
- `produtos_list.js` passou a importar `localGET` e `localINSERT`.
- `index.html`, `login.html` e `acesso_negado.html` receberam `meta viewport`.
- `index.html` passou a carregar CSS das paginas da SPA.

## Pendencias

- Backend real ainda nao existe.
- Banco real ainda nao existe.
- Configuracao ainda esta em JS do front-end; quando houver backend/empacotamento, avaliar arquivos `config/ambiente.json` e `config/perfis/*.json`.
- Revisao visual responsiva completa ainda deve seguir em etapa propria.
