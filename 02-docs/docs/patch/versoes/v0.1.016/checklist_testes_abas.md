# v0.1.016 - Checklist de testes por abas

## Ambiente de teste oficial

- Comando:
  `py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"`
- URLs:
  - `http://100.108.26.10:8000/login.html`
  - `http://100.108.26.10:8000/index.html`

## Criterios por aba

- [ ] Abre a tela da aba
- [ ] Nao gera erro JS no console
- [ ] Nao gera overflow lateral em mobile
- [ ] Funciona em desktop
- [ ] Funciona em 390px
- [ ] Funciona em 430px
- [ ] Menu navega corretamente
- [ ] Botoes principais aparecem corretamente

## Abas principais

### Dashboard
- [ ] Checklist completo executado

### Produtos
- [ ] Checklist completo executado
- [x] Correcao de overflow mobile aplicada nesta versao (pendente validacao visual final em dispositivo)

### Processos
- [ ] Checklist completo executado

### Estoque
- [ ] Checklist completo executado

### Ordens de Producao
- [ ] Checklist completo executado
- [x] Rotulo visual no menu atualizado de "Ordens" para "Ordens de Producao"
