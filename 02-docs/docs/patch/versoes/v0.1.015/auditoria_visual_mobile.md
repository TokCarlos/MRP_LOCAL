# Auditoria Visual Mobile sem Alteracao - v0.1.015A

Data do registro: 2026-05-17
Status: `AUDITORIA_VISUAL_MOBILE_SEM_ALTERACAO`

## Arquivos analisados

- `01-mrp/front_end/index.html`
- `01-mrp/front_end/login.html`
- `01-mrp/front_end/acesso_negado.html`
- `01-mrp/front_end/css/style.css`
- `01-mrp/front_end/css/responsive.css`
- `01-mrp/front_end/js/responsive.js`
- `01-mrp/front_end/js/pages/dashboard.js`
- `01-mrp/front_end/js/pages/produtos_list.js`
- `01-mrp/front_end/js/config.js`

## Diagnostico por problema

### 1) Sidebar/barra lateral sem utilidade no mobile

Problema encontrado:

- Nao existe sidebar real; o que existe e um menu horizontal (`nav.menu`) que vira painel expansivel no mobile.
- O botao `Menu` abre uma grade de links em bloco com deslocamento forte do `main`.

Arquivo/linha aproximada:

- `index.html`: linha 28 (`btnResponsiveMenu`) e linha 30 (`nav#mainMenu`).
- `css/responsive.css`: linhas 206-222 (`.responsive-menu-toggle`, `.menu`, `.menu.is-open`).
- `css/responsive.css`: linhas 231-233 e 251-253 (`body.menu-open main` com `margin-top` grande).
- `js/responsive.js`: linhas 12-14 (toggle de classes) e 18-24 (abertura/fechamento).

Ajuste recomendado:

- Em vez de empurrar o `main` com `margin-top` fixo grande, usar menu mobile em overlay/absolute sob o header, com altura calculada e scroll proprio.
- Manter `menu-open` apenas para controlar visibilidade, sem reflow agressivo no body/main.

Risco do ajuste:

- Baixo a medio. Se mal aplicado, pode sobrepor conteudo ou esconder links.

### 2) Botoes EDIT grandes demais

Problema encontrado:

- Regra global define `min-height: 44px` para `preview-table button`, deixando botoes de linha de tabela muito altos.
- O botao EDIT vem inline em `produtos_list.js` sem classe dedicada para tamanho de contexto de tabela.

Arquivo/linha aproximada:

- `css/responsive.css`: linhas 90-98 (inclui `.preview-table button` no touch target global).
- `js/pages/produtos_list.js`: linha 26 (botao `Editar` sem classe).

Ajuste recomendado:

- Criar classe especifica para botao de linha (ex.: `.btn-row-action`) e retirar `preview-table button` da regra global de `44px`.
- Manter `44px` para botoes primarios (`Menu`, `Sair`, `Entrar`, `+ Novo Produto`), mas reduzir linha de tabela para faixa 32-36px.

Risco do ajuste:

- Baixo. Impacto localizado na tabela.

### 3) Logo JPL colado ao titulo

Problema encontrado:

- O espacamento entre logo e titulo depende de regra em `style.css` para classe `.logo` e em `responsive.css` para `.logo-area img`, criando comportamento inconsistente.
- Em mobile menor, margens sao reduzidas e o titulo sofre `ellipsis`, aproximando visualmente os elementos.

Arquivo/linha aproximada:

- `index.html`: linhas 23-25 (logo + titulo no mesmo bloco).
- `css/style.css`: linhas 98-101 (`.logo` com `margin-right: 14px`).
- `css/responsive.css`: linhas 66-70 (logo responsivo sem margem definida para `.logo-area img`).
- `css/responsive.css`: linhas 270-274 (reduz margem para 6px em <=360px).

Ajuste recomendado:

- Unificar regra de espacamento em um unico seletor (`.logo-area img`) com `margin-right: clamp(8px, 1.8vw, 14px)`.
- Evitar competir com `.logo` legado quando a imagem nao usa essa classe.

Risco do ajuste:

- Baixo. Mudanca visual pontual no header.

### 4) Distorcoes de body/header em mobile e zoom

Problema encontrado:

- `style.css` e `responsive.css` ambos mexem em header, `main` e espacamentos de topo.
- Em mobile, `main` recebe `margin-top` em mais de uma regra e ainda muda para valores fixos quando `menu-open`.
- Isso causa "saltos" de layout em zoom e em trocas de orientacao.

Arquivo/linha aproximada:

- `css/style.css`: linhas 35-38 (margem/padding base do `main`).
- `css/style.css`: linhas 252-255 (override mobile com `margin-top: 120px`).
- `css/responsive.css`: linhas 52-56 (`main` width/padding).
- `css/responsive.css`: linhas 192-194 e 235-238 (margens de `main` por breakpoint).
- `css/responsive.css`: linhas 231-233 e 251-253 (margens fixas em `menu-open`).

Ajuste recomendado:

- Consolidar logica de espacamento vertical em uma unica fonte: `--header-height` + `padding-top` do `main`, sem margens fixas por estado.
- Remover dependencia de valores fixos (`240px`, `350px`) para `menu-open`.

Risco do ajuste:

- Medio. Pode afetar todas as telas da SPA se feito sem teste de regressao.

## Media queries que afetam 480px, 390px e 360px

- `css/responsive.css`: `@media (max-width: 480px)` linhas 241-267.
- `css/responsive.css`: `@media (max-width: 360px)` linhas 269-290.
- `390px` e impactado indiretamente pelo bloco de `480px`.

## responsive.css esta sobrescrevendo style.css de forma correta?

Diagnostico:

- Parcialmente correto. A ordem de carga esta certa (`responsive.css` depois), mas ha sobreposicao agressiva em header/main.
- Existe duplicidade de responsabilidade entre `style.css` e `responsive.css` para os mesmos elementos.

Recomendacao:

- Deixar `style.css` como base desktop.
- Concentrar so adaptacoes mobile em `responsive.css`.
- Evitar sobrescrever o mesmo atributo em muitos pontos para `main/header`.

## responsive.js e realmente necessario?

Diagnostico:

- Sim, para o estado de abrir/fechar menu mobile e `aria-expanded`.
- Sem ele, o botao `Menu` nao teria comportamento.

Observacao:

- O arquivo e pequeno e objetivo. O problema principal nao e a existencia do JS, mas o impacto de CSS (`menu-open` com margens fixas).

## Valores de configuracao

- `js/config.js` esta neutro para layout (linhas 5-22) e nao e causa dos problemas visuais atuais.

## Ordem recomendada de implementacao (proxima etapa)

1. Ajustar menu mobile para nao empurrar `main` com margem fixa (`240px`/`350px`).
2. Ajustar tamanho de botoes de linha de tabela (`Editar`) com classe especifica.
3. Unificar espacamento logo/titulo em um seletor unico com `clamp`.
4. Consolidar regras de `main/header` para reduzir conflitos entre `style.css` e `responsive.css`.
5. Testar em 480px, 390px, 360px e zoom 125/150/175.

## Arquivos que devem ser alterados na proxima etapa

- `01-mrp/front_end/css/responsive.css`
- `01-mrp/front_end/css/style.css`
- `01-mrp/front_end/js/pages/produtos_list.js`
- `01-mrp/front_end/js/responsive.js` (somente se ajuste de comportamento exigir)
- `01-mrp/front_end/index.html` (somente se precisar pequeno ajuste estrutural do header/menu)
