# Checklist v0.1.007 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `REFATORACAO_FRONTEND_LOCAL_BASE`

## Entrada

- [x] Verificar existencia de `03-vs/entrada_original/mrp-main.zip`.
- [x] Extrair zip somente para `03-vs/patches/v0.1.007/origem_extraida`.
- [x] Identificar estrutura do projeto antigo.
- [x] Nao apagar arquivos originais.

## Base de trabalho

- [x] Criar `03-vs/patches/v0.1.007/mrp_local_frontend_base`.
- [x] Copiar `front_end` aproveitavel para `mrp_local_frontend_base/front_end`.
- [x] Localizar HTML aproveitavel.
- [x] Localizar CSS aproveitavel.
- [x] Localizar JavaScript aproveitavel.
- [x] Localizar imagens aproveitaveis.
- [x] Localizar paginas e assets aproveitaveis.
- [x] Preservar visual, layout, paginas, estilos e navegacao sempre que possivel.

## Refatoracao local

- [x] Remover StackAuth do fluxo de login.
- [x] Remover Neon REST do adaptador de dados.
- [x] Remover URLs externas de API.
- [x] Remover JWT online obrigatorio.
- [x] Isolar dependencia de dominio/hospedagem online.
- [x] Criar login local temporario `admin` / `admin`.
- [x] Salvar sessao local em `localStorage`.
- [x] Manter logout funcionando.
- [x] Criar adaptador local temporario com dados mockados.
- [x] Criar `front_end/data/mock_data.json`.
- [x] Manter `index.html`, `login.html` e SPA abrindo localmente por servidor estatico.

## Documentacao

- [x] Criar `README_LOCAL.md`.
- [x] Criar `triagem_mrp_main.md`.
- [x] Criar `checklist.md` da versao.
- [x] Criar `registro.md` da versao.

## Restricoes

- [x] Nao alterar `01-mrp`.
- [x] Trabalhar somente em `03-vs` para arquivos de patch.
- [x] Documentar em `02-docs`.
- [x] Nao criar backend.
- [x] Nao criar banco.
- [x] Nao instalar dependencias.
- [x] Nao usar acentos em nomes fisicos novos.
- [x] Registrar dependencias removidas no relatorio.

## Validacao executada

- [x] Busca textual sem dependencias online na base `front_end`.
- [x] `node --check` aprovado para `auth.js`.
- [x] `node --check` aprovado para `api.js`.
- [x] `node --check` aprovado para `security.js`.
- [x] `node --check` aprovado para `spa.js`.
- [x] `login.html` respondeu HTTP 200 via servidor estatico temporario.
- [x] `index.html` respondeu HTTP 200 via servidor estatico temporario.

## Validacao pendente antes de promocao

- [ ] Teste manual completo no navegador pelo usuario.
- [ ] Conferencia visual das telas.
- [ ] Definir backend FastAPI futuro.
- [ ] Definir banco local futuro.
- [ ] Criar checklist formal de promocao para `01-mrp`.
