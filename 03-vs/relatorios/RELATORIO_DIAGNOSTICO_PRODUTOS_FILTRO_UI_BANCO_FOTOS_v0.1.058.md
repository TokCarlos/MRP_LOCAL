# RELATORIO DIAGNOSTICO PRODUTOS - FILTRO, UI, BANCO E FOTOS v0.1.058

Data: 2026-05-22
Escopo: avaliacao apenas, sem correcao de codigo, sem alteracao em .git, sem tocar pasta PCP.

## 1. Causa provavel do filtro quebrado

Causa principal: campo ausente na resposta de lista da API.

O frontend de `01-mrp/front_end/js/pages/produtos_list.js` espera estes campos para filtro e renderizacao:

- Pesquisa: `nome_oficial`, `arp`, `ata_numero`, `ata_origem`, `origem_ata`, `cliente`, `orgao`, `empresa`, `item_ata`, `produto_key`.
- Filtro ATA: `arp_key` ou `arp`, junto com `ata_key` ou `ata_numero`.
- Filtro Empresa: `empresa`.
- Filtro Categoria: `categoria`.
- Renderizacao da tabela: `id`, `imagem.preview` ou `imagem_path`, `arp`, `ata_numero`, `empresa`, `nome_oficial`.

O formato real de `GET /api/produtos` esta correto na casca (`{"ok": true, "data": [...]}`), mas a lista vem incompleta para os campos de base:

- `base_ata_id`: `null`
- `ata_numero`: `null`
- `arp`: `null`
- `empresa`: `null`
- `empresa_key`: preenchido
- `ata_key`: preenchido

Confirmacao adicional: `GET /api/produtos/1` retorna os campos completos (`base_ata_id=1`, `ata_numero=07/2023`, `arp=CIM-JEQUI`, `empresa=JPL`). Portanto o banco e o endpoint individual sabem a informacao; o problema esta no caminho da listagem.

Ponto tecnico provavel:

- `ProdutosRepository.list_produtos()` seleciona apenas `b.empresa_key` e `b.ata_key`, mas nao seleciona `p.base_ata_id`, `b.ata_nome`, `b.numero_ata`, `b.empresa_nome`.
- Depois disso, `ProdutosService.make_contract_item()` tenta montar `base_ata_id`, `ata_numero`, `arp` e `empresa` a partir de chaves que nao existem no row da listagem.

Classificacao solicitada:

- a) campo ausente na API: SIM, causa principal.
- b) parser frontend errado: NAO como causa principal; o parser aceita `data`, `data.items` e `items`.
- c) dados do banco incompletos: NAO, banco contem base, empresa, ATA e imagens.
- d) filtro ainda usando mock/seed antigo: NAO quando backend esta ativo; ele usa API. Se API cair, cai para seed/mock.
- e) lista renderizada diferente da lista filtrada: NAO; ambas usam `produtosState.produtos`. O problema e a lista API ja chegar sem campos.

Efeitos visiveis:

- Filtro de empresa fica vazio porque `produto.empresa` vem `null`.
- Filtro de ATA nao monta label porque `arp` e `ata_numero` vem `null`.
- Coluna EMPRESA renderiza vazia.
- Coluna ATA + No tende a renderizar vazia na lista API.
- Modal Editar Produto pode abrir sem `base_ata_id`, porque a listagem nao entrega o id da base.

## 2. Estado real do banco

Banco verificado: `01-mrp/data/db/mrp_local_dev.sqlite`

Resumo SQLite:

- Tabelas: `produto_base_ata`, `produto_bom`, `produtos`.
- Bases ATA totais: 5.
- Bases ATA ativas: 5.
- Produtos totais: 163.
- Produtos ativos: 163.
- Produtos inativos: 0.
- Produtos sem categoria: 0.
- Produtos sem empresa: 0.
- Produtos sem ATA: 0.
- Produtos sem `imagem_path`: 0.
- Produtos com `imagem_path` inexistente: 0.
- Duplicidade de `produto_key`: 0 grupos duplicados.
- Itens BOM ativos: 1.

Distribuicao de produtos ativos por empresa:

- ACO: 110.
- JPL: 53.

Bases ATA cadastradas:

