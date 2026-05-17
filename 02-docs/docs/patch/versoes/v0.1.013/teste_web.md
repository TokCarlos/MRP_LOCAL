# Teste Web - v0.1.013

Data do registro: 2026-05-17
Status: `01_MRP_AUDITADO_E_ALINHADO_COM_ARQUITETURA_ATUAL`

## Comando oficial de teste

```powershell
py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"
```

## URL oficial validada

`http://100.108.26.10:8000/login.html`

Resultado: HTTP 200 OK.

Observacao: a porta `100.108.26.10:8000` ja estava com servidor ativo no momento da validacao, entao nenhum novo servidor foi iniciado nessa porta e nenhum processo existente foi encerrado.

## Teste temporario local adicional

Foi iniciado servidor estatico temporario em loopback para validar arquivos alterados sem interferir na porta oficial.

Resultado:

- `http://127.0.0.1:8013/login.html`: HTTP 200.
- `http://127.0.0.1:8013/index.html`: HTTP 200.
- `http://127.0.0.1:8013/js/config.js`: HTTP 200.

O servidor temporario foi encerrado apos o teste.

## Checagem sintatica

Aprovados com `node --check`:

- `js/config.js`.
- `js/auth.js`.
- `js/api.js`.
- `js/spa.js`.
- `js/pages/dashboard.js`.
- `js/pages/produtos_list.js`.

## Busca de dependencias e valores fixos

Busca em `01-mrp/front_end` nao encontrou:

- StackAuth.
- Neon.
- URLs externas.
- JWT online obrigatorio.
- `Authorization` / `Bearer`.
- `HOME-MACHINE`.
- `X:\`.
- `100.108.26.10`.
- `100.90.190.4`.
- `localhost`.
- porta `8000` como regra funcional.

## Resultado

O front-end principal segue abrindo corretamente e esta alinhado para continuar ajustes de layout/responsividade.
