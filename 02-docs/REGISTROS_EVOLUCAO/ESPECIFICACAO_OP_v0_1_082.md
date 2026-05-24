# ESPECIFICAÇÃO TÉCNICA — MÓDULO ORDENS DE PRODUÇÃO v0.1.082

## 1. Objetivo do módulo

O módulo Ordens de Produção será um módulo novo do sistema MRP_LOCAL.

A OP será um registro operacional no banco de dados, e não um arquivo Excel/PDF.

PDF/Excel/exportação ficam para etapa futura.

O módulo OP deve:
- criar ordens de produção;
- vincular produtos já existentes;
- copiar snapshot da BOM dos produtos;
- calcular consumo real pela quantidade da OP;
- controlar processos produtivos;
- permitir edição da OP;
- registrar histórico;
- preparar integração futura com estoque e dashboards.

## 2. Regra principal de preservação

O módulo Produtos NÃO deve ser alterado.

A OP pode consultar:
- produto_id;
- produto_key;
- item_ata;
- nome_oficial;
- empresa_key;
- empresa_nome;
- ata_key;
- ata_nome;
- numero_ata;
- imagem_path;
- BOM do produto.

Mas a OP NÃO pode alterar:
- cadastro do produto;
- imagem do produto;
- status ativo/desativado do produto;
- BOM padrão do produto;
- histórico da BOM do produto.

## 3. Relação entre Produto, BOM e OP

Produto = cadastro técnico.  
BOM do Produto = padrão técnico unitário.  
OP = documento operacional vivo no banco.  
Produto dentro da OP = item operacional com quantidade.  
BOM da OP = snapshot da BOM do Produto, multiplicada pela quantidade da OP.

Regra crítica:  
Quando um produto é adicionado à OP, o sistema copia a BOM atual do produto para a OP.

Depois disso:
- alteração futura na BOM do produto não altera OP antiga;
- edição da BOM da OP não altera o produto;
- edição da BOM da OP altera somente aquela OP.

## 4. Cabeçalho da OP

A OP deve possuir os seguintes campos conceituais:

- id
- numero_op
- ano
- seq
- rev
- empresa_key
- empresa_nome
- ata_key
- ata_nome
- numero_ata
- cliente
- obra
- modelo
- tipo
- material
- solicitante
- data_entrega_tipo
- data_entrega_data
- data_entrega_valor
- status
- observacoes
- created_at
- updated_at
- created_by
- ativo

Explicação:
- empresa_key é técnica: aco, jpl, tcr.
- empresa_nome é visual: Aço, JPL, TCR.
- Aço/JPL/TCR no cabeçalho da OP representam a empresa da ATA regente, não o material.
- material é outro campo: CARBONO, INOX, CARBONO+INOX etc.

## 5. Numeração da OP

A numeração da OP deve seguir padrão inspirado no VBA atual, mas controlado pelo backend.

Formato inicial:  
NNN-AA

Exemplo:
- 001-26
- 002-26
- 051-26

Regras:
- NNN é sequência anual com 3 dígitos.
- AA é ano com 2 dígitos.
- A sequência reinicia a cada ano.
- O backend deve garantir sequência segura.
- O número não deve ser digitado manualmente na criação normal.
- Futuramente pode existir ajuste administrativo protegido.

Tabela ou mecanismo recomendado:  
op_contadores:
- ano
- ultimo_seq
- updated_at

## 6. Data de entrega

A data de entrega da OP deve ser editável e flexível.

Deve aceitar:
- data real;
- texto controlado/livre.

Campos:
- data_entrega_tipo
- data_entrega_data
- data_entrega_valor

Exemplos:

Caso data real:  
data_entrega_tipo = DATA  
data_entrega_data = 2026-06-20  
data_entrega_valor = 20/06/2026

Caso texto:  
data_entrega_tipo = TEXTO  
data_entrega_data = NULL  
data_entrega_valor = NÃO DEFINIDO

Textos aceitos inicialmente:
- NÃO DEFINIDO
- A DEFINIR
- URGENTE
- AGUARDANDO CLIENTE
- SEM DATA

