# Triagem mrp-main - v0.1.005

Data do registro: 2026-05-17
Status: `REFATORACAO_FRONTEND_LOCAL_BASE`

## Escopo

Triagem e refatoracao inicial do antigo `mrp-main` para base local do `MRP_LOCAL`.

## Origem

- Zip original: `03-vs/entrada_original/mrp-main.zip`.
- Extracao realizada em: `03-vs/patches/v0.1.005/origem_extraida`.

## Destino de trabalho

- Base local criada em: `03-vs/patches/v0.1.005/mrp_local_frontend_base`.
- Front-end copiado para: `03-vs/patches/v0.1.005/mrp_local_frontend_base/front_end`.

## Estrutura aproveitada

Foram preservados:

- HTML.
- CSS.
- JavaScript da SPA.
- Imagens.
- Paginas em `front_end/pages`.
- Layout visual existente.

## Dependencias online removidas

- StackAuth removido de `front_end/js/auth.js`.
- Neon REST removido de `front_end/js/api.js`.
- URL externa Neon removida de `front_end/js/api.js`.
- Chamada externa StackAuth removida de `front_end/js/auth.js`.
- Token JWT online obrigatorio removido do fluxo de seguranca.
- Validacao JWT por `atob(token.split(".")[1])` removida de `front_end/js/security.js`.
- Helper generico de API online em `front_end/js/utils.js` foi desativado para esta etapa.

## Refatoracao aplicada

### `front_end/js/auth.js`

- Criada autenticacao local temporaria.
- Usuario temporario: `admin`.
- Senha temporaria: `admin`.
- Sessao salva em `localStorage`.
- Logout remove sessao local e retorna para `login.html`.
- Funcoes de JWT removidas do fluxo local temporario.

### `front_end/js/api.js`

- Neon REST substituido por adaptador local temporario.
- Dados mockados carregados a partir de seed interno.
- Dados persistidos temporariamente em `localStorage`.
- Funcoes legadas `neonGET` e `neonINSERT` mantidas para evitar refatoracao ampla das paginas nesta etapa.
- Criadas aliases `localGET` e `localINSERT` para uso futuro.

### `front_end/js/security.js`

- Validacao de JWT removida.
- Acesso passa a depender apenas de sessao local temporaria.

### `front_end/login.html`

- Campo de login alterado para usuario local.
- Validacao ajustada para retorno local `ok`.

### `front_end/data/mock_data.json`

- Criado arquivo de referencia com dados mockados.
- O adaptador local usa seed interno para evitar dependencia de fetch externo.

## Como testar

1. Abrir terminal em `03-vs/patches/v0.1.005/mrp_local_frontend_base/front_end`.
2. Rodar `python -m http.server 8080`.
3. Acessar `http://localhost:8080/login.html`.
4. Usar `admin` / `admin`.
5. Conferir dashboard, produtos e logout.

## Validacao executada

- Busca textual em `front_end` sem ocorrencias de StackAuth, Neon, URLs externas, `Authorization`, `Bearer`, `token.split`, `access_token` ou `JWT`.
- Checagem sintatica com Node aprovada para `js/auth.js`, `js/api.js`, `js/security.js` e `js/spa.js`.
- Servidor estatico temporario retornou HTTP 200 para `login.html` e `index.html`.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Codigo funcional promovido para `01-mrp`: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Frontend criado em `01-mrp`: NAO.
- Arquivos originais apagados: NAO.
- Dependencias instaladas: NAO.

## Observacoes tecnicas

Esta base ainda e temporaria. O objetivo e permitir avaliacao local do visual, SPA e fluxo de navegacao sem depender de StackAuth, Neon REST ou JWT online. O backend e o banco locais devem ser definidos em etapa futura antes de qualquer promocao formal para `01-mrp`.
