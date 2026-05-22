# RELATORIO SANEAMENTO E ORGANIZACAO MRP_LOCAL

Data: 2026-05-21
Versao alvo: v0.1.054
Escopo: saneamento estrutural, regras de ambiente, quarentena e preparacao portable.

## 1. Auditoria inicial sem alteracao

Status: concluida antes de outras alteracoes.

Raiz fisica oficial analisada:

```text
C:\Users\carlo\Desktop\PCP SERVIDOR\SISTEMA_MRP
```

Caminho operacional de rede:

```text
\\HOME-MACHINE\system_jpl
```

Unidade mapeada operacional:

```text
X:\
```

## 2. Estrutura atual de pastas

Estrutura de primeiro nivel encontrada:

```text
.codex/
.git/
00-manual-dev/
01-mrp/
02-docs/
03-vs/
portable/
.gitignore
AGENTS.md
CRIAR_ATALHO_PAINEL_SERVIDOR.bat
GERAR_PACOTE_LIMPO_DEV.bat
ideias.txt
manifesto_workspace.json
MRP_MENU_SISTEMA.bat
MRP_PAINEL_SERVIDOR.cmd
MRP_PAINEL_SERVIDOR.vbs
README.md
Readme.txt
REGRAS_MRP.txt
REPARAR_CACHE_ICONES_WINDOWS.bat
Stop.ps1
system_jpl.zip
```

Estrutura atual principal de `01-mrp`:

```text
adapters/
assets/
back_end/
backups/
config/
data/
db/
docs_runtime/
engine/
front_end/
health/
install/
logs/
runtime/
tmp/
tools/
```

Estrutura atual de `02-docs` e `03-vs` esta funcional e nao deve receber reorganizacao profunda nesta etapa.

## 3. Arquivos suspeitos

| Origem | Motivo | Acao inicial |
|---|---|---|
| `Stop.ps1` | Script solto na raiz, com caminho hardcoded para `\\HOME-MACHINE\system_jpl` e logica operacional agressiva de parada/limpeza. | Candidato a quarentena. |
| `system_jpl.zip` | Pacote zip pesado solto na raiz, 61 MB, aparenta artefato gerado. | Candidato a quarentena. |
| `portable/*PC_TRABALHO*` e textos antigos | Material de deploy/teste antigo com destino `X:\PCP`/`X:\9_Sistema`. | Candidato a quarentena ao tornar portable minimo. |
| Scripts soltos na raiz `MRP_*`, `CRIAR_ATALHO_*`, `GERAR_PACOTE_*`, `REPARAR_CACHE_*` | Podem ser atalhos operacionais, mas a raiz esta poluida. | Preservar nesta etapa, revisar depois. |

## 4. Arquivos temporarios, logs, caches e pycache

Encontrado:

```text
01-mrp/back_end/app/**/__pycache__/
01-mrp/back_end/app/**/*.pyc
03-vs/scripts/backend/__pycache__/
03-vs/scripts/painel/__pycache__/
01-mrp/logs/admin/launcher_painel.log
01-mrp/logs/admin/painel_admin.log
01-mrp/logs/servicos/frontend.err.log
01-mrp/logs/servicos/frontend.health.log
01-mrp/logs/servicos/frontend.out.log
01-mrp/logs/servicos/frontend.start.log
01-mrp/logs/servicos/frontend.stop.log
```

Nao foi identificado `Thumbs.db` na primeira varredura.

## 5. Arquivos soltos na raiz

Arquivos soltos preservados inicialmente para evitar quebra operacional:

```text
.gitignore
AGENTS.md
CRIAR_ATALHO_PAINEL_SERVIDOR.bat
GERAR_PACOTE_LIMPO_DEV.bat
ideias.txt
manifesto_workspace.json
MRP_MENU_SISTEMA.bat
MRP_PAINEL_SERVIDOR.cmd
MRP_PAINEL_SERVIDOR.vbs
README.md
Readme.txt
REGRAS_MRP.txt
REPARAR_CACHE_ICONES_WINDOWS.bat
Stop.ps1
system_jpl.zip
```

