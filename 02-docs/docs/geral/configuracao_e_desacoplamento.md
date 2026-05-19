# Configuracao e Desacoplamento - MRP_LOCAL

Versao de referencia: v0.1.012
Data do registro: 2026-05-17
Status: `REGRA_CONFIGURACAO_MOTOR_ADAPTADOR_REGISTRADA`

## Regra central

```text
Tudo que depende do ambiente deve ser configuravel.
Tudo que e regra de negocio deve ficar isolado em motor desacoplado.
Tudo que conecta o motor ao mundo externo deve ser adaptador.
```

A logica de negocio nao deve depender do ambiente, dispositivo, rede, caminho, IP ou meio de acesso.

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

## Principio operacional

```text
O ambiente muda.
O adaptador muda.
A regra central nao muda.
```

Exemplo conceitual:

```text
2 + 2 = 4
```

Esse resultado e o mesmo em telefone, calculadora, computador, papel ou sistema. No `MRP_LOCAL`, a regra deve ser igualmente independente do meio.

## Camada CONFIGURACAO

A camada `CONFIGURACAO` guarda valores variaveis por ambiente ou operacao.

Itens previstos:

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

Configuracoes futuras devem ficar em arquivos proprios, por exemplo:

```text
config/ambiente.json
config/perfis/TESTE_HOME.json
config/perfis/PRODUCAO_TRABALHO.json
```

## Camada MOTOR

A camada `MOTOR` guarda regra central e deve ser desacoplada de interface e infraestrutura.

Itens previstos:

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

Motores futuros devem ficar desacoplados de:

- navegador
- telefone
- rede
- Tailscale
- FastAPI
- PostgreSQL
- arquivos
- Excel/VBA legado
- APIs externas

## Camada ADAPTADORES

A camada `ADAPTADORES` conecta o motor ao mundo externo.

Itens previstos:

- navegador
- telefone
- rede local
- Tailscale
- FastAPI
- PostgreSQL
- arquivos
- Excel/VBA legado
- futuras APIs externas

Adaptadores podem mudar conforme ambiente e tecnologia. Essa mudanca nao deve alterar a regra central.

## Perfis de ambiente

Perfis previstos:

- `TESTE_HOME`
- `PRODUCAO_TRABALHO`
- `FUTURO_HOMOLOGACAO`

O mesmo motor deve operar nos perfis acima sem alteracao de regra de negocio.

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

## Regras de implementacao futura

- Nao colocar IP fixo em regra de negocio.
- Nao colocar caminho local em regra de negocio.
- Nao colocar porta fixa em regra de negocio.
- Nao colocar nome de servidor em regra de negocio.
- Nao misturar regra de negocio com interface.
- Nao misturar regra de negocio com banco.
- Nao misturar regra de negocio com Tailscale ou rede local.
- Usar adaptadores para infraestrutura.
- Usar configuracao para valores variaveis.
- Usar motores para regra central.

## Controle de escopo desta etapa

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Apenas documentacao: SIM.
