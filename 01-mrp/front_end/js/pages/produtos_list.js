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
        const arp = p.arp || "";
        const ataNumeroRaw = p.ata_numero || p.ata || "";
        const ataNumero = `${arp} ${ataNumeroRaw}`.trim();
        const itemAta = `${p.item_ata ?? ""}`;
        const empresa = p.empresa || "";

        tr.innerHTML = `
            <td class="col-id">${id}</td>
            <td class="col-preview">
                <img class="produto-preview" src="${preview}" alt="Preview demo" width="56" height="32" loading="lazy" onerror="this.onerror=null;this.src='${PLACEHOLDER}';">
            </td>
            <td class="col-ata-numero">${ataNumero}</td>
            <td class="col-item-ata">${itemAta}</td>
            <td class="col-produto">${nome}</td>
            <td class="col-empresa">${empresa}</td>
            <td class="col-acao"><button class="btn-row-action" type="button" onclick="alert('Futuro: editar')">Editar</button></td>
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
