# Roadmap — MRP_LOCAL

## Etapa 1 — Interface visual conceitual

Status: PLANEJADO / EM ANDAMENTO

Objetivo:

```text
Fechar aparência, telas, menus, fluxo e identidade visual.
```

Inclui:

```text
login visual
dashboard
menu lateral
cards
tabelas fake
formulários fake
status visuais
módulos conceituais navegáveis
```

Não inclui:

```text
banco real
login real
gravação real
integração com Excel/VBA
integração real com REDE_WORK
```

## Etapa 2 — Backend local básico

Objetivo:

```text
Subir FastAPI de forma estável no servidor local.
```

Inclui:

```text
estrutura de app
configuração por ambiente
healthcheck
rotas básicas
servir front-end
```

## Etapa 3 — Login, usuários e permissões

Objetivo:

```text
Criar autenticação local real.
```

Inclui:

```text
usuários
senhas
perfis
permissões
sessão
controle de acesso por módulo
```

## Etapa 4 — Cadastros principais

Objetivo:

```text
Criar base operacional do sistema.
```

Inclui:

```text
produtos
clientes
obras
fornecedores
usuários
setores
```

## Etapa 5 — Produção, estoque e compras

Objetivo:

```text
Modelar os módulos operacionais.
```

Inclui:

```text
ordens de produção
processos
materiais
estoque
requisições
ordens de compra
pendências
```

## Etapa 6 — REDE_WORK

Objetivo:

```text
Integrar arquivos locais e versionamento controlado.
```

Inclui:

```text
MEDIÇÕES\SERVIDOR
MEDIÇÕES\LOCAL
version
CONFIG_
manifesto
conflitos
promoção controlada
```

## Etapa 7 — Integração com Excel/VBA legado

Objetivo:

```text
Ler logs, JSON, planilhas e processos já existentes sem quebrar o que funciona.
```

Inclui:

```text
REQ
O.P
Compras
RH
logs
metadados
auditoria
```

## Etapa 8 — Substituição gradual

Objetivo:

```text
Transferir funções do Excel/VBA para o sistema web apenas quando houver equivalência funcional comprovada.
```

Regra:

```text
Nada é substituído sem comparação, teste e validação.
```
