# Regras do Projeto — MRP_LOCAL

## 1. Documentação antes do código

Antes de qualquer implementação, alteração ou refatoração, deve existir documentação mínima explicando:

```text
O que será feito
Por que será feito
Qual módulo será afetado
Qual problema será resolvido
Qual regra será preservada
Qual risco existe
Qual será o status depois da alteração
```

Nenhum código deve ser alterado sem registro.

## 2. Versionamento obrigatório

Toda entrega deve ter versão própria.

Padrão:

```text
MRP_LOCAL_v0.1.000
MRP_LOCAL_v0.2.000
MRP_LOCAL_v0.2.001
MRP_LOCAL_v0.3.000
```

Leitura:

```text
v0.1.000 = base inicial
v0.2.000 = nova etapa ou módulo grande
v0.2.001 = correção pequena dentro da etapa
v0.3.000 = próximo bloco estrutural
```

Nada deve ser chamado de final ou funcional sem teste real.

## 3. Status técnico obrigatório

Cada versão, módulo ou entrega deve ter status claro.

Status permitidos:

```text
PLANEJADO
EM DESENVOLVIMENTO
IMPLEMENTADO
TESTADO LOCALMENTE
VALIDADO PELO USUÁRIO
FUNCIONAL
CONGELADO
OBSOLETO
NÃO HOMOLOGADO
```

Regra:

```text
Só pode ser marcado como FUNCIONAL ou CONGELADO depois de validação real.
```

## 4. Módulos separados

O sistema deve ser dividido por módulos, e cada módulo deve ter documentação própria.

Módulos iniciais:

```text
00_BASE_DO_SISTEMA
01_INTERFACE_UI
02_LOGIN_USUARIOS
03_DASHBOARD
04_CADASTROS
05_PRODUTOS
06_ESTOQUE
07_PRODUCAO
08_COMPRAS
09_REQUISICOES
10_ORDEM_DE_COMPRA
11_MEDICOES_CONTRATOS
12_REDE_WORK
13_RELATORIOS
14_CONFIGURACOES
15_LOGS_AUDITORIA
```

Cada módulo deve ter, quando aplicável:

```text
regras.md
estado.md
historico.md
pendencias.md
testes.md
```

## 5. O que estiver certo não deve ser mexido

Implementação já corrigida, validada ou funcional não deve ser alterada sem necessidade real.

Só pode mexer se for para:

```text
integração obrigatória
correção de erro comprovado
compatibilidade com outro módulo
melhoria estrutural documentada
segurança
padronização necessária
```

Não pode mexer por limpeza, preferência, melhoria visual genérica ou refatoração sem justificativa.

## 6. Alteração em parte funcional exige aviso

Se algo funcional precisar ser tocado, registrar antes:

```text
Módulo afetado:
Arquivo afetado:
Função ou componente afetado:
Motivo:
Risco:
Como preservar o comportamento anterior:
Como testar:
```

Integração pode exigir adaptação, mas adaptação não pode virar reescrita cega.

## 7. Separar integração de alteração

Integração não é a mesma coisa que alterar lógica.

Permitido:

```text
fazer o módulo de produtos conversar com o dashboard
```

Não permitido sem justificativa:

```text
reescrever o módulo de produtos inteiro só porque o dashboard será integrado
```

Sempre que possível, usar adaptadores, interfaces ou camadas intermediárias.

## 8. Interface visual primeiro

A etapa atual é:

```text
MRP_LOCAL_UI_CONCEITUAL
```

Objetivo:

```text
Criar interface completa, navegável e conceitual.
```

Nesta fase:

```text
não precisa gravar dados reais
não precisa PostgreSQL ativo
não precisa regra de negócio final
não precisa substituir Excel/VBA
não precisa integrar REDE_WORK ainda
```

Precisa ter:

```text
login visual
menu lateral
dashboard
telas conceituais
tabelas simuladas
cards
formulários fake
status visuais
navegação limpa
identidade visual do sistema
```

## 9. Dados simulados são permitidos nesta etapa

Na fase visual, usar dados falsos/mockados.

Exemplos:

```text
Produtos fictícios
Obras fictícias
Ordens de produção fictícias
Requisições fictícias
Ordens de compra fictícias
Medições fictícias
Logs fictícios
Usuários fictícios
```

Regra:

```text
Dado falso deve parecer real, mas deve estar claramente marcado como MOCK.
```

