# REGISTRO DO ESTADO ATUAL — MRP_LOCAL v0.1.081

## 1. Objetivo deste registro

Este arquivo congela documentalmente o estado funcional atual do sistema antes do inicio do modulo de Ordens de Producao.

O proximo modulo sera criado de forma incremental, sem sobrescrever ou degradar o modulo Produtos/BOM/Imagens.

## 2. Estrutura geral atual do projeto

- `01-mrp/` como sistema oficial/dev principal.
- `01-mrp/front_end/` como frontend oficial.
- `01-mrp/back_end/` como backend oficial.
- `01-mrp/data/` como dados locais oficiais, banco SQLite e midia.
- `01-mrp/infrastructure/` como estrutura de migracoes/persistencia.
- `portable/` como versao portatil reduzida.
- `portable/app/frontend/` como frontend portable.
- `portable/app/backend/` como backend portable.
- `portable/runtime/` como runtime portable.
- `03-vs/` como area de scripts, painel e ferramentas operacionais.
- `02-docs/` como documentacao tecnica.

## 3. Modulo Produtos — estado atual

O modulo Produtos esta funcional e deve ser tratado como concluido nesta fase.

- Produtos possuem `id` numerico interno.
- Produtos possuem `produto_key` textual tecnico.
- Produtos possuem `item_ata`.
- Produtos possuem `nome_oficial`.
- Produtos possuem `categoria`.
- Produtos possuem `imagem_path`.
- Produtos possuem status `ativo`.
- Produto ativo/desativado esta funcional.
- O botao/estado correto e `Ativar/Desativar`.
- Nao usar logica antiga de `Inativar`.
- Produto desativado mantem opacidade visual `0.40`.
- Numero do item aparece abaixo da imagem no card.
- Produtos NAO devem ser alterados diretamente por futuros modulos, apenas consultados.

## 4. Padronizacao `aco` / `Aco`

Regra oficial:

- `aco` e chave tecnica.
- `Aco` e texto visual.
- `ao` e errado como chave.
- `aco`, `ACO` ou acento em path/chave tecnica nao deve ser usado fora do padrao tecnico oficial.
- `ACO` maiusculo nao deve ser usado como chave nova.
- `empresa_key = aco`.
- `empresa_nome = Aco`.

Aplicar o mesmo conceito para outras empresas:

- `jpl` tecnico, `JPL` visual.
- `tcr` tecnico, `TCR` visual.

Padrao de uso:

- Em paths, slugs, JSON tecnico, banco, API e chaves internas, usar padrao limpo sem acento.
- Em texto visivel para usuario, usar nome correto visual.

## 5. Imagens de Produtos — estado atual

- A imagem oficial do produto e controlada pelo backend.
- O banco guarda o caminho em `produtos.imagem_path`.
- O frontend so usa imagens locais como preview/fallback.
- O upload novo deve ser feito contra o `produto_id`.
- O backend busca o produto e amarra a imagem pela relacao `empresa_key + ata_key + item_ata`.
- Modelo adotado: imagem unica oficial por produto.
- Novo upload substitui a imagem oficial anterior.
- Dados do produto, BOM e historico nao devem ser alterados ao trocar imagem.
- Se a imagem oficial nao existir, o frontend usa preview local.
- Se o preview local nao existir, usa placeholder.

Estrutura recomendada/atual para novas imagens:

`media/produtos/{empresa_key}/{ata_key}/item_{item_ata}.{ext}`

Exemplo:

`media/produtos/aco/cimasp_029_2025/item_057.png`

As imagens antigas do frontend ainda podem existir como fallback ate futura migracao/auditoria.

## 6. BOM de Produto — estado atual

A BOM do produto esta estruturada e funcional.

Campos oficiais:

- `grupo`
- `cod`
- `material`
- `dim1`
- `dim2`
- `espessura`
- `revestimento`
- `tamanho`
- `unidade`
- `quantidade`
- `ordem`
- `ativo`

Grupos:

- `TUBOS`
- `CHAPAS`
- `INSUMOS`

Estrutura visual:

TUBOS:
`COD | MATERIAL | DIM1 | DIM2 | ESPESSURA | REVESTIMENTO | TAMANHO | QUANTIDADE`

CHAPAS:
`COD | MATERIAL | DIM1 | DIM2 | ESPESSURA | REVESTIMENTO | TAMANHO | QUANTIDADE`

INSUMOS:
`COD | MATERIAL | DIM1 | DIM2 | ESPESSURA | REVESTIMENTO | UNIDADE | QUANTIDADE`

Regra:

- Tubos e Chapas usam `tamanho`.
- Insumos usa `unidade`.
- `cod` e alfanumerico.
- A BOM do produto e o padrao tecnico unitario.
- A BOM do produto nao deve ser alterada por uma OP; a OP deve copiar snapshot.

Descritivos visuais:

- TUBOS -> PECAS TUBULARES
- CHAPAS -> PECAS DE CHAPARIA
- INSUMOS -> MONTAGEM, INSTALACAO E ACABAMENTO

## 7. Edicao da BOM — estado atual

