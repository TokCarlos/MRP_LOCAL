# RELATORIO - OP UI TABELA STICKY v0.1.089

## Escopo

Patch incremental sobre v0.1.088.

## Ajustes

- Cabeçalho da tabela de itens adicionados recebeu comportamento sticky reforçado.
- Tabela de itens adicionados passou a usar border-collapse separado para reduzir falhas visuais do cabeçalho fixo.
- Cabeçalho recebeu fundo opaco, z-index e sombra para não parecer solto durante a rolagem.
- Área rolável dos itens adicionados foi ajustada para rolagem vertical/horizontal controlada.
- Bloco final de STATUS e OBSERVAÇÕES recebeu alinhamento por grid.
- Select de STATUS e textarea de OBSERVAÇÕES agora usam altura equivalente.

## Arquivos alterados

- 01-mrp/front_end/css/pages/ordens_producao_list.css
- portable/app/frontend/css/pages/ordens_producao_list.css
