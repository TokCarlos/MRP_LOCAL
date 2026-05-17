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

## Principio de configuracao, motor e adaptadores

Status de referencia: `REGRA_CONFIGURACAO_MOTOR_ADAPTADOR_REGISTRADA`

Regra central:

```text
Tudo que depende do ambiente deve ser configuravel.
Tudo que e regra de negocio deve ficar isolado em motor desacoplado.
Tudo que conecta o motor ao mundo externo deve ser adaptador.
```

O sistema deve funcionar em `TESTE_HOME` e `PRODUCAO_TRABALHO` sem mudar regra de negocio.

Nao travar no codigo valores como:

```text
HOME-MACHINE
X:\
100.108.26.10
portas
caminhos
nomes de servidor
```

## Camadas conceituais

### CONFIGURACAO

Inclui ambiente, servidor, IP, porta, caminho raiz, modo de acesso, banco, credenciais, permissoes, tema visual e parametros operacionais.

### MOTOR

Inclui calculos, validacoes, regras de negocio, regras de permissao, processamento de estoque, processamento de producao, processamento de compras, logs tecnicos, auditoria e consistencia dos dados.

### ADAPTADORES

Inclui navegador, telefone, rede local, Tailscale, FastAPI, PostgreSQL, arquivos, Excel/VBA legado e futuras APIs externas.

## Principio operacional

```text
O ambiente muda.
O adaptador muda.
A regra central nao muda.
```

Exemplo conceitual: `2 + 2 = 4` independente de telefone, calculadora, computador, papel ou sistema. No `MRP_LOCAL`, a regra deve ser igualmente independente do meio.

## Estrutura futura sugerida

```text
01-mrp
├─ backend
│  ├─ app
│  │  ├─ core          = configuracao, settings, ambiente
│  │  ├─ engines       = motores puros de regra de negocio
│  │  ├─ services      = coordenacao de fluxos
│  │  ├─ adapters      = banco, arquivos, Excel, APIs externas
│  │  ├─ api           = rotas FastAPI
│  │  └─ models        = modelos de dados
│  └─ tests
├─ front_end
└─ config
   ├─ ambiente.json
   └─ perfis
      ├─ TESTE_HOME.json
      └─ PRODUCAO_TRABALHO.json
```

Configuracoes futuras devem ficar em arquivos proprios, por exemplo:

```text
config/ambiente.json
config/perfis/TESTE_HOME.json
config/perfis/PRODUCAO_TRABALHO.json
```

Motores futuros devem ficar desacoplados de interface e infraestrutura.

## Dominio de dados operacionais

- EMPRESA representa somente dominio interno operacional: `JPL`, `AÇO`, `TCR`.
- `GOV. RIO` nao pertence ao dominio EMPRESA; deve ficar em campos de cliente/orgao/origem de ata.
- Filtros de interface devem manter separacao entre `EMPRESA` e `ATA/ORIGEM`.
