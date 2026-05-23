---

<!-- ARQUIVO: LEIA_PRIMEIRO.md -->

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


---

<!-- ARQUIVO: docs/geral/regras_do_projeto.md -->

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


---

<!-- ARQUIVO: docs/geral/arquitetura.md -->

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


---

<!-- ARQUIVO: docs/geral/roadmap.md -->

# Roadmap — MRP_LOCAL

## Etapa 1 — Interface visual conceitual

Status: PLANEJADO / EM ANDAMENTO

Objetivo:

```text
Fechar aparência, telas, menus, fluxo e identidade visual.
```

Inclui:

```text
login visual
dashboard
menu lateral
cards
tabelas fake
formulários fake
status visuais
módulos conceituais navegáveis
```

Não inclui:

```text
banco real
login real
gravação real
integração com Excel/VBA
integração real com REDE_WORK
```

## Etapa 2 — Backend local básico

Objetivo:

```text
Subir FastAPI de forma estável no servidor local.
```

Inclui:

```text
estrutura de app
configuração por ambiente
healthcheck
rotas básicas
servir front-end
```

## Etapa 3 — Login, usuários e permissões

Objetivo:

```text
Criar autenticação local real.
```

Inclui:

```text
usuários
senhas
perfis
permissões
sessão
controle de acesso por módulo
```

## Etapa 4 — Cadastros principais

Objetivo:

```text
Criar base operacional do sistema.
```

Inclui:

```text
produtos
clientes
obras
fornecedores
usuários
setores
```

## Etapa 5 — Produção, estoque e compras

Objetivo:

```text
Modelar os módulos operacionais.
```

Inclui:

```text
ordens de produção
processos
materiais
estoque
requisições
ordens de compra
pendências
```

## Etapa 6 — REDE_WORK

Objetivo:

```text
Integrar arquivos locais e versionamento controlado.
```

Inclui:

```text
MEDIÇÕES\SERVIDOR
MEDIÇÕES\LOCAL
version
CONFIG_
manifesto
conflitos
promoção controlada
```

## Etapa 7 — Integração com Excel/VBA legado

Objetivo:

```text
Ler logs, JSON, planilhas e processos já existentes sem quebrar o que funciona.
```

Inclui:

```text
REQ
O.P
Compras
RH
logs
metadados
auditoria
```

## Etapa 8 — Substituição gradual

Objetivo:

```text
Transferir funções do Excel/VBA para o sistema web apenas quando houver equivalência funcional comprovada.
```

Regra:

```text
Nada é substituído sem comparação, teste e validação.
```


---

<!-- ARQUIVO: docs/geral/status_geral.md -->

# Status Geral — MRP_LOCAL

## Status atual

```text
Projeto: MRP_LOCAL
Versão documental: v0.1.000
Status: PLANEJADO / BASE DOCUMENTAL
Homologação: NÃO HOMOLOGADO
```

## Decisão técnica atual

O projeto deve começar pela interface visual e conceitual, antes de aprofundar banco de dados, backend real ou regra de negócio.

## Ambiente de teste

```text
Servidor de teste conhecido:
\\HOME-MACHINE
```

## Observação

O sistema ainda não substitui Excel/VBA.

Excel/VBA continua sendo a operação real onde já está funcional.

MRP_LOCAL será inicialmente uma camada visual, organizacional e futura camada de integração.


---

<!-- ARQUIVO: codex/INSTRUCOES_PARA_CODEX.md -->

# Instruções para Codex / IA de Desenvolvimento — MRP_LOCAL

## Regra principal

Não reescreva o sistema inteiro.

Trabalhe por escopo, módulo, versão e registro.

## Antes de alterar código

Leia obrigatoriamente:

```text
LEIA_PRIMEIRO.md
docs/geral/regras_do_projeto.md
docs/geral/status_geral.md
docs/geral/arquitetura.md
docs/geral/roadmap.md
```

Depois, leia a documentação do módulo afetado em:

```text
docs/modulos/<modulo>
```

## Proibições

Não fazer:

```text
reescrita total sem pedido explícito
troca de tecnologia sem justificativa
remoção de arquivos sem inventário
alteração de módulo funcional sem aviso
misturar refatoração com correção
alterar partes fora do escopo
fixar HOME-MACHINE no código como valor definitivo
introduzir dependência externa desnecessária
depender de cloud quando o objetivo é rede local
chamar protótipo de funcional sem teste real
```

## Obrigações

Sempre fazer:

```text
registrar mudança
atualizar status
preservar o que já funciona
limitar escopo
usar versionamento
separar módulo
tratar encoding e caminhos com cuidado
proteger caracteres especiais
testar o que foi alterado
informar pendências
```

## Escopo atual recomendado

A fase atual é:

```text
MRP_LOCAL_UI_CONCEITUAL
```

Prioridade:

```text
interface visual
navegação
telas fake
dados mockados
menu lateral
dashboard
padrão visual
```

Não priorizar agora:

```text
banco real
autenticação real
integração real com Excel/VBA
integração real com REDE_WORK
publicação em nuvem
```

## Servidor de teste

Referência atual:

```text
\\HOME-MACHINE
```

Mas isso deve ser configurável futuramente. Não fixar como regra definitiva do sistema.

## Resposta esperada ao concluir tarefa

Ao concluir qualquer alteração, informar:

```text
Versão:
Módulo:
Arquivos alterados:
O que foi feito:
O que foi preservado:
Teste realizado:
Status:
Pendências:
```


---

<!-- ARQUIVO: codex/PROMPT_BASE_PARA_CODEX.md -->

# Prompt Base para usar no Codex — MRP_LOCAL

Você está trabalhando no projeto MRP_LOCAL.

Antes de alterar qualquer código, leia a documentação do projeto.

Regras obrigatórias:

1. Não reescreva o sistema inteiro.
2. Não altere módulos funcionais sem aviso.
3. Não remova arquivos sem registrar.
4. Não troque arquitetura sem justificativa técnica.
5. Não introduza dependência externa desnecessária.
6. Faça apenas o escopo solicitado.
7. Atualize a documentação correspondente.
8. Registre versão, módulo, problema, solução, impacto, teste e pendências.
9. Preserve tudo que já estiver funcional.
10. Trate encoding, acentos, cedilha, espaços, caminhos UNC e nomes em português como requisito obrigatório.

Estado atual:

O projeto está na fase de interface visual e conceitual.

Prioridade atual:

- login visual;
- dashboard;
- menu lateral;
- telas fake;
- dados mockados;
- cards;
- tabelas;
- formulários;
- navegação;
- identidade visual.

Não priorizar ainda:

- banco real;
- login real;
- API completa;
- integração com Excel/VBA;
- integração real com REDE_WORK;
- substituição de processos existentes.

Servidor de teste atual:

```text
\\HOME-MACHINE
```

Mas isso deve ser configurável no futuro.

Ao terminar, retorne:

```text
Versão:
Módulo:
Arquivos alterados:
Resumo técnico:
O que foi preservado:
Testes:
Status:
Pendências:
```
