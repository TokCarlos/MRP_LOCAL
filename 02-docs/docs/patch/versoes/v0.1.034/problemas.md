# v0.1.034 — Problema corrigido

## Problema

Na v0.1.033, o arquivo `01-mrp/front_end/js/pages/produtos_list.js` recebeu chamadas para `escapeHtml(...)` durante a proteção básica contra injeção HTML, mas a função auxiliar não foi incluída no arquivo ativo.

## Efeito

Ao carregar a tela de Produtos, a renderização da tabela era interrompida por erro JavaScript (`ReferenceError: escapeHtml is not defined`). Com isso, os produtos ativos podiam deixar de aparecer na interface, mesmo com `produtos_seed.json` preservado.

## Classificação

```text
Tipo: HOTFIX
Área: Frontend / Produtos
Risco: Alto na tela de Produtos
Dados perdidos: NÃO
Banco real: NÃO EXISTE AINDA
JSON ativo preservado: SIM
```
