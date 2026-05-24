# RELATÓRIO — OP GUIADA v0.1.085

## Escopo executado

Patch incremental para Ordens de Produção, mantendo fora do escopo Produtos, BOM de Produto, Histórico da BOM, imagens/upload, portable, PDF, Excel, estoque, WhatsApp e drag-and-drop.

## Ajustes implementados

1. Criação guiada de OP com blocos operacionais:
   - CLIENTE
   - OBRA
   - SOLICITANTE | DATA DE ENTREGA
   - MODELO ATA
   - ITENS / APARELHOS
   - OBSERVAÇÕES

2. Campo único de Data de Entrega:
   - `data_entrega_input` na UI e backend.
   - Reconhece `dd/mm/aaaa`, `dd/mm/aa`, `dd-mm-aaaa`, `dd.mm.aaaa`.
   - Converte para `data_entrega_tipo=DATA`, `data_entrega_data=YYYY-MM-DD`, `data_entrega_valor=DD/MM/AAAA`.
   - Textos operacionais viram `data_entrega_tipo=TEXTO`, `data_entrega_data=NULL`, `data_entrega_valor` em maiúsculo.
   - Normaliza `NAO DEFINIDO` para `NÃO DEFINIDO`.

3. Modelo ATA:
   - Seleção de ATA no modal da OP.
   - Empresa automática conforme ATA selecionada.
   - Opção `ESPECIAL` permite selecionar produtos de todas as ATAs.
   - ATA específica filtra produtos daquela ATA.
   - Em `ESPECIAL`, card mostra ATA/empresa do produto.

4. Itens/aparelhos na criação:
   - Lista visual com imagem, item ATA, nome do aparelho, quantidade e botão adicionar.
   - Lista de selecionados com edição de quantidade e remoção.
   - Nova OP já nasce com produtos selecionados.

5. Backend ACID:
   - Nova rotina `create_ordem_completa` cria OP + produtos + snapshot BOM + processos + histórico dentro de uma única transação SQLite.
   - Evita OP parcial em falha durante criação guiada.

6. Kanban / exclusão:
   - Ação `Cancelar OP` adicionada no menu do card.
   - Backend mantém soft delete: `ativo=0`, status `CANCELADA`, histórico registrado.
   - UI recarrega Kanban após cancelamento.
   - Ações de status/mover/pular/concluir continuam recarregando Kanban após persistência.

## Arquivos alterados

- `01-mrp/back_end/app/domain/ordens_producao_models.py`
- `01-mrp/back_end/app/repositories/ordens_producao_repository.py`
- `01-mrp/back_end/app/services/ordens_producao_service.py`
- `01-mrp/front_end/pages/ordens_producao_list.html`
- `01-mrp/front_end/js/pages/ordens_producao_list.js`
- `01-mrp/front_end/css/pages/ordens_producao_list.css`

## Validação local executada

- `python -m compileall -q 01-mrp/back_end/app`
- `node --check 01-mrp/front_end/js/pages/ordens_producao_list.js`
- Teste funcional em SQLite temporário:
  - criação de OP guiada com produto;
  - snapshot de BOM;
  - criação de 10 processos padrão;
  - entrada no Kanban;
  - mover próximo;
  - pular etapa;
  - cancelamento soft delete removendo do Kanban ativo.
