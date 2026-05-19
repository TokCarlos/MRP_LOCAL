# Protocolo de fechamento de tarefa — MRP_LOCAL

## Antes de fechar

1. Ler `REGRAS_MRP.txt`.
2. Confirmar escopo da alteração.
3. Confirmar que não houve alteração funcional indevida.
4. Validar encoding.
5. Validar JSON.
6. Validar scripts afetados.
7. Atualizar documentação afetada.
8. Remover logs reais e lixo operacional.
9. Rodar precheck Git.

## Fechamento automático

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\git_fechar_versao.ps1" -Versao "vX.Y.Z" -Mensagem "mensagem" -Auto
```

## Bloqueadores

- Mojibake.
- BOM indevido.
- Logs reais.
- Cache.
- `Thumbs.db`.
- Caminho físico fixo em scripts ativos.
- Documentação dizendo que algo está blindado sem validação real.
