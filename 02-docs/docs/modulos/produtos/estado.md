# Modulo Produtos - Estado atual (v0.1.020)

- Fonte oficial inicial importada para seed local.
- 147 produtos carregados da lista enviada pelo usuario.
- Nomes oficiais preservados nos campos de exibicao.
- Estrutura de preview demo criada por `empresa/arp/ata/item`.
- Tela de Produtos exibindo preview + nome oficial + acao.

## Atualizacao v0.1.025

- Integracao do pacote `GOV_RIO_PREP_CRM.zip` concluida sem backend.
- +20 itens da ATA GOV. RIO adicionados ao seed.
- Itens GOV. RIO com preview real (`imagem.status = REAL_ATA`).
- Total atual no seed: 167 produtos.

## Observacoes

- Imagens ainda sao DEMO e serao substituidas por imagens reais ATA por ATA.
- Categoria atual e provisoria por inferencia textual.
- Backend e banco continuam fora do escopo nesta etapa.

## Atualizacao v0.1.058

- Banco SQLite DEV ativo em `01-mrp/data/db/mrp_local_dev.sqlite`.
- Estado verificado: 5 bases ATA, 163 produtos ativos, 0 produtos sem categoria, 0 produtos sem empresa, 0 produtos sem ATA, 0 produtos sem `imagem_path`, 0 imagens inexistentes e 0 duplicidade de `produto_key`.
- `GET /api/produtos` corrigido para devolver os campos necessarios ao filtro e renderizacao.
- Fichas de Nova Base ATA, Produto e Editar BOM alinhadas ao padrao visual branco translucido da tabela Produtos.
- Produto passa a aceitar selecao de arquivo bruto para upload de imagem.
- Upload salva arquivo em `assets/images/produtos` no frontend DEV e grava caminho relativo no SQLite.
