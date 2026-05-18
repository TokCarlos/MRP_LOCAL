# Status Geral — MRP_LOCAL

## Status atual

```text
Projeto: MRP_LOCAL
Versão documental: v0.1.002
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


## Estrutura física oficial

```text
01-mrp
02-docs
03-vs
```

Status da estrutura: DEFINIDO em v0.1.002.

## Atualizacao v0.1.027

- Dominio de empresas corrigido para: JPL, AÇO e TCR.
- GOV. RIO reclassificado para dominio de ATA/origem/cliente/orgao.
- TCR mantido como empresa valida futura, sem dados operacionais.
- Nenhum backend criado.
- Nenhuma persistencia real implementada.
- Alteracao restrita ao CRM visual/seed/config/documentacao.

## Atualizacao v0.1.028

- ATA GOV RIO / SEHIS GOV RJ normalizada para `SEHIS - GOV. RIO`.
- Numero da ATA preservado nos registros existentes.
- GOV. RIO permanece fora do dominio empresa.
- Empresas validas mantidas: JPL, AÇO e TCR.
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
- Nome visual da empresa corrigido de `AÃ‡O` para `AÇO` nos dados ativos.
- Regra absoluta de encoding documentada como bloqueadora de commit.
- Validacao obrigatoria de encoding criada em `03-vs/scripts/validar_encoding.ps1`.
- Relatorios de encoding gerados em `03-vs/relatorios/encoding`.
