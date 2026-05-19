# Firewall Frontend 8765

Script de regra:

- `X:\03-vs\scripts\servicos\mrp_firewall_8765.ps1`

Regra prevista:

- Nome: `MRP_LOCAL_FRONTEND_8765`
- Direcao: entrada
- Protocolo: TCP
- Porta: 8765
- Perfil: Private

Comportamento:

- Se a regra ja existir, o script nao duplica.
