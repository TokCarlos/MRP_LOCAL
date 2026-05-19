# Status Geral â€” MRP_LOCAL

## Status atual

```text
Projeto: MRP_LOCAL
VersÃ£o documental: v0.1.002
Status: PLANEJADO / BASE DOCUMENTAL
HomologaÃ§Ã£o: NÃƒO HOMOLOGADO
```

## DecisÃ£o tÃ©cnica atual

O projeto deve comeÃ§ar pela interface visual e conceitual, antes de aprofundar banco de dados, backend real ou regra de negÃ³cio.

## Ambiente de teste

```text
Servidor de teste conhecido:
\\HOME-MACHINE
```

## ObservaÃ§Ã£o

O sistema ainda nÃ£o substitui Excel/VBA.

Excel/VBA continua sendo a operaÃ§Ã£o real onde jÃ¡ estÃ¡ funcional.

MRP_LOCAL serÃ¡ inicialmente uma camada visual, organizacional e futura camada de integraÃ§Ã£o.


## Estrutura fÃ­sica oficial

```text
01-mrp
02-docs
03-vs
```

Status da estrutura: DEFINIDO em v0.1.002.

## Atualizacao v0.1.027

- Dominio de empresas corrigido para: JPL, AÃ‡O e TCR.
- GOV. RIO reclassificado para dominio de ATA/origem/cliente/orgao.
- TCR mantido como empresa valida futura, sem dados operacionais.
- Nenhum backend criado.
- Nenhuma persistencia real implementada.
- Alteracao restrita ao CRM visual/seed/config/documentacao.

## Atualizacao v0.1.028

- ATA GOV RIO / SEHIS GOV RJ normalizada para `SEHIS - GOV. RIO`.
- Numero da ATA preservado nos registros existentes.
- GOV. RIO permanece fora do dominio empresa.
- Empresas validas mantidas: JPL, AÃ‡O e TCR.
- TCR permanece sem dados operacionais.
- Imagens reais preservadas sem renomear/mover arquivos.
- Nenhum backend criado.
- Nenhum banco criado.
- Alteracao restrita a seed/config/filtros/documentacao/validacao.

## Atualizacao v0.1.030

- Imagens reorganizadas para `01-mrp/front_end/img`.
- Estrutura oficial aplicada: `img/produtos/{empresa}/atas/{origem}`.
- `assets/produtos` tratado como legado e movido para quarentena.
- Produtos 128-147 preservaram nomes e `item_ata`.
- Previews reais corrigidos para ATA `SEHIS - GOV. RIO`.
- GOV. RIO removido da estrutura de empresa de imagens.
- Sem backend.
- Sem banco.
- Sem alteracao funcional alem da resolucao correta de imagem.

## Atualizacao v0.1.031

- Auditoria de limpeza estrutural executada (nao destrutiva).
- Nenhum arquivo removido, movido ou alterado funcionalmente.
- Relatorios gerados em `03-vs/relatorios/limpeza`.
- Proxima etapa de limpeza depende de aprovacao manual.

## Atualizacao v0.1.031

- Nome oficial da ATA consolidado para `SEHIS - GOV. RIO 114443801/2025`.
- Produtos oficiais da ATA mantidos nos IDs 128-147.
- Previews dos IDs 128-147 migrados para PNG real por pareamento de `item_ata`.
- IDs 148-167 removidos do seed ativo e enviados para quarentena documental.
- Duplicidade de `produto_key` removida do seed ativo.
- Dominio de empresa preservado: JPL, ACO, TCR (TCR sem dados operacionais).
- Sem backend e sem banco.

## Atualizacao v0.1.032

- Erro de encoding detectado em textos visuais (mojibake).
- Nome visual da empresa corrigido para `AÃ‡O` nos dados ativos, removendo mojibake.
- Regra absoluta de encoding documentada como bloqueadora de commit.
- Validacao obrigatoria de encoding criada em `03-vs/scripts/validar_encoding.ps1`.
- Relatorios de encoding gerados em `03-vs/relatorios/encoding`.

## Atualizacao v0.1.033

- CorreÃ§Ã£o preventiva executada sem backend e sem banco real.
- `produtos_seed.json` permanece com 147 produtos ativos: JPL 53, AÃ‡O 94, TCR 0.
- `imagem.preview` e `imagem.pasta` alinhados para `img/produtos`.
- `catalogo_ata_gov_rio.json` corrigido para caminhos fÃ­sicos existentes.
- Validador de encoding ajustado para evitar falso positivo e nÃ£o validar o prÃ³prio script.
- Auditoria de limpeza ajustada para raiz dinÃ¢mica, sem dependÃªncia fixa de `X:\`.
- Tabela de produtos protegida contra injeÃ§Ã£o HTML bÃ¡sica antes de futura API/banco.
- RelatÃ³rios v0.1.033 gerados em `03-vs/relatorios/precheck` e `03-vs/relatorios/limpeza`.
- Commit automÃ¡tico nÃ£o executado por pedido do usuÃ¡rio; fechamento manual.

## Atualizacao v0.1.034

- Hotfix aplicado em `01-mrp/front_end/js/pages/produtos_list.js`.
- Causa: chamada `escapeHtml(...)` sem funÃ§Ã£o auxiliar definida.
- Efeito anterior: tela de Produtos podia ficar sem renderizar a tabela.
- Dados preservados: `produtos_seed.json` continua com 147 produtos ativos.
- Nenhum backend criado.
- Nenhum banco criado.
- Commit automÃ¡tico nÃ£o executado.

## Atualizacao v0.1.036

- Servidor frontend estatico preparado para execucao automatica em Windows por scripts e tarefa agendada.
- Porta 8000 descontinuada; porta oficial 8765.
- Bind operacional padrao: 0.0.0.0 (LAN + Tailscale).
- Sem alteracao em JS/CSS/HTML/dados/imagens do frontend funcional nesta etapa.
- Sem backend e sem PostgreSQL nesta etapa.
