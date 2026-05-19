
# AGENTS.md — MRP_LOCAL

Este projeto deve ser operado conforme `REGRAS_MRP.txt`.

Regras operacionais resumidas:

1. Antes de execução grande, ler `REGRAS_MRP.txt`.
2. Antes de alterar código, registrar problema, causa, solução, escopo, risco, status e versão.
3. Não chamar o sistema de blindado sem validação real em Windows.
4. Não criar dependência de `X:\`, `\\HOME-MACHINE`, usuário Windows, drive mapeado, IP fixo ou porta fora de configuração.
5. Texto visual pode usar acento; chaves técnicas devem ser ASCII-safe.
6. UTF-8 sem BOM é o padrão para texto persistente.
7. Logs reais, cache, temporários, `.git`, `.codex` e arquivos específicos de máquina não entram em pacote limpo.
8. Frontend atual é estático/mock local; backend e banco real ainda são etapas futuras.
9. Empacotamento futuro deve funcionar como programa instalável: precheck, runtime, instalação, firewall, tarefa/watchdog e healthcheck.
