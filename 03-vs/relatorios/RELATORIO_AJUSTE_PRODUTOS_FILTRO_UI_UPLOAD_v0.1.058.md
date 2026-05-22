# RELATORIO AJUSTE PRODUTOS - FILTRO, UI E UPLOAD v0.1.058

Data: 2026-05-22

## Objetivo

Corrigir os pontos diagnosticados no modulo Produtos:

- filtro quebrado por campos ausentes em `GET /api/produtos`;
- UI dos formularios fora do padrao da tabela Produtos;
- validacao do estado real do SQLite;
- registro de fotos por upload real em vez de caminho digitado.

## Resultado

- API de listagem corrigida.
- Filtro Produtos passa a receber ATA, numero da ATA e empresa.
- Modais de Nova Base ATA, Produto e Editar BOM alinhados ao fundo branco translucido.
- Produto passa a aceitar arquivo bruto pelo navegador.
- Backend recebe `multipart/form-data` e salva imagem com nome tecnico seguro.
- Banco continua sem migracao de schema.

## Arquivos principais

- `01-mrp/back_end/app/repositories/produtos_repository.py`
- `01-mrp/back_end/app/services/produtos_service.py`
- `01-mrp/back_end/app/routes/produtos.py`
- `01-mrp/back_end/app/config.py`
- `01-mrp/back_end/requirements.txt`
- `01-mrp/front_end/js/pages/produtos_list.js`
- `01-mrp/front_end/pages/produtos_list.html`
- `01-mrp/front_end/css/pages/produtos_list.css`
- `03-vs/scripts/backend/test_backend_produtos_v0_1_057.py`
- `03-vs/scripts/backend/setup_backend_dev_env.ps1`
- `03-vs/scripts/servicos/mrp_backend_start.ps1`

## Validacao executada

- Compilacao Python: OK.
- TestClient backend Produtos: OK.
- API em subprocesso: OK.
- `GET /api/produtos`: 163 produtos.
- Primeiro produto retornou:
  - `base_ata_id=1`;
  - `arp=CIM-JEQUI`;
  - `ata_numero=07/2023`;
  - `empresa=JPL`.

## Pendencias

- Validar upload real manualmente no navegador.
- Definir politica de remocao/substituicao de imagem antiga.
- Criar teste automatizado de upload com banco temporario.
