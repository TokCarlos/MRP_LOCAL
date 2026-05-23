# Execucao automatica - MRP_LOCAL

Status atual: backend FastAPI existe para Produtos, mas execucao automatica ainda nao esta homologada.

## Estado atual

- Frontend: porta 8765.
- Backend: porta 8876.
- Painel local pode iniciar/parar/status/healthcheck.
- Backend deve iniciar usando a venv em `01-mrp/runtime/venv_backend` quando existir.

## Pendente

- watchdog continuo;
- tarefa Windows;
- reboot/logoff/logon;
- queda de energia;
- queda de rede;
- validacao prolongada.

Nao chamar de blindado/homologado ate essas validacoes serem feitas.
