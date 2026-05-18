# Solução — v0.1.033

## Correções aplicadas

1. `produtos_seed.json`
   - `imagem.pasta` alinhada ao diretório real de `imagem.preview`.
   - Removida referência ativa remanescente para `assets/produtos` dentro da metadata operacional.

2. `catalogo_ata_gov_rio.json`
   - `arquivo_sistema` e `path_relativo_sistema` alinhados aos arquivos reais usados nos produtos oficiais IDs 128-147.

3. `validar_encoding.ps1`
   - Falso positivo amplo substituído por padrões de mojibake mais específicos.
   - O script deixa de validar o próprio arquivo de regras de padrões.
   - Removidos exemplos literais de mojibake da documentação geral.

4. `auditoria_limpeza_v031.ps1`
   - Raiz fixa `X:\` substituída por raiz dinâmica calculada a partir da pasta do script.
   - Auditoria passa a ignorar histórico de patch, quarentena e relatórios ao calcular referências ativas.
   - Filtro de temporários ajustado para não classificar `testes.md` como temporário.

5. `produtos_list.js`
   - Dados da tabela passam por escape antes de entrar no HTML.
   - A alteração é preventiva e não muda regra visual da página.

6. Documentação
   - Criado registro v0.1.033.
   - `status_geral.md`, `checklist_atual.md`, `README.md`, `AGENTS.md` e manifestos atualizados para refletir estado atual.

## Limpeza

Nenhum arquivo ativo foi apagado nesta etapa.

A limpeza definitiva de imagens órfãs fica pendente para patch futuro, porque ainda exige revisão visual/manual.
