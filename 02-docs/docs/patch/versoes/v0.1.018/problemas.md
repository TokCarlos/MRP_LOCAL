# v0.1.018 - Problemas

## Contexto consolidacao

- Havia uso de variaveis CSS legadas (`--cor-painel`, `--cor-subtexto`, `--cor-botao`) em estilos de pagina, sem aliases explicitos no `:root`.
- Rotas de menu existentes (`processos_list`, `estoque_list`, `ordens_list`) apontavam para HTMLs vazios, sem conteudo minimo funcional.
- Nao existiam modulos JS correspondentes para essas rotas `_list`.
- Base mock local estava com estrutura reduzida para acoplamento futuro de dados.
- Existem arquivos historicos/inativos (ex.: `aparelho.*`, `processos.js`, `estoque.js`) que precisam decisao controlada de limpeza sem quebrar referencias.

## Restricao aplicada

- Aparencia visual aprovada preservada.
- Sem alteracao de layout global, cores, espacamentos, header, menu, responsividade validada ou estilo da tela Produtos.
- Sem backend e sem banco.
