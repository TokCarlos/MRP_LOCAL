# Triagem mrp-main - v0.1.007

Data do registro: 2026-05-17
Status: `REFATORACAO_FRONTEND_LOCAL_BASE`

## Escopo

Triagem e refatoracao inicial do antigo `mrp-main` para base local temporaria do `MRP_LOCAL`.

## Origem

- Zip original: `03-vs/entrada_original/mrp-main.zip`.
- Extracao: `03-vs/patches/v0.1.007/origem_extraida`.

## Destino de trabalho

- Base local: `03-vs/patches/v0.1.007/mrp_local_frontend_base`.
- Front-end: `03-vs/patches/v0.1.007/mrp_local_frontend_base/front_end`.

## Estrutura identificada no projeto antigo

- Raiz extraida: `mrp-main`.
- Arquivos de apoio: `.gitignore`, `deploy_plus.bat`, `estrutura_mrp.txt`.
- Front-end aproveitavel: `front_end`.
- HTML principal: `front_end/index.html`, `front_end/login.html`, `front_end/acesso_negado.html`.
- CSS: `front_end/css` e `front_end/css/pages`.
- JavaScript: `front_end/js`, `front_end/js/pages`.
- Paginas SPA: `front_end/pages`.
- Imagens: `front_end/img`.

## Assets aproveitados

Foram preservados na base de trabalho:

- HTML das telas.
- CSS e estilos por pagina.
- JavaScript da SPA e paginas.
- Imagens `background_jpl.png` e `logo_jpl.png`.
- Estrutura de navegacao existente.
- Layout visual existente, com alteracao apenas na logica necessaria para modo local.

## Dependencias online encontradas

- StackAuth em `front_end/js/auth.js`.
- `STACK_PROJECT_ID` no arquivo original.
- `STACK_PUBLIC_KEY` no arquivo original.
- Endpoint `https://api.stack-auth.com/api/v1` no arquivo original.
- Neon REST em `front_end/js/api.js`.
- Endpoint Neon REST externo em `front_end/js/api.js`.
- Header `Authorization: Bearer` no arquivo original.
- Token JWT obrigatorio e `stack_jwt` em `front_end/js/auth.js`.
- Validacao JWT por `token.split` em `front_end/js/security.js`.
- Helper generico de API online em `front_end/js/utils.js`.
- Dependencia pratica de hospedagem/servidor web remoto substituida por servidor estatico local.

## Dependencias removidas ou substituidas

### `front_end/js/auth.js`

- StackAuth removido.
- Chaves/identificadores Stack removidos da base de trabalho.
- JWT online removido.
- Login local temporario criado.
- Usuario temporario: `admin`.
- Senha temporaria: `admin`.
- Sessao salva em `localStorage`.
- Logout remove sessao local e retorna para `login.html`.

### `front_end/js/api.js`

- Neon REST removido.
- URL externa Neon removida.
- Headers `Authorization` e `Bearer` removidos.
- Adaptador local temporario criado com dados mockados.
- Dados persistidos temporariamente em `localStorage`.
- Nomes legados `neonGET` e `neonINSERT` mantidos para preservar as telas existentes nesta etapa.
- Aliases `localGET` e `localINSERT` criados para uso futuro.

### `front_end/js/security.js`

- Validacao JWT removida.
- Acesso passa a depender apenas de sessao local temporaria.

### `front_end/login.html`

- Campo de login ajustado para usuario local.
- Validacao alterada para retorno local `ok`.

### `front_end/js/utils.js`

- Helper de API online desativado nesta etapa.
- Funcao passa a retornar `null` com aviso no console.

### `front_end/data/mock_data.json`

- Criado arquivo de referencia com dados mockados.
- O adaptador `js/api.js` usa seed interno para nao depender de `fetch` externo.

## Arquivos sensiveis ou pontos de atencao

- O original continha `STACK_PROJECT_ID` e `STACK_PUBLIC_KEY` em `front_end/js/auth.js`.
- O original continha endpoint Neon REST externo em `front_end/js/api.js`.
- Esses valores nao foram mantidos na base refatorada.
- Nao foram identificados `.env`, bancos reais ou credenciais privadas em arquivos copiados para a base de trabalho.

## Validacao executada

- Busca textual em `front_end` sem ocorrencias de StackAuth, Stack keys, Neon, endpoints externos, `Authorization`, `Bearer`, `token.split`, `access_token`, `JWT` ou `jwt`.
- Checagem sintatica com Node aprovada para `js/auth.js`, `js/api.js`, `js/security.js` e `js/spa.js`.
- Servidor estatico temporario retornou HTTP 200 para `login.html` e `index.html`.
- Servidor temporario foi encerrado apos a validacao.

## Como testar

1. Abrir terminal em `03-vs/patches/v0.1.007/mrp_local_frontend_base/front_end`.
2. Rodar `python -m http.server 8080`.
3. Acessar `http://localhost:8080/login.html`.
4. Usar `admin` / `admin`.
5. Conferir dashboard, produtos e logout.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Codigo promovido para `01-mrp`: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Dependencias instaladas: NAO.
- Arquivos originais apagados: NAO.
- Sistema funcional implementado em `01-mrp`: NAO.

## Status para promocao futura

Nao esta pronto para promocao imediata ao `01-mrp`.

A base esta pronta para avaliacao local em `03-vs`. Antes de promocao futura, ainda precisa de validacao visual pelo usuario, decisao sobre backend FastAPI, decisao sobre banco local e checklist formal de promocao.
