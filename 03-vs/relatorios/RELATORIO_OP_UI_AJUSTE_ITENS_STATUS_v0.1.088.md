# RELATÓRIO - OP UI AJUSTE ITENS/STATUS v0.1.088

Base incremental: patch_op_ui_itens_acoes_v0_1_087.zip.

## Ajustes aplicados

1. Removido o título externo duplicado `ITENS ADICIONADOS`.
2. Mantido apenas o cabeçalho compacto/expansível `Itens adicionados na OP`.
3. A lista de produtos adicionados permanece entre os formulários principais e a tabela de produtos disponíveis.
4. Ao expandir a lista de itens adicionados, a tabela agora possui rolagem vertical e horizontal.
5. O campo `STATUS` foi removido da posição acima de `ITENS ADICIONADOS`.
6. O campo `STATUS` foi movido para o bloco final, junto de `OBSERVAÇÕES`.

## Arquivos alterados

- 01-mrp/front_end/pages/ordens_producao_list.html
- 01-mrp/front_end/css/pages/ordens_producao_list.css

## Validação

- OK: `node --check 01-mrp/front_end/js/pages/ordens_producao_list.js`
- OK: `python3 -m compileall` nos arquivos backend de OP
