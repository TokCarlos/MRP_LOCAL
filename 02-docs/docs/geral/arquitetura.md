# Arquitetura Inicial — MRP_LOCAL

## Objetivo

Construir um sistema web local para operar em rede interna, usando navegador como interface, servidor local como host, FastAPI como backend, PostgreSQL como banco principal e arquivos físicos como camada documental.

## Ambiente atual de teste

```text
Servidor de teste:
\\HOME-MACHINE
```

Acesso local esperado:

```text
http://HOME-MACHINE:8000
http://IP_DO_SERVIDOR:8000
```

## Arquitetura lógica final

```text
Usuário
↓
Navegador
↓
Front-end web local
↓
FastAPI
↓
PostgreSQL
↓
Arquivos físicos / REDE_WORK
```

## Tecnologias planejadas

```text
Front-end: HTML, CSS, JavaScript ou framework futuro conforme necessidade
Backend: Python / FastAPI
Banco principal: PostgreSQL
Arquivos: estrutura local/rede, C:\REDE_WORK e pastas controladas
Acesso: rede local da empresa
Acesso externo futuro: opcional, com Tailscale ou solução segura equivalente
```

## O que não deve ser obrigatório

```text
hospedagem cloud
domínio público
StackAuth
Neon
serviço pago externo
internet para uso interno
```

## Diretriz atual

A interface visual vem primeiro.

Banco, autenticação real e regras de negócio devem entrar depois, por módulo, com documentação e versionamento.
