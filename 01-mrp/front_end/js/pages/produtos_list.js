import { localGET } from "../api.js";

const SEED_PATH = "data/produtos_seed.json";
const PLACEHOLDER = "assets/produtos/_placeholder.svg";

const produtosState = {
    produtos: [],
    filtros: {
        pesquisa: "",
        ata: "",
        empresa: "",
        categoria: ""
    }
};

export async function init() {
    const addBtn = document.getElementById("btnAddProd");
    if (addBtn) {
        addBtn.addEventListener("click", () => {
            alert("Cadastro manual fora do escopo desta etapa.");
        });
    }

    produtosState.produtos = await loadProdutosSeed();
    initFiltros();
    popularFiltros(produtosState.produtos);
    renderProdutosFiltrados();
}

function normalizeSearchText(value) {
    return String(value || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

function buildAtaFiltroKey(produto) {
    const arpKey = produto.arp_key || normalizeSearchText(produto.arp || "").replace(/\s+/g, "_");
    const ataKey = produto.ata_key || normalizeSearchText(produto.ata_numero || "").replace(/\s+/g, "_").replace(/\//g, "_");
    return `${arpKey}__${ataKey}`;
}

function initFiltros() {
    const inputPesquisa = document.getElementById("filtroPesquisa");
    const selectAta = document.getElementById("filtroAta");
    const selectEmpresa = document.getElementById("filtroEmpresa");
    const selectCategoria = document.getElementById("filtroCategoria");
    const btnLimpar = document.getElementById("btnLimparFiltros");

    if (inputPesquisa) {
        inputPesquisa.addEventListener("input", (e) => {
            produtosState.filtros.pesquisa = e.target.value || "";
            renderProdutosFiltrados();
        });
    }

    if (selectAta) {
        selectAta.addEventListener("change", (e) => {
            produtosState.filtros.ata = e.target.value || "";
            renderProdutosFiltrados();
        });
    }

    if (selectEmpresa) {
        selectEmpresa.addEventListener("change", (e) => {
            produtosState.filtros.empresa = e.target.value || "";
            renderProdutosFiltrados();
        });
    }

    if (selectCategoria) {
        selectCategoria.addEventListener("change", (e) => {
            produtosState.filtros.categoria = e.target.value || "";
            renderProdutosFiltrados();
        });
    }

    if (btnLimpar) {
        btnLimpar.addEventListener("click", () => {
            produtosState.filtros = { pesquisa: "", ata: "", empresa: "", categoria: "" };

            if (inputPesquisa) inputPesquisa.value = "";
            if (selectAta) selectAta.value = "";
            if (selectEmpresa) selectEmpresa.value = "";
            if (selectCategoria) selectCategoria.value = "";

            renderProdutosFiltrados();
        });
    }
}

function popularFiltros(produtos) {
    const selectAta = document.getElementById("filtroAta");
    const selectEmpresa = document.getElementById("filtroEmpresa");
    const selectCategoria = document.getElementById("filtroCategoria");

    const atasMap = new Map();
    const empresasSet = new Set();
    const categoriasSet = new Set();

    produtos.forEach((produto) => {
        const ataKey = buildAtaFiltroKey(produto);
        const ataLabel = `${produto.arp || ""} ${produto.ata_numero || ""}`.trim();
        if (ataLabel && !atasMap.has(ataKey)) atasMap.set(ataKey, ataLabel);

        if (produto.empresa) empresasSet.add(produto.empresa);
        if (produto.categoria) categoriasSet.add(produto.categoria);
    });

    if (selectAta) {
        setSelectOptions(selectAta, [{ value: "", label: "Todas as ATAs" }].concat(
            [...atasMap.entries()].map(([value, label]) => ({ value, label }))
        ));
    }

    if (selectEmpresa) {
        setSelectOptions(selectEmpresa, [{ value: "", label: "Todas as Empresas" }].concat(
            [...empresasSet].sort().map((value) => ({ value, label: value }))
        ));
    }

    if (selectCategoria) {
        setSelectOptions(selectCategoria, [{ value: "", label: "Todas as Categorias" }].concat(
            [...categoriasSet].sort().map((value) => ({ value, label: value }))
        ));
    }
}

function setSelectOptions(select, options) {
    select.innerHTML = "";
    options.forEach((opt) => {
        const option = document.createElement("option");
        option.value = opt.value;
        option.textContent = opt.label;
        select.appendChild(option);
    });
}

function aplicarFiltros(produtos) {
    const pesquisa = normalizeSearchText(produtosState.filtros.pesquisa);
    const ata = produtosState.filtros.ata;
    const empresa = produtosState.filtros.empresa;
    const categoria = produtosState.filtros.categoria;

    return produtos.filter((produto) => {
        const ataKey = buildAtaFiltroKey(produto);
        const textoBusca = normalizeSearchText([
            produto.nome_oficial,
            produto.arp,
            produto.ata_numero,
            produto.empresa,
            produto.item_ata,
            produto.produto_key
        ].join(" "));

        const matchPesquisa = !pesquisa || textoBusca.includes(pesquisa);
        const matchAta = !ata || ataKey === ata;
        const matchEmpresa = !empresa || produto.empresa === empresa;
        const matchCategoria = !categoria || produto.categoria === categoria;

        return matchPesquisa && matchAta && matchEmpresa && matchCategoria;
    });
}

function renderProdutosFiltrados() {
    const total = produtosState.produtos.length;
    const filtrados = aplicarFiltros(produtosState.produtos);
    renderTabela(filtrados);
    updateContador(filtrados.length, total);
}

function updateContador(exibidos, total) {
    const contador = document.getElementById("produtosContador");
    if (!contador) return;

    if (exibidos === 0) {
        contador.textContent = "0 produtos encontrados";
        return;
    }

    contador.textContent = `Exibindo ${exibidos} de ${total} produtos`;
}

function renderTabela(produtos) {
    const tbody = document.querySelector("#tblProdutos tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    if (!produtos.length) {
        const tr = document.createElement("tr");
        tr.className = "produtos-empty-row";
        tr.innerHTML = `<td colspan="7" class="produtos-empty-msg">Nenhum produto encontrado com os filtros atuais.</td>`;
        tbody.appendChild(tr);
        return;
    }

    produtos.forEach((p, index) => {
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
            <td class="col-id" data-label="ID">${id}</td>
            <td class="col-preview" data-label="PREVIEW">
                <img class="produto-preview" src="${preview}" alt="Preview demo" width="56" height="32" loading="lazy" onerror="this.onerror=null;this.src='${PLACEHOLDER}';">
            </td>
            <td class="col-ata-numero" data-label="ATA+Nº">${ataNumero}</td>
            <td class="col-item" data-label="Nº ITEM">${itemAta}</td>
            <td class="col-produto" data-label="PRODUTO">${nome}</td>
            <td class="col-empresa" data-label="EMPRESA">${empresa}</td>
            <td class="col-acao" data-label="AÇÃO"><button class="btn-row-action" type="button" onclick="alert('Futuro: editar')">Editar</button></td>
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
