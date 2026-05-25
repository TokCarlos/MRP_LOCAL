# RELATORIO OP KANBAN CARD v0.1.092

## Objetivo

Correção incremental focada no frontend de Ordens de Produção para alinhar Kanban/card/menu ao comportamento esperado após a trilha v0.1.091, sem alterar Produtos, BOM de Produto, Histórico da BOM, upload/imagens de Produto e demais módulos fora de OP.

## Problemas identificados

1. Clique direto no card abria modal de produtos em vez de visão operacional.
2. Modal operacional do card não listava itens com imagem.
3. Fluxo ativo ainda mantinha ações legadas de Kanban (botões soltos e textos antigos).
4. Pular etapa usava `window.prompt` sem modal CSS dedicado.
5. Menu `...` misturava área administrativa com movimentação de Kanban.
6. Opacidade visual dos cards estava fora da meta de 65%.

## Causa

- Reaproveitamento parcial de estruturas antigas no JS de OP, mantendo handlers e renderizações legadas no card e no modal `...`.
- Ausência de modal dedicado para pular etapa.
- CSS do card/coluna em valor de transparência menor do que a especificação operacional.

## Solução aplicada

1. Clique no card:
- Alterado para abrir modal operacional dedicado da OP.
- Modal mostra resumo da OP, processo atual, seletor único de status, botão de pular etapa e lista de itens/produtos com imagem.

2. Imagens do modal operacional:
- Implementada função única de resolução de imagem com suporte a:
  - `imagem_path`
  - `produto_imagem_path`
  - `imagem_url`
  - `imagem.preview`
  - `imagem`
  - `media/...`
  - `img/produtos/...`
  - `http(s)`
  - `data:`

3. Ações legadas de Kanban:
- Removidas do fluxo ativo de renderização do card.
- Mantido no operacional somente seletor de status + ação de pular etapa.

4. Pular etapa:
- Substituído `window.prompt` por modal CSS próprio.
- Modal com OP atual, processo atual, seleção de próxima etapa, erro inline e botões Voltar/Confirmar.
- Persistência feita por rota existente de backend (`/kanban/pular`).

5. Menu `...`:
- Mantido somente administrativo (Abrir produtos, Editar cabeçalho, BOM, Processos, Histórico, Cancelar OP).
- Removida seção textual/funcional de movimentação de Kanban.

6. Opacidade:
- Ajustado `background` de colunas e cards para `rgba(..., 0.65)` via `background`, sem aplicar `opacity` no container inteiro.

## Arquivos alterados

- `01-mrp/front_end/js/pages/ordens_producao_list.js`
- `01-mrp/front_end/pages/ordens_producao_list.html`
- `01-mrp/front_end/css/pages/ordens_producao_list.css`

## O que foi preservado

- Nova OP guiada em blocos.
- Empresa automática por ATA no backend.
- `data_entrega_input` e motor de normalização.
- Regras de quantidade inteira positiva.
- Lista compacta/expansível de itens com tabela rolável e cabeçalho sticky.
- Bloco final de Status com Observações.
- Cancelamento por soft delete no backend + modal CSS de confirmação.

## Validações executadas

- `python -m compileall 01-mrp/back_end/app`
- `node --check 01-mrp/front_end/js/pages/ordens_producao_list.js`
- Buscas de conformidade:
  - `window.prompt`
  - `Mover Próximo`
  - `Concluir e Mover`
  - `Movimentação do Kanban`

## Situação do portable

Portable não sincronizado nesta etapa.

Motivo: o espelho portable atual está em linha funcional reduzida e backend portable sem rotas Kanban equivalentes ao fluxo operacional da versão oficial. Aplicar o mesmo JS sem alinhar o backend portable geraria comportamento inconsistente.

