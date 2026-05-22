import { localGET } from "../api.js";

const SEED_PATH = "data/produtos_seed.json";
const PRODUTOS_API_URL = "http://localhost:8876/api/produtos";
const PLACEHOLDER = "img/ui/placeholders/produto_placeholder.svg";

const produtosState = {
    produtos: [],
    filtros: {
        pesquisa: "",
        ata: "",
        empresa: "",
        categoria: ""
    },
    sourceInfo: ""
};

const bomState = {
    produtoSelecionado: null
};

let tbodyDelegationHandler = null;
let lightboxCloseBtnHandler = null;
let lightboxOverlayHandler = null;
let lightboxKeydownHandler = null;
let voltarBomHandler = null;
let navResetHandlerBound = false;

export async function init() {
    const addBtn = document.getElementById("btnAddProd");
    if (addBtn) {
        addBtn.addEventListener("click", () => {
            alert("Cadastro manual fora do escopo desta etapa.");
        });
    }

    produtosState.produtos = await loadProdutosSeed();
    initFiltros();
    bindNavResetHook();
    initProdutosInteractions();
    popularFiltros(produtosState.produtos);
    resetUiStateAfterBom();
    renderProdutos();
    bindProdutosEvents();
    bindImageZoom();
}

function renderProdutos() {
    renderProdutosFiltrados();
}

function bindProdutosEvents() {
    initProdutosInteractions();
}

function bindImageZoom() {
    initProdutosInteractions();
}

