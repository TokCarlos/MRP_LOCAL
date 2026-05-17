# Checklist v0.1.005 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `REFATORACAO_FRONTEND_LOCAL_BASE`

## Entrada

- [x] Verificar existencia de `03-vs/entrada_original/mrp-main.zip`.
- [x] Extrair zip somente para `03-vs/patches/v0.1.005/origem_extraida`.
- [x] Nao apagar arquivos originais.

## Base de trabalho

- [x] Criar `03-vs/patches/v0.1.005/mrp_local_frontend_base`.
- [x] Copiar `front_end` aproveitavel para `mrp_local_frontend_base/front_end`.
- [x] Preservar HTML.
- [x] Preservar CSS.
- [x] Preservar JS da SPA.
- [x] Preservar imagens.
- [x] Preservar paginas.

## Refatoracao local

- [x] Remover StackAuth do fluxo de login.
- [x] Remover Neon REST do adaptador de dados.
- [x] Remover URLs externas de API.
- [x] Remover JWT online obrigatorio.
- [x] Criar login local temporario `admin` / `admin`.
- [x] Salvar sessao local em `localStorage`.
- [x] Manter logout funcionando.
- [x] Criar adaptador local temporario com dados mockados.
- [x] Validar apenas sessao local temporaria em `security.js`.
- [x] Criar `front_end/data/mock_data.json`.

## Documentacao

- [x] Criar `README_LOCAL.md`.
- [x] Criar `triagem_mrp_main.md`.
- [x] Criar `checklist.md` da versao.
- [x] Criar `registro.md` da versao.

## Restricoes

- [x] Nao alterar `01-mrp`.
- [x] Nao criar backend.
- [x] Nao criar banco.
- [x] Nao instalar dependencias.
- [x] Nao criar sistema funcional em `01-mrp`.
- [x] Nao usar acentos em nomes fisicos novos.

## Validacao pendente

- [x] Validar resposta HTTP local de `login.html` e `index.html` via servidor estatico temporario.
- [ ] Testar manualmente no navegador via servidor estatico local.
- [ ] Conferir visual completo com usuario antes de promocao futura.
- [ ] Definir backend e banco locais em etapa futura.
