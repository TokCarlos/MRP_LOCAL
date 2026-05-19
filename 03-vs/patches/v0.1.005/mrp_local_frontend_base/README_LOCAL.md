# MRP_LOCAL Frontend Base - v0.1.005

Base temporaria criada a partir de `mrp-main.zip` para triagem e refatoracao local.

## Local

`03-vs/patches/v0.1.005/mrp_local_frontend_base/front_end`

## Como testar

1. Abra um terminal na pasta `front_end`.
2. Inicie um servidor estatico local, por exemplo:

```powershell
python -m http.server 8080
```

3. Acesse no navegador:

```text
http://localhost:8080/login.html
```

4. Entre com:

```text
usuario: admin
senha: admin
```

## Observacoes

- Esta etapa nao cria backend.
- Esta etapa nao cria banco de dados.
- A autenticacao e local e temporaria.
- Os dados sao mockados em `js/api.js` e documentados em `front_end/data/mock_data.json`.
- A SPA usa carregamento local de paginas em `front_end/pages`.
- Para evitar bloqueios de modulo ES e `fetch` local, teste via servidor estatico local em vez de abrir o HTML diretamente por `file://`.

## Dependencias online removidas

- StackAuth.
- Neon REST.
- JWT online obrigatorio.
- Chamadas externas de API.
