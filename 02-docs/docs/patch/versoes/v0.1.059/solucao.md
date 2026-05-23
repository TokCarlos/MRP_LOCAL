# Solucao v0.1.059 - upload de Produto

## Ajustes

- Corrigida resolucao de paths DEV para priorizar `01-mrp/front_end`.
- Backend passou a usar `01-mrp/data/media/produtos` como destino de upload.
- Backend passou a expor `StaticFiles` em `/media`.
- Frontend Produtos passou a resolver `media/...` pela origem do backend na porta `8876`.
- `.gitignore` passou a ignorar arquivos reais de midia runtime e preservar apenas `.gitkeep`.
- Registro local legado do produto ID 110 foi migrado para o caminho canonico.

## Compatibilidade

- Caminhos antigos `img/produtos/...` continuam validos para imagens oficiais do seed.
- Caminhos absolutos seguem proibidos.
- `assets/images/produtos` deixa de ser destino valido para upload real.
