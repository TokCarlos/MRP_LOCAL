# docs_runtime

Documentacao do nucleo transportavel de `01-mrp`.

O objetivo e separar o que pertence ao pacote executavel do MRP_LOCAL do que pertence ao ambiente DEV.

Regras:
- `front_end` e o frontend atual funcional;
- `back_end`, `engine` e `adapters` estao reservados;
- `config` deve concentrar variaveis de ambiente;
- `runtime`, `db`, `logs`, `tmp` e `backups` nao devem misturar codigo-fonte com estado local;
- caminhos fisicos podem existir em config, scripts de ambiente ou documentacao, mas nao em regra de negocio.