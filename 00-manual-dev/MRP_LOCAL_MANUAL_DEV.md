# LEGADO/HISTORICO - MRP_LOCAL_MANUAL_DEV.md

Este arquivo e legado/historico e nao e o manual operacional principal atual.
Manuais principais atuais:
- 00-manual-dev/MANUAL_DEV_COMPLETO.txt
- 00-manual-dev/RESUMO_OPERACIONAL_DO_SISTEMA.txt

# MRP_LOCAL - Manual do Dono/Dev

Este manual é o guia operacional do projeto MRP_LOCAL para o dono/dev do sistema.
Ele fica fora da aplicação principal e não faz parte do runtime de `01-mrp`.

## 1. Visão geral

O MRP_LOCAL é um sistema local-first em fase de teste, atualmente rodando o frontend como site estático no Windows.

Estado atual:

- Ambiente de teste: `X:\`
- Servidor atual: `HOME-MACHINE`
- Frontend atual: arquivos estáticos em `X:\01-mrp\front_end`
- Backend FastAPI: ainda não criado
- PostgreSQL: ainda não criado
- Autenticação real: ainda não criada
- Acesso remoto: Tailscale
- Sincronização por MEGA: descontinuada

O objetivo nesta fase é manter a carcaça visual e operacional estável antes de conectar backend, banco e autenticação real.

## 2. Estrutura de pastas

Estrutura oficial:

```text
X:\
├─ 01-mrp
│  ├─ front_end
│  └─ logs
├─ 02-docs
│  └─ docs
├─ 03-vs
│  ├─ scripts
│  ├─ patches
│  ├─ snapshots
│  └─ relatorios
└─ 00-manual-dev
```

Uso de cada pasta:

- `01-mrp`: sistema principal executável.
- `02-docs`: documentação, regras, decisões, histórico e auditoria.
- `03-vs`: versionamento, scripts, patches, staging, snapshots e releases.
- `00-manual-dev`: manual pessoal/operacional do dono/dev.

## 3. Ambiente atual

Ambiente de teste:

- Raiz do projeto: `X:\`
- Pasta de rede usada no teste: `\\HOME-MACHINE\system_jpl`
- Servidor de teste: `HOME-MACHINE`
- Porta oficial do frontend: `8765`
- Bind operacional: `0.0.0.0`
- Tarefa Windows: `MRP_LOCAL_FRONTEND`

URLs esperadas:

- Local no próprio servidor: `http://localhost:8765`
- Rede local: `http://IP_LOCAL_DO_SERVIDOR:8765`
- Tailscale: `http://IP_TAILSCALE_DO_SERVIDOR:8765`

## 4. Como copiar ou clonar para outra máquina

Opção com Git:

```powershell
git clone <URL_DO_REPOSITORIO> X:\
```

Opção por cópia manual:

1. Copiar `01-mrp`, `02-docs`, `03-vs`, `00-manual-dev`, `README.md`, `AGENTS.md`, `.gitignore` e arquivos de controle do projeto.
2. Não copiar logs reais, caches, runtime local, `.env`, bancos locais ou arquivos temporários.
3. Conferir se `X:\01-mrp\front_end\index.html` existe.
4. Rodar status e healthcheck depois da cópia.

Se `X:\` não existir na nova máquina, criar o mapeamento ou ajustar os scripts futuramente para o caminho local definitivo do servidor.

## 5. Pré-requisitos

Obrigatórios nesta fase:

- Windows
- PowerShell
- Python instalado com comando `py`
- Git, se for versionar ou atualizar pelo GitHub
- Navegador moderno
- Tailscale, se precisar de acesso remoto

Ainda não necessários:

- FastAPI
- PostgreSQL
- Node.js
- npm
- Docker

## 6. Verificar Python

```powershell
py --version
```

Teste rápido do módulo HTTP:

```powershell
py -m http.server --help
```

Se `py` não existir, instalar Python para Windows e marcar a opção de launcher/associação durante a instalação.

## 7. Iniciar frontend manualmente

Comando antigo, documentado apenas como histórico:

```powershell
py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"
```

Esse comando antigo fica descontinuado porque:

- usa porta `8000`;
- prende o bind ao IP Tailscale;
- não atende corretamente LAN + Tailscale;
- depende de terminal manual aberto.

Comando novo oficial:

```powershell
py -m http.server 8765 --bind 0.0.0.0 --directory "X:\01-mrp\front_end"
```

## 8. Scripts principais

Pasta:

```text
X:\03-vs\scripts\servicos
```

Scripts:

- `mrp_frontend_start.ps1`: inicia o frontend estático na porta `8765`.
- `mrp_frontend_stop.ps1`: para apenas o servidor estático do MRP_LOCAL.
- `mrp_frontend_status.ps1`: mostra porta, HTTP, pasta e URLs prováveis.
- `mrp_frontend_healthcheck.ps1`: valida se o serviço está saudável.
- `mrp_frontend_watchdog.ps1`: verifica saúde e tenta iniciar se necessário.
- `mrp_frontend_task_install.ps1`: instala a tarefa Windows.
- `mrp_frontend_task_uninstall.ps1`: remove a tarefa Windows.
- `mrp_firewall_8765.ps1`: libera entrada TCP `8765` no firewall.

## 9. Iniciar, parar e reiniciar

Iniciar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_start.ps1"
```