## 10. Servidor de teste atual

Ambiente inicial conhecido:

```text
Servidor de teste:
\\HOME-MACHINE
```

Acesso web esperado:

```text
http://HOME-MACHINE:8000
http://IP_DO_SERVIDOR:8000
```

Mas isso não pode ficar fixo no código.

Deve ser configurável futuramente em:

```text
config
.env
arquivo JSON
painel de configurações
```

## 11. Preparar para rede local

Modelo final:

```text
Usuário
↓
Navegador
↓
Servidor local da empresa
↓
FastAPI
↓
PostgreSQL
↓
Arquivos físicos / REDE_WORK
```

O sistema não deve depender obrigatoriamente de:

```text
domínio público
hospedagem cloud
StackAuth
Neon
serviços pagos
internet para funcionar internamente
```

## 12. Banco de dados não é prioridade nesta etapa

PostgreSQL continua sendo a escolha principal para o sistema robusto.

Nesta fase:

```text
Banco fica preparado.
Interface vem primeiro.
```

Não travar o avanço visual por causa de banco, login real ou API final.

## 13. Excel/VBA legado não será substituído agora

Excel/VBA continua sendo a operação real onde já funciona.

MRP_LOCAL nasce como camada visual, organizacional e futura integração.

Substituição somente gradual, documentada e validada.

## 14. REDE_WORK será módulo próprio

Estrutura conceitual:

```text
C:\REDE_WORK
├─ MEDIÇÕES
│  ├─ SERVIDOR
│  └─ LOCAL
├─ version
└─ CONFIG_
```

Regra:

```text
Robocopy alimenta SERVIDOR.
LOCAL é área de trabalho.
Promoção SERVIDOR -> LOCAL deve ser controlada.
Nunca sobrescrever LOCAL cegamente.
```

## 15. Toda alteração deve gerar registro

Cada mudança deve registrar:

```text
Data
Versão
Módulo
Arquivo
Problema
Solução
Status
Impacto
Teste feito
Pendências
```

## 16. Nenhuma entrega deve misturar tudo

Errado:

```text
mexer no login, produtos, estoque, dashboard, banco e arquivos ao mesmo tempo
```

Certo:

```text
v0.2.000 = interface visual geral
v0.2.001 = correção do menu lateral
v0.2.002 = telas fake de produtos
v0.2.003 = telas fake de produção
v0.3.000 = login local real
```

## 17. Proteção contra revisão cega

Proibido:

```text
reescrever por estilo
trocar tecnologia sem necessidade
remover código antigo sem inventário
alterar fluxo validado sem aviso
misturar correção com refatoração
chamar protótipo de funcional
```

Obrigatório:

```text
inventariar
documentar
alterar pequeno
testar
registrar
versionar
```

## 18. Regra de encoding e caminhos

Em scripts, BAT, CMD, PowerShell, Python, VBA e qualquer automação de arquivos/caminhos, tratar caracteres especiais como requisito obrigatório.

Considerar:

```text
acentos
cedilha
ordinal ª/º
espaços
nomes em português
ANSI
UTF-8
OEM do CMD
caminhos entre aspas
UNC
nomes de máquina
```

Preferir soluções blindadas que evitem depender de caracteres acentuados quando possível, usando curingas, Unicode/UTF-8 correto, caminhos entre aspas e validação visual/teste de encoding antes da entrega.

## 19. Regra máxima

O projeto deve evoluir por etapas pequenas, documentadas, versionadas e reversíveis.

Tudo que estiver funcional deve ser preservado.

Tudo que for alterado deve ter motivo, registro e teste.

## 20. Configuracao, motor e adaptadores

Regra central:

```text
Tudo que depende do ambiente deve ser configuravel.
Tudo que e regra de negocio deve ficar isolado em motor desacoplado.
Tudo que conecta o motor ao mundo externo deve ser adaptador.
```

O sistema deve funcionar em `TESTE_HOME` e `PRODUCAO_TRABALHO` sem mudar regra de negocio.

Proibido travar no codigo valores como:

```text
HOME-MACHINE
X:\
100.108.26.10
portas
caminhos
nomes de servidor
```

O projeto deve aceitar perfis de ambiente:

```text
TESTE_HOME
PRODUCAO_TRABALHO
FUTURO_HOMOLOGACAO
```

Principio:

