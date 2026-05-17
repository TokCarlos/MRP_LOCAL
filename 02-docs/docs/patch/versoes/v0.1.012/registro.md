# Registro v0.1.012 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `REGRA_CONFIGURACAO_MOTOR_ADAPTADOR_REGISTRADA`

## Objetivo

Registrar o principio de configuracao, motores e adaptadores para garantir que a logica de negocio do `MRP_LOCAL` nao dependa de ambiente, dispositivo, rede, caminho, IP ou meio de acesso.

## Arquivos criados ou atualizados

- `02-docs/docs/geral/arquitetura.md`.
- `02-docs/docs/geral/regras_do_projeto.md`.
- `02-docs/docs/geral/configuracao_e_desacoplamento.md`.
- `02-docs/docs/patch/versoes/v0.1.012/registro.md`.

## Regra central registrada

```text
Tudo que depende do ambiente deve ser configuravel.
Tudo que e regra de negocio deve ficar isolado em motor desacoplado.
Tudo que conecta o motor ao mundo externo deve ser adaptador.
```

## Camadas registradas

### CONFIGURACAO

- ambiente
- servidor
- IP
- porta
- caminho raiz
- modo de acesso
- banco
- credenciais
- permissoes
- tema visual
- parametros operacionais

### MOTOR

- calculos
- validacoes
- regras de negocio
- regras de permissao
- processamento de estoque
- processamento de producao
- processamento de compras
- logs tecnicos
- auditoria
- consistencia dos dados

### ADAPTADORES

- navegador
- telefone
- rede local
- Tailscale
- FastAPI
- PostgreSQL
- arquivos
- Excel/VBA legado
- futuras APIs externas

## Principios registrados

- O sistema deve funcionar em `TESTE_HOME` e `PRODUCAO_TRABALHO` sem mudar regra de negocio.
- Nao travar no codigo valores como `HOME-MACHINE`, `X:\`, `100.108.26.10`, portas, caminhos ou nomes de servidor.
- O ambiente muda.
- O adaptador muda.
- A regra central nao muda.
- Motores futuros devem ficar desacoplados de interface e infraestrutura.

## Exemplo conceitual registrado

`2 + 2 = 4` independente de telefone, calculadora, computador, papel ou sistema. No `MRP_LOCAL`, a regra deve ser igualmente independente do meio.

## Configuracoes futuras registradas

```text
config/ambiente.json
config/perfis/TESTE_HOME.json
config/perfis/PRODUCAO_TRABALHO.json
```

## Estrutura futura registrada

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

## Controle de escopo

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Apenas documentacao: SIM.
