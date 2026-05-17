# Teste Mobile - v0.1.015B

Data do registro: 2026-05-17
Status: `LAYOUT_MOBILE_CORRECAO_CIRURGICA_APLICADA`

## Escopo de teste

Validar que as correcoes cirurgicas nao quebraram carregamento basico e removeram os pontos de conflito identificados no relatorio v0.1.015A.

## Validacoes executadas

### 1. Sintaxe JS

Comando:

```powershell
node --check 01-mrp/front_end/js/pages/produtos_list.js
```

Resultado: aprovado.

### 2. Carregamento HTTP local temporario

Comando de teste temporario:

```powershell
py -m http.server 8015 --bind 127.0.0.1
```

Resultados:

- `http://127.0.0.1:8015/login.html` -> HTTP 200
- `http://127.0.0.1:8015/index.html` -> HTTP 200
- `http://127.0.0.1:8015/css/responsive.css` -> HTTP 200

Servidor temporario encerrado apos validacao.

### 3. Conferencia de regras-chave

Busca confirmou:

- Botao `Editar` com classe `.btn-row-action`.
- Nao existe mais regra `body.menu-open main` com margem fixa grande.
- Existe regra de espacamento unificado para logo em `.logo-area img`.

## Checklist funcional das correcoes

- [x] Menu mobile nao empurra mais o `main` com margem fixa.
- [x] Menu mobile abre como overlay abaixo do header.
- [x] Botao de linha `Editar` tem classe dedicada.
- [x] Regra global de toque nao afeta mais botoes da tabela.
- [x] Espacamento logo/titulo unificado com `clamp`.
- [x] Conflito principal entre `style.css` e `responsive.css` reduzido.

## Pendencia de validacao visual humana

Ainda recomendado validar visualmente em dispositivos reais ou em emulacao de:

- 480px
- 390px
- 360px
- zoom 125%, 150%, 175%

## Comando oficial de fechamento da versao

```powershell
powershell -ExecutionPolicy Bypass -File "X:\03-vs\scripts\git_fechar_versao.ps1" -Versao "v0.1.015" -Mensagem "corrigir layout mobile header menu e botoes" -Auto
```
