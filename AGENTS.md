# AGENTS.md — MRP_LOCAL

## Leitura obrigatoria antes de qualquer trabalho

Antes de diagnosticar, codar, mover arquivo, limpar, documentar ou executar patch, ler primeiro:

1. `02-docs/REGRAS_ATUAIS_MRP.txt`
2. `02-docs/LOG_PROGRESSO_MRP.txt`
3. `COMO_CRIAR_COMANDOS_CODEX.txt`, quando for montar comando ou revisar escopo.

Esses arquivos sao a fonte atual. Documentos antigos podem existir apenas como historico.

## Estrutura oficial

- `01-mrp` = sistema funcional.
- `02-docs` = documentacao, regras, progresso e historico.
- `03-vs` = scripts, relatorios, patches, pacotes e versionamento.
- `portable` = pacote/apoio operacional separado, pausado para evolucao nesta fase.

## Estado atual resumido

- Frontend oficial atual: `01-mrp/front_end`.
- Backend oficial atual: `01-mrp/back_end`.
- Backend Produtos usa FastAPI + SQLite em DEV.
- Porta frontend: `8765`.
- Porta backend: `8876`.
- Upload de usuario em Produtos deve salvar em `01-mrp/data/media/produtos` e ser servido por `/media/produtos`.
- `01-mrp/app/backend` e `01-mrp/app/frontend` nao sao fontes ativas nesta fase.
- Sistema ainda nao esta homologado/blindado.

## Chave de area restrita

Alterar `01-mrp` ou `.git` exige a chave explicita:

`LIBERADO`

Sem essa chave, pode ler, diagnosticar e planejar, mas nao alterar area restrita.

Mesmo com a chave:
- nao tocar na pasta PCP;
- nao alterar `.git` internamente;
- nao fazer commit/push sem pedido explicito;
- nao criar sujeira;
- nao mudar modulo fora do escopo.

## Pasta proibida absoluta

Nunca tocar:

`C:\Users\carlo\Desktop\PCP SERVIDOR\PCP`

Essa pasta so pode aparecer em regra/validador/documentacao como bloqueio explicito.

## Git

Regra atual:
- Nao fazer commit/push automatico.
- Deixar staged/preparado somente quando o usuario pedir.
- Commit/push dependem de ordem explicita do usuario.

Regra antiga de auto-commit esta obsoleta.

## Documentacao e progresso

Toda alteracao relevante deve atualizar:
- `02-docs/LOG_PROGRESSO_MRP.txt`
- relatorio da versao em `03-vs/relatorios`, quando aplicavel.

Documentacao obsoleta deve ir para:
- `02-docs/obsolete/`

Arquivo obsoleto de sistema dentro de `01-mrp` deve ir para:
- `01-mrp/_obsolete/`

Sempre criar manifesto explicando origem, destino, motivo e substituto.
