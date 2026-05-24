# REVISAO DO FLUXO DE ORDENS DE PRODUCAO - KANBAN v0.1.083

## 1. Motivo da revisao

A OP 002 criou base tecnica funcional (banco, API e CRUD), mas o fluxo visual/processual ainda esta administrativo demais para operacao diaria.

A tela principal de Ordens de Producao passa a ser um Kanban operacional por processo e status, em vez de uma visao principal em formato de tabela comum.

## 2. Nova regra do Kanban

A OP deve ser acompanhada por processo produtivo.

Estrutura oficial:

PROCESSO  
  NAO INICIADO: cards horizontais  
  EM ANDAMENTO: cards horizontais  
  CONCLUIDO: cards horizontais

Exemplo:

CORTE  
  NAO INICIADO: [OP 001] [OP 002]  
  EM ANDAMENTO: [OP 003]  
  CONCLUIDO: [OP 004]

DOBRA  
  NAO INICIADO: [OP 005]  
  EM ANDAMENTO: -  
  CONCLUIDO: -

## 3. Processos oficiais

Ordem oficial:

1. Corte
2. Dobra
3. Montagem Solda
4. Soldagem
5. Acabamento
6. Pintura
7. Sublimacao
8. Montagem
9. Teste
10. Expedicao

Keys tecnicas:

- corte
- dobra
- montagem_solda
- solda
- acabamento
- pintura
- sublimacao
- montagem
- teste
- expedicao

Observacoes:

- Visualmente usar Soldagem.
- A key tecnica pode permanecer `solda` por compatibilidade.
- Sublimacao permanece opcional/manual nesta fase.
- Expedicao tera subcontrole interno/externo em etapa futura.

## 4. Status oficiais do processo

Status tecnicos:

- NAO_INICIADO
- EM_ANDAMENTO
- CONCLUIDO

Visual:

- Nao Iniciado
- Em Andamento
- Concluido

Compatibilidade no Kanban:

- `PENDENTE` -> `NAO_INICIADO`
- `CONCLUÍDO` legado -> `CONCLUIDO`
- `PAUSADO` -> `EM_ANDAMENTO` (somente para exibicao/camada Kanban nesta etapa)

## 5. Card resumido

Cada card do Kanban principal deve conter somente:

- Numero da OP
- Cliente
- Obra
- Data de entrega
- Contador de prazo quando houver data real

Exemplo com data real:

OP 051-26  
TAPURAH-MT  
ADESAO TAPURAH-MT  
Entrega: 20/06/2026 | Faltam 28 dias

Exemplo sem data real:

OP 051-26  
TAPURAH-MT  
ADESAO TAPURAH-MT  
Entrega: NAO DEFINIDO

Nao exibir no card principal:

- BOM
- produtos
- imagem
- quantidade
- material
- observacoes longas
- processos detalhados

## 6. Prazo

Se `data_entrega_tipo = DATA` e `data_entrega_data` existir:

- diferenca > 0 -> `Faltam X dias`
- diferenca == 0 -> `Hoje`
- diferenca < 0 -> `Atrasado X dias`

Se `data_entrega_tipo = TEXTO`:

- nao calcular prazo
- exibir `data_entrega_valor`

## 7. OP macro e processo

Cada item/produto da OP tem processo proprio.

No Kanban principal, a OP macro aparece no processo mais atrasado entre os itens ativos.

Exemplo:

- 4 itens em Pintura
- 1 item em Corte

Resultado macro: a OP aparece em Corte.

## 8. Movimento

Nesta etapa nao existe drag-and-drop.

Movimento por acao:

- alterar status
- concluir
- mover para proximo processo
- pular para etapa especifica (quando habilitado)

Ao concluir processo, o sistema deve oferecer:

- mover para proximo processo
- pular para etapa especifica
- manter no processo atual concluido

Toda validacao de movimento deve ocorrer no backend.

## 9. Visual

Diretriz visual:

- estilo moderno operacional (linha Notion/Trello/Linear)
- processos em blocos retangulares verticais
- borda suave, radius alto, sombra leve
- raias horizontais por status
- cards retangulares arredondados
- rolagem horizontal por status
- sem visual de planilha/tabela como visao principal

## 10. Escopo desta etapa

Implementa:

- endpoint Kanban
- calculo de processo macro
- calculo de prazo
- renderizacao Kanban
- cards resumidos
- acoes basicas por card/status
- sem drag-and-drop

Nao implementa:

- PDF
- Excel
- estoque
- WhatsApp
- portable
- drag-and-drop

## 11. Preservacoes

Nao alterar:

- Produtos
- BOM de Produtos
- Historico da BOM
- Imagens
- Upload
- Ativar/Desativar
- `produtos_list.js/html/css`
- portable
