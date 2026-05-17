// =======================================================
// SPA LOADER - CARREGA PAGINAS E MODULOS INTERNOS
// =======================================================

import { logout } from "./auth.js";

const app = document.getElementById("app");
const menu = document.getElementById("mainMenu");
const menuToggle = document.getElementById("btnMenuMobile");

function closeMobileMenu() {
    if (!menu || !menuToggle) return;

    menu.classList.remove("is-open");
    document.body.classList.remove("menu-open");
    menuToggle.setAttribute("aria-expanded", "false");
}

if (menuToggle && menu) {
    menuToggle.addEventListener("click", () => {
        const isOpen = menu.classList.toggle("is-open");
        document.body.classList.toggle("menu-open", isOpen);
        menuToggle.setAttribute("aria-expanded", String(isOpen));
    });
}

// Botao de logout
document.getElementById("btnLogout").addEventListener("click", logout);

// Eventos do menu superior
document.querySelectorAll("nav.menu a").forEach(a => {
    a.addEventListener("click", e => {
        e.preventDefault();
        closeMobileMenu();
        loadModule(a.dataset.module);
    });
});

// Carrega modulos HTML + JS
async function loadModule(moduleName) {
    try {
        const html = await (await fetch(`pages/${moduleName}.html`)).text();
        app.innerHTML = html;

        try {
            const jsModule = await import(`./pages/${moduleName}.js`);
            if (jsModule.init) jsModule.init();
        } catch (err) {
            console.log("JS opcional nao encontrado:", moduleName);
        }

    } catch (e) {
        app.innerHTML = "<p>Erro ao carregar o modulo.</p>";
    }
}

// Modulo inicial
loadModule("dashboard");
