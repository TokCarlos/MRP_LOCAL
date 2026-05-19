# docs_runtime

Documentacao do nucleo transportavel de `01-mrp`.

O objetivo e separar o que pertence ao pacote executavel do MRP_LOCAL do que pertence ao ambiente DEV.
Etapa atual: v0.1.049-painel-admin-local-preparacao.

Regras:
- `front_end` e o frontend atual funcional;
- `back_end`, `engine` e `adapters` estao reservados;
- backend real e banco real ainda nao estao ativos;
- `config` deve concentrar variaveis de ambiente;
- `runtime`, `db`, `logs`, `tmp` e `backups` nao devem misturar codigo-fonte com estado local;
- caminhos fisicos podem existir em config, scripts de ambiente ou documentacao, mas nao em regra de negocio.
- pasta `portable` (raiz do projeto) e area auxiliar operacional de deploy/teste externo, fora da regra de negocio.
- painel administrativo local separado do index.html para uso no servidor.

Planejamento registrado:
- proxima etapa planejada: validacao operacional no DEV casa com painel admin local;
- etapa seguinte planejada: watchdog/tarefa automatica/reboot.
