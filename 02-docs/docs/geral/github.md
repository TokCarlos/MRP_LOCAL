# GitHub — MRP_LOCAL

GitHub é histórico técnico e rastreabilidade. Não substitui documentação operacional nem validação real.

## Regras

- Não versionar logs reais.
- Não versionar runtime, cache ou temporários.
- Não versionar credenciais.
- Não versionar pacotes `.zip` gerados, salvo exceção explícita documentada.
- Rodar validação de encoding antes de commit.
- Rodar `git diff --check` antes de commit.

## Script de fechamento

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\03-vs\scripts\git_fechar_versao.ps1" -Versao "vX.Y.Z" -Mensagem "mensagem" -Auto
```
