# Git e GitHub — MRP_LOCAL

## Fechamento padrão

Usar o script:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\git_fechar_versao.ps1" -Versao "vX.Y.Z" -Mensagem "mensagem" -Auto
```

## Prechecks obrigatórios

- Encoding sem mojibake.
- UTF-8 sem BOM em texto persistente.
- `git diff --check` limpo.
- Sem logs reais.
- Sem `Thumbs.db`.
- Sem cache/runtime.
- Sem credenciais.
- Sem dependência indevida de caminho físico em scripts ativos.

## Observação

O pacote limpo de entrega não precisa carregar `.git`. O repositório de trabalho real deve manter Git, mas com estado limpo.
