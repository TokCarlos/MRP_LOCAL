# v0.1.058 - Produtos filtro, UI e upload

Data: 2026-05-22

## Escopo

- Corrigir causa do filtro quebrado no modulo Produtos.
- Alinhar formularios ao padrao visual da tabela Produtos.
- Trocar registro manual de foto por upload real de arquivo.
- Preservar banco SQLite DEV e dados ja migrados.

## Mudancas tecnicas

- `GET /api/produtos` passa a retornar campos completos de Base ATA e Empresa.
- `ProdutosRepository.list_produtos()` inclui `base_ata_id`, `ata_nome`, `numero_ata` e `empresa_nome`.
- Frontend normaliza `empresa`, `arp` e `ata_numero` quando recebe aliases.
- Formulario Produto passa a usar `input type=file` para nova imagem.
- Backend adiciona `POST /api/produtos/{id}/imagem/upload`.
- Upload valida extensao e tamanho maximo de 5 MB.
- Upload salva arquivo em `assets/images/produtos` e grava caminho relativo em `produtos.imagem_path`.
- Modais usam fundo branco translucido e inputs claros, alinhados ao padrao Produtos.

## Validacoes

- `python -m py_compile` em arquivos backend alterados.
- `03-vs/scripts/backend/test_backend_produtos_v0_1_057.py` executado com sucesso.
- API validada em subprocesso:
  - `/health`: OK;
  - `/api/produtos`: 163 produtos;
  - primeiro produto com `base_ata_id=1`, `arp=CIM-JEQUI`, `ata_numero=07/2023`, `empresa=JPL`.

## Observacoes

- `python-multipart` foi adicionado ao `requirements.txt`.
- Upload real pelo navegador ainda deve ser validado manualmente em ambiente DEV aberto.
- Nao houve alteracao de schema do SQLite.
