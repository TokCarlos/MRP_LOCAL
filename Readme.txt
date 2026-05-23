MRP_LOCAL - LEITURA RAPIDA

LER PRIMEIRO:
1. 02-docs/REGRAS_ATUAIS_MRP.txt
2. 02-docs/LOG_PROGRESSO_MRP.txt
3. COMO_CRIAR_COMANDOS_CODEX.txt, quando for montar comando/revisao.

ESTADO ATUAL:
- Frontend ativo: 01-mrp/front_end
- Backend ativo: 01-mrp/back_end
- Frontend: porta 8765
- Backend FastAPI: porta 8876
- Produtos: modulo backend real com SQLite DEV
- Banco runtime DEV: 01-mrp/data/db/mrp_local_dev.sqlite
- Upload de imagens: 01-mrp/data/media/produtos
- Imagens oficiais/seed: 01-mrp/front_end/img/produtos
- Portable: pausado por enquanto
- Sistema: funcional em partes, mas ainda nao homologado/blindado

PROIBIDO:
- tocar em C:\Users\carlo\Desktop\PCP SERVIDOR\PCP
- usar raiz direta em C:\ como raiz do MRP
- commit/push sem ordem explicita
- alterar 01-mrp sem chave LIBERADO
- versionar logs reais, runtime, venv, cache, banco SQLite runtime ou credenciais

COMANDOS DEV:
Backend:
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_backend_start.ps1

Frontend:
powershell -NoProfile -ExecutionPolicy Bypass -File .\03-vs\scripts\servicos\mrp_frontend_start.ps1

Painel:
MRP_PAINEL_SERVIDOR.vbs
