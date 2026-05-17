# Instruções para Codex / IA de Desenvolvimento — MRP_LOCAL

## Regra principal

Não reescreva o sistema inteiro.

Trabalhe por escopo, módulo, versão e registro.

## Antes de alterar código

Leia obrigatoriamente:

```text
LEIA_PRIMEIRO.md
docs/geral/regras_do_projeto.md
docs/geral/status_geral.md
docs/geral/arquitetura.md
docs/geral/roadmap.md
```

Depois, leia a documentação do módulo afetado em:

```text
docs/modulos/<modulo>
```

## Proibições

Não fazer:

```text
reescrita total sem pedido explícito
troca de tecnologia sem justificativa
remoção de arquivos sem inventário
alteração de módulo funcional sem aviso
misturar refatoração com correção
alterar partes fora do escopo
fixar HOME-MACHINE no código como valor definitivo
introduzir dependência externa desnecessária
depender de cloud quando o objetivo é rede local
chamar protótipo de funcional sem teste real
```

## Obrigações

Sempre fazer:

```text
registrar mudança
atualizar status
preservar o que já funciona
limitar escopo
usar versionamento
separar módulo
tratar encoding e caminhos com cuidado
proteger caracteres especiais
testar o que foi alterado
informar pendências
```

## Escopo atual recomendado

A fase atual é:

```text
MRP_LOCAL_UI_CONCEITUAL
```

Prioridade:

```text
interface visual
navegação
telas fake
dados mockados
menu lateral
dashboard
padrão visual
```

Não priorizar agora:

```text
banco real
autenticação real
integração real com Excel/VBA
integração real com REDE_WORK
publicação em nuvem
```

## Servidor de teste

Referência atual:

```text
\\HOME-MACHINE
```

Mas isso deve ser configurável futuramente. Não fixar como regra definitiva do sistema.

## Resposta esperada ao concluir tarefa

Ao concluir qualquer alteração, informar:

```text
Versão:
Módulo:
Arquivos alterados:
O que foi feito:
O que foi preservado:
Teste realizado:
Status:
Pendências:
```
