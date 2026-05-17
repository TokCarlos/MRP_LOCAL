# v0.1.026 - Solucao

## Escopo aplicado

- Ajuste restrito a tela Produtos (CSS/JS/HTML da propria pagina).
- Sem alteracao de backend, banco, seed, nomes oficiais ou imagens.
- Fallback placeholder preservado.

## Ajuste 1 - Preview mini

- Tamanho do preview aumentado de forma moderada.
- `object-fit: contain` mantido para nao cortar equipamentos.
- Desktop e mobile ajustados sem alterar o layout geral da tela.

## Ajuste 2 - Lightbox / modal

- Clique na imagem abre modal sobreposto com imagem ampliada.
- Fundo escurecido.
- Fechamento por:
  - botao `X`
  - clique fora da imagem
  - tecla `ESC`
- Limites:
  - desktop: `max-width: 88vw`, `max-height: 84vh`
  - mobile: `max-width: 94vw`, `max-height: 80vh`

## Arquivos alterados

- `01-mrp/front_end/pages/produtos_list.html`
- `01-mrp/front_end/js/pages/produtos_list.js`
- `01-mrp/front_end/css/pages/produtos_list.css`
