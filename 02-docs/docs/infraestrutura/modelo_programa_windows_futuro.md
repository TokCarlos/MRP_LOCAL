# Modelo programa Windows futuro - v0.1.050

## Objetivo

Registrar a direcao futura do MRP_LOCAL como programa Windows instalado, com instalador unico e estrutura operacional separada do repositorio DEV.

## Diferenca entre DEV e release instalado

- DEV: fonte, scripts, documentacao, relatorios e historico de evolucao.
- Release instalado: executaveis, runtime interno, bibliotecas e estrutura de operacao local.

O repositorio DEV nao deve virar pasta de build/release.

## Estrutura conceitual de programa Windows

Exemplo conceitual de artefatos:

- `MRP_LOCAL_Setup.exe`
- `MRP_Server.exe`
- `MRP_Painel.exe`
- `runtime/`
- `app/`
- `config/`
- `data/`
- `logs/`
- `db/`

## Papel de .exe, .dll, .bin, runtime e config

- `.exe`: entrada principal do programa instalado.
- `.dll`/`.pyd`/`.bin`: dependencias e componentes de runtime.
- `runtime/`: bibliotecas e interpretador empacotado quando necessario.
- `config/`: configuracoes locais do ambiente instalado.

## O que nao fazer agora

- nao gerar `.exe`;
- nao criar `.dll`, `.pyd` ou `.bin`;
- nao empacotar runtime;
- nao converter repositorio DEV em estrutura de release.

## Quando retomar

Retomar em etapa propria de build/release, apos maturidade suficiente de backend, contratos, validacao operacional e estrategia de instalador.

## Relacao com instalador futuro

- instalador unico e artefato de distribuicao;
- deve preparar estrutura local com separacao de codigo/config/runtime/dados/logs;
- nao pode depender de `X:\`, `\\HOME-MACHINE`, usuario fixo ou unidade mapeada;
- deve validar pendencias antes de concluir.

## Relacao com Python portable, FastAPI e PostgreSQL

- Python portable: candidato de runtime interno no release.
- FastAPI: backend futuro a ser empacotado no artefato instalado.
- PostgreSQL: banco real preferencial futuro (interno ou externo conforme arquitetura final).
- nesta etapa, nada disso e ativado.