## 6. Scripts com caminhos hardcoded

Ocorrencias relevantes encontradas:

```text
Stop.ps1 -> \\HOME-MACHINE\system_jpl
03-vs/scripts/catalogar_img_cimasp_v0_1_044.ps1 -> X:\
portable/MRP_TRABALHO_PRECHECK.bat -> X:\PCP\09_Sistema
portable/LEIA_SEGURANCA_PC_TRABALHO.txt -> X:\PCP\09_Sistema
portable/LEIA_INSTALACAO_PC_TRABALHO.txt -> X:\PCP\09_Sistema
portable/LEIA_FIX_START_STOP_STATUS.txt -> X:\PCP\09_Sistema
portable/COLINHA_EXECUCAO_PC_TRABALHO_MRP_ATUALIZADA.txt -> X:\9_Sistema / X:\PCP\09_Sistema
```

Ocorrencias em documentacao historica existem e devem ser tratadas como historico, nao necessariamente como codigo ativo.

## 7. Ocorrencias de caminhos monitorados

Padroes verificados:

```text
C:\system_jpl
C:\MRP_REDE_FAKE
\\HOME-MACHINE\system_jpl
X:\
C:\Users\carlo\Desktop\PCP SERVIDOR\PCP
C:\Users\carlo\Desktop\PCP SERVIDOR\SISTEMA_MRP
```

Resultado inicial:

