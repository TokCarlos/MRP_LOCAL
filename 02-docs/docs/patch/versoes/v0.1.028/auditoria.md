# v0.1.028 - auditoria

Resumo da auditoria antes da correcao:
- Variacoes de ATA/origem encontradas no seed e catalogo: `ATA GOV. RIO`, `GOV. RIO`, `SEHIS - GOV. RJ`, `gov_rio`, `ata_gov_rio`.
- Nao houve GOV/SEHIS como empresa apos v0.1.027, mas havia duplicidade conceitual de nome de ATA/origem.
- `TCR` nao apareceu em produtos operacionais.
- Caminhos de imagem estavam funcionais e foram preservados.

Arquivos com impacto direto:
- `01-mrp/front_end/data/produtos_seed.json`
- `01-mrp/front_end/data/catalogo_ata_gov_rio.json`
- `01-mrp/front_end/data/dominios_seed.json`
- `03-vs/scripts/validar_dominio_empresas.ps1`
- documentacao geral em `02-docs/docs/geral` e `README.md`
