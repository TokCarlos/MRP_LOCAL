# Modulo Produtos - Estado atual

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

## Observacoes atuais

- O backend Produtos existe e esta ativo em `01-mrp/back_end`.
- O banco SQLite DEV e runtime/local, nao deve ser versionado.
- O seed legado continua util para recriar dados iniciais.
- Imagens oficiais/seed ficam em `01-mrp/front_end/img/produtos`.
- Uploads de usuario ficam em `01-mrp/data/media/produtos`.
- Registros antigos deste arquivo foram mantidos como historico, mas a fonte atual deve ser `02-docs/LOG_PROGRESSO_MRP.txt`.

## Atualizacao v0.1.058

- Banco SQLite DEV ativo em `01-mrp/data/db/mrp_local_dev.sqlite`.
- Estado verificado: 5 bases ATA, 163 produtos ativos, 0 produtos sem categoria, 0 produtos sem empresa, 0 produtos sem ATA, 0 produtos sem `imagem_path`, 0 imagens inexistentes e 0 duplicidade de `produto_key`.
- `GET /api/produtos` corrigido para devolver os campos necessarios ao filtro e renderizacao.
- Fichas de Nova Base ATA, Produto e Editar BOM alinhadas ao padrao visual branco translucido da tabela Produtos.
- Produto passa a aceitar selecao de arquivo bruto para upload de imagem.
- Upload v0.1.058 salvava arquivo em `assets/images/produtos`; esse caminho foi substituido na v0.1.059.

## Atualizacao v0.1.059

- Upload real de imagem de Produto passa a salvar arquivo em `01-mrp/data/media/produtos`.
- `produtos.imagem_path` passa a guardar caminho relativo no formato `media/produtos/{arquivo}`.
- Backend expoe midia runtime em `/media/produtos/{arquivo}`.
- Frontend resolve `media/...` pela API/backend e continua aceitando `img/produtos/...` para imagens oficiais do catalogo/seed.
- Registro local testado do produto ID 110 foi migrado de `assets/images/produtos/...` para `media/produtos/...`.
