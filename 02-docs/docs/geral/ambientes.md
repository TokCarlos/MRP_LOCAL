# Ambientes - MRP_LOCAL

Versao de referencia: v0.1.011
Data do registro: 2026-05-17
Status: `AMBIENTES_TESTE_E_PRODUCAO_REGISTRADOS`

## Objetivo

Registrar os ambientes previstos para o `MRP_LOCAL` e separar claramente ambiente de teste, ambiente de producao e ambiente futuro de homologacao.

## Regra principal

O ambiente atual e de teste, nao producao.

Configuracoes de ambiente nao devem ficar fixas no codigo. IPs, nomes de servidor, portas e caminhos devem ser configuraveis.

O projeto deve aceitar perfis de ambiente:

- `TESTE_HOME`
- `PRODUCAO_TRABALHO`
- `FUTURO_HOMOLOGACAO`

## TESTE_HOME

Uso: desenvolvimento, testes, validacao mobile e interface.

Dados registrados:

- Servidor atual: `HOME-MACHINE`.
- Pasta de rede: `\\HOME-MACHINE\system_jpl`.
- Unidade local usada: `X:\`.
- IP Tailscale do PC: `100.108.26.10`.
- Telefone validado: `m15-de-carlos-alberto`.
- IP Tailscale do telefone: `100.90.190.4`.
- URL validada: `http://100.108.26.10:8000/login.html`.

Observacoes:

- Tailscale foi validado para teste mobile.
- Este ambiente nao representa a operacao final da empresa.
- Subnet routes nao foram necessarios no teste validado.

## PRODUCAO_TRABALHO

Uso: operacao principal da empresa.

Regras previstas:

- O acesso principal deve ser por rede local da empresa.
- Dispositivos devem acessar conectados ao Wi-Fi corporativo ou cabo de rede.
- Tailscale nao deve ser dependencia obrigatoria da operacao.
- Tailscale pode ser usado futuramente apenas como acesso tecnico remoto opcional.
- O servidor real devera ter IP local fixo ou nome de maquina confiavel.
- A URL final devera apontar para o servidor local da empresa.

## FUTURO_HOMOLOGACAO

Uso previsto: validacao controlada antes de promocao para producao.

Regras iniciais:

- Deve ficar separado de `PRODUCAO_TRABALHO`.
- Deve permitir testes sem afetar a operacao principal.
- Deve documentar versao, origem, destino, responsavel e resultado dos testes.

## Diretrizes de configuracao

- Nao fixar IPs no codigo.
- Nao fixar nomes de servidor no codigo.
- Nao fixar portas no codigo.
- Nao fixar caminhos locais no codigo.
- Usar configuracao por perfil de ambiente quando backend e empacotamento forem definidos.

## Controle de escopo desta etapa

- `01-mrp` alterado: NAO.
- Codigo funcional alterado: NAO.
- Backend criado: NAO.
- Banco criado: NAO.
- Apenas documentacao: SIM.
