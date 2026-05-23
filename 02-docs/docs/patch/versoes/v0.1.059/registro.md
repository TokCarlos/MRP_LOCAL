# Registro v0.1.059 - upload de imagem e midia canonica

## Escopo

Corrigir a troca de imagem de Produto apos upload real e fixar a estrutura canonica de dados e midia.

## Decisao

- Dados estruturados ficam em `01-mrp/data/db`.
- Seeds ficam em `01-mrp/data/seed`.
- Imagens oficiais do catalogo continuam em `01-mrp/front_end/img/produtos`.
- Uploads reais do usuario ficam em `01-mrp/data/media/produtos`.
- Banco salva caminho relativo `media/produtos/{arquivo}`.
- Backend serve a midia em `/media/produtos/{arquivo}`.

## Motivo

A v0.1.058 salvava upload em `assets/images/produtos` e o ambiente DEV resolveu esse caminho para `01-mrp/app/frontend/assets`, que nao e o frontend ativo. O arquivo era enviado, mas a tela nao trocava a imagem exibida.
