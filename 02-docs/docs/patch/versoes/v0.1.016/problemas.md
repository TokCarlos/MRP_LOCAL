# v0.1.016 - Diagnostico tecnico overflow mobile (Produtos)

## Escopo desta etapa

- Somente auditoria.
- Nenhuma correcao aplicada nesta etapa.
- Nenhuma alteracao de backend ou logica funcional.

## Arquivos auditados

- `01-mrp/front_end/pages/produtos_list.html`
- `01-mrp/front_end/js/pages/produtos_list.js`
- `01-mrp/front_end/css/style.css`
- `01-mrp/front_end/css/responsive.css`
- `01-mrp/front_end/css/pages/produtos_list.css`
- `01-mrp/front_end/index.html`

## Elemento causador (confirmado por codigo)

**Causa principal:** largura minima efetiva da tabela de Produtos acima da viewport mobile.

- Arquivo: `01-mrp/front_end/css/responsive.css`
- Seletor: `.preview-table` (linha 149)
- Regra atual: `width: max(100%, 36rem);`
- Regra em mobile pequeno: `@media (max-width: 480px) .preview-table { width: max(100%, 32rem); }` (linha 280)

### Impacto tecnico

- Em 360px: `32rem` (base 16px) = **512px** > viewport.
- Em 390px: **512px** > viewport.
- Em 430px: **512px** > viewport.

Mesmo com `.table-responsive { overflow-x: auto; }`, a tabela fica maior que a viewport por definicao. Se algum ancestral ou gesto lateral do navegador expor area fora do fluxo, o usuario percebe a faixa branca lateral.

## Evidencias complementares

1. `pages/produtos_list.html`:
   - `.table-responsive` (linha 5)
   - `table.preview-table` (linha 6)
   - coluna `Ações` (linha 11)
2. `js/pages/produtos_list.js`:
   - botao `Editar` com classe `.btn-row-action` (linha 26), sem largura fixa excessiva no JS.
3. `css/responsive.css`:
   - wrapper da tabela com `overflow-x: auto` (linha 141)
   - regra que expande tabela alem da viewport em mobile (linhas 149 e 280)

## Itens investigados e descartados como causa principal

- `width: 100vw` em containers relevantes: nao encontrado na cadeia principal de Produtos.
- `white-space: nowrap` em `th/td` de Produtos: nao encontrado.
- `btn-row-action` com largura fixa/margem exagerada: nao encontrado.
- Header/menu com largura fixa maior que viewport: sem indicio de causa direta especifica da aba Produtos.

## Correcao minima recomendada (nao aplicada nesta etapa)

1. Trocar largura da tabela para comportamento menos agressivo em mobile:
   - substituir `width: max(100%, 36rem)` por regra que preserve leitura sem forcar largura minima fixa grande em telas pequenas.
2. Manter `overflow-x: auto` apenas no wrapper `.table-responsive`.
3. Se necessario, aplicar ajuste por breakpoint para coluna de acoes (sem alterar logica).

## Risco da alteracao recomendada

- **Baixo a medio**: pode reduzir largura visual da tabela em desktop se regra nao for condicionada por breakpoint.
- Mitigacao: ajustar somente em `@media` mobile e manter comportamento atual em desktop/tablet maior.

## Observacao de validacao automatica

Tentativa de validacao headless no ambiente atual falhou por restricao de execucao:
- `CreateProcessWithLogonW failed: 267`

Para confirmacao final no navegador, executar script DevTools informado no pedido em:
- 360px
- 390px
- 430px
