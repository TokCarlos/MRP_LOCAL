# PENDENCIAS_MODELO - v0.1.045

Modelo de classificacao para instalador/preparador futuro.

## CRITICO

- Sem isso o sistema nao funciona.
- Bloqueia execucao/conclusao.

Exemplos:
- config invalida;
- frontend ausente;
- porta principal ocupada sem alternativa;
- pasta de dados/logs sem permissao de escrita;
- Python portable ausente quando backend depender dele;
- PostgreSQL inacessivel quando banco for obrigatorio;
- migracao obrigatoria pendente.

## OPCIONAL

- Nao impede operacao basica.
- Registra pendencia, alerta e permite continuar.

Exemplos:
- atalho ausente;
- firewall LAN nao liberado quando uso for somente local;
- backup automatico ainda nao configurado;
- tarefa Windows ainda nao instalada quando execucao manual for aceita temporariamente.

## RECOMENDADO

- Melhora estabilidade, seguranca ou manutencao.
- Registra e alerta.

Exemplos:
- Tailscale nao validado;
- log rotation nao configurado;
- watchdog ainda nao validado por tempo prolongado;
- reboot/queda de energia ainda nao validado.
