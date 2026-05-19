# Configuração e desacoplamento — MRP_LOCAL

## Regra

Tudo que depende do ambiente deve ficar em configuração ou adaptador. Regra de negócio não depende de caminho físico.

## Configuração atual

Arquivo:

`01-mrp/config/mrp_local.env.json`

Responsabilidades:

- porta do frontend;
- bind;
- diretório relativo do frontend;
- diretório relativo de logs;
- nome da tarefa Windows;
- intervalo do watchdog;
- estratégia de Python/runtime.

## Raiz do projeto

A raiz deve ser resolvida automaticamente a partir dos scripts ou informada por `MRP_LOCAL_ROOT`.

## Futuro

Quando virar programa instalável, o instalador deve gerar/ajustar a configuração local sem alterar regra de negócio.