- JPL / CIM-JEQUI / 07/2023.
- JPL / CIM-JEQUI / 028/2023.
- JPL / SOMAR-MARICA / 011/2025.
- ACO / CIMASP / 029/2025.
- ACO / SEHIS - GOV. RIO 114443801/2025 / 114443801/2025.

Migracao seed/mock:

- `01-mrp/front_end/data/produtos_seed.json` tem 163 produtos.
- 163 produtos sao validos para bootstrap.
- 0 produtos foram pulados.
- 5 bases distintas no seed.
- O banco tem 163 produtos ativos e 5 bases, portanto os dados do seed foram migrados integralmente para o SQLite.

Observacao importante:

- A API de lista nao reflete corretamente todos os dados do banco por falha de selecao/contrato na listagem, nao por ausencia de dados no SQLite.

## 3. Problema visual dos formularios

Formularios avaliados:

- Nova Base ATA: `#modalBaseAta`.
- Novo Produto / Editar Produto: `#modalProduto`.
- Editar BOM: `#modalBom`.

Classes usadas:

- Estrutura: `.modal`, `.modal-content`, `.modal-actions`, `.modal-bom`.
- Botoes: `.btn-row-action`.
- Tabelas BOM dentro do modal: `.preview-table`, `.produtos-table`.
- Inputs/selects: regras de `.modal-content input` e `.modal-content select`.

Diagnostico visual:

- A tabela Produtos usa fundo branco com 70% de transparencia (`rgba(255, 255, 255, 0.70)`).
- Os filtros tambem usam fundo branco com 70% de transparencia e inputs claros.
- Os modais nao seguem esse padrao: `.modal-content` usa `var(--cor-painel)`, que e painel escuro.
- Inputs/selects dos modais usam fundo `rgba(255,255,255,0.1)` e texto branco, criando visual escuro/transparente destoante da tabela Produtos.
- A largura fixa de 380px em `.modal-content` e limitada para telas menores e nao segue o padrao responsivo dos filtros/tabela.
- `modal-bom` tem largura responsiva (`min(960px, 94vw)`), mas a tabela interna pode ficar pesada em mobile.
- Botoes usam `.btn-row-action`, entao estao mais proximos do padrao do sistema, mas o conjunto visual do modal nao esta alinhado com tabela/card Produtos.

Conclusao:

- O problema visual e de CSS/padrao: os formularios ainda estao no estilo de painel escuro, enquanto Produtos ja usa superficies brancas translucidas.
- A cor/transparencia e o comportamento responsivo devem ser ajustados sem criar linguagem visual nova.

Proposta visual objetiva:

- `.modal-content`: fundo `rgba(255, 255, 255, 0.70)`, texto escuro, borda leve e mesmo raio/espacamento de Produtos.
- Inputs/selects do modal: fundo `rgba(255, 255, 255, 0.92)`, texto `#111`, borda `rgba(0,0,0,0.18)`.
- Largura: `width: min(520px, 94vw)` para Base ATA/Produto.
- `modal-bom`: manter `min(960px, 94vw)`, com overflow interno horizontal para tabela.
- Botoes: manter `.btn-row-action`/`.btn-add` ou consolidar classe comum, sem criar estilo novo destoante.

## 4. Estado atual do registro de fotos

Fluxo atual:

- O formulario de Produto tem `input type="text"` em `#produtoImagemPath`.
- O usuario informa um caminho/endereco relativo manualmente.
- O frontend envia `imagem_path` no payload de `POST /api/produtos` ou `PUT /api/produtos/{id}`.
- Existe `PATCH /api/produtos/{id}/imagem`, mas ele tambem recebe apenas JSON com `imagem_path`.
- Nao existe upload bruto de arquivo no backend atual.
- Nao ha uso de `UploadFile`, `File(...)` ou `multipart/form-data`.
- `imagem_path` e salvo na tabela `produtos.imagem_path`.
- O zoom usa `imagem.preview` ou `imagem_path`; portanto o zoom depende do caminho salvo.

Onde as imagens ficam hoje:

- Caminhos salvos apontam para `img/produtos/...`.
- No modo DEV, esses arquivos existem em `01-mrp/front_end/img/produtos/...`.
- A config atual resolve `produtos_image_root` como `frontend_root`, entao `imagem_path=img/produtos/...` e validado/consultado a partir de `01-mrp/front_end`.

Validacao atual:

- O backend rejeita caminho absoluto `C:\`, `X:\`, UNC `\\home-machine`, `http://`, `https://`.
- O backend rejeita caminho contendo `pcp servidor\pcp`.
- Nao valida extensao/tamanho real de arquivo porque nao recebe arquivo bruto.

Proposta minima para upload real:

- Frontend trocar o campo de texto por `input type="file"` aceitando imagens.
- Backend criar endpoint multipart, por exemplo `POST /api/produtos/{id}/imagem/upload`.
- Backend validar extensao permitida (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg` se aceito pelo projeto) e tamanho maximo.
- Backend gerar nome tecnico seguro com base em `produto_key` ou UUID curto.
- Backend salvar em `assets/images/produtos` conforme diretriz futura, ou alinhar explicitamente se o alvo DEV permanecer `front_end/img/produtos`.
- Banco salvar apenas caminho relativo estavel.
- Frontend atualizar preview/zoom usando o caminho relativo retornado pela API.

## 5. Correcoes recomendadas em ordem

1. Corrigir a API de listagem de Produtos.
   - Ajustar `ProdutosRepository.list_produtos()` para retornar `base_ata_id`, `ata_nome`, `numero_ata`, `empresa_nome`.
   - Garantir que `GET /api/produtos` devolva o mesmo contrato essencial de `GET /api/produtos/{id}`.

2. Validar filtros e renderizacao com API ativa.
   - Confirmar opcoes de ATA, Empresa e Categoria.
   - Confirmar contador e coluna EMPRESA.
   - Confirmar que Editar Produto recebe `base_ata_id` corretamente.

3. Ajustar CSS dos modais ao padrao Produtos.
   - Fundo branco 70% translucido.
   - Inputs claros.
   - Largura responsiva.
   - Botoes consistentes.

4. Padronizar contrato de fotos por caminho relativo antes do upload.
   - Definir raiz oficial: `01-mrp/front_end/img/produtos` no DEV atual ou `assets/images/produtos` na diretriz futura.
   - Evitar divergencia entre placeholder do campo (`assets/images/produtos/...`) e caminhos reais (`img/produtos/...`).

5. Implementar upload real em etapa separada.
   - Endpoint multipart.
   - Validacao de extensao/tamanho.
   - Nome tecnico seguro.
   - Persistencia do caminho relativo.
   - Atualizacao de preview/zoom.

## 6. O que deve ser corrigido primeiro

Primeiro: `GET /api/produtos`.

Justificativa direta:

- O banco esta bom.
- O seed foi migrado integralmente.
- O filtro quebra porque a listagem da API perde campos que o frontend precisa.
- Corrigir UI antes disso mascara o problema principal.
- Corrigir upload antes disso aumenta escopo sem resolver a listagem.

## 7. Arquivos que provavelmente precisarao alteracao depois

Para corrigir filtro/listagem:

- `01-mrp/back_end/app/repositories/produtos_repository.py`
- `01-mrp/back_end/app/services/produtos_service.py`
- `01-mrp/back_end/app/routes/produtos.py` (provavelmente so validacao/contrato, se necessario)
- `01-mrp/back_end/app/tests/` ou `03-vs/scripts/backend/test_backend_produtos_v0_1_057.py`
- `01-mrp/front_end/js/pages/produtos_list.js` (apenas se for necessario robustecer fallback/normalizacao)

Para corrigir visual dos formularios:

- `01-mrp/front_end/css/pages/produtos_list.css`
- `01-mrp/front_end/pages/produtos_list.html` (se precisar classes auxiliares ou estrutura responsiva)

Para upload real de fotos:

- `01-mrp/front_end/pages/produtos_list.html`
- `01-mrp/front_end/js/pages/produtos_list.js`
- `01-mrp/back_end/app/routes/produtos.py`
- `01-mrp/back_end/app/services/produtos_service.py`
- `01-mrp/back_end/app/domain/produtos_models.py` (se mantiver modelos auxiliares)
- `01-mrp/back_end/app/config.py`
- Possivel pasta alvo futura: `01-mrp/assets/images/produtos` ou ajuste para raiz atual `01-mrp/front_end/img/produtos`.

## Fechamento

Nao foi aplicada correcao.
Nao foi feito commit.
Nao foi feito push.
Nao foi tocada a pasta PCP.
Foi gerado somente este relatorio diagnostico solicitado.
