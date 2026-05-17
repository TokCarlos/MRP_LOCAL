# Conformidade Configuracao Motor Adaptador - v0.1.013

Data do registro: 2026-05-17
Status: `01_MRP_AUDITADO_E_ALINHADO_COM_ARQUITETURA_ATUAL`

## Regra avaliada

```text
Ambiente e configuracao.
Meio de acesso e adaptador.
Regra de negocio e motor.
```

O sistema nao pode ficar preso a `HOME-MACHINE`, `X:\`, IP Tailscale, porta fixa, caminho absoluto ou dominio antigo.

## Resultado da auditoria

O `01-mrp/front_end` ficou alinhado com a regra no escopo atual do front-end.

## CONFIGURACAO

Criado:

`01-mrp/front_end/js/config.js`

Configuracoes centralizadas:

- `ambiente`: `TESTE_HOME`.
- `authMode`: `LOCAL_TEMPORARIO`.
- `dataMode`: `MOCK_LOCAL`.
- `sessionKey`.
- `mockStorageKey`.
- login temporario `admin/admin`.
- `api.baseUrl` vazio para modo mock atual.
- `api.useMock` como `true`.
- `flags.debug`.

## MOTOR

Ainda nao existe motor de regra de negocio formal no `01-mrp`.

Nesta etapa, o front-end usa dados mockados e regras temporarias simples. A auditoria registrou que motores futuros devem ficar desacoplados de interface e infraestrutura.

## ADAPTADORES

Adaptadores atuais no front-end:

- `js/api.js`: adaptador local/mock de dados.
- `js/auth.js`: autenticacao local temporaria baseada em configuracao.
- `js/security.js`: validacao de sessao local.
- `js/spa.js`: adaptador de navegacao SPA no navegador.

## Dependencias online

Nao foram encontradas dependencias online ativas apos os ajustes:

- StackAuth: NAO encontrado.
- Neon: NAO encontrado.
- URLs externas de API: NAO encontradas.
- JWT online obrigatorio: NAO encontrado.
- Hospedagem antiga: NAO encontrada.

## Valores fixos

Nao foram encontrados em codigo funcional apos os ajustes:

- `HOME-MACHINE`.
- `X:\`.
- `100.108.26.10`.
- `100.90.190.4`.
- `localhost`.
- porta `8000`.

## Valores mantidos apenas como teste/documentacao

- Comando oficial: `py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"`.
- URL validada: `http://100.108.26.10:8000/login.html`.

Esses valores nao foram gravados como regra funcional do sistema.

## Decisao

O `01-mrp/front_end` esta apto a continuar os proximos ajustes de layout e responsividade, desde que novas alteracoes continuem respeitando configuracao, motor e adaptadores.

## Pendencias arquiteturais futuras

- Criar backend FastAPI somente em etapa propria.
- Criar banco local somente em etapa propria.
- Separar motores reais de regra de negocio quando os modulos funcionais forem implementados.
- Avaliar migracao futura de configuracao para `config/ambiente.json` e `config/perfis/*.json`.
