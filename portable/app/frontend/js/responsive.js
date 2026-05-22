// =======================================================
// COMPORTAMENTO RESPONSIVO - MRP_LOCAL
// v0.1.014
// =======================================================

const menu = document.getElementById("mainMenu");
const toggle = document.getElementById("btnResponsiveMenu");

function setMenuState(isOpen) {
    if (!menu || !toggle) return;

    menu.classList.toggle("is-open", isOpen);
    document.body.classList.toggle("menu-open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
}

if (menu && toggle) {
    toggle.addEventListener("click", () => {
        setMenuState(!menu.classList.contains("is-open"));
    });

    menu.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", () => setMenuState(false));
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) {
            setMenuState(false);
        }
    });
}
