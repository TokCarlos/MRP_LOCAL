MRP_LOCAL - README PORTABLE

O que e:
- Pacote portable funcional para rodar/testar o MRP_LOCAL fora do repositorio DEV.
- Contem frontend, backend, configuracao minima, assets, dados de teste e scripts de operacao.

Como executar:
1. Abra terminal dentro da pasta `portable`.
2. Rode `MRP_MENU_SISTEMA.bat` para operar por menu.
3. Ou rode `start_mrp.bat` diretamente.
4. Rode `status_mrp.bat` para verificar processos e portas.

Como parar:
- Rode `stop_mrp.bat`.

Como verificar saude:
- Rode `healthcheck_mrp.bat`.

Portas usadas:
- Frontend: `8765` (configuravel no topo de `start_mrp.bat`).
- Backend: `8876` (configuravel no topo de `start_mrp.bat`).

Atalho e painel:
- `CRIAR_ATALHO_PAINEL_SERVIDOR.bat` cria atalho na area de trabalho.
- `MRP_PAINEL_SERVIDOR.vbs` abre o launcher silencioso.
- `MRP_PAINEL_SERVIDOR.cmd` executa o painel local.

Dependencias minimas:
- Windows com `cmd` e `powershell`.
- Python no PATH para frontend estatico.
- Para backend: Python com `fastapi` e `uvicorn`.

Avisos:
- Nao e instalador final.
- Nao contem documentacao DEV completa.
- Nao contem Git, historico ou quarentena.
- Logs ficam em `portable/logs`.
