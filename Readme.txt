MRP_LOCAL - LEITURA RAPIDA

Versao documental: v0.1.043-preparacao-portabilidade
Base funcional: v0.1.042 recovery
Commit base: 8c649e6 - chore: recovery funcional e saneamento operacional do MRP local

Estado real:
- frontend validado pelo usuario;
- porta 8765 OK;
- healthcheck OK;
- sistema abrindo corretamente;
- sem backend;
- sem banco real;
- ainda nao blindado.

Comando antigo apenas historico:
py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"

Comando novo oficial DEV:
py -m http.server 8765 --bind 0.0.0.0 --directory "X:\01-mrp\front_end"

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