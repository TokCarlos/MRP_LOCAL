# Backend Produtos - estado acumulado

## Papel do modulo Produtos

Produto e o aparelho/equipamento principal do sistema MRP_LOCAL.
Produtos e o cadastro-mestre que sera referenciado por materiais, tubos, chapas, insumos, processos, estoque e ordens de producao em etapas futuras.

## Regras de dominio

- Produto pertence ao contexto de `empresa + ATA`.
- Campos principais: `ITEM DA ATA`, `NOME OFICIAL`, `CATEGORIA`, `IMAGEM` opcional.
- Produto nao e material, tubo, chapa nem insumo.
- Materiais e composicao/BOM sao modulos futuros.
- Nao criar TCR artificial.
- Nao criar GOV como empresa.
- Nao duplicar por acento/encoding.
- Visual pode ter acento; keys tecnicas devem ser ASCII-safe.

## Fonte atual e fonte futura

- Fonte backend atual em DEV: SQLite runtime em `01-mrp/data/db/mrp_local_dev.sqlite`.
- Seed ativo/legado ainda usado para recriacao inicial: `01-mrp/front_end/data/produtos_seed.json`.
- Imagens oficiais/seed: `01-mrp/front_end/img/produtos`.
- Uploads do usuario: `01-mrp/data/media/produtos`.
- Caminho salvo no banco para upload: `media/produtos/{arquivo}`.
- Fonte futura para producao: PostgreSQL ou outro banco definido em etapa propria.
- Banco/API guardam referencia relativa de imagem, mantendo arquivo fisico separado.

## Escopo da v0.1.051

- definir contrato e base tecnica backend do modulo Produtos;
- validar seed com adapter/service sem alterar dados;
- nao ativar FastAPI;
- nao criar banco real;
- nao alterar frontend funcional.

## Saneamento v0.1.052b

- resolucao de `imagem_path` ajustada para montagem portavel com `pathlib`;
- sem alteracao de `produtos_seed.json`;
- sem alteracao funcional de frontend.

## Etapa v0.1.053

- API minima de leitura de Produtos ativa em `/api/produtos`;
- backend local responde `/health` e `/api/status`;
- dados continuam vindo de seed (sem banco real nesta etapa).

## Etapa v0.1.058

- Corrigido contrato real de `GET /api/produtos` para incluir dados de Base ATA e Empresa na listagem.
- Listagem passa a devolver `base_ata_id`, `arp`, `ata_numero` e `empresa`, alinhada ao endpoint individual.
- Filtro do frontend Produtos volta a ter dados suficientes para ATA, Empresa, Categoria e pesquisa.
- Implementado endpoint de upload real de imagem: `POST /api/produtos/{id}/imagem/upload`.
- Campo multipart esperado: `arquivo`.
- Extensoes permitidas: `.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`.
- Limite inicial: 5 MB.
- Upload gera nome tecnico seguro baseado no `produto_key`.
- O caminho relativo salvo no banco passa a apontar para `assets/images/produtos/...` na v0.1.058; esse destino foi substituido na v0.1.059.
- `python-multipart` passa a ser dependencia obrigatoria do backend FastAPI.

## Etapa v0.1.059

- Upload real passa a salvar arquivo em `01-mrp/data/media/produtos`.
- `produtos.imagem_path` passa a usar o padrao canonico `media/produtos/{arquivo}`.
- Backend monta `StaticFiles` em `/media` para servir midia runtime.
- Frontend Produtos converte `media/...` para URL do backend em `http(s)://host:8876/media/...`.
- Imagens oficiais do seed continuam em `01-mrp/front_end/img/produtos`.
- `01-mrp/app/frontend` permanece estrutura alvo futura e nao deve receber uploads no DEV atual.
