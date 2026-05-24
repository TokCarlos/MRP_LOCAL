# RELATORIO_OP_AJUSTE_IMAGEM_QTD_v0.1.086

## Escopo
Patch incremental sobre `patch_op_nova_op_guiada_v0_1_085.zip`.

## Ajustes aplicados

1. Imagens dos produtos na Nova OP
   - Corrigida a resolução de caminho da imagem no módulo de Ordens de Produção.
   - Caminhos `media/...` continuam apontando para o backend `http://host:8876/media/...`.
   - Caminhos locais do frontend, como `img/produtos/...`, deixam de ser enviados incorretamente para o backend e passam a ser usados como caminho relativo do frontend.
   - URLs absolutas `http(s)` e `data:` continuam preservadas.

2. Quantidade de produtos apenas inteira
   - Inputs de quantidade de produtos alterados de `step=0.01` para `step=1`, `min=1`, `inputmode=numeric` e `pattern=\\d+`.
   - Sanitização no frontend remove caracteres não numéricos na seleção guiada e edição de produtos da OP.
   - Validação no frontend bloqueia quantidade vazia, zero ou decimal.
   - Validação no backend bloqueia quantidade decimal em criação da OP, adição de produto e atualização de produto da OP.
   - Modelo de contrato de produto da OP alterado de `float` para `int`.

## Arquivos alterados

- `01-mrp/back_end/app/domain/ordens_producao_models.py`
- `01-mrp/back_end/app/services/ordens_producao_service.py`
- `01-mrp/front_end/pages/ordens_producao_list.html`
- `01-mrp/front_end/js/pages/ordens_producao_list.js`

## Validação executada

- `python -m compileall` nos arquivos backend alterados.
- `node --check` no JavaScript alterado.
- Teste direto da validação `_positive_int`, confirmando rejeição de `0`, `1.2`, `"1.2"`, texto inválido e nulo.
