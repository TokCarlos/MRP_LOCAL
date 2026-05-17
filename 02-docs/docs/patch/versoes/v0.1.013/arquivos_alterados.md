# Arquivos Alterados - v0.1.013

Data do registro: 2026-05-17
Status: `01_MRP_AUDITADO_E_ALINHADO_COM_ARQUITETURA_ATUAL`

## Snapshot criado

- `03-vs/snapshots/antes_v0.1.013/01-mrp`

## Arquivos alterados em `01-mrp`

### Criado

- `01-mrp/front_end/js/config.js`

### Alterados

- `01-mrp/front_end/index.html`
- `01-mrp/front_end/login.html`
- `01-mrp/front_end/acesso_negado.html`
- `01-mrp/front_end/js/auth.js`
- `01-mrp/front_end/js/api.js`
- `01-mrp/front_end/js/pages/dashboard.js`
- `01-mrp/front_end/js/pages/produtos_list.js`

## Detalhe das alteracoes

### `js/config.js`

Criado para centralizar configuracoes do front-end:

- ambiente atual.
- modo de autenticacao temporario.
- modo de dados mockados.
- chave de sessao.
- chave de storage mockado.
- usuario/senha temporarios `admin/admin`.
- flag de API mockada.
- flag de debug.

### `js/auth.js`

- Importa `APP_CONFIG`.
- Remove constantes locais fixas de usuario, senha, sessao e modo.
- Mantem autenticacao local temporaria `admin/admin` via configuracao.
- Mantem logout funcional.

### `js/api.js`

- Importa `APP_CONFIG`.
- Move chave de storage mockado para configuracao.
- Remove nomes legados `neonGET` e `neonINSERT`.
- Mantem adaptador local/mock com `localGET` e `localINSERT`.

### `js/pages/dashboard.js`

- Troca importacao de `neonGET` para `localGET`.

### `js/pages/produtos_list.js`

- Troca importacao de `neonGET/neonINSERT` para `localGET/localINSERT`.

### HTML

- `index.html`: adicionado `meta viewport` e links CSS das paginas da SPA.
- `login.html`: adicionado `meta viewport`.
- `acesso_negado.html`: adicionado `meta viewport`.

## Arquivos documentais criados

- `02-docs/docs/patch/versoes/v0.1.013/registro.md`.
- `02-docs/docs/patch/versoes/v0.1.013/auditoria_01_mrp.md`.
- `02-docs/docs/patch/versoes/v0.1.013/arquivos_alterados.md`.
- `02-docs/docs/patch/versoes/v0.1.013/conformidade_config_motor_adaptador.md`.
- `02-docs/docs/patch/versoes/v0.1.013/teste_web.md`.

## Arquivos nao alterados

- Nenhum arquivo foi apagado.
- Nenhum backend foi criado.
- Nenhum banco foi criado.
- Nenhuma dependencia foi instalada.
