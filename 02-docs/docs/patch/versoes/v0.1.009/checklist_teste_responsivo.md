# Checklist de Teste Responsivo - v0.1.009

Data do registro: 2026-05-17
Status: `FRONTEND_RESPONSIVO_BASE_EM_TESTE`

## Preparacao

- [x] Criar patch em `03-vs/patches/v0.1.009/frontend_responsivo_base`.
- [x] Copiar `01-mrp/front_end` para o patch.
- [x] Trabalhar primeiro no patch.
- [x] Documentar em `02-docs/docs/patch/versoes/v0.1.009`.

## HTML

- [x] Verificar `index.html`.
- [x] Verificar `login.html`.
- [x] Verificar `acesso_negado.html`.
- [x] Adicionar `meta viewport` nos HTML principais.

## CSS responsivo

- [x] Aplicar `box-sizing: border-box` global.
- [x] Usar `clamp()` em fontes e espacamentos principais.
- [x] Usar `flex-wrap` no header/menu.
- [x] Usar grid responsivo no dashboard.
- [x] Usar `overflow-x: auto` para tabela.
- [x] Criar breakpoints `1024px`, `768px`, `480px` e `360px`.
- [x] Ajustar area minima de toque para botoes/campos.

## JS

- [x] Criar controle de abrir/fechar menu mobile em `js/spa.js`.
- [x] Manter login local `admin/admin`.
- [x] Nao alterar autenticacao funcional.

## Validacao executada

- [x] `node --check js/spa.js`.
- [x] `node --check js/auth.js`.
- [x] `node --check js/api.js`.
- [x] HTTP 200 em `http://127.0.0.1:8099/login.html`.
- [x] HTTP 200 em `http://127.0.0.1:8099/index.html`.

## Teste manual pendente

- [ ] Testar `http://localhost:8000/login.html` em desktop.
- [ ] Testar `http://localhost:8000/index.html` em desktop.
- [ ] Testar largura 1024px.
- [ ] Testar largura 768px.
- [ ] Testar largura 480px.
- [ ] Testar largura 360px.
- [ ] Testar zoom 125%.
- [ ] Testar zoom 150%.
- [ ] Testar zoom 175%.
- [ ] Testar smartphone real.
- [ ] Testar tablet real.
- [ ] Validar menu mobile abrindo e fechando.
- [ ] Validar dashboard em uma coluna no smartphone.
- [ ] Validar tabela com rolagem horizontal controlada.

## Criterio para promocao futura

Promover para `01-mrp` somente depois de teste visual/manual aprovado e registro formal de promocao.