function bindNavResetHook() {
    if (navResetHandlerBound) return;
    navResetHandlerBound = true;
    document.addEventListener("mrp:before-module-change", resetUiStateAfterBom);
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

function buildOrigemAtaLabel(produto) {
    const origem = produto.ata_origem || produto.origem_ata || produto.cliente || produto.orgao || "";
    const arp = String(produto.arp || "").trim();
    const ataNumero = String(produto.ata_numero || "").trim();
    const ataLabel = arp.includes(ataNumero) || !ataNumero ? arp : `${arp} ${ataNumero}`.trim();
    if (!origem) return ataLabel;
    return normalizeSearchText(origem) === normalizeSearchText(ataLabel)
        ? ataLabel
        : `${ataLabel} (${origem})`;
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
        const ataLabel = buildOrigemAtaLabel(produto);
        if (ataLabel && !atasMap.has(ataKey)) atasMap.set(ataKey, ataLabel);

        if (produto.empresa) empresasSet.add(produto.empresa);
        if (produto.categoria) categoriasSet.add(produto.categoria);
    });

    if (selectAta) {
        setSelectOptions(selectAta, [{ value: "", label: "Todas as ATAs/Origens" }].concat(
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

function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
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
            produto.ata_origem,
            produto.origem_ata,
            produto.cliente,
            produto.orgao,
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

    const source = produtosState.sourceInfo ? ` | ${produtosState.sourceInfo}` : "";

    if (exibidos === 0) {
        contador.textContent = `0 produtos encontrados${source}`;
        return;
    }

    contador.textContent = `Exibindo ${exibidos} de ${total} produtos${source}`;
}

function renderTabela(produtos) {
    const tbody = document.querySelector("#tblProdutos tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    if (!produtos.length) {
        const tr = document.createElement("tr");
        tr.className = "produtos-empty-row";
        tr.innerHTML = `<td colspan="6" class="produtos-empty-msg">Nenhum produto encontrado com os filtros atuais.</td>`;
        tbody.appendChild(tr);
        return;
    }

    produtos.forEach((p, index) => {
        const tr = document.createElement("tr");
        const nome = p.nome_oficial || p.nome || "";
        const id = p.id ?? index + 1;
        const preview = p?.imagem?.preview || PLACEHOLDER;
        const arp = String(p.arp || "").trim();
        const ataNumeroRaw = String(p.ata_numero || p.ata || "").trim();
        const ataNumero = arp.includes(ataNumeroRaw) || !ataNumeroRaw
            ? arp
            : `${arp} ${ataNumeroRaw}`.trim();
        const empresa = p.empresa || "";

        const safeId = escapeHtml(id);
        const safePreview = escapeHtml(preview);
        const safePlaceholder = escapeHtml(PLACEHOLDER);
        const safeAtaNumero = escapeHtml(ataNumero);
        const safeNome = escapeHtml(nome);
        const safeEmpresa = escapeHtml(empresa);

        tr.innerHTML = `
            <td class="col-id" data-label="ID">${safeId}</td>
            <td class="col-preview" data-label="PREVIEW">
                <img class="produto-preview js-produto-preview" data-action="zoom-image" src="${safePreview}" alt="Preview demo" width="56" height="32" loading="lazy" onerror="this.onerror=null;this.src='${safePlaceholder}';">
            </td>
            <td class="col-ata-numero" data-label="ATA + Nº">${safeAtaNumero}</td>
            <td class="col-produto" data-label="PRODUTO">${safeNome}</td>
            <td class="col-empresa" data-label="EMPRESA">${safeEmpresa}</td>
            <td class="col-acao" data-label="AÇÃO"><button class="btn-row-action js-btn-bom" data-action="open-bom" type="button" data-produto-id="${safeId}">BOM</button></td>
        `;
        tbody.appendChild(tr);
    });
}

function initProdutosInteractions() {
    const tbody = document.querySelector("#tblProdutos tbody");
    const lightbox = document.getElementById("produtoLightbox");
    const lightboxImg = document.getElementById("produtoLightboxImg");
    const closeBtn = document.getElementById("produtoLightboxClose");
    const voltarBtn = document.getElementById("btnVoltarProdutos");
    if (!tbody || !voltarBtn || !lightbox || !lightboxImg || !closeBtn) return;

    if (tbodyDelegationHandler) {
        tbody.removeEventListener("click", tbodyDelegationHandler);
    }
    tbodyDelegationHandler = (event) => {
        const target = event.target;
        if (!(target instanceof HTMLElement)) return;

        const btn = target.closest("[data-action='open-bom']");
        if (btn instanceof HTMLButtonElement) {
            const produtoId = Number(btn.dataset.produtoId || "");
            if (!Number.isFinite(produtoId)) return;
            const produto = produtosState.produtos.find((item) => Number(item.id) === produtoId);
            if (!produto) return;
            abrirBomProduto(produto);
            return;
        }

        const img = target.closest("[data-action='zoom-image']");
        if (img instanceof HTMLImageElement) {
            const src = img.dataset.image || img.currentSrc || img.src || PLACEHOLDER;
            if (!src) {
                console.warn("Zoom ignorado: imagem ausente.");
                return;
            }
            openLightbox(src, img.alt || "Preview ampliado do produto");
        }
    };
    tbody.addEventListener("click", tbodyDelegationHandler);

    if (voltarBomHandler) {
        voltarBtn.removeEventListener("click", voltarBomHandler);
    }
    voltarBomHandler = () => returnToProdutos();
    voltarBtn.addEventListener("click", voltarBomHandler);

    if (lightboxCloseBtnHandler) {
        closeBtn.removeEventListener("click", lightboxCloseBtnHandler);
    }
    lightboxCloseBtnHandler = () => closeLightbox();
    closeBtn.addEventListener("click", lightboxCloseBtnHandler);

    if (lightboxOverlayHandler) {
        lightbox.removeEventListener("click", lightboxOverlayHandler);
    }
    lightboxOverlayHandler = (event) => {
        if (event.target === lightbox) closeLightbox();
    };
    lightbox.addEventListener("click", lightboxOverlayHandler);

    if (lightboxKeydownHandler) {
        document.removeEventListener("keydown", lightboxKeydownHandler);
    }
    lightboxKeydownHandler = (event) => {
        if (event.key === "Escape") closeLightbox();
    };
    document.addEventListener("keydown", lightboxKeydownHandler);
}

function abrirBomProduto(produto) {
    bomState.produtoSelecionado = produto;

    const lista = document.getElementById("produtosListaSection");
    const bom = document.getElementById("produtoBomSection");
    const titulo = document.getElementById("bomProdutoTitulo");
    if (!lista || !bom || !titulo) return;

    const ataNumero = String(produto.ata_numero || produto.ata || "").trim();
    const produtoNome = String(produto.nome_oficial || produto.nome || "").trim();
    const empresa = String(produto.empresa || "").trim();
    const id = String(produto.id || "").trim();

    titulo.textContent = `Produto selecionado: ID ${id} | ATA + Nº ${ataNumero} | PRODUTO ${produtoNome} | EMPRESA ${empresa}`;

    const bomData = buildBomMock(produto);
    renderBomTabela("tblBomTubos", bomData.tubos, "tamanho");
    renderBomTabela("tblBomChapas", bomData.chapas, "tamanho");
    renderBomTabela("tblBomInsumos", bomData.insumos, "unidade");

    lista.classList.add("hidden");
    bom.classList.remove("hidden");
}

function returnToProdutos() {
    const lista = document.getElementById("produtosListaSection");
    const bom = document.getElementById("produtoBomSection");
    if (!lista || !bom) return;

    closeLightbox();
    bom.classList.add("hidden");
    lista.classList.remove("hidden");
    bomState.produtoSelecionado = null;
}

function resetUiStateAfterBom() {
    closeLightbox();
    returnToProdutos();
    const lightbox = document.getElementById("produtoLightbox");
    if (lightbox) {
        lightbox.classList.remove("active", "is-open", "open");
        lightbox.classList.add("hidden");
        lightbox.style.pointerEvents = "none";
    }
    document.body.style.overflow = "";
    document.body.style.pointerEvents = "";
}

function renderBomTabela(tableId, rows, medidaKey) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    if (!tbody) return;

    tbody.innerHTML = "";
    rows.forEach((row) => {
        const tr = document.createElement("tr");
        const medida = medidaKey === "unidade" ? row.unidade : row.tamanho;
        tr.innerHTML = `
            <td>${escapeHtml(row.cod)}</td>
            <td>${escapeHtml(row.material)}</td>
            <td>${escapeHtml(row.dim_1)}</td>
            <td>${escapeHtml(row.dim_2)}</td>
            <td>${escapeHtml(row.espessura)}</td>
            <td>${escapeHtml(row.revestimento)}</td>
            <td>${escapeHtml(medida)}</td>
            <td>${escapeHtml(row.quantidade)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function buildBomMock(produto) {
    const baseCod = String(produto.id || "0");

    return {
        tubos: [
            {
                cod: `TB-${baseCod}-01`,
                material: "ACO CARBONO",
                dim_1: "2\"",
                dim_2: "1.5\"",
                espessura: "2.65MM",
                revestimento: "GALVANIZADO",
                tamanho: "6M",
                quantidade: "08"
            },
            {
                cod: `TB-${baseCod}-02`,
                material: "ACO INOX",
                dim_1: "1\"",
                dim_2: "0.75\"",
                espessura: "1.50MM",
                revestimento: "POLIDO",
                tamanho: "3M",
                quantidade: "12"
            }
        ],
        chapas: [
            {
                cod: `CH-${baseCod}-01`,
                material: "CHAPA ACO",
                dim_1: "2000MM",
                dim_2: "1000MM",
                espessura: "3.00MM",
                revestimento: "PINTURA EPOXI",
                tamanho: "2M2",
                quantidade: "04"
            },
            {
                cod: `CH-${baseCod}-02`,
                material: "CHAPA PERFURADA",
                dim_1: "1200MM",
                dim_2: "800MM",
                espessura: "2.00MM",
                revestimento: "GALVANIZADO",
                tamanho: "0.96M2",
                quantidade: "06"
            }
        ],
        insumos: [
            {
                cod: `IN-${baseCod}-01`,
                material: "PARAFUSO SEXTAVADO",
                dim_1: "M10",
                dim_2: "50MM",
                espessura: "-",
                revestimento: "ZINCADO",
                unidade: "UN",
                quantidade: "64"
            },
            {
                cod: `IN-${baseCod}-02`,
                material: "TINTA EPOXI",
                dim_1: "BALDE",
                dim_2: "18L",
                espessura: "-",
                revestimento: "NA",
                unidade: "KG",
                quantidade: "18"
            }
        ]
    };
}

function openLightbox(src, alt) {
    const lightbox = document.getElementById("produtoLightbox");
    const lightboxImg = document.getElementById("produtoLightboxImg");
    if (!lightbox || !lightboxImg) return;
    lightboxImg.src = src || PLACEHOLDER;
    lightboxImg.alt = alt;
    lightbox.style.pointerEvents = "auto";
    lightbox.classList.remove("hidden");
    lightbox.setAttribute("aria-hidden", "false");
}

function closeLightbox() {
    const lightbox = document.getElementById("produtoLightbox");
    const lightboxImg = document.getElementById("produtoLightboxImg");
    if (!lightbox || !lightboxImg) return;
    lightbox.classList.remove("active", "is-open", "open");
    lightbox.classList.add("hidden");
    lightbox.setAttribute("aria-hidden", "true");
    lightbox.style.pointerEvents = "none";
    lightboxImg.src = "";
    document.body.style.overflow = "";
    document.body.style.pointerEvents = "";
}

async function loadProdutosSeed() {
    let apiError = "";
    try {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), 6000);
        const response = await fetch(PRODUTOS_API_URL, { cache: "no-store", signal: ctrl.signal });
        clearTimeout(timer);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (data && data.ok === true && Array.isArray(data.items)) {
            produtosState.sourceInfo = "Fonte: API backend";
            return data.items;
        }
        throw new Error("Payload invalido da API");
    } catch (err) {
        apiError = `API indisponivel (${err?.message || "falha"}).`;
    }

    try {
        const response = await fetch(SEED_PATH, { cache: "no-store" });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (Array.isArray(data) && data.length) {
            produtosState.sourceInfo = `${apiError} Fallback: seed local`;
            return data;
        }
    } catch (seedErr) {
        apiError = `${apiError} Seed indisponivel (${seedErr?.message || "falha"}).`;
    }

    produtosState.sourceInfo = `${apiError} Fallback: mock local`;
    return localGET("produtos");
}
