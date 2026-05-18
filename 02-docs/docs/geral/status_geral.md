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
