# Arquivos Alterados - v0.1.009

Data do registro: 2026-05-17
Status: `FRONTEND_RESPONSIVO_BASE_EM_TESTE`

## Arquivos HTML alterados

- `03-vs/patches/v0.1.009/frontend_responsivo_base/front_end/index.html`
  - Adicionado `meta viewport`.
  - Adicionado botao de menu mobile.
  - Adicionado `id` ao menu principal.
  - Incluidos CSS de paginas da SPA.
- `03-vs/patches/v0.1.009/frontend_responsivo_base/front_end/login.html`
  - Adicionado `meta viewport`.
- `03-vs/patches/v0.1.009/frontend_responsivo_base/front_end/acesso_negado.html`
  - Adicionado `meta viewport`.
- `03-vs/patches/v0.1.009/frontend_responsivo_base/front_end/pages/produtos_list.html`
  - Tabela envolvida em `.table-responsive`.

## Arquivos CSS alterados

- `03-vs/patches/v0.1.009/frontend_responsivo_base/front_end/css/style.css`
  - Base responsiva global.
  - Breakpoints `1024px`, `768px`, `480px` e `360px`.
  - Menu mobile.
  - Ajustes de login e area de toque.
  - `.table-responsive` com rolagem horizontal.
- `03-vs/patches/v0.1.009/frontend_responsivo_base/front_end/css/pages/dashboard.css`
  - Grid responsivo com `minmax()`.
  - Cards adaptados para smartphone.
- `03-vs/patches/v0.1.009/frontend_responsivo_base/front_end/css/pages/produtos_list.css`
  - Tabela responsiva.
  - Botoes com area minima de toque.
  - Modal com largura fluida.

## Arquivos JS alterados

- `03-vs/patches/v0.1.009/frontend_responsivo_base/front_end/js/spa.js`
  - Controle de menu mobile.
  - Fechamento automatico do menu ao selecionar item.
  - Textos de log mantidos sem afetar funcionalidade.

## Arquivos nao alterados funcionalmente

- `js/auth.js`: login local `admin/admin` mantido.
- `js/api.js`: adaptador local mockado mantido.
- `js/security.js`: validacao de sessao local mantida.

## Pendencias

- Revisao visual manual em navegador real.
- Validacao em zoom alto.
- Validacao em tablet e smartphone reais.
- Aprovacao formal antes de promocao para `01-mrp`.
