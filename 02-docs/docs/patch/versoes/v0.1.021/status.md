# v0.1.021 - Status

- Status: AJUSTE_COLUNAS_PRODUTOS_APLICADO
- Backend: fora do escopo
- Banco: fora do escopo

## Validacao tecnica executada

- Cabecalho na ordem oficial:
  `ID | Preview | ATA+Nº | Nº Item | Produto | Empresa | Ação`
- `ATA+Nº` calculado por `arp + ata_numero`.
- `Nº Item` usa `item_ata` e nao usa `id`.
- Produto com alinhamento a esquerda e quebra de texto.
- Colunas demais centralizadas com quebra.
- Cabecalhos em caixa alta conforme padrao solicitado.
- Tabela com fundo branco translucido para ganho de legibilidade.
- Fundo da pagina escurecido em ~20% sem alterar arquivo de imagem.

## Observacao

- Validacao visual final em mobile (360px, 390px, 430px) permanece pendente de confirmacao no navegador do usuario:
  `document.documentElement.scrollWidth <= document.documentElement.clientWidth`
