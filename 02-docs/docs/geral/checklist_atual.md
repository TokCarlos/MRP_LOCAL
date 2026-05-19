# Checklist atual — MRP_LOCAL

## Base limpa

- [x] `REGRAS_MRP.txt` incorporado.
- [x] Configuração central criada.
- [x] Scripts de serviço sem dependência direta de raiz fixa.
- [x] Logs reais removidos do pacote limpo.
- [x] `Thumbs.db` removido.
- [x] `.git` e `.codex` removidos do pacote limpo.
- [x] Watchdog reestruturado para execução contínua.
- [x] Manual e resumo operacional em `.txt` criados.
- [x] Gancho de instalador/empacotamento futuro registrado.

## Ainda pendente de validação em Windows real

- [ ] Start manual.
- [ ] Healthcheck manual.
- [ ] Stop manual.
- [ ] Watchdog reiniciando processo morto.
- [ ] Tarefa Windows após logoff/logon.
- [ ] Reboot.
- [ ] Queda de rede.
- [ ] Queda de energia.
- [ ] Acesso LAN.
- [ ] Acesso Tailscale, se usado.
- [ ] Empacotamento com runtime portable ou instalador automático.
