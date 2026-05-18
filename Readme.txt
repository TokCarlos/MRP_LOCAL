py -m http.server 8000 --bind 100.108.26.10 --directory "X:\01-mrp\front_end"

http://100.108.26.10:8000/login.html

powershell -ExecutionPolicy Bypass -File "X:\03-vs\scripts\git_fechar_versao.ps1" -Versao "v0.1.014" -Mensagem "persistir protocolo de fechamento de tarefa"



net use X: "\\HOME-MACHINE\system_jpl" /persistent:yes
Set-Location X:\
git status
git diff --stat
git add .
git commit -m "v0.1.013 - auditar e alinhar 01-mrp com arquitetura atual"
git tag v0.1.013
git push
git push origin v0.1.013
git status
git tag

//Exception
git push origin v0.1.013




Use as referências públicas abaixo apenas como base conceitual de layout responsivo:

- https://preview.tabler.io/
- https://adminlte.io/
- https://getbootstrap.com/docs/5.0/examples/sidebars/
- https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/CSS_layout/Responsive_Design
- https://web.dev/learn/design

Objetivo:
Analisar padrões de dashboard responsivo e aplicar no nosso front-end existente em X:\01-mrp\front_end.

Regras:
1. Não baixar template completo.
2. Não instalar dependências.
3. Não substituir identidade visual.
4. Não trocar framework.
5. Não copiar código grande de terceiros.
6. Usar apenas como referência de comportamento:
   - sidebar responsiva
   - header responsivo
   - cards fluidos
   - tabelas com overflow-x
   - login mobile
   - breakpoints
   - viewport
   - body sem overflow lateral

Aplicar no projeto:
- criar/ajustar css/responsive.css
- criar/ajustar js/responsive.js se necessário
- garantir meta viewport em login.html e index.html
- preservar layout atual
- corrigir distorções em smartphone e zoom

Registrar em:
02-docs/docs/patch/versoes/v0.1.014/referencias_layout.md