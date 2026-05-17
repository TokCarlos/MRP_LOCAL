# v0.1.027 - auditoria inicial

Arquivos com ocorrencias relevantes na triagem:
- `01-mrp/front_end/data/produtos_seed.json`
- `01-mrp/front_end/js/pages/produtos_list.js`
- `03-vs/scripts/gen_produtos_seed_v0_1_020.ps1`

Resumo da auditoria antes da correcao:
- Encontrados registros com `empresa=GOV. RIO` e `empresa_key=gov_rio` (ATA GOV. RIO).
- Filtro de Produtos ja era separado por `ATA` e `EMPRESA`, mas pesquisa e labels ainda tratavam sem enfase de `ATA/ORIGEM`.
- `TCR` nao apareceu em produtos operacionais.

Resumo apos correcao:
- Nenhum produto com `empresa=GOV. RIO`.
- Nenhum produto com `empresa_key=gov_rio`.
- Registros da ATA GOV. RIO classificados como `cliente/orgao/origem_ata/ata_origem`.
