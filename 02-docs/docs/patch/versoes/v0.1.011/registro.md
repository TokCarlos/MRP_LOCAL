# Registro v0.1.011 - MRP_LOCAL

Data do registro: 2026-05-17
Status: `AMBIENTES_TESTE_E_PRODUCAO_REGISTRADOS`

## Objetivo

Registrar os ambientes `TESTE_HOME` e `PRODUCAO_TRABALHO`, deixando claro que o acesso mobile via Tailscale validado pertence ao ambiente de teste e nao representa a operacao final da empresa.

## Arquivos criados ou atualizados

- `02-docs/docs/geral/ambientes.md`.
- `02-docs/docs/geral/acesso_local_e_tailscale.md`.
- `02-docs/docs/patch/versoes/v0.1.011/registro.md`.
- `02-docs/docs/patch/versoes/v0.1.011/checklist_ambientes.md`.

## TESTE_HOME registrado

- Servidor atual: `HOME-MACHINE`.
- Pasta de rede: `\\HOME-MACHINE\system_jpl`.
- Unidade local usada: `X:\`.
- IP Tailscale do PC: `100.108.26.10`.
- Telefone validado: `m15-de-carlos-alberto`.
- IP Tailscale do telefone: `100.90.190.4`.
- URL validada: `http://100.108.26.10:8000/login.html`.
- Uso: desenvolvimento, testes, validacao mobile e interface.

## PRODUCAO_TRABALHO registrado

- Acesso principal deve ser por rede local da empresa.
- Dispositivos devem acessar conectados ao Wi-Fi corporativo ou cabo de rede.
- Tailscale nao deve ser dependencia obrigatoria da operacao.
- Tailscale pode ser usado futuramente apenas como acesso tecnico remoto opcional.
- O servidor real devera ter IP local fixo ou nome de maquina confiavel.
- A URL final devera apontar para o servidor local da empresa.

## Regra de ambiente

Configuracoes de ambiente nao devem ficar fixas no codigo.

Devem ser configuraveis:

- IPs.
- Nomes de servidor.
- Portas.
- Caminhos.

Perfis previstos:

- `TESTE_HOME`.
- `PRODUCAO_TRABALHO`.
- `FUTURO_HOMOLOGACAO`.

## Estado atual

O ambiente atual e de teste, nao producao.

## Controle de escopo

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Apenas documentacao: SIM.
