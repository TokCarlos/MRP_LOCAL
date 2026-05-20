MRP_LOCAL - LEITURA RAPIDA

Versao documental: v0.1.049-fix-launcher-painel-admin
Base anterior concluida: v0.1.049 painel admin local preparacao
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
- painel admin local em preparacao, separado do index.html.
- launcher clicavel principal: MRP_PAINEL_SERVIDOR.vbs
- launcher diagnostico: MRP_PAINEL_SERVIDOR.cmd

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

Planejamento registrado:
- proxima etapa planejada: validacao operacional no DEV casa com painel admin local
- etapa seguinte planejada: watchdog/tarefa automatica/reboot

Regra estrategica v0.1.050:
- objetivo futuro de distribuicao por instalador unico (exemplo: MRP_LOCAL_Setup.exe);
- nao implementar instalador agora;
- nao gerar exe agora;
- nao empacotar release agora;
- instalador futuro deve fazer precheck e classificar pendencias: CRITICO/OPCIONAL/RECOMENDADO;
- instalador futuro deve pedir aprovacao para acoes sensiveis;
- tecnologia do instalador sera decidida em etapa futura.

Registro adicional v0.1.050:
- acesso futuro por nome amigavel/proxy para ocultar IP e porta ao usuario final;
- 8765 continua interna/configuravel;
- integracao IA futura somente via backend com ferramentas controladas;
- sem implementacao de proxy/DNS/Tailscale Serve/IA nesta etapa;
- sem criacao de segredo, token ou API key nesta etapa.

Registro v0.1.051:
- base tecnica do backend para modulo Produtos iniciada;
- contrato de API planejado criado (sem API ativa);
- seed continua fonte temporaria;
- sem banco real e sem instalacao de dependencias;
- frontend e painel admin preservados.

Registro documental adicional:
- objetivo futuro de programa Windows instalado com instalador unico;
- artefatos de release podem incluir exe/dll/pyd/bin/runtime interno;
- repositorio DEV nao deve virar pasta de build;
- backend Produtos segue como proxima frente tecnica.
