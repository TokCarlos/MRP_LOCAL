# Empacotamento / instalador futuro

Regra de negocio registrada: o MRP_LOCAL deve evoluir para um programa instalavel/empacotado.

Cenario alvo: a maquina de desenvolvimento tem tudo pronto, mas uma maquina limpa nao tem Python, runtime, firewall, tarefa Windows, configuracao, permissao nem estrutura local. O instalador futuro deve preparar tudo antes de iniciar o sistema.

Requisitos minimos do instalador futuro:

1. Precheck do Windows, permissao, PowerShell e rede local.
2. Instalar ou embutir runtime necessario, preferencialmente portatil.
3. Copiar arquivos do sistema para local padrao configuravel.
4. Criar configuracao local sem hardcode de maquina.
5. Criar firewall da porta ativa.
6. Criar tarefa/servico de inicializacao.
7. Ativar watchdog e healthcheck.
8. Registrar logs de instalacao.
9. Falhar de forma clara se dependencia obrigatoria nao puder ser instalada.
10. Nao colocar regra de negocio no instalador. O instalador apenas prepara ambiente.
