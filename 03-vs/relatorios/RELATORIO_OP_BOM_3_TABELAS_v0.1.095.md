# RELATORIO OP BOM 3 TABELAS v0.1.095

## Base usada
- Versao base: `v0.1.094`
- Commit base: `425e161af54f2b9e83651bf070cd527d589436bc`
- Branch: `main`

## Objetivo
- Ajustar somente a BOM consultiva da OP para o padrao em 3 tabelas:
  - TUBOS
  - CHAPAS
  - INSUMOS
- Manter o fluxo atual da OP sem alterar criacao, Kanban, edicao, card operacional e menu administrativo.

## Arquivos alterados
- `01-mrp/front_end/js/pages/ordens_producao_list.js`
- `01-mrp/front_end/pages/ordens_producao_list.html`
- `01-mrp/front_end/css/pages/ordens_producao_list.css`
- `03-vs/relatorios/RELATORIO_OP_BOM_3_TABELAS_v0.1.095.md`
- `02-docs/LOG_PROGRESSO_MRP.txt`

## Reaproveitamento do padrao de Produtos
- Referencia lida em `produtos_list.js`:
  - `normalizeBomGrupo(value)` e agrupamento por `grupo`.
  - tabelas separadas por `tubos`, `chapas`, `insumos`.
- Na OP foi aplicada a mesma regra de classificacao por `grupo` em minusculo, com fallback igual ao modulo Produtos:
  - valor invalido/ausente -> `tubos`.

## Como TUBOS/CHAPAS/INSUMOS foram separados
- Adicionadas funcoes no JS da OP:
  - `normalizeOpBomGrupo(value)`
  - `renderOpBomGrupoRows(tbodyId, rows, qtdProdutoOp)`
- No detalhe da BOM da OP:
  - filtra itens por `op_produto_id`;
  - classifica por grupo;
  - renderiza em 3 tabelas independentes:
    - `opBomTubosRows`
    - `opBomChapasRows`
    - `opBomInsumosRows`

## Campos exibidos nas 3 tabelas
- CODIGO
- DESCRICAO
- UNIDADE
- QTD UNITARIA
- QTD PRODUTO OP
- TOTAL OP

## Regra de totalizacao
- Aplicada quando possivel:
  - `Total OP = quantidade_unitaria * quantidade_produto`
- Quando nao houver dado numerico suficiente:
  - usa `quantidade_total` retornada pela API, se disponivel;
  - sem dado confiavel, exibe `-`.

## Confirmacao de somente leitura
- Nao foram adicionados inputs, botoes de editar/remover/salvar na BOM detalhada da OP.
- A tela continua consultiva.

## Testes executados
- `python -m compileall 01-mrp/back_end/app` -> OK
- `node --check 01-mrp/front_end/js/pages/ordens_producao_list.js` -> OK

## Buscas de seguranca
- `window.prompt` -> sem ocorrencia
- `Mover Próximo` -> sem ocorrencia
- `Concluir e Mover` -> sem ocorrencia
- `Movimentação do Kanban` -> sem ocorrencia
- `Editar cabeçalho` -> sem ocorrencia

## Validacao manual
- Pendencia nesta execucao: teste manual de navegador nao foi concluido no ambiente atual.
- Fluxo esperado preservado:
  - lista de aparelhos da OP;
  - detalhe da BOM em 3 tabelas;
  - botao Voltar para retornar aos aparelhos.

## Portable
- Portable nao sincronizado nesta etapa.
