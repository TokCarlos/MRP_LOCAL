# v0.1.018 - Solucao

## A) Consolidacao de variaveis CSS (sem mudanca visual)

Arquivo: `01-mrp/front_end/css/style.css`

Incluidos aliases tecnicos no `:root`:
- `--cor-painel: var(--color-panel);`
- `--cor-subtexto: var(--color-text-muted);`
- `--cor-botao: var(--color-accent);`

Sem troca de cor/valor visual.

## B) Rotas funcionais minimas preenchidas

Arquivos HTML preenchidos:
- `01-mrp/front_end/pages/processos_list.html`
- `01-mrp/front_end/pages/estoque_list.html`
- `01-mrp/front_end/pages/ordens_list.html`

Arquivos JS criados:
- `01-mrp/front_end/js/pages/processos_list.js`
- `01-mrp/front_end/js/pages/estoque_list.js`
- `01-mrp/front_end/js/pages/ordens_list.js`

Padrao visual reaproveitado:
- `table-responsive`
- `preview-table`
- `btn-row-action` (onde aplicavel)

## C) Mock de dados expandido para acoplamento futuro

Arquivo: `01-mrp/front_end/js/api.js`

Estruturas consolidadas:
- `produtos`: `id`, `codigo`, `nome`, `unidade`, `categoria`, `status`
- `processos`: `id`, `codigo`, `nome`, `setor`, `tempo_padrao_min`, `status`
- `estoque`: `id`, `produto_id`, `local`, `quantidade`, `minimo`, `unidade`, `status`
- `ordens_producao`: `id`, `numero`, `produto_id`, `quantidade`, `status`, `prioridade`, `data_prevista`

Compatibilidade preservada:
- Dashboard segue consumindo contagem por tabela.
- Produtos segue funcionando com `nome`.

## D) Limpeza controlada (decisao)

Arquivos avaliados:
- `pages/aparelho.html`
- `js/pages/aparelho.js`
- `css/pages/aparelho.css`
- `js/pages/processos.js`
- `js/pages/estoque.js`

Decisao:
- **Mantidos como modulos reservados nao ativos** nesta etapa para evitar ruptura historica e permitir evolucao incremental.
- Sem remocao de historico/documentacao.

## E) Checklist tecnico

Criado documento:
- `02-docs/docs/patch/versoes/v0.1.018/checklist_tecnico.md`
