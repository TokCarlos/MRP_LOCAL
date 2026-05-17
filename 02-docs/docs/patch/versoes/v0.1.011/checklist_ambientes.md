# Checklist de Ambientes - v0.1.011

Data do registro: 2026-05-17
Status: `AMBIENTES_TESTE_E_PRODUCAO_REGISTRADOS`

## Documentacao

- [x] Criar ou atualizar `02-docs/docs/geral/ambientes.md`.
- [x] Criar ou atualizar `02-docs/docs/geral/acesso_local_e_tailscale.md`.
- [x] Criar `02-docs/docs/patch/versoes/v0.1.011/registro.md`.
- [x] Criar `02-docs/docs/patch/versoes/v0.1.011/checklist_ambientes.md`.

## TESTE_HOME

- [x] Registrar servidor atual `HOME-MACHINE`.
- [x] Registrar pasta de rede `\\HOME-MACHINE\system_jpl`.
- [x] Registrar unidade local usada `X:\`.
- [x] Registrar IP Tailscale do PC `100.108.26.10`.
- [x] Registrar telefone validado `m15-de-carlos-alberto`.
- [x] Registrar IP Tailscale do telefone `100.90.190.4`.
- [x] Registrar URL validada `http://100.108.26.10:8000/login.html`.
- [x] Registrar uso: desenvolvimento, testes, validacao mobile e interface.
- [x] Registrar que o ambiente atual e de teste, nao producao.

## PRODUCAO_TRABALHO

- [x] Registrar que o acesso principal deve ser por rede local da empresa.
- [x] Registrar Wi-Fi corporativo ou cabo de rede como acesso dos dispositivos.
- [x] Registrar que Tailscale nao deve ser dependencia obrigatoria da operacao.
- [x] Registrar Tailscale como possivel acesso tecnico remoto opcional futuro.
- [x] Registrar necessidade de IP local fixo ou nome de maquina confiavel.
- [x] Registrar que a URL final deve apontar para servidor local da empresa.

## Regras de configuracao

- [x] Registrar que configuracoes de ambiente nao devem ficar fixas no codigo.
- [x] Registrar que IPs devem ser configuraveis.
- [x] Registrar que nomes de servidor devem ser configuraveis.
- [x] Registrar que portas devem ser configuraveis.
- [x] Registrar que caminhos devem ser configuraveis.
- [x] Registrar perfil `TESTE_HOME`.
- [x] Registrar perfil `PRODUCAO_TRABALHO`.
- [x] Registrar perfil `FUTURO_HOMOLOGACAO`.

## Restricoes aplicadas

- [x] Nao alterar `01-mrp`.
- [x] Nao alterar codigo funcional.
- [x] Nao criar backend.
- [x] Nao criar banco.
- [x] Apenas documentar.

## Pendencias futuras

- [ ] Definir dados reais de rede da empresa.
- [ ] Definir IP local fixo ou nome confiavel do servidor em `PRODUCAO_TRABALHO`.
- [ ] Definir mecanismo tecnico de configuracao por perfil quando backend/empacotamento forem criados.
- [ ] Validar URL final no Wi-Fi corporativo ou cabo de rede.
