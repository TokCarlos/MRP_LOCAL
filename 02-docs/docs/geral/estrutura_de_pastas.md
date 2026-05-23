# Estrutura de Pastas do Workspace MRP_LOCAL

Versão: v0.1.002
Status: DEFINIDO

## Regra principal

A raiz do workspace deve conter somente três pastas principais:

```text
01-mrp
02-docs
03-vs
```

Os nomes físicos devem permanecer curtos, minúsculos e sem acentos. Esta regra reduz risco em CMD, BAT, PowerShell, Python, Git, ZIP, caminhos UNC e automações futuras.

## 01-mrp

Pasta do sistema funcional.

Deve conter somente arquivos que serão usados pelo sistema, agora ou no futuro.

Estrutura inicial prevista:

```text
01-mrp
├─ backend
├─ front_end
├─ config
├─ scripts
├─ database
├─ runtime
└─ logs
```

Regra: não colocar documentação geral, versões antigas, pacotes de entrega, arquivos de teste soltos ou fontes descartadas nesta pasta.

## 02-docs

Pasta documental do projeto.

Deve conter documentação, regras, histórico, roadmap, inventários, registros de decisão, registros de patch, pendências, testes e material de orientação para Codex/IA.

Estrutura atual:

```text
02-docs
├─ LEIA_PRIMEIRO.md
├─ manifesto.json
├─ codex
└─ docs
   ├─ geral
   ├─ modulos
   ├─ templates
   ├─ inventario
   └─ patch
      └─ versoes
```

Regra: toda decisão técnica deve ser registrada aqui antes de ser aplicada em `01-mrp`, salvo correção emergencial registrada imediatamente depois.

## 03-vs

Pasta de versionamento.

Deve conter pacotes, patches, histórico, releases e entradas originais recebidas.

Estrutura inicial prevista:

```text
03-vs
├─ pacotes
├─ patches
├─ historico
├─ releases
└─ entrada_original
```

Regra: toda versão ajustada de `01-mrp` deve ser gerada e registrada em `03-vs`, seguindo padrão documental em `02-docs/docs/patch/versoes`.

## Fluxo obrigatório

1. Registrar regra, decisão ou alteração em `02-docs`.
2. Definir escopo da mudança.
3. Aplicar somente no módulo ou pasta necessária em `01-mrp`.
4. Registrar problema, solução e status.
5. Gerar pacote/patch em `03-vs`.
6. Atualizar log geral.

## Estado atual

Nesta versão foi aplicada a padronização física das três pastas raiz:

```text
01-mrp
02-docs
03-vs
```

O projeto antigo `mrp-main.zip` segue apenas inventariado. Ele ainda não foi incorporado ao `01-mrp`.
## Atualizacao v0.1.059 - dados e midia runtime

Separacao oficial:

```text
01-mrp/data/db
01-mrp/data/seed
01-mrp/data/media/produtos
01-mrp/front_end/img/produtos
portable/data/media/produtos
```

Regras:

- `01-mrp/data/db` guarda banco local DEV.
- `01-mrp/data/seed` guarda carga inicial tecnica.
- `01-mrp/data/media/produtos` guarda uploads reais feitos pelo usuario.
- `01-mrp/front_end/img/produtos` guarda imagens oficiais do catalogo/seed.
- `portable/data/media/produtos` e a area equivalente para runtime portable.
- `01-mrp/app/frontend` nao e destino de upload no DEV atual.
- `assets/images/produtos` nao e raiz oficial de imagem de produto.
- O banco guarda caminho relativo, por exemplo `media/produtos/arquivo.png`.
