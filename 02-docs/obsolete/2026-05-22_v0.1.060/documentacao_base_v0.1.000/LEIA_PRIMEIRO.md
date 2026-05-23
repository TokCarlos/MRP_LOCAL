# MRP_LOCAL — Documentação Base v0.1.000

Data de criação: 2026-05-17

Este pacote é a base documental inicial do projeto **MRP_LOCAL**.

Objetivo desta documentação:

- definir as regras obrigatórias de trabalho;
- impedir revisão cega;
- controlar versionamento;
- separar módulos;
- registrar etapas;
- proteger implementações já funcionais;
- orientar o uso em ambiente de Projeto/Codex;
- manter o desenvolvimento rastreável, reversível e organizado.

## Estado atual do projeto

O projeto está na fase de **interface visual e conceitual**.

Nesta fase, o foco é construir a interface navegável do sistema local, sem obrigação de banco real, login real, API final ou integração com arquivos reais.

## Ambiente de teste atual

Servidor de teste local conhecido:

```text
\\HOME-MACHINE
```

Acesso web esperado em ambiente local:

```text
http://HOME-MACHINE:8000
http://IP_DO_SERVIDOR:8000
```

Esses valores são apenas referência inicial. No futuro, servidor, IP, nome da máquina e caminhos devem ser configuráveis.

## Regra principal

O projeto deve evoluir por etapas pequenas, documentadas, versionadas e reversíveis.

Tudo que estiver funcional deve ser preservado.

Tudo que for alterado deve ter motivo, registro e teste.