```text
O ambiente muda.
O adaptador muda.
A regra central nao muda.
```

Exemplo: `2 + 2 = 4` independente de telefone, calculadora, computador, papel ou sistema. No `MRP_LOCAL`, regra de negocio deve ser igualmente independente do meio.

Configuracoes futuras devem ficar em arquivos proprios, por exemplo:

```text
config/ambiente.json
config/perfis/TESTE_HOME.json
config/perfis/PRODUCAO_TRABALHO.json
```

Motores futuros devem ficar desacoplados de interface e infraestrutura.
## Regra de dominio - Empresa x ATA/Cliente/Orgao

EMPRESA e um dominio fechado e representa somente empresas internas/reais do sistema.

Empresas validas:
- JPL
- AÇO
- TCR

Situacao atual:
- JPL: ativa com dados.
- AÇO: ativa com dados.
- TCR: valida para uso futuro, sem dados operacionais nesta fase.

GOV. RIO nao e empresa.
GOV. RIO deve ser tratado como cliente, orgao, origem de ata ou ata de referencia.

E proibido:
- usar GOV. RIO no campo empresa;
- usar gov_rio no campo empresa_key;
- criar produtos artificiais para TCR antes da entrada real de dados;
- misturar filtro de empresa com filtro de ATA/origem.

Filtros:
- filtro EMPRESA deve trabalhar com JPL, AÇO e futuramente TCR;
- filtro ATA/ORIGEM deve trabalhar com GOV. RIO, SEHIS - GOV. RJ e outras atas/clientes/orgaos.

GOV. RJ nao e empresa.
SEHIS nao e empresa.

## Regra de normalizacao de ATA - SEHIS / GOV. RIO

As referencias abaixo representam a mesma ATA/origem:
- ATA GOV RIO
- GOV. RIO
- GOV RIO
- ATA SEHIS - GOV. RJ
- SEHIS - GOV. RJ
- SEHIS GOV RJ
- GOV. RJ

Nome canonico no sistema:
- SEHIS - GOV. RIO

Key canonica:
- sehis_gov_rio

O numero da ATA deve ser preservado conforme os registros originais.
E proibido criar duplicidade de origem/ATA para o mesmo conjunto de produtos.

As imagens fisicas podem continuar em pasta tecnica legada, como:
- assets/produtos/gov_rio/ata_gov_rio/safe/

O caminho fisico da imagem nao define o nome logico da ATA.
Renomeacao de pasta de imagem deve ocorrer apenas em patch futuro separado com migracao controlada.

## Regra de imagens do frontend

A pasta oficial para imagens e:

`01-mrp/front_end/img/`

A pasta `assets` nao deve ser usada como raiz de imagens de produtos.

Estrutura oficial:

`img/produtos/{empresa_key}/atas/{origem_ata_key}/{arquivo}`

## Regra permanente da ATA SEHIS - GOV. RIO

Nome oficial da ATA:
- SEHIS - GOV. RIO 114443801/2025

Key oficial da ATA:
- sehis_gov_rio

Produtos oficiais desta ATA no seed ativo:
- IDs 128 ate 147

Regras:
- produtos 128-147 devem manter nome oficial e item_ata
- produtos 128-147 devem usar imagem.preview PNG real e imagem.status REAL_ATA
- IDs 148-167 sao duplicados temporarios e nao devem ficar no seed ativo
- empresa continua dominio fechado: JPL, ACO e TCR
- GOV. RIO e SEHIS nao podem ser empresa

Exemplo:

`img/produtos/aco/atas/sehis_gov_rio/item_2_1_esqui.png`

Empresas validas:
- jpl
- aco
- tcr

TCR e reservado para uso futuro e nao deve receber imagens/produtos nesta fase.

GOV. RIO nao e empresa.
SEHIS nao e empresa.
SEHIS - GOV. RIO e ATA/origem.

E proibido:
- criar `img/produtos/gov_rio`;
- criar `img/produtos/sehis`;
- criar `assets/produtos` como raiz oficial;
- usar origem_ata como empresa;
- usar cliente/orgao como empresa;
- usar `gov_rio` em `empresa_key`;
- usar `sehis_gov_rio` em `empresa_key`.

Imagens de produtos devem usar `imagem.preview` com caminho relativo ao front-end:

`img/produtos/{empresa_key}/atas/{origem_ata_key}/{arquivo}`
