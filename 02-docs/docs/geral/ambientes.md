# Ambientes — MRP_LOCAL

## DEV atual

O ambiente atual é local-first e de teste. A raiz física pode ser diferente entre máquinas; por isso os scripts devem resolver a raiz automaticamente ou usar `MRP_LOCAL_ROOT`.

## Regra

Nenhuma regra de negócio deve depender de letra de unidade, usuário Windows, nome da máquina, IP fixo ou porta fora da configuração.

## Configuração oficial

Arquivo:

`01-mrp/config/mrp_local.env.json`

Campos principais:

- `frontend.port`
- `frontend.bind`
- `frontend.relative_dir`
- `logs.relative_dir`
- `windows_task.name`
- `watchdog.interval_seconds`

## Produção futura

A produção deve usar instalação/empacotamento controlado, com precheck, runtime, configuração, tarefa/watchdog e healthcheck.
