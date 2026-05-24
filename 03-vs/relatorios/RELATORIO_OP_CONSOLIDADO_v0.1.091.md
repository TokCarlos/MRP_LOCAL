# RELATORIO OP CONSOLIDADO v0.1.091

## Marco

VERSAO v0.1.091 - OP GUIADA + KANBAN SIMPLIFICADO + UI DE ITENS

## Sequencia consolidada de patches

- patch_op_nova_op_guiada_v0_1_085.zip
- patch_op_ajuste_imagem_qtd_v0_1_086.zip
- patch_op_ui_itens_acoes_v0_1_087.zip
- patch_op_ui_itens_status_v0_1_088.zip
- patch_op_ui_tabela_sticky_v0_1_089.zip
- patch_op_kanban_acoes_simplificadas_v0_1_090.zip
- patch_op_kanban_correcao_reforco_v0_1_091.zip

## Resumo tecnico consolidado

1. Nova OP guiada
- Fluxo por blocos: CLIENTE, OBRA, SOLICITANTE | DATA DE ENTREGA, MODELO ATA, ITENS/APARELHOS, STATUS | OBSERVACOES.
- Campo Empresa removido da UI.
- Empresa permanece automatica por MODELO ATA no backend.
- Status inicial automatico em RASCUNHO.
- Criacao transacional com OP + produtos + BOM snapshot + processos + historico.

2. Motor de Data de Entrega
- Campo unico `data_entrega_input`.
- Suporte de formatos: `dd/mm/aaaa`, `dd/mm/aa`, `dd-mm-aaaa`, `dd.mm.aaaa`.
- Conversao para: `data_entrega_tipo=DATA`, `data_entrega_data=YYYY-MM-DD`, `data_entrega_valor=DD/MM/AAAA`.
- Textos operacionais (NAO DEFINIDO, A DEFINIR, URGENTE, SEM DATA, AGUARDANDO CLIENTE) convertidos para tipo TEXTO com `data_entrega_data=NULL` e valor normalizado em maiusculo.

3. Produtos na Nova OP
- Produtos ocultos antes da selecao de ATA.
- ATA especifica exibe apenas produtos da ATA.
- ESPECIAL exibe produtos de todas as ATAs.
- Em ESPECIAL, produto exibe ATA/empresa de origem.
- Ajustes de imagem para `media`, `img/produtos`, `http(s)` e `data`.
- Quantidade aceita somente inteiro positivo.
- Decimal, texto invalido, zero e nulo rejeitados.

4. Itens adicionados
- Lista compacta entre formularios e tabela de produtos.
- Expansao/recolhimento por clique.
- Tabela rolavel no modo expandido.
- Cabecalho sticky.
- Colunas: ITEM, IMAGEM, PRODUTO, ATA, QTD, ACAO.
- Titulo duplicado removido; mantido apenas "Itens adicionados na OP".

5. Status e Observacoes
- Status removido da posicao intermediaria.
- Status movido para bloco final com Observacoes.
- Campos com altura equivalente.

6. Kanban / Cards
- Opacidade de cards ajustada para 65%.
- Clique direto no card com foco operacional.
- Modal operacional do card com resumo, itens/produtos com imagem, seletor unico de status e botao Pular etapa.
- Filtro antigo do modal removido.
- Botoes antigos de movimentacao removidos na proposta da versao, substituidos por seletor unico de status.
- Pular etapa separado em acao propria com modal CSS.

7. Menu dos tres pontos
- Menu "..." assumido como area administrativa.
- Acoes previstas: Abrir produtos, Editar cabecalho, BOM, Processos, Historico, Cancelar OP.
- Movimentacao Kanban retirada do menu administrativo na proposta da versao.
- Cancelar OP com modal CSS proprio.

8. Cancelamento OP
- Soft delete com `ativo=0`.
- `status=CANCELADA`.
- Historico registrado.
- Kanban recarregado apos cancelamento.
- OP cancelada removida do Kanban ativo.

## Validacao tecnica executada nesta consolidacao

- OK: `python -m compileall 01-mrp/back_end/app`
- OK: `node --check 01-mrp/front_end/js/pages/ordens_producao_list.js`
- OK: `node --check portable/app/frontend/js/pages/ordens_producao_list.js`

## Verificacao de conformidade solicitada (estado atual do codigo)

- PENDENTE: ainda existe `window.prompt` no fluxo de pular etapa em `01-mrp/front_end/js/pages/ordens_producao_list.js` (linha 792).
- PENDENTE: ainda existem `alert/confirm` nativos no JS oficial e no espelho portable.
- PENDENTE: ainda existem textos antigos visiveis no JS oficial: "Mover Proximo" e "Concluir e Mover".

## Escopo preservado

- Sem alteracao em Produtos, BOM de Produto, Historico da BOM, imagens/upload de Produto, PDF, Excel, estoque, WhatsApp e drag-and-drop nesta etapa documental.