Parar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_stop.ps1"
```

Reiniciar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_stop.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_start.ps1"
```

## 10. Verificar status

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_status.ps1"
```

O status deve mostrar:

- porta `8765` ouvindo;
- HTTP respondendo;
- pasta `X:\01-mrp\front_end`;
- URLs prováveis local e Tailscale.

## 11. Executar healthcheck

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_healthcheck.ps1"
```

Resultado esperado:

```text
HEALTHCHECK=OK
```

Se falhar, verificar:

- se `X:\` está acessível;
- se `X:\01-mrp\front_end` existe;
- se `index.html` existe;
- se a porta `8765` está ocupada por outro processo;
- se firewall está bloqueando.

## 12. Instalar tarefa automática

Nome da tarefa:

```text
MRP_LOCAL_FRONTEND
```

Instalar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_task_install.ps1"
```

A tarefa executa o watchdog no logon do usuário atual:

```powershell
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "X:\03-vs\scripts\servicos\mrp_frontend_watchdog.ps1"
```

Observação: no ambiente atual, `X:\` pode depender do usuário logado. Em produção futura, o caminho deve ser local/servidor e não depender de mapeamento frágil.

## 13. Remover tarefa automática

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_task_uninstall.ps1"
```

Esse comando remove apenas a tarefa. Ele não apaga arquivos, logs ou documentação.

## 14. Firewall porta 8765

