# RELATORIO_OP_UI_ITENS_ACOES_v0.1.087

Patch incremental sobre v0.1.086.

## Ajustes aplicados

1. Nova OP
- Campo/formulario de Empresa removido da tela.
- Empresa permanece automatica no backend pela ATA selecionada.
- Produtos disponiveis ficam limpos ate selecionar MODELO ATA.
- ATA especifica lista somente produtos da respectiva ATA.
- ESPECIAL lista produtos de todas as ATAs.

2. Itens adicionados
- Lista compacta posicionada entre os formularios principais e a tabela/lista de produtos disponiveis.
- Lista inicia compactada.
- Clique no cabecalho expande/recolhe.
- Conteudo expandido em tabela com Item, Imagem, Produto, ATA, Quantidade e Acao.
- Quantidade preservada como inteiro.

3. Menu dos tres pontos do card
- Submenu pequeno/retro removido do fluxo de uso.
- Clique nos tres pontos abre modal grande de acoes da OP.
- Modal exibe tabela de resumo da OP e botoes organizados por grupo: Cadastro/detalhes, Movimentacao Kanban e Cancelamento.

4. Cancelamento de OP
- Confirmacao via window.confirm substituida por modal interno estilizado via CSS.
- Cancelamento continua chamando DELETE/soft delete ja existente no backend.

## Validacoes
- node --check em ordens_producao_list.js.
- python compileall nos arquivos backend de OP.
