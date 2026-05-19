# db

Direcao preferencial futura: PostgreSQL para banco real do MRP_LOCAL.

Estado atual:
- nenhum banco real ativo nesta etapa;
- SQLite pode existir somente como apoio de prototipo local futuro, nao como banco industrial principal.

Regras:
- nao versionar banco real, dumps ou backups reais;
- banco real futuro exige backup, controle de acesso, migracao e separacao dev/teste/prod;
- esta etapa v0.1.045 cria apenas documentacao e estrutura preparatoria.
