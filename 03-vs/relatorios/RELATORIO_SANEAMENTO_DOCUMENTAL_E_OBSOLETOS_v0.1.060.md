# RELATORIO_SANEAMENTO_DOCUMENTAL_E_OBSOLETOS_v0.1.060

## Objetivo

Consolidar fonte atual de regras/progresso, corrigir documentacao divergente e separar obsoletos sem apagar historico.

## Criado

- `02-docs/REGRAS_ATUAIS_MRP.txt`
- `02-docs/LOG_PROGRESSO_MRP.txt`
- `COMO_CRIAR_COMANDOS_CODEX.txt`
- `REGRAS_MRP.txt` atualizado como ponte de compatibilidade para `02-docs/REGRAS_ATUAIS_MRP.txt`
- `02-docs/obsolete/README.md`
- `01-mrp/_obsolete/README.md`
- `02-docs/docs/geral/protocolo_trabalho_codex.md`

## Atualizado

- `AGENTS.md`
- `README.md`
- `Readme.txt`
- `01-mrp/back_end/README.md`
- `01-mrp/back_end/app/contracts/README.md`
- `01-mrp/docs_runtime/README.md`
- `02-docs/docs/geral/git_github.md`
- `02-docs/docs/infraestrutura/portas.md`
- `02-docs/docs/infraestrutura/execucao_automatica.md`

## Movido para obsoleto

- Documentacao base v0.1.000 divergente com estado atual.
- Protocolo antigo de auto-commit.
- Regras duplicadas antigas em `02-docs/docs/geral/REGRAS_MRP.txt`.
- Imagem de upload gerada em caminho incorreto dentro de `01-mrp/app/frontend/assets`.

## Estado atual registrado

- Backend oficial: `01-mrp/back_end`.
- Frontend oficial: `01-mrp/front_end`.
- Upload de usuario: `01-mrp/data/media/produtos`.
- Midia publica: `/media/produtos`.
- App/backend e app/frontend nao sao fontes ativas nesta fase.
- Commit/push nao sao automaticos.

## Pendencias

- Revisar docs historicas restantes em lotes menores.
- Validar manualmente CRUD Produtos/BOM/Upload apos aplicar no PC.
- Fechar commit seletivo pelo usuario.