Liberar porta:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_firewall_8765.ps1"
```

Regra esperada:

- Nome: `MRP_LOCAL_FRONTEND_8765`
- Porta: TCP `8765`
- Direção: entrada
- Perfil: Private

Executar este comando como administrador se o Windows exigir permissão.

## 15. Acessos

No próprio servidor:

```text
http://localhost:8765
```

Na rede local:

```text
http://IP_LOCAL_DO_SERVIDOR:8765
```

Via Tailscale:

```text
http://IP_TAILSCALE_DO_SERVIDOR:8765
```

Regra operacional:

- Rede local é o acesso principal.
- Tailscale é acesso remoto.
- Não abrir porta pública no roteador nesta fase.

## 16. Portas oficiais

Atual:

- Frontend estático: `8765`

Descontinuada:

- Frontend antigo/manual: `8000`

Futuro:

- API FastAPI: ainda não definida
- PostgreSQL: porta padrão provável `5432`, ainda não ativada

## 17. Logs

Pasta:

```text
X:\01-mrp\logs\servicos
```

Arquivos esperados:

- `frontend.out.log`
- `frontend.err.log`
- `frontend.health.log`
- `frontend.watchdog.log`

Regras:

- logs reais não devem ser versionados;
- `.gitkeep` pode existir apenas para manter a pasta;
- logs grandes devem ser limpos ou arquivados fora do Git.

## 18. Commit manual

Verificar estado:

```powershell
git status
```

Adicionar alterações:

```powershell
git add .
```

Criar commit:

```powershell
git commit -m "v0.1.036 - documenta execucao automatica do frontend"
```

Criar tag, se aplicável:

```powershell
git tag v0.1.036
```

## 19. Push manual

Enviar branch:

```powershell
git push
```

Enviar tag:

```powershell
git push origin v0.1.036
```

Antes de push:

- validar que não há `.env`;
- validar que logs reais não foram adicionados;
- validar que não há banco local versionado;
- validar que o frontend funcional não foi alterado sem escopo.

## 20. Regras de segurança

Não versionar:

- `.env`
- `.venv`
- `node_modules`
- `__pycache__`
- `*.db`
- `*.sqlite`
- logs reais
- caches
- credenciais
- runtime local
- arquivos pessoais

Não fazer nesta fase:

- criar backend FastAPI;
- criar PostgreSQL;
- criar autenticação real;
- abrir porta pública no roteador;
- usar MEGA como arquitetura;
- usar `01-mrp` como laboratório sem escopo explícito.

## 21. O que não copiar como runtime

Ao migrar para outra máquina, não copiar como parte operacional:

- logs antigos;
- caches;
- bancos de teste;
- arquivos temporários;
- `.env`;
- credenciais pessoais;
- pacotes antigos sem necessidade;
- resíduos de build.

## 22. Decisões oficiais

- `MEGA` está descontinuado na arquitetura.
- `Tailscale` será usado para acesso remoto.
- O sistema é `local-first`.
- O frontend atual é estático até existir backend real.
- Backend FastAPI será criado em etapa futura.
- PostgreSQL será criado em etapa futura.
- Serviços futuros devem ser separados: frontend, API, banco e backup.

## 23. Futuro backend FastAPI

Ainda não criar.

Quando aprovado, o backend deverá:

- rodar como serviço próprio;
- expor API local;
- não depender do frontend estático;
- respeitar perfis de ambiente;
- centralizar regras em motores desacoplados;
- usar adaptadores para banco, arquivos e integrações.

## 24. Futuro PostgreSQL

Ainda não criar.

Quando aprovado, o banco deverá:

- rodar localmente ou em servidor interno;
- ter backup definido;
- ter credenciais fora do código;
- ter scripts de migração;
- não ser versionado no Git como arquivo de banco real.

## 25. Checklist de reinstalação em nova máquina

1. Instalar Git.
2. Instalar Python.
3. Instalar Tailscale, se precisar acesso remoto.
4. Copiar ou clonar o projeto.
5. Garantir acesso a `X:\`.
6. Confirmar `X:\01-mrp\front_end\index.html`.
7. Rodar `py --version`.
8. Rodar `mrp_frontend_status.ps1`.
9. Rodar `mrp_frontend_start.ps1`.
10. Abrir `http://localhost:8765`.
11. Liberar firewall na porta `8765`.
12. Testar acesso LAN.
13. Testar acesso Tailscale.
14. Instalar tarefa `MRP_LOCAL_FRONTEND`, se aprovado.
15. Reiniciar o Windows e confirmar que o sistema volta.

## 26. Checklist de diagnóstico quando não abrir

1. Conferir se `X:\` está montado.
2. Conferir se `X:\01-mrp\front_end\index.html` existe.
3. Rodar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_status.ps1"
```

4. Rodar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_healthcheck.ps1"
```

5. Verificar se a porta `8765` está ocupada:

```powershell
netstat -ano | findstr :8765
```

6. Conferir logs em:

```text
X:\01-mrp\logs\servicos
```

7. Confirmar firewall.
8. Confirmar IP local do servidor.
9. Confirmar Tailscale online, se for acesso remoto.
10. Reiniciar serviço com stop/start.

## 27. Histórico inicial de versões

- `v0.1.008`: promoção do frontend base para `01-mrp`.
- `v0.1.009`: base responsiva em teste.
- `v0.1.010`: acesso mobile via Tailscale validado.
- `v0.1.011`: ambientes `TESTE_HOME` e `PRODUCAO_TRABALHO` registrados.
- `v0.1.012`: regra configuração/motor/adaptador registrada.
- `v0.1.013`: auditoria excepcional do `01-mrp`.
- `v0.1.014`: protocolo de fechamento de tarefa.
- `v0.1.015`: correção mobile inicial.
- `v0.1.016`: overflow mobile em Produtos e testes por abas.
- `v0.1.017`: correção de overflow na tabela Produtos.
- `v0.1.018`: consolidação visual e dados mock.
- `v0.1.020` a `v0.1.030`: ajustes de Produtos, imagens reais e domínio empresa/ATA.
- `v0.1.031` a `v0.1.035`: limpeza, encoding e estabilização documental.
- `v0.1.036`: preparação da execução automática do frontend estático no Windows.

## 28. Resumo operacional mínimo

Para iniciar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_start.ps1"
```

Para verificar:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "X:\03-vs\scripts\servicos\mrp_frontend_status.ps1"
```

Para acessar:

```text
http://localhost:8765
```