Regra:  
Dashboards futuros usam data_entrega_data quando existir.  
A tela mostra data_entrega_valor.

## 7. Produtos dentro da OP

Cada OP pode ter vários produtos.

Tabela conceitual:  
ordem_producao_produtos

Campos:
- id
- op_id
- produto_id
- produto_key
- item_ata
- nome_produto
- empresa_key
- empresa_nome
- ata_key
- ata_nome
- numero_ata
- imagem_path
- quantidade
- quantidade_inauguracao
- material
- ordem_item
- observacao
- ativo
- created_at
- updated_at

Regras:
- produto_id referencia produtos.id.
- Os demais campos são snapshot no momento da inclusão.
- A quantidade do produto multiplica a BOM.
- Alterar quantidade recalcula quantidade_total da BOM da OP.
- Remover produto da OP não remove produto do cadastro.
- Remoção deve ser lógica, ativo = 0.

## 8. BOM da OP

Tabela conceitual:  
ordem_producao_bom

Campos:
- id
- op_id
- op_produto_id
- produto_id
- bom_item_id_origem
- grupo
- cod
- material
- dim1
- dim2
- espessura
- revestimento
- tamanho
- unidade
- quantidade_unitaria
- quantidade_produto
- quantidade_total
- ordem_item
- editado_manual
- ativo
- created_at
- updated_at

Regra:  
quantidade_total = quantidade_unitaria x quantidade_produto

Grupos:
- TUBOS
- CHAPAS
- INSUMOS

TUBOS e CHAPAS usam tamanho.  
INSUMOS usa unidade.

O cod da BOM é alfanumérico.

Editar BOM da OP:
- permitido;
- altera somente a OP;
- marca editado_manual = 1;
- registra histórico.

## 9. Processos produtivos da OP

Os processos antigos simples Corte/Pintura/Expedição são insuficientes.

Processos padrão corretos:

1. Corte
2. Dobra
3. Montagem Solda
4. Solda
5. Acabamento
6. Pintura
7. Sublimação
8. Montagem
9. Teste
10. Expedição

Tabela conceitual:  
ordem_producao_processos

Campos:
- id
- op_id
- op_produto_id
- processo_key
- processo_nome
- ordem
- quantidade_planejada
- quantidade_concluida
- quantidade_falta
- status
- observacao
- created_at
- updated_at

Processo keys:
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

Regra:  
Ao adicionar produto à OP, criar processos padrão para esse produto.

quantidade_planejada = quantidade do produto  
quantidade_concluida = 0  
quantidade_falta = quantidade_planejada

Ao atualizar quantidade_concluida:  
quantidade_falta = quantidade_planejada - quantidade_concluida

## 10. Histórico da OP

Tabela conceitual:  
ordem_producao_historico

Campos:
- id
- op_id
- entidade
- entidade_id
- acao
- detalhe
- dados_antes
- dados_depois
- created_at
- created_by

Eventos iniciais:
- OP_CRIADA
- OP_EDITADA
- PRODUTO_ADICIONADO
- PRODUTO_REMOVIDO
- QUANTIDADE_ALTERADA
- BOM_OP_EDITADA
- DATA_ENTREGA_ALTERADA
- STATUS_ALTERADO
- PROCESSO_ATUALIZADO
- OBSERVACAO_ALTERADA

Regra:  
Toda alteração relevante na OP deve registrar histórico.

## 11. Status da OP

Status iniciais recomendados:
- RASCUNHO
- PLANEJADA
- EM_PRODUCAO
- PAUSADA
- CONCLUIDA
- CANCELADA

A tela deve permitir alteração de status.  
Toda alteração deve registrar histórico.

## 12. API conceitual

Rotas planejadas:

OP:
GET    /api/ordens-producao  
POST   /api/ordens-producao  
GET    /api/ordens-producao/{op_id}  
PUT    /api/ordens-producao/{op_id}  
DELETE /api/ordens-producao/{op_id}

