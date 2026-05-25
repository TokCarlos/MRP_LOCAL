# RELATORIO OP EDITAR BOM v0.1.093

## Base utilizada
- Versao base: `v0.1.092`
- Commit base: `b70b65061278f9368cedc512d2d214af011ad71e`
- Branch de trabalho: `main`

## Objetivo da v0.1.093
- Ajustar a experiencia operacional do card da OP.
- Entregar fluxo de edicao completa da OP pelo botao `Editar OP`.
- Remover `Editar cabecalho` do menu `...`.
- Reestruturar BOM da OP para consulta em duas etapas:
  - lista de aparelhos/produtos da OP;
  - BOM detalhada por aparelho, somente leitura.

## Arquivos alterados
- `01-mrp/front_end/js/pages/ordens_producao_list.js`
- `01-mrp/front_end/pages/ordens_producao_list.html`
- `01-mrp/front_end/css/pages/ordens_producao_list.css`
- `03-vs/relatorios/RELATORIO_OP_EDITAR_BOM_v0.1.093.md`

## Alteracoes no modal operacional do card
- Linha de contexto `CLIENTE | OBRA | ENTREGA` reforcada visualmente.
- Lista de itens convertida para tabela com colunas:
  - `IMAGEM | ITEM | PRODUTO | ATA | QTD`
- QTD passou a ser editavel no proprio modal operacional, com sanitizacao para inteiro positivo.
- Persistencia da QTD mantida em endpoint existente de OP/produtos.
- Inclusao de botao `Editar OP` no rodape do modal operacional.

## Alteracoes na tabela de itens da OP
- QTD nos fluxos de edicao/criacao foi alinhada para entrada textual numerica (`inputmode="numeric"` + sanitizacao JS), sem aceitar decimal/texto/zero.
- Fluxo de edicao carrega itens atuais e permite:
  - alterar quantidade;
  - remover itens;
  - adicionar novos produtos;
  - salvar alteracoes com sincronizacao de itens.

## Alteracoes na edicao completa da OP
- `Editar OP` abre o formulario completo com cabecalho e itens.
- O bloco de itens guiados permanece ativo tambem em edicao.
- Salvamento em edicao aplica:
  - `PUT /api/ordens-producao/{id}` para cabecalho;
  - sincronizacao de itens por endpoints existentes:
    - `POST /produtos`
    - `PUT /produtos/{op_produto_id}`
    - `DELETE /produtos/{op_produto_id}`

## Menu "..." ajustado
- Removido `Editar cabecalho` do menu administrativo.
- Mantido menu administrativo com:
  - Produtos da OP
  - BOM
  - Processos
  - Historico
  - Cancelar OP

## Nova BOM consultiva da OP
- Primeira tela de BOM mostra aparelhos/produtos da OP (somente leitura):
  - `IMAGEM | ITEM | APARELHO/PRODUTO | ATA | QTD OP`
- Cada linha abre BOM detalhada por aparelho (somente leitura).
- BOM detalhada exibe:
  - `CODIGO | DESCRICAO | UNIDADE | QTD UNITARIA | QTD PRODUTO OP | TOTAL OP`
- `TOTAL OP` calculado no frontend quando necessario com base em `quantidade_unitaria * quantidade_produto`.

## Preservacoes da v0.1.092
- Clique no card continua abrindo modal operacional.
- Kanban permanece com seletor unico de status + pular etapa.
- Modal CSS de pular etapa preservado.
- Cancelamento por modal CSS preservado.
- Sem retorno de `window.prompt`, `Mover Proximo`, `Concluir e Mover`, `Movimentacao do Kanban`, `Editar cabecalho` no fluxo ativo.
- Nova OP guiada preservada com regras de ATA/empresa automatica e validacoes de quantidade.

## Situacao do portable
- Portable nao sincronizado nesta etapa.

## Testes executados
- `python -m compileall 01-mrp/back_end/app` -> OK
- `node --check 01-mrp/front_end/js/pages/ordens_producao_list.js` -> OK
- Buscas obrigatorias:
  - `window.prompt` -> sem ocorrencia
  - `Mover Próximo` -> sem ocorrencia
  - `Concluir e Mover` -> sem ocorrencia
  - `Movimentação do Kanban` -> sem ocorrencia
  - `Editar cabeçalho` -> sem ocorrencia

## Pendencias conhecidas
- Nao houve sincronizacao do portable nesta entrega.
- Validacao manual completa em navegador local deve ser executada no ambiente operacional com backend/frontend em execucao.
