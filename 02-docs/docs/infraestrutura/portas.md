# Portas - MRP_LOCAL

Status atual: v0.1.060.

## Portas oficiais DEV

- Frontend web: `8765`
- Backend FastAPI/API: `8876`

## Endpoints backend principais

- `GET http://<host>:8876/health`
- `GET http://<host>:8876/api/status`
- `GET http://<host>:8876/api/produtos`
- `GET http://<host>:8876/api/produtos/bases`
- `GET http://<host>:8876/media/produtos/<arquivo>`

## Regra

O frontend pode ser acessado por localhost, hostname, IP LAN ou Tailscale. O JS deve montar a API usando o mesmo host da pagina e porta `8876`, evitando `127.0.0.1` fixo quando acessado por outro PC.