- `X:\` aparece em documentacao historica, regras antigas, scripts e portable antigo.
- `\\HOME-MACHINE\system_jpl` aparece em documentacao e em `Stop.ps1`.
- A pasta proibida `C:\Users\carlo\Desktop\PCP SERVIDOR\PCP` deve aparecer apenas em regras/validadores como bloqueio.
- A raiz fisica oficial deve aparecer apenas em documentacao operacional, scripts de infraestrutura e validadores.

## 8. Pode ser movido para quarentena

Itens candidatos:

| Origem | Destino proposto | Motivo | Risco | Status |
|---|---|---|---|---|
| `Stop.ps1` | `03-vs/quarentena/<timestamp>/Stop.ps1` | Script solto com hardcode e logica agressiva. | Medio: pode haver atalho antigo chamando o arquivo. | Pendente. |
| `system_jpl.zip` | `03-vs/quarentena/<timestamp>/system_jpl.zip` | Artefato zip pesado na raiz. | Baixo/medio: pode ser pacote antigo usado manualmente. | Pendente. |
| `01-mrp/**/__pycache__` | `03-vs/quarentena/<timestamp>/...` | Cache Python. | Baixo. | Pendente. |
| `01-mrp/**/*.pyc` | `03-vs/quarentena/<timestamp>/...` | Bytecode Python. | Baixo. | Pendente. |
| `03-vs/scripts/**/__pycache__` | `03-vs/quarentena/<timestamp>/...` | Cache Python em scripts de apoio. | Baixo. | Pendente. |
| `01-mrp/logs/**/*.log` | `03-vs/quarentena/<timestamp>/...` | Logs reais de execucao. | Baixo. | Pendente. |
| `portable` antigo de PC trabalho | `03-vs/quarentena/<timestamp>/portable_old/...` | Portable deve virar pacote minimo. | Medio: scripts antigos podem ser usados manualmente. | Pendente. |

## 9. Deve permanecer

```text
.git/
.codex/
01-mrp/ codigo ativo e estrutura operacional
02-docs/
03-vs/
portable/ como area oficial auxiliar, apos saneamento
AGENTS.md
.gitignore
REGRAS_MRP.txt
README.md
Readme.txt
manifesto_workspace.json
```

## 10. Deve ser reorganizado

`01-mrp` pode evoluir para estrutura profissional por camadas:

```text
app/frontend
app/backend
core/engine
infrastructure/adapters
infrastructure/config
operations/health
operations/install
operations/tools
assets
data
runtime
logs
tmp
backups
docs_runtime
```

Risco principal: scripts e imports existentes ainda apontam para `front_end`, `back_end`, `engine`, `adapters`, `config`, `health`, `install` e `tools`. Reorganizacao completa deve atualizar referencias ou manter compatibilidade.

## 11. Riscos de quebra

1. Mover `front_end` para `app/frontend` quebra scripts que servem `01-mrp/front_end`.
2. Mover `back_end` para `app/backend` pode quebrar imports Python e comandos de execucao.
3. Mover `config` pode quebrar scripts e backend que procuram `01-mrp/config`.
4. Mover `tools`, `install` e `health` pode quebrar comandos operacionais antigos.
5. Limpar `portable` pode remover material antigo ainda usado manualmente; por isso deve ir para quarentena, nao ser apagado.
6. O validador novo usa caminhos de infraestrutura DEV/teste; isso deve ficar isolado em scripts operacionais, sem virar regra de negocio.

## 12. Proxima fase

Executar documentacao das novas regras em arquivos oficiais e depois aplicar mudancas com quarentena e validacao.

---

## 13. Relatorio final da execucao

Status: execucao parcial concluida com bloqueio de commit por falha de validacao de ambiente.

## 14. O que foi alterado

Documentacao:

- `REGRAS_MRP.txt` atualizado com regra v0.1.054.
- `README.md` atualizado.
- `Readme.txt` atualizado.
- `02-docs/docs/geral/REGRAS_MRP.txt` sincronizado.
- `02-docs/docs/geral/status_geral.md` atualizado.
- `02-docs/docs/MANUAL_DEV_COMPLETO.txt` criado.
- `02-docs/docs/RESUMO_OPERACIONAL_DO_SISTEMA.txt` criado.
- registro de patch criado em `02-docs/docs/patch/versoes/v0.1.054`.

Infraestrutura:

- criado `01-mrp/tools/validate_environment.ps1`;
- criado log controlado em `01-mrp/logs/validation`;
- criados scripts oficiais em `portable`:
  - `01_configurar_share_sistema_mrp_admin.ps1`;
  - `02_mapear_x_sistema_mrp_usuario.bat`;
  - `03_validar_ambiente_sistema_mrp.ps1`;
  - `start_mrp.bat`;
  - `stop_mrp.bat`;
  - `status_mrp.bat`;
  - `healthcheck_mrp.bat`.

Estrutura:

- criada estrutura alvo em `01-mrp/app`, `01-mrp/core`, `01-mrp/infrastructure`, `01-mrp/operations`, `01-mrp/data/*` e `01-mrp/assets/images`;
- `adapters` migrado para `infrastructure/adapters` com compatibilidade em `01-mrp/adapters`;
- `engine` migrado para `core/engine` com compatibilidade em `01-mrp/engine`;
- `front_end`, `back_end`, `config`, `health`, `install` e `tools` ativos preservados para evitar quebra.

Portable:

- portable antigo movido para quarentena;
- portable atual reduzido a scripts oficiais, README e pastas minimas `config`, `app`, `runtime` e `assets`.

Gitignore:

- `03-vs/quarentena/**`, `portable/logs/**`, `portable/tmp/**`, `01-mrp/logs/**`, `01-mrp/tmp/**`, `01-mrp/runtime/**`, `__pycache__`, `*.pyc`, `Thumbs.db`, `*.tmp`, `*.bak` e `*.old` cobertos/preservados com `.gitkeep` quando necessario.

## 15. O que foi movido para quarentena

Destino:

```text
03-vs/quarentena/2026-05-21_200953_saneamento_estrutura/
```

Movido:

- `Stop.ps1`;
- `system_jpl.zip`;
- `01-mrp/back_end/app/**/__pycache__`;
- `03-vs/scripts/backend/__pycache__`;
- `03-vs/scripts/painel/__pycache__`;
- `01-mrp/logs/admin/*.log`;
- `01-mrp/logs/servicos/*.log`;
- portable legado de PC trabalho, incluindo `CONFIGURAR_ACESSO_MRP_REDE.bat`, `MRP_TRABALHO_*`, `LEIA_*` e relatorio antigo.

Observacao: quarentena nao foi apagada e esta ignorada pelo Git; apenas `03-vs/quarentena/.gitkeep` deve ser versionado.

## 16. O que foi preservado

- `.git`;
- `.codex`;
- `01-mrp/front_end`;
- `01-mrp/back_end`;
- `01-mrp/config`;
- `01-mrp/health`;
- `01-mrp/install`;
- `01-mrp/tools`;
- `02-docs`;
- `03-vs`;
- scripts operacionais de servico em `03-vs/scripts/servicos`;
- arquivos raiz essenciais: `AGENTS.md`, `.gitignore`, `README.md`, `Readme.txt`, `REGRAS_MRP.txt`.

## 17. O que nao foi alterado por risco

- `front_end` nao foi movido para `app/frontend` porque scripts ativos ainda servem `01-mrp/front_end`.
- `back_end` nao foi movido para `app/backend` porque imports Python e scripts de backend usam `01-mrp/back_end`.
- `config` nao foi movido para `infrastructure/config` porque scripts leem `01-mrp/config/mrp_local.env.json`.
- `health`, `install` e `tools` nao foram movidos porque existem contratos operacionais ativos e o validador novo foi especificado em `01-mrp/tools`.

## 18. Testes executados

- `git diff --check`: OK.
- Parse dos scripts PowerShell novos: OK.
- AST parse de 33 arquivos Python em `01-mrp/back_end/app` e `03-vs/scripts`: OK.
- `node --check` em `01-mrp/front_end/js/**/*.js`: OK.
- Busca por `__pycache__` e `*.pyc` fora da quarentena: OK.
- Revisao do conteudo atual de `portable`: OK, pacote minimo.

## 19. Testes que falharam

`01-mrp/tools/validate_environment.ps1` executou e retornou `exit code 1`.

Motivos:

- `Get-SmbShare system_jpl` retornou `Acesso negado` nesta sessao;
- `X:\` nao existe nesta sessao.

Isso impede confirmar:

- share `system_jpl` apontando para a raiz oficial;
- gravacao em `X:\`;
- reflexo do arquivo temporario na raiz fisica oficial;
- ausencia do arquivo temporario na pasta PCP.

## 20. Testes nao executados

- `portable/01_configurar_share_sistema_mrp_admin.ps1`, porque exige Administrador.
- validacao real de frontend/backend rodando.
- commit final, bloqueado pela falha de validacao.

## 21. Riscos restantes

1. Ambiente Windows ainda precisa confirmar share e mapeamento `X:\`.
2. Documentacao historica ainda possui muitas referencias a `X:\` e `\\HOME-MACHINE\system_jpl`; isso e aceitavel como historico, mas pode confundir operadores.
3. Ha alteracoes preexistentes no worktree fora deste saneamento; commit seletivo deve evitar incluir trabalho alheio.
4. A migracao estrutural completa de `front_end` e `back_end` deve ser feita em etapa propria, com atualizacao de scripts e imports.

## 22. Proxima acao recomendada

1. Rodar `portable/01_configurar_share_sistema_mrp_admin.ps1` como Administrador.
2. Rodar `portable/02_mapear_x_sistema_mrp_usuario.bat` como usuario normal.
3. Rodar `portable/03_validar_ambiente_sistema_mrp.ps1`.
4. Se o validador retornar `exit code 0`, fazer commit seletivo da v0.1.054.
