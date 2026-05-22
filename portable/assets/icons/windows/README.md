# Icones oficiais Windows - MRP_LOCAL

## Finalidade

Pacote visual oficial para atalhos Windows do MRP_LOCAL.

## Local oficial

- fonte PNG: `01-mrp/assets/icons/source/*.png`
- icones oficiais `.ico`: `01-mrp/assets/icons/windows/ico/*.ico`
- preview: `01-mrp/assets/icons/windows/preview/*.png`

## 4 icones oficiais atuais

- `mrp_pcp_light.ico`
- `mrp_jpl_dark.ico`
- `mrp_mrp_light.ico`
- `mrp_mrp_dark.ico`

## Uso recomendado em atalhos

- usar `.ico` direto no atalho Windows;
- atalho principal do painel: `mrp_mrp_dark.ico`;
- alternativo: `mrp_pcp_light.ico`.

## DLL de icones

- recurso historico/opcional/futuro;
- nao e o caminho principal atual para atalho;
- pode ser retomado somente em etapa especifica de empacotamento/instalador.

## Regras

- recurso visual/launcher, nao regra de negocio;
- pode ser reutilizado por instalador futuro;
- nao mover para `front_end` nem para runtime Python;
- .ico direto e mais confiavel para renderizacao da Area de Trabalho.
