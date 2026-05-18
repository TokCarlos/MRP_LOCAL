# v0.1.028 - solucao

- Nome canonico aplicado para ATA/origem GOV/SEHIS:
  - `SEHIS - GOV. RIO`
  - key: `sehis_gov_rio`

- Seed de produtos normalizado sem alterar imagens:
  - `arp`, `arp_key`, `origem_ata`, `origem_ata_key`, `ata_origem`, `ata_origem_key` normalizados.
  - `empresa` mantida em dominio valido (`JPL`/`AÇO`), sem GOV/SEHIS.
  - `cliente/orgao` mantidos como `GOV. RIO`.
  - caminhos `imagem.preview`, `imagem.status`, `pasta` preservados.

- Catalogo da ATA normalizado:
  - `origem` e campos de origem/arp atualizados para o nome canonico.
  - caminhos e nomes de PNG preservados.

- Dominio atualizado:
  - adicionada secao `atas_origens` com entrada canonica `SEHIS - GOV. RIO`.
  - regras com `nome_canonico_ata_gov_rio` e `key_canonica_ata_gov_rio`.

- Validador PowerShell refeito:
  - bloqueia GOV/SEHIS em `empresa`/`empresa_key`.
  - valida TCR sem dados operacionais.
  - valida campos canonicos de ATA/origem para registros GOV/SEHIS.
  - bloqueia variacoes antigas.