- Janela Editar BOM e flutuante.
- Janela pode ser arrastada.
- Campos estao alinhados.
- Cabecalho usa `TAMANHO / UN.`.
- Nao existe mais label interno redundante `TAMANHO` dentro da celula.
- A edicao da BOM de Produto altera apenas a BOM padrao do Produto.
- Futuros modulos devem consultar a BOM e copiar snapshot quando necessario.

## 8. Historico da BOM — estado atual

- Existe botao no topo da BOM:
`Ultima atualizacao: DDD - DD/MM/AAAA - HH:MM`
- Se nao houver historico:
`Ultima atualizacao: sem registro`
- Ao clicar, abre janela flutuante de historico.
- Historico e por produto.
- Historico mostra:
`DATA/HORA | ACAO | GRUPO | COD | MATERIAL | DETALHE`
- Historico registra:
`item adicionado`, `item modificado`, `item removido`, `BOM atualizada`, `historico limpo`.
- Limpeza de historico nao aparece na UI comum.
- Limpeza fica apenas no Painel Administrativo Local protegido.

## 9. Backend oficial — estado atual

Arquitetura:

- `routes` para API HTTP.
- `services` para regras de negocio.
- `repositories` para banco/persistencia.
- `domain` para modelos.
- `core` para normalizacao/utilitarios.
- `contracts` para contratos/documentacao de API.

O backend oficial usa SQLite.

Banco principal:

`01-mrp/data/db/mrp_local_dev.sqlite`

Tabelas atuais relevantes:

- `produto_base_ata`
- `produtos`
- `produto_bom`
- `produto_bom_historico`

As rotas de Produtos, Imagens, BOM e Historico da BOM ja existem e devem ser preservadas.

## 10. Portable — estado atual

- Portable e uma versao reduzida, mas funcional.
- Deve acompanhar comportamento essencial do oficial.
- Portable usa runtime/JSON quando adequado.
- Portable nao precisa ser identico ao oficial em infraestrutura, mas deve ser equivalente em comportamento.
- Produtos, BOM, historico BOM e upload de imagem devem funcionar tambem no portable.
- `portable/runtime/` e a area de dados runtime do portable.

## 11. Painel Administrativo Local — estado atual

- Painel administrativo existe.
- Deve concentrar tarefas protegidas.
- Funcoes sensiveis nao devem aparecer na UI comum.
- Limpeza de historico da BOM fica no painel.
- Futuramente o painel deve receber auditorias, migracoes, validacoes e manutencoes.

## 12. Regras de preservacao para proximos modulos

Futuros modulos, principalmente Ordens de Producao, NAO PODEM:

- alterar Produtos diretamente;
- alterar BOM padrao do Produto diretamente;
- quebrar Ativar/Desativar;
- quebrar opacidade `0.40`;
- remover numero do item abaixo da imagem;
- remover historico da BOM;
- alterar upload de imagens sem necessidade;
- alterar `aco/Aco` fora do padrao;
- substituir backend portable por logica incompleta;
- remover compatibilidade existente.

## 13. Proximo modulo planejado: Ordens de Producao

O proximo modulo sera `Ordens de Producao`.

Diretriz:

- Produtos serao apenas consultados.
- A OP tera modelo proprio de dados.
- A OP tera produtos vinculados.
- A OP copiara snapshot da BOM do Produto.
- A OP tera BOM operacional propria e editavel.
- Editar BOM da OP NAO altera BOM do Produto.
- A OP tera processos proprios.
- A OP tera historico proprio.
- A OP sera representada em cards seguindo o padrao visual do modulo Produtos.
- Exportacao PDF/Excel nao entra no primeiro momento.
- O Excel/VBA atual e referencia visual e conceitual, nao motor operacional.

## 14. Processos padrao futuros da OP

Processos corretos:

1. Corte
2. Dobra
3. Montagem Solda
4. Solda
5. Acabamento
6. Pintura
7. Sublimacao
8. Montagem
9. Teste
10. Expedicao

Os processos antigos simples `Corte/Pintura/Expedicao` sao insuficientes para o novo modulo.

## 15. Data de entrega da OP

Regra futura:

- Data de entrega sera editavel.
- Deve aceitar data real.
- Deve aceitar texto controlado/livre, como:
`NAO DEFINIDO`, `A DEFINIR`, `URGENTE`, `AGUARDANDO CLIENTE`, `SEM DATA`.
- Banco deve separar data real de texto exibido.
- Dashboard futuro deve usar data real quando existir.

## 16. Validacao final desta tarefa documental

Conferencia desta tarefa:

- arquivo criado no local documental correto;
- nenhum arquivo funcional foi alterado por esta tarefa;
- nenhuma migracao foi criada;
- nenhum patch funcional foi aplicado;
- documentacao em UTF-8.

Relatorio final simples desta tarefa:

- caminho do arquivo criado:
`02-docs/REGISTROS_EVOLUCAO/REGISTRO_ESTADO_ATUAL_v0_1_081.md`
- lista de arquivos alterados nesta tarefa:
`02-docs/REGISTROS_EVOLUCAO/REGISTRO_ESTADO_ATUAL_v0_1_081.md`
- confirmacao:
nenhuma logica funcional foi mexida nesta tarefa documental.
