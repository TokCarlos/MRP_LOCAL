
# Registro de saneamento v0.1.037

Ação: base limpa para retomada de desenvolvimento.

Removido do pacote limpo:
- `.git/`
- `.codex/`
- logs reais de runtime
- `Thumbs.db`
- `03-vs/entrada_original`
- `03-vs/patches` antigos duplicados
- `03-vs/snapshots` antigos duplicados
- `03-vs/quarentena` pesada
- `03-vs/relatorios` gerados anteriormente

Mantido/criado:
- `REGRAS_MRP.txt`
- configuração central `01-mrp/config/mrp_local.env.json`
- scripts de serviço configuráveis
- watchdog contínuo
- scripts iniciais de instalador/precheck
- `MANUAL_DEV_COMPLETO.txt`
- `RESUMO_OPERACIONAL_DO_SISTEMA.txt`

Status: pacote limpo preparado. Validação operacional completa ainda depende de execução em Windows real.
