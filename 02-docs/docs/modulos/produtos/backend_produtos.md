# Backend Produtos - v0.1.051

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

- Fonte atual temporaria: `01-mrp/front_end/data/produtos_seed.json`.
- Imagens atuais: `01-mrp/front_end/img/produtos`.
- Fonte futura real: PostgreSQL.
- Banco/API devem guardar referencia de imagem (caminho), mantendo arquivo fisico separado.

## Escopo da v0.1.051

- definir contrato e base tecnica backend do modulo Produtos;
- validar seed com adapter/service sem alterar dados;
- nao ativar FastAPI;
- nao criar banco real;
- nao alterar frontend funcional.
