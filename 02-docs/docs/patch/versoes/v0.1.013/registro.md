# Registro v0.1.013 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `01_MRP_AUDITADO_E_ALINHADO_COM_ARQUITETURA_ATUAL`

## Objetivo

Auditar e alinhar excepcionalmente o `01-mrp` com a arquitetura atual do projeto, preservando o sistema principal executavel e aplicando apenas ajustes controlados.

## Autorizacao excepcional

Nesta etapa foi autorizada revisao e ajuste direto em `01-mrp`.

## Snapshot criado antes da alteracao

Snapshot criado em:

`03-vs/snapshots/antes_v0.1.013/01-mrp`

O snapshot foi criado antes de qualquer alteracao em `01-mrp`.

## Documentos lidos antes da alteracao

- `AGENTS.md`.
- `02-docs/docs/geral/arquitetura.md`.
- `02-docs/docs/geral/regras_do_projeto.md`.
- `02-docs/docs/geral/ambientes.md`.
- `02-docs/docs/geral/acesso_local_e_tailscale.md`.
- `02-docs/docs/geral/configuracao_e_desacoplamento.md`.

## Resumo da auditoria

- Estrutura `01-mrp` auditada.
- Estrutura `01-mrp/front_end` auditada.
- `login.html` encontrado.
- `index.html` encontrado.
- `css` encontrado.
- `js` encontrado.
- `img` encontrado.
- `data` encontrado.
- `pages` encontrado.

## Ajustes realizados

- Criado `01-mrp/front_end/js/config.js` para centralizar configuracoes do front-end.
- `auth.js` passou a ler usuario, senha, modo de autenticacao e chave de sessao a partir de `config.js`.
- `api.js` passou a ler chave de storage mockada a partir de `config.js`.
- Removidos nomes funcionais legados `neonGET` e `neonINSERT`; telas passaram a usar `localGET` e `localINSERT`.
- Adicionado `meta viewport` em `index.html`, `login.html` e `acesso_negado.html`.
- `index.html` passou a carregar CSS das paginas existentes da SPA.

## Dependencias online encontradas

Nenhuma dependencia online ativa foi encontrada em `01-mrp/front_end` apos auditoria.

A busca nao encontrou:

- StackAuth.
- Neon.
- URLs externas de API.
- JWT online obrigatorio.
- Header `Authorization: Bearer`.
- Referencias funcionais a hospedagem antiga.

## Valores fixos encontrados

Nao foram encontrados valores fixos indevidos em codigo funcional para:

- `HOME-MACHINE`.
- `X:\`.
- `100.108.26.10`.
- `100.90.190.4`.
- `localhost`.
- porta `8000`.

## Valores fixos mantidos apenas como documentacao/teste

- Comando oficial de teste: `py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"`.
- URL validada: `http://100.108.26.10:8000/login.html`.

Esses valores foram mantidos como registro de teste e nao como regra central do codigo.

## Valores substituidos por configuracao

Movidos para `01-mrp/front_end/js/config.js`:

- Ambiente atual: `TESTE_HOME`.
- Modo de autenticacao temporario: `LOCAL_TEMPORARIO`.
- Modo de dados: `MOCK_LOCAL`.
- Chave de sessao local.
- Chave de storage mockado.
- Usuario temporario `admin`.
- Senha temporaria `admin`.
- Flag de API mockada.
- Flag de debug.

## Validacao

- `node --check` aprovado para `js/config.js`.
- `node --check` aprovado para `js/auth.js`.
- `node --check` aprovado para `js/api.js`.
- `node --check` aprovado para `js/spa.js`.
- `node --check` aprovado para `js/pages/dashboard.js`.
- `node --check` aprovado para `js/pages/produtos_list.js`.
- `login.html` respondeu HTTP 200 em teste temporario local.
- `index.html` respondeu HTTP 200 em teste temporario local.
- `js/config.js` respondeu HTTP 200 em teste temporario local.
- URL oficial `http://100.108.26.10:8000/login.html` respondeu HTTP 200.

## Conformidade

O `01-mrp/front_end` ficou alinhado com a regra atual de `configuracao / motor / adaptador` no escopo do front-end atual.

## Controle de escopo

- Backend criado: NAO.
- Banco criado: NAO.
- Dependencias instaladas: NAO.
- Framework trocado: NAO.
- Layout reescrito: NAO.
- Arquivos apagados: NAO.
