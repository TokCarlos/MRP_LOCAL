MRP_LOCAL - LEITURA RAPIDA

Versao documental: v0.1.045-preparacao-portabilidade-pos-cimasp
Base anterior concluida: v0.1.044 imagens CIMASP
Commit base anterior: 60e5d6e - v0.1.044 - Cataloga imagens CIMASP

Estado real:
- frontend validado pelo usuario;
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
