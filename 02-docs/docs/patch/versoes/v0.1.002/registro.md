# Registro de Patch - v0.1.002

## Tipo

Organização estrutural.

## Escopo

Padronização das três pastas raiz do workspace.

## Alteração aplicada

```text
01-MRP_Projeto -> 01-mrp
02-Documentacao -> 02-docs
03-Versionamento -> 03-vs
```

## Motivo técnico

Os novos nomes são curtos, minúsculos e ASCII. Isso reduz risco com:

- CMD/BAT;
- PowerShell;
- Python;
- Git;
- ZIP;
- caminhos UNC;
- automações futuras;
- caracteres especiais e encoding.

## Regra consolidada

A partir desta versão, a raiz oficial do projeto passa a ser:

```text
01-mrp
02-docs
03-vs
```

## Status

APLICADO.

## Observação

Nenhum código funcional foi movido para `01-mrp` nesta etapa. O `mrp-main.zip` continua apenas inventariado para triagem futura.
