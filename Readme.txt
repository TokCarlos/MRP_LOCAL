MRP_LOCAL - LEITURA RAPIDA

Versao documental: v0.1.047-registro-deploy-trabalho-e-teste-dev
Base anterior concluida: v0.1.046 pacote protegido validado no trabalho
Commit base relevante anterior: 173456b - chore: preparar portabilidade pos-cimasp v0.1.045

Estado real:
- frontend validado pelo usuario;
- deploy no trabalho validado;
- acesso por outras maquinas da rede validado;
- acesso remoto via Tailscale validado;
- porta 8765 OK;
- healthcheck OK;
- sistema abrindo corretamente;
- sem backend;
- sem banco real;
- sem PostgreSQL instalado pelo sistema;
- sem Python portable ativado;
- sem FastAPI funcional;
- ainda nao blindado.

Operacao principal:
- MRP_MENU_SISTEMA.bat
- .\03-vs\scripts\servicos\mrp_frontend_start.ps1
- .\03-vs\scripts\servicos\mrp_frontend_stop.ps1
- .\03-vs\scripts\servicos\mrp_frontend_status.ps1
- .\03-vs\scripts\servicos\mrp_frontend_healthcheck.ps1

Comando py/http.server:
- apenas diagnostico tecnico;
- nao usar como operacao principal.

Area portable:
- pasta oficial auxiliar para deploy/teste/acesso externo;
- manter conteudo em `portable` sem mover para raiz;
- `portable\CONFIGURAR_ACESSO_MRP_REDE.bat` usado para alinhar PCs clientes (LAN/Tailscale/proxy bypass quando aplicavel).

IPs de teste operacional (nao sao regra fixa):
- LAN: 192.168.1.71
- Tailscale: 100.117.224.127

Scripts:
- .\03-vs\scripts\servicos\mrp_frontend_start.ps1
- .\03-vs\scripts\servicos\mrp_frontend_stop.ps1
- .\03-vs\scripts\servicos\mrp_frontend_status.ps1
- .\03-vs\scripts\servicos\mrp_frontend_healthcheck.ps1

Precheck portabilidade:
.\01-mrp\install\mrp_install_precheck.ps1

Precheck saude:
.\01-mrp\health\mrp_health_precheck.ps1

Pendencias antes de blindagem:
- watchdog continuo;
- tarefa Windows;
- reboot;
- queda de energia;
- queda de rede;
- logs em execucao prolongada;
- pacote release separado do pacote dev.
