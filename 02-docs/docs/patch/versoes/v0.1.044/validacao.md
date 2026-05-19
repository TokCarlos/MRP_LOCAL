# Validacao v0.1.044 - Imagens CIMASP

## Validacoes previstas

- JSON do seed deve carregar sem erro.
- Todos os previews CIMASP devem apontar para arquivo fisico PNG.
- Itens CIMASP devem usar `imagem.status = REAL_ATA`.
- Validacao de imagens deve aceitar CIMASP como ATA com PNG real.

## Resultado

- JSON do seed carregado com sucesso.
- Total de produtos no seed: 163.
- Total CIMASP: 90.
- CIMASP REAL_ATA: 90.
- CIMASP com preview PNG: 90.
- Variacoes CIMASP cadastradas: 16.
- `validar_img_produtos.ps1`: OK.
- `validar_dominio_empresas.ps1`: OK.
