# Git e GitHub - MRP_LOCAL

Status: atualizado para regra manual/controlada.
Versao de referencia atual: v0.1.060.

## Regra atual

- Nao fazer commit/push automatico.
- Preparar staged somente quando o usuario pedir.
- Commit/push exigem ordem explicita do usuario.
- Nao alterar internamente `.git`.
- Antes de commit, validar arquivos proibidos e `git diff --check`.

## Fluxo recomendado

```text
03-vs registra relatorios/scripts
02-docs registra regras/progresso
01-mrp executa sistema
Git guarda historico somente apos autorizacao
```

## Antes de commitar

Validar:

```powershell
git status --short
git diff --check
git diff --cached --check
git ls-files -o --exclude-standard
```

Nao versionar:
- `.env`
- `.venv` / venv
- `node_modules`
- `__pycache__`
- `*.pyc`
- `*.db`, `*.sqlite`, `*.sqlite3`
- `*.log` real
- runtime gerado
- tmp/cache
- credenciais
- `.codex`

## Regra antiga

A regra antiga de `AUTO_COMMIT_E_PUSH` automatico esta obsoleta. Historico antigo foi mantido em `02-docs/obsolete` quando aplicavel.
