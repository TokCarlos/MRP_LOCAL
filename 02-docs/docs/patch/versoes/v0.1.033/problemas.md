# Problemas — v0.1.033

## 1. Metadata ativa ainda apontava para pasta legada

`produtos_seed.json` já usava `imagem.preview` em `img/produtos`, mas `imagem.pasta` ainda apontava para `assets/produtos`.

Risco: scripts futuros poderiam ler `imagem.pasta` e voltar a usar estrutura legada.

## 2. Catálogo ATA apontava para PNGs inexistentes

`catalogo_ata_gov_rio.json` mantinha `path_relativo_sistema` no padrão antigo de arquivo, enquanto os arquivos reais ativos estavam com nomes `item_*`.

Risco: futura tela, importador ou backend poderia usar o catálogo e quebrar a imagem.

## 3. Validador de encoding tinha falso positivo perigoso

A regra de encoding procurava padrão amplo demais e poderia acusar erro em texto correto, além de escanear o próprio arquivo de validação.

Risco: bloqueio falso de commit e ruído em fechamento de versão.

## 4. Auditoria de limpeza estava presa em `X:\`

O script `auditoria_limpeza_v031.ps1` usava raiz fixa.

Risco: falha em outra máquina, pasta clonada, servidor real ou caminho diferente.

## 5. Renderização de produtos usava HTML direto com dados

A tabela de produtos montava `innerHTML` com dados do seed.

Risco: quando o mock virar banco/API, texto vindo de cadastro poderia injetar HTML se não for tratado.

## 6. Documentação de status estava atrasada

Alguns documentos ainda descreviam frontend como não iniciado, apesar de a interface visual já existir.

Risco: Codex/IA ou manutenção futura tomar decisão errada com base documental defasada.
