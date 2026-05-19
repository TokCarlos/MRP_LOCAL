# Regras do Projeto — MRP_LOCAL

A fonte absoluta atual é `REGRAS_MRP.txt` na raiz do projeto.

Este arquivo existe apenas como ponte documental para evitar divergência entre regras antigas e regras consolidadas.

## Regra operacional

Antes de qualquer execução grande, ler:

`REGRAS_MRP.txt`

## Resumo não substitutivo

- Sistema local-first.
- Configuração/motor/adaptador separados.
- Regra de negócio sem dependência de caminho físico, usuário Windows, drive mapeado, IP fixo ou Tailscale.
- UTF-8 sem BOM para texto persistente.
- Texto visual com acento correto; keys técnicas ASCII-safe.
- Logs reais fora do versionamento.
- Nada é final/blindado sem validação real.
- Futuro: empacotar como programa instalável com precheck, runtime, configuração, firewall, tarefa/watchdog e healthcheck.
