# Empacotamento e instalador futuro - v0.1.050

## Visao

O MRP_LOCAL deve evoluir para distribuicao por instalador unico, com comportamento de programa local-first instalavel.
Exemplo conceitual de artefato futuro: `MRP_LOCAL_Setup.exe`.

Nesta etapa, o conteudo e apenas estrategico/documental.
Nao ha implementacao de instalador real agora.

## ZIP de teste x instalador final

- ZIP de teste: pacote tecnico para DEV/diagnostico/manual.
- Instalador final: artefato unico de distribuicao para uso operacional comum.

O instalador final deve reduzir dependencia de passos manuais em maquina limpa.

## Instalador unico como artefato de distribuicao

O instalador futuro deve:

1. preparar estrutura e arquivos necessarios;
2. validar ambiente antes de concluir;
3. registrar log de instalacao/preparo;
4. criar base operacional local para start/status/healthcheck.

## Estrutura interna apos instalacao

Mesmo instalado por artefato unico, o sistema deve manter separacao interna:

- codigo
- frontend
- backend
- engine
- adapters
- runtime
- config
- data
- logs
- backups
- tmp

## Precheck obrigatorio no fluxo de instalacao

O instalador futuro deve executar precheck antes da conclusao:

- estrutura minima;
- permissao de escrita;
- disponibilidade de portas;
- validacao de configuracao;
- validacao de dependencias exigidas pela fase.

## Modelo de pendencias

Classificacao obrigatoria:

- `CRITICO`: bloqueia conclusao/execucao.
- `OPCIONAL`: alerta, registra e permite continuar quando nao bloquear operacao.
- `RECOMENDADO`: alerta, registra e permite continuar.

## Acoes que exigem aprovacao

Qualquer acao sensivel deve pedir aprovacao explicita:

- firewall;
- servico Windows;
- tarefa Windows;
- permissoes de pasta/sistema;
- download externo;
- instalacao externa;
- alteracoes de ambiente.

## Restricoes estruturais

O instalador futuro:

- nao pode depender de `X:\`;
- nao pode depender de `\\HOME-MACHINE`;
- nao pode depender de usuario Windows especifico;
- nao pode depender de letra de unidade mapeada.

## Fora de escopo agora

- criar instalador real;
- gerar `.exe`;
- empacotar release;
- instalar dependencias automaticamente;
- ativar watchdog/tarefa automatica;
- criar backend novo;
- criar banco novo.

## Decisao de ferramenta

A escolha de tecnologia (Inno Setup, NSIS, WiX, PyInstaller, cx_Freeze ou outra) fica para etapa futura, apos maturidade operacional.
