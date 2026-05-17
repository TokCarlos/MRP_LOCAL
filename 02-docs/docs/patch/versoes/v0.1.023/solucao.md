# v0.1.023 - Solucao

## Escopo

- Alteracao exclusiva da pagina Produtos.
- Sem backend/banco.
- Sem alteracao no seed, nomes oficiais ou imagens.
- Preservado desktop em tabela e mobile em cards.

## Entregas

1. Pesquisa livre (case-insensitive e accent-insensitive):
   - pesquisa em `nome_oficial`, `arp`, `ata_numero`, `empresa`, `item_ata`, `produto_key`.
2. Filtro `ATA+Nº` com opcoes dinamicas por seed.
3. Filtro `EMPRESA` com opcoes dinamicas.
4. Filtro `CATEGORIA` com opcoes dinamicas.
5. Botao `Limpar` para reset completo dos filtros.
6. Contador de resultados:
   - `Exibindo X de Y produtos`
   - `0 produtos encontrados`
7. Mensagem sem resultado:
   - `Nenhum produto encontrado com os filtros atuais.`

## Arquivos alterados

- `01-mrp/front_end/pages/produtos_list.html`
- `01-mrp/front_end/js/pages/produtos_list.js`
- `01-mrp/front_end/css/pages/produtos_list.css`
