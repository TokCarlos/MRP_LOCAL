# Log Geral — MRP_LOCAL

## 2026-05-17 — v0.1.000

### Tipo

```text
Criação da documentação base
```

### Descrição

Criado pacote documental inicial para orientar o desenvolvimento do projeto MRP_LOCAL.

### Regras consolidadas

```text
Documentação antes do código
Versionamento obrigatório
Módulos separados
Status técnico obrigatório
Proteção contra revisão cega
Preservação de implementações funcionais
Interface visual primeiro
Servidor de teste atual: \\HOME-MACHINE
REDE_WORK como módulo próprio
Excel/VBA legado preservado
```

### Status

```text
IMPLEMENTADO DOCUMENTALMENTE
NÃO HOMOLOGADO COMO SISTEMA FUNCIONAL
```


---

## 2026-05-17 — v0.1.001

Organização inicial do workspace em `01-mrp`, `02-docs` e `03-vs`. Documentação base v0.1.000 incorporada em `02-docs`. `mrp-main.zip` inventariado, mas não incorporado ao sistema funcional.

---

## v0.1.002 - Padronização das pastas raiz

Data: 2026-05-17

Alteração:

```text
01-MRP_Projeto -> 01-mrp
02-Documentacao -> 02-docs
03-Versionamento -> 03-vs
```

Motivo: reduzir nomes, manter padrão físico curto, minúsculo e seguro para CMD, BAT, PowerShell, Python, ZIP, Git e caminhos de rede.

Status: APLICADO.

---

## 2026-05-17 — v0.1.033

### Tipo

Correção preventiva e limpeza controlada sem commit automático.

### Descrição

Corrigidos riscos de caminho legado em produtos, catálogo ATA com imagens inexistentes, falso positivo de encoding, auditoria presa em `X:\` e renderização de tabela com HTML não escapado.

### Resultado

```text
PRECHECK_OK
JSON_OK
JS_SYNTAX_OK
REFERENCIAS_ATIVAS_QUEBRADAS=0
COMMIT_MANUAL_SOLICITADO_PELO_USUARIO
```

### Status

```text
PREPARADO PARA COMMIT MANUAL
```

---

## 2026-05-18 — v0.1.034

### Tipo

Hotfix corretivo da tela de Produtos.

### Descrição

Corrigido erro introduzido na v0.1.033: `produtos_list.js` chamava `escapeHtml(...)`, mas a função auxiliar não existia no arquivo. Isso interrompia a renderização da tabela de Produtos.

### Resultado

```text
PRODUTOS_SEED_PRESERVADO=147
JS_SYNTAX_OK
ESCAPE_HTML_PRESENTE=SIM
DADOS_PERDIDOS=NAO
COMMIT_AUTOMATICO=NAO
```

### Status

```text
HOTFIX PARA COMMIT MANUAL
```
