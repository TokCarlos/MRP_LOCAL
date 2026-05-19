# Validacao v0.1.036

Checklist previsto:

- `git status`
- `git diff --check`
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_status.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_healthcheck.ps1`

Teste opcional:

- start -> abrir `http://localhost:8765` -> status -> stop

Observacao:

- Nao executar commit/push neste patch.
