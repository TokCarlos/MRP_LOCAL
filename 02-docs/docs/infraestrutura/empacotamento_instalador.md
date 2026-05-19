
# Empacotamento e Instalador Futuro — MRP_LOCAL

## Regra de negócio registrada

O MRP_LOCAL deve evoluir para um programa instalável/empacotável.

A regra final esperada é: o ambiente DEV pode ter tudo configurado manualmente, mas uma máquina limpa deve receber um pacote de instalação capaz de preparar tudo que o sistema precisa para rodar.

## Analogia operacional

Como um jogo ou programa padrão:

1. O usuário executa um instalador.
2. O instalador verifica pré-requisitos.
3. Se faltar runtime/dependência, informa e instala ou orienta a instalação.
4. O instalador copia os arquivos do sistema.
5. O instalador cria configuração local.
6. O instalador libera firewall quando autorizado.
7. O instalador cria serviço/tarefa/watchdog.
8. O instalador executa healthcheck.
9. O sistema fica pronto para rodar.

## O que uma máquina limpa precisará

- Windows compatível.
- PowerShell funcional.
- Permissão para criar tarefa Windows.
- Permissão para liberar firewall, quando necessário.
- Runtime Python portable ou instalador automático de Python.
- Pasta de instalação definida.
- Configuração local gerada.
- Logs fora da área versionável.
- Healthcheck de confirmação.

## Estratégia preferencial

A estratégia preferencial é carregar runtime controlado junto do pacote, por exemplo:

`01-mrp/runtime/python/python.exe`

Se runtime portable não for usado, o instalador deve detectar ausência de Python e executar rotina autorizada de instalação/preparo.

## Separação obrigatória

O instalador não contém regra de negócio.

O instalador apenas prepara ambiente.

A regra de negócio deve ficar no motor/backend/engine e continuar independente de caminho físico, usuário Windows, drive mapeado ou máquina específica.

## Scripts iniciais criados

- `03-vs/scripts/instalador/mrp_precheck_instalacao.ps1`
- `03-vs/scripts/instalador/mrp_install_local.ps1`

Esses scripts são ganchos iniciais e ainda não substituem um instalador final assinado/empacotado.
