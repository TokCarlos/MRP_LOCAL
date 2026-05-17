import { localGET } from "../api.js";

const SEED_PATH = "data/produtos_seed.json";
const PLACEHOLDER = "assets/produtos/_placeholder.svg";

export async function init() {
    const addBtn = document.getElementById("btnAddProd");
    if (addBtn) {
        addBtn.addEventListener("click", () => {
            alert("Cadastro manual fora do escopo desta etapa.");
        });
    }

    await loadProdutos();
}

async function loadProdutos() {
    const tbody = document.querySelector("#tblProdutos tbody");
    if (!tbody) return;

    const data = await loadProdutosSeed();
    tbody.innerHTML = "";

    data.forEach((p, index) => {
        const tr = document.createElement("tr");
        const nome = p.nome_oficial || p.nome || "";
        const id = p.id ?? index + 1;
        const preview = p?.imagem?.preview || PLACEHOLDER;

        tr.innerHTML = `
            <td>
                <img src="${preview}" alt="Preview demo" width="56" height="32" loading="lazy" onerror="this.onerror=null;this.src='${PLACEHOLDER}';">
            </td>
            <td>${id}</td>
            <td>${nome}</td>
            <td><button class="btn-row-action" type="button" onclick="alert('Futuro: editar')">Editar</button></td>
        `;
        tbody.appendChild(tr);
    });
}

async function loadProdutosSeed() {
    try {
        const response = await fetch(SEED_PATH, { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (Array.isArray(data) && data.length) return data;
    } catch {
        // fallback local temporario
    }

    return localGET("produtos");
}
