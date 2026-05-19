# Queda de energia — MRP_LOCAL

## Estado real

Ainda não validado.

## Requisitos para considerar estável

- Windows inicia após retorno de energia.
- Tarefa Windows dispara corretamente.
- Watchdog inicia.
- Frontend volta a responder.
- Logs registram o ciclo.
- Acesso local e LAN funcionam.

## Observação

Se a máquina exigir login manual, a estratégia de tarefa/serviço deve ser ajustada. Não declarar blindagem antes do teste real.
