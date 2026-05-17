# Acesso Local e Tailscale - MRP_LOCAL

Versao de referencia: v0.1.011
Data do registro: 2026-05-17
Status: `AMBIENTES_TESTE_E_PRODUCAO_REGISTRADOS`

## Objetivo

Registrar o procedimento validado para acessar o front-end do `MRP_LOCAL` pela rede Tailscale no ambiente `TESTE_HOME` e separar esse teste da futura operacao em `PRODUCAO_TRABALHO`.

## Ambiente atual

O ambiente atual e de teste, nao producao.

## TESTE_HOME

Uso: desenvolvimento, testes, validacao mobile e interface.

- Servidor atual: `HOME-MACHINE`.
- Pasta de rede: `\\HOME-MACHINE\system_jpl`.
- Unidade local usada: `X:\`.
- Sistema principal servido no teste: `X:\01-mrp\front_end`.
- Servidor local: Python HTTP server.
- IP Tailscale do PC: `100.108.26.10`.
- Telefone validado: `m15-de-carlos-alberto`.
- IP Tailscale do telefone: `100.90.190.4`.
- URL validada: `http://100.108.26.10:8000/login.html`.

## Comando oficial no TESTE_HOME

Executar no PC/SERVIDOR:

```powershell
py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"
```

## Resultado validado

A pagina `login.html` abriu corretamente no telefone via Tailscale.

## Subnet routes

Subnet routes nao foram necessarios neste cenario.

Motivo: o telefone acessou diretamente o IP Tailscale do PC (`100.108.26.10`) na porta `8000`.

## Diagnostico do problema anterior

O problema anterior era que o telefone aparecia offline no Tailscale. Depois que o telefone ficou online, o acesso funcionou.

## PRODUCAO_TRABALHO

O acesso principal deve ocorrer pela rede local da empresa.

Regras previstas:

- Dispositivos devem acessar conectados ao Wi-Fi corporativo ou cabo de rede.
- Tailscale nao deve ser dependencia obrigatoria da operacao.
- Tailscale pode ser usado futuramente apenas como acesso tecnico remoto opcional.
- O servidor real devera ter IP local fixo ou nome de maquina confiavel.
- A URL final devera apontar para o servidor local da empresa.

## Perfis de ambiente previstos

O projeto deve aceitar perfis de ambiente:

- `TESTE_HOME`
- `PRODUCAO_TRABALHO`
- `FUTURO_HOMOLOGACAO`

## Regra de configuracao

Configuracoes de ambiente nao devem ficar fixas no codigo.

Devem ser configuraveis:

- IPs.
- Nomes de servidor.
- Portas.
- Caminhos.

## Checklist rapido para TESTE_HOME

- [ ] Confirmar que o PC esta online no Tailscale.
- [ ] Confirmar que o telefone esta online no Tailscale.
- [ ] Iniciar o servidor com bind no IP Tailscale do PC.
- [ ] Abrir `http://100.108.26.10:8000/login.html` no telefone.
- [ ] Se falhar, verificar se o telefone aparece offline no Tailscale.

## Regras

- Este procedimento nao cria backend.
- Este procedimento nao cria banco.
- Este procedimento nao altera codigo funcional.
- Este procedimento serve apenas o front-end existente para teste local/remoto controlado.