Produtos da OP:
GET    /api/ordens-producao/{op_id}/produtos  
POST   /api/ordens-producao/{op_id}/produtos  
PUT    /api/ordens-producao/{op_id}/produtos/{op_produto_id}  
DELETE /api/ordens-producao/{op_id}/produtos/{op_produto_id}

BOM da OP:
GET    /api/ordens-producao/{op_id}/bom  
PUT    /api/ordens-producao/{op_id}/bom

Processos:
GET    /api/ordens-producao/{op_id}/processos  
PUT    /api/ordens-producao/{op_id}/processos/{processo_id}

Histórico:
GET    /api/ordens-producao/{op_id}/historico

Exportação futura, fora desta primeira etapa:
POST   /api/ordens-producao/{op_id}/exportar/pdf  
POST   /api/ordens-producao/{op_id}/exportar/xlsx

## 13. UI conceitual

A UI deve seguir o mesmo padrão visual do módulo Produtos.

Tela:  
Ordens de Produção

Componentes:
- filtros no topo;
- botão Nova OP;
- cards de OP;
- ações por card;
- janelas/modais flutuantes;
- layout responsivo;
- padrão visual compatível com produtos_list.

Card da OP deve mostrar:
- número da OP;
- empresa da ATA regente;
- cliente;
- obra;
- data de entrega;
- status;
- quantidade de produtos;
- total de unidades;
- ações.

Ações iniciais:
- Abrir
- Editar
- Produtos
- BOM
- Processos
- Histórico

## 14. Criação da OP

Fluxo conceitual:

1. Usuário clica Nova OP.
2. Sistema gera número da OP.
3. Usuário preenche cabeçalho.
4. Usuário seleciona produtos existentes.
5. Sistema consulta Produtos.
6. Sistema copia dados do Produto para ordem_producao_produtos.
7. Sistema copia BOM do Produto para ordem_producao_bom.
8. Sistema cria processos padrão.
9. Sistema registra histórico.
10. OP aparece como card.

## 15. Regra de ATA regente

A OP deve possuir empresa/ATA regente.

Regra inicial recomendada:  
A OP deve preferencialmente conter produtos da mesma empresa/ATA regente.

Ao adicionar produto de empresa/ATA diferente:
- o sistema deve bloquear; ou
- exigir confirmação administrativa em etapa futura.

Para primeira implementação, registrar como regra recomendada:  
não misturar empresas/ATAs diferentes na mesma OP.

## 16. Exportação futura

Exportação PDF/Excel não faz parte do núcleo inicial.

O Excel/VBA atual servirá apenas como referência visual e conceitual.

O sistema deverá futuramente recriar o padrão visual da OP em HTML/CSS, sem depender do Excel.

A OP real fica no banco.

## 17. Portable

O módulo OP deverá ter versão portable reduzida futuramente.

Portable deve ser equivalente em comportamento essencial, mas pode usar JSON/runtime em vez de SQLite.

Nesta especificação, portable é necessário, mas a implementação pode ser faseada.

## 18. O que NÃO fazer na implementação futura

- não alterar módulo Produtos;
- não alterar BOM do Produto ao editar OP;
- não usar Excel como fonte de dados;
- não gerar PDF automaticamente ao criar OP;
- não implementar estoque nesta primeira etapa;
- não implementar WhatsApp nesta primeira etapa;
- não misturar exportação com núcleo da OP;
- não apagar dados existentes;
- não refatorar produtos_list.js nesta etapa.

## 19. Validação desta documentação

Após criar o arquivo, relatório desta tarefa:

- caminho do arquivo criado:
`02-docs/REGISTROS_EVOLUCAO/ESPECIFICACAO_OP_v0_1_082.md`
- arquivos alterados:
`02-docs/REGISTROS_EVOLUCAO/ESPECIFICACAO_OP_v0_1_082.md`
- confirmação:
foi apenas documentação.
- confirmação:
Produtos não foi alterado.
- confirmação:
não foi criada migração.
- confirmação:
não foi criado backend/frontend funcional.
