# DLL de icones Windows - MRP_LOCAL

## Finalidade

Pacote visual para atalhos Windows do MRP_LOCAL.

## Local oficial

- `01-mrp/assets/icons/windows/MRP_ICONS.dll`
- `01-mrp/assets/icons/windows/MRP_ICONS.rc`
- `01-mrp/assets/icons/windows/manifest_icons.json`
- `01-mrp/assets/icons/windows/icons/*.ico`
- `01-mrp/assets/icons/windows/preview/*.png`

## Uso em atalhos

- `MRP_ICONS.dll,0` = principal PCP/MRP
- `MRP_ICONS.dll,1` = servidor
- `MRP_ICONS.dll,2` = painel admin
- `MRP_ICONS.dll,3` = produtos/aparelhos
- `MRP_ICONS.dll,4` = rede/Tailscale/clientes

## Regras

- recurso visual/launcher, nao regra de negocio;
- pode ser reutilizado por instalador futuro;
- nao mover para `front_end` nem para runtime Python.
