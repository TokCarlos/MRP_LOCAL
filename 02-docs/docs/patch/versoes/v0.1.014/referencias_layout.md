# Referencias de Layout Responsivo - v0.1.014

Data do registro: 2026-05-17
Status: `REFERENCIAS_LAYOUT_RESPONSIVO_APLICADAS`

## Objetivo

Registrar as referencias publicas usadas apenas como base conceitual de comportamento responsivo e documentar os ajustes aplicados no front-end existente em `01-mrp/front_end`.

## Referencias consultadas

- Tabler Preview: `https://preview.tabler.io/`
- AdminLTE: `https://adminlte.io/`
- Bootstrap Sidebars: `https://getbootstrap.com/docs/5.0/examples/sidebars/`
- MDN Responsive Design: `https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/CSS_layout/Responsive_Design`
- web.dev Learn Responsive Design: `https://web.dev/learn/design`

## Uso das referencias

As referencias foram usadas somente como base conceitual. Nenhum template completo foi baixado, nenhuma dependencia foi instalada e nenhum codigo grande de terceiros foi copiado.

Pontos conceituais considerados:

- Sidebar/menu responsivo.
- Header responsivo.
- Cards fluidos.
- Tabelas com `overflow-x` controlado.
- Login mobile.
- Breakpoints.
- `meta viewport`.
- `body` sem overflow lateral indevido.

## Padroes extraidos conceitualmente

### MDN / web.dev

- Layout responsivo deve evitar largura fixa que cause rolagem horizontal indevida.
- Grids fluidos e media queries devem adaptar a interface ao tamanho da tela.
- Imagens e conteudos devem respeitar a largura do container.
- `meta viewport` e base mobile-friendly sao obrigatorios para smartphone.

### Bootstrap Sidebars

- Navegacao deve se adaptar em telas menores.
- Menus podem ser recolhidos ou reorganizados sem quebrar a navegacao desktop.

### Tabler / AdminLTE

- Dashboards usam header/menu, cards, tabelas e conteudo em containers fluidos.
- Componentes de painel devem ser reutilizaveis, responsivos e preservar consistencia visual.

## Arquivos alterados em `01-mrp/front_end`

### Criados

- `css/responsive.css`.
- `js/responsive.js`.

### Alterados

- `index.html`.
- `login.html`.
- `acesso_negado.html`.
- `pages/produtos_list.html`.

## Ajustes aplicados

### `css/responsive.css`

Criada camada responsiva separada para preservar o visual atual e evitar reescrita agressiva.

Inclui:

- `min-width: 320px` em `html/body`.
- `overflow-x: hidden` no `body`.
- midias fluidas com `max-width: 100%`.
- area minima de toque para botoes, links, inputs e controles.
- header com flex-wrap e comportamento responsivo.
- botao de menu mobile.
- menu recolhido abaixo de `768px`.
- cards do dashboard com grid fluido.
- tabela com `.table-responsive` e rolagem horizontal controlada.
- login com largura fluida e limite de largura no smartphone.
- breakpoints `1024px`, `768px`, `480px` e `360px`.

### `js/responsive.js`

Criado controle pequeno para abrir/fechar menu mobile.

Comportamento:

- Alterna classe `is-open` no menu.
- Alterna classe `menu-open` no `body`.
- Atualiza `aria-expanded`.
- Fecha menu ao clicar em item.
- Fecha menu ao voltar para largura desktop.

### `index.html`

- Incluido `css/responsive.css`.
- Adicionado botao `btnResponsiveMenu`.
- Adicionado `id="mainMenu"` no menu.
- Incluido `js/responsive.js`.

### `login.html` e `acesso_negado.html`

- Incluido `css/responsive.css`.
- `meta viewport` ja estava presente e foi mantido.

### `pages/produtos_list.html`

- Tabela envolvida em `.table-responsive`.

## Regras preservadas

- Nao baixar template completo.
- Nao instalar dependencias.
- Nao substituir identidade visual.
- Nao trocar framework.
- Nao copiar codigo grande de terceiros.
- Preservar layout atual ao maximo.
- Manter login local temporario existente.
- Manter adaptador local/mock existente.

## Validacao executada

- `node --check js/responsive.js`: aprovado.
- Busca sem StackAuth, Neon, URLs externas, JWT ou Authorization/Bearer em `01-mrp/front_end`.
- Servidor estatico temporario retornou HTTP 200 para:
  - `login.html`.
  - `index.html`.
  - `css/responsive.css`.
  - `js/responsive.js`.

## Pendencias

- Validar visualmente em navegador real nos tamanhos 1024px, 768px, 480px e 360px.
- Validar zoom do navegador em 125%, 150% e 175%.
- Validar smartphone real e tablet real.
- Ajustar detalhes finos de layout apos revisao visual do usuario.

## Conclusao

A base responsiva foi aplicada diretamente no front-end existente de `01-mrp/front_end` com escopo controlado. O sistema segue sem dependencia de template externo e sem troca de identidade visual.
