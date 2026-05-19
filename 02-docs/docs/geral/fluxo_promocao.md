# Fluxo de promoção — MRP_LOCAL

## Regra

Nada funcional deve ser promovido sem documentação, validação e status real.

## Fluxo recomendado

1. Ler `REGRAS_MRP.txt`.
2. Registrar problema, causa, solução, escopo, risco, status e versão.
3. Aplicar correção em cópia controlada.
4. Validar encoding.
5. Validar scripts e JSON.
6. Validar interface.
7. Atualizar manual/resumo quando afetar operação.
8. Executar precheck Git.
9. Commit/push automático somente se aprovado pelo fluxo.

## Estado atual

Base limpa para retomada de desenvolvimento. Ainda exige validação em Windows real antes de declarar blindagem.
