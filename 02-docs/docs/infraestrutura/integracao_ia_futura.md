# Integracao IA futura no MRP_LOCAL - v0.1.050

## Visao futura

Integrar assistente IA ao MRP com controle operacional, permissao e auditoria.

## Arquitetura futura

Frontend MRP
-> Backend FastAPI
-> Modulo IA / Orquestrador
-> API de IA
-> Ferramentas internas controladas
-> Engine / Banco / Logs / Relatorios

## O que pode fazer (futuro)

1. Chat interno em modo leitura.
2. Assistente operacional com ferramentas controladas.
3. Acoes administrativas somente com permissao, confirmacao e log.

Ferramentas conceituais:

- `buscar_produtos`
- `consultar_ata`
- `consultar_estoque`
- `gerar_resumo`
- `gerar_relatorio`
- `validar_ordem`
- `consultar_status_sistema`
- `solicitar_healthcheck`

## O que nao pode fazer

- expor API key no frontend;
- executar PowerShell livre;
- acessar banco diretamente sem camada de controle;
- executar acao critica sem confirmacao;
- operar sem logs.

## Seguranca

- chaves/tokens fora do Git;
- backend com autenticacao/autorizacao;
- permissao por perfil para acao administrativa;
- logs obrigatorios para toda acao assistida por IA;
- trilha de auditoria para comandos e respostas operacionais.

## Dependencias para habilitacao futura

- backend minimo funcional;
- autenticacao de backend;
- modelo de permissao;
- contrato de API;
- modelo de dados minimo;
- politica de logs/auditoria.

## Fora de escopo agora

- integrar OpenAI/API externa;
- criar webhook;
- criar backend real;
- criar banco real;
- instalar dependencias.

## Relacao com FastAPI

FastAPI e camada preferencial para controlar:

- entrada de prompts;
- roteamento de ferramentas;
- validacoes de permissao;
- confirmacoes de acoes criticas;
- persistencia de logs.
