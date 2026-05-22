import { localGET } from "../api.js";

const SEED_PATH = "data/produtos_seed.json";
const API_HOST = window.location.hostname || "127.0.0.1";
const API_PROTOCOL = window.location.protocol === "http:" || window.location.protocol === "https:" ? window.location.protocol : "http:";
const BASE_API = `${API_PROTOCOL}//${API_HOST}:8876/api/produtos`;
const PLACEHOLDER = "img/ui/placeholders/produto_placeholder.svg";
const EMPRESAS = [
    { key: "jpl", nome: "JPL" },
    { key: "aco", nome: "AÇO" },
    { key: "tcr", nome: "TCR" }
];
const BOM_GRUPOS = ["tubos", "chapas", "insumos"];

function toBoolean(value) {
    if (value === true || value === 1) return true;
    if (value === false || value === 0 || value === null || value === undefined) return false;
    const normalized = String(value).trim().toLowerCase();
    return normalized === "1" || normalized === "true" || normalized === "sim" || normalized === "ativo";
}

function normalizeProdutoRecord(produto) {
    if (!produto || typeof produto !== "object") return produto;
    return {
        ...produto,
        empresa: produto.empresa || produto.empresa_nome || produto.empresa_key || "",
        arp: produto.arp || produto.ata_nome || "",
        ata_numero: produto.ata_numero || produto.numero_ata || "",
        ativo: toBoolean(produto.ativo ?? true)
    };
}

function normalizeProdutoList(produtos) {
    return Array.isArray(produtos) ? produtos.map(normalizeProdutoRecord) : [];
}

const produtosState = {
    produtos: [],
    bases: [],
    filtros: { pesquisa: "", ata: "", empresa: "", categoria: "" },
    selectedBaseId: null,
    sourceInfo: ""
};

const bomState = { produtoSelecionado: null, itens: [] };
const uiState = { modalOpen: null, modalProdutoId: null };
const listenerState = { navBound: false, keyBound: false };

export async function init() {
    bindNavResetHook();
    bindTopButtons();
    initFiltros();
    await reloadData();
    resetUiStateAfterBom();
    renderProdutosFiltrados();
    initProdutosInteractions();
}

function bindTopButtons() {
    const btnBase = document.getElementById("btnNovaBaseAta");
    const btnProduto = document.getElementById("btnNovoProduto");
    if (btnBase) btnBase.onclick = () => openBaseModal();
    if (btnProduto) btnProduto.onclick = () => openProdutoModal(null);
}

function bindNavResetHook() {
    if (listenerState.navBound) return;
    listenerState.navBound = true;
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
        inputPesquisa.oninput = (e) => {
            produtosState.filtros.pesquisa = e.target.value || "";
            renderProdutosFiltrados();
        };
    }

    if (selectAta) {
        selectAta.onchange = (e) => {
            produtosState.filtros.ata = e.target.value || "";
            renderProdutosFiltrados();
        };
    }

    if (selectEmpresa) {
        selectEmpresa.onchange = (e) => {
            produtosState.filtros.empresa = e.target.value || "";
            renderProdutosFiltrados();
        };
    }

    if (selectCategoria) {
        selectCategoria.onchange = (e) => {
            produtosState.filtros.categoria = e.target.value || "";
            renderProdutosFiltrados();
        };
    }

    if (btnLimpar) {
        btnLimpar.onclick = () => {
            produtosState.filtros = { pesquisa: "", ata: "", empresa: "", categoria: "" };

            if (inputPesquisa) inputPesquisa.value = "";
            if (selectAta) selectAta.value = "";
            if (selectEmpresa) selectEmpresa.value = "";
            if (selectCategoria) selectCategoria.value = "";

            renderProdutosFiltrados();
        };
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

function reportUiError(context, err) {
    const message = err?.message || String(err || "falha desconhecida");
    console.error(`${context}:`, err);
    alert(`${context}: ${message}`);
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
        const preview = p?.imagem?.preview || p.imagem_path || PLACEHOLDER;
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
            <td class="col-acao" data-label="AÇÃO">
                <div class="prod-actions">
                    <button class="btn-row-action js-btn-bom" data-action="open-bom" type="button" data-produto-id="${safeId}">BOM</button>
                    <button class="btn-row-action" data-action="edit-produto" type="button" data-produto-id="${safeId}">Editar</button>
                    <button class="btn-row-action" data-action="toggle-produto" type="button" data-produto-id="${safeId}">${toBoolean(p.ativo) ? "Inativar" : "Ativar"}</button>
                </div>
            </td>
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

    tbody.onclick = async (event) => {
        const target = event.target;
        if (!(target instanceof HTMLElement)) return;

        const btn = target.closest("[data-action='open-bom']");
        if (btn instanceof HTMLButtonElement) {
            const produtoId = Number(btn.dataset.produtoId || "");
            if (!Number.isFinite(produtoId)) return;
            const produto = produtosState.produtos.find((item) => Number(item.id) === produtoId);
            if (!produto) return;
            try {
                await abrirBomProduto(produto);
            } catch (err) {
                reportUiError("Erro ao abrir BOM", err);
            }
            return;
        }
        const editBtn = target.closest("[data-action='edit-produto']");
        if (editBtn instanceof HTMLButtonElement) {
            const produtoId = Number(editBtn.dataset.produtoId || "");
            if (Number.isFinite(produtoId)) openProdutoModal(produtoId);
            return;
        }
        const toggleBtn = target.closest("[data-action='toggle-produto']");
        if (toggleBtn instanceof HTMLButtonElement) {
            const produtoId = Number(toggleBtn.dataset.produtoId || "");
            if (Number.isFinite(produtoId)) {
                try {
                    await toggleProdutoAtivo(produtoId);
                } catch (err) {
                    reportUiError("Erro ao alterar status do produto", err);
                }
            }
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

    voltarBtn.onclick = () => returnToProdutos();
    closeBtn.onclick = () => closeLightbox();
    lightbox.onclick = (event) => {
        if (event.target === lightbox) closeLightbox();
    };

    if (!listenerState.keyBound) {
        listenerState.keyBound = true;
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeLightbox();
                closeCurrentModal();
            }
        });
    }

    bindModalEvents();
}

async function abrirBomProduto(produto) {
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

    bomState.itens = await fetchBom(produto.id);
    renderBomTabela("tblBomTubos", bomState.itens.filter((x) => x.grupo === "tubos"));
    renderBomTabela("tblBomChapas", bomState.itens.filter((x) => x.grupo === "chapas"));
    renderBomTabela("tblBomInsumos", bomState.itens.filter((x) => x.grupo === "insumos"));

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
    closeCurrentModal();
    const lightbox = document.getElementById("produtoLightbox");
    if (lightbox) {
        lightbox.classList.remove("active", "is-open", "open");
        lightbox.classList.add("hidden");
        lightbox.style.pointerEvents = "none";
    }
    document.body.style.overflow = "";
    document.body.style.pointerEvents = "";
}

function renderBomTabela(tableId, rows) {
    const tbody = document.querySelector(`#${tableId} tbody`);
    if (!tbody) return;

    tbody.innerHTML = "";
    if (!rows.length) {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td colspan="8">Sem itens</td>`;
        tbody.appendChild(tr);
        return;
    }
    rows.forEach((row) => {
        const tr = document.createElement("tr");
        const medida = row.unidade || "-";
        tr.innerHTML = `
            <td>${escapeHtml(row.id)}</td>
            <td>${escapeHtml(row.item_nome)}</td>
            <td>${escapeHtml(row.observacao || "-")}</td>
            <td>-</td>
            <td>-</td>
            <td>${escapeHtml(row.grupo)}</td>
            <td>${escapeHtml(medida)}</td>
            <td>${escapeHtml(row.quantidade ?? "-")}</td>
        `;
        tbody.appendChild(tr);
    });
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

function extractProdutosPayload(data) {
    if (!data || data.ok !== true) return null;
    if (Array.isArray(data.data)) return data.data;
    if (Array.isArray(data.data?.items)) return data.data.items;
    if (Array.isArray(data.items)) return data.items;
    return null;
}

async function loadProdutosSeed() {
    let apiError = "";
    try {
        const data = await api("GET", "");
        const produtos = extractProdutosPayload(data);
        if (produtos) {
            produtosState.sourceInfo = "Fonte: API backend";
            return normalizeProdutoList(produtos);
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
            return normalizeProdutoList(data);
        }
    } catch (seedErr) {
        apiError = `${apiError} Seed indisponivel (${seedErr?.message || "falha"}).`;
    }

    produtosState.sourceInfo = `${apiError} Fallback: mock local`;
    return normalizeProdutoList(localGET("produtos"));
}

async function fetchBases() {
    try {
        const data = await api("GET", "/bases");
        if (data.ok && Array.isArray(data.data)) return data.data;
    } catch {
        return [];
    }
    return [];
}

async function fetchBom(produtoId) {
    try {
        const data = await api("GET", `/${produtoId}/bom`);
        return data.ok && Array.isArray(data.data) ? data.data : [];
    } catch {
        return [];
    }
}

async function reloadData() {
    produtosState.produtos = await loadProdutosSeed();
    produtosState.bases = await fetchBases();
    popularFiltros(produtosState.produtos);
}

function bindModalEvents() {
    const closeButtons = document.querySelectorAll("[data-action='close-modal']");
    closeButtons.forEach((btn) => {
        btn.onclick = () => closeCurrentModal();
    });

    const saveBase = document.getElementById("btnSalvarBaseAta");
    if (saveBase) {
        saveBase.onclick = async () => {
            const ata = document.getElementById("baseAtaNome")?.value?.trim() || "";
            const numero = document.getElementById("baseAtaNumero")?.value?.trim() || "";
            const empresa = document.getElementById("baseEmpresa")?.value || "";
            if (!ata || !numero || !empresa) return alert("Preencha ATA, numero e empresa.");
            try {
                await api("POST", "/bases", { ata_nome: ata, numero_ata: numero, empresa_key: empresa });
                closeCurrentModal();
                await reloadData();
                renderProdutosFiltrados();
            } catch (err) {
                reportUiError("Erro ao salvar Base ATA", err);
            }
        };
    }

    const saveProduto = document.getElementById("btnSalvarProduto");
    if (saveProduto) {
        saveProduto.onclick = async () => {
            const formData = collectProdutoForm();
            if (!formData) return;
            try {
                let saved;
                if (uiState.modalProdutoId) {
                    saved = await api("PUT", `/${uiState.modalProdutoId}`, formData.payload);
                } else {
                    saved = await api("POST", "", formData.payload);
                }
                const produtoId = saved?.data?.id || uiState.modalProdutoId;
                if (formData.imagemFile && produtoId) {
                    await uploadProdutoImagem(produtoId, formData.imagemFile);
                }
                closeCurrentModal();
                await reloadData();
                renderProdutosFiltrados();
            } catch (err) {
                reportUiError("Erro ao salvar Produto", err);
            }
        };
    }

    const saveBom = document.getElementById("btnSalvarBom");
    if (saveBom) {
        saveBom.onclick = async () => {
            if (!bomState.produtoSelecionado) return;
            const itens = collectBomFormRows();
            try {
                await api("PUT", `/${bomState.produtoSelecionado.id}/bom`, { itens });
                closeCurrentModal();
                await abrirBomProduto(bomState.produtoSelecionado);
            } catch (err) {
                reportUiError("Erro ao salvar BOM", err);
            }
        };
    }

    const addBomItem = document.getElementById("btnAdicionarBomItem");
    if (addBomItem) {
        addBomItem.onclick = () => addBomRow();
    }

    const btnEditarBom = document.getElementById("btnEditarBom");
    if (btnEditarBom) {
        btnEditarBom.onclick = () => openBomModal();
    }
}

function openBaseModal() {
    uiState.modalProdutoId = null;
    openModal("modalBaseAta");
}

function openProdutoModal(produtoId) {
    uiState.modalProdutoId = produtoId || null;
    populateBaseSelect("produtoBaseAta");
    if (produtoId) {
        const p = produtosState.produtos.find((x) => Number(x.id) === Number(produtoId));
        if (p) fillProdutoForm(p);
    } else {
        clearProdutoForm();
    }
    openModal("modalProduto");
}

function openBomModal() {
    if (!bomState.produtoSelecionado) return;
    const tbody = document.getElementById("bomEditRows");
    if (!tbody) return;
    tbody.innerHTML = "";
    (bomState.itens || []).forEach((item) => addBomRow(item));
    if (!bomState.itens.length) addBomRow();
    openModal("modalBom");
}

function openModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    uiState.modalOpen = id;
    modal.classList.remove("hidden");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
}

function closeCurrentModal() {
    if (!uiState.modalOpen) return;
    const modal = document.getElementById(uiState.modalOpen);
    if (modal) {
        modal.classList.add("hidden");
        modal.setAttribute("aria-hidden", "true");
    }
    uiState.modalOpen = null;
    document.body.style.overflow = "";
}

function populateBaseSelect(selectId) {
    const select = document.getElementById(selectId);
    if (!select) return;
    const opts = [{ value: "", label: "Selecione..." }].concat(
        produtosState.bases
            .filter((b) => toBoolean(b.ativo ?? true))
            .map((b) => ({ value: String(b.id), label: `${b.ata_nome} | ${b.numero_ata} | ${b.empresa_nome}` }))
    );
    setSelectOptions(select, opts);
}

function clearProdutoForm() {
    const ids = ["produtoItemAta", "produtoNomeOficial", "produtoCategoria", "produtoImagemPath"];
    ids.forEach((id) => {
        const el = document.getElementById(id);
        if (el) el.value = "";
    });
    const file = document.getElementById("produtoImagemFile");
    if (file) file.value = "";
    const base = document.getElementById("produtoBaseAta");
    if (base) base.value = "";
}

function fillProdutoForm(produto) {
    const base = document.getElementById("produtoBaseAta");
    const item = document.getElementById("produtoItemAta");
    const nome = document.getElementById("produtoNomeOficial");
    const cat = document.getElementById("produtoCategoria");
    const img = document.getElementById("produtoImagemPath");
    const file = document.getElementById("produtoImagemFile");
    if (base) base.value = String(produto.base_ata_id || "");
    if (item) item.value = produto.item_ata || "";
    if (nome) nome.value = produto.nome_oficial || "";
    if (cat) cat.value = produto.categoria || "";
    if (img) img.value = produto.imagem_path || "";
    if (file) file.value = "";
}

function collectProdutoForm() {
    const base = Number(document.getElementById("produtoBaseAta")?.value || "");
    const item = document.getElementById("produtoItemAta")?.value?.trim() || "";
    const nome = document.getElementById("produtoNomeOficial")?.value?.trim() || "";
    const categoria = document.getElementById("produtoCategoria")?.value?.trim() || "";
    const imagem = document.getElementById("produtoImagemPath")?.value?.trim() || null;
    const fileInput = document.getElementById("produtoImagemFile");
    const imagemFile = fileInput?.files?.[0] || null;
    if (!base || !item || !nome) {
        alert("Base ATA, Item ATA e Nome Oficial sao obrigatorios.");
        return null;
    }
    return {
        payload: {
            base_ata_id: base,
            item_ata: item,
            nome_oficial: nome,
            categoria: categoria || null,
            imagem_path: imagem
        },
        imagemFile
    };
}

async function uploadProdutoImagem(produtoId, file) {
    const form = new FormData();
    form.append("arquivo", file);
    return apiForm("POST", `/${produtoId}/imagem/upload`, form);
}

function addBomRow(row = null) {
    const tbody = document.getElementById("bomEditRows");
    if (!tbody) return;
    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td><select class="bom-grupo">${BOM_GRUPOS.map((g) => `<option value="${g}">${g}</option>`).join("")}</select></td>
        <td><input class="bom-item-nome" type="text" value="${escapeHtml(row?.item_nome || "")}"></td>
        <td><input class="bom-quantidade" type="number" step="0.01" value="${escapeHtml(row?.quantidade ?? "")}"></td>
        <td><input class="bom-unidade" type="text" value="${escapeHtml(row?.unidade || "")}"></td>
        <td><input class="bom-observacao" type="text" value="${escapeHtml(row?.observacao || "")}"></td>
        <td><button type="button" class="btn-row-action" data-action="remove-bom-row">Remover</button></td>
    `;
    tbody.appendChild(tr);
    const g = tr.querySelector(".bom-grupo");
    if (g && row?.grupo) g.value = row.grupo;
    const rm = tr.querySelector("[data-action='remove-bom-row']");
    if (rm) rm.addEventListener("click", () => tr.remove());
}

function collectBomFormRows() {
    const tbody = document.getElementById("bomEditRows");
    if (!tbody) return [];
    const rows = [...tbody.querySelectorAll("tr")];
    return rows
        .map((tr, idx) => {
            const grupo = tr.querySelector(".bom-grupo")?.value || "";
            const itemNome = tr.querySelector(".bom-item-nome")?.value?.trim() || "";
            const qtdRaw = tr.querySelector(".bom-quantidade")?.value || "";
            const unidade = tr.querySelector(".bom-unidade")?.value?.trim() || null;
            const obs = tr.querySelector(".bom-observacao")?.value?.trim() || null;
            if (!itemNome || !BOM_GRUPOS.includes(grupo)) return null;
            return {
                grupo,
                item_nome: itemNome,
                quantidade: qtdRaw === "" ? null : Number(qtdRaw),
                unidade,
                observacao: obs,
                ordem: idx + 1
            };
        })
        .filter(Boolean);
}

async function toggleProdutoAtivo(produtoId) {
    const produto = produtosState.produtos.find((p) => Number(p.id) === Number(produtoId));
    if (!produto) return;
    const payload = {
        base_ata_id: produto.base_ata_id,
        item_ata: produto.item_ata,
        nome_oficial: produto.nome_oficial,
        categoria: produto.categoria || null,
        imagem_path: produto.imagem_path || null,
        ativo: !toBoolean(produto.ativo)
    };
    await api("PUT", `/${produtoId}`, payload);
    await reloadData();
    renderProdutosFiltrados();
}

async function api(method, path, body = null) {
    let response;
    try {
        response = await fetch(`${BASE_API}${path}`, {
            method,
            headers: { "Content-Type": "application/json" },
            body: body ? JSON.stringify(body) : undefined
        });
    } catch (err) {
        throw new Error(`Falha de conexao com API (${BASE_API}). Verifique se o backend esta ativo na porta 8876 e acessivel pelo mesmo host da tela. Detalhe: ${err?.message || err}`);
    }

    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.ok === false) {
        const msg = data?.error?.message || data?.detail?.error?.message || `Falha API ${response.status}`;
        throw new Error(msg);
    }
    return data;
}

async function apiForm(method, path, formData) {
    let response;
    try {
        response = await fetch(`${BASE_API}${path}`, {
            method,
            body: formData
        });
    } catch (err) {
        throw new Error(`Falha de conexao com API (${BASE_API}). Verifique se o backend esta ativo na porta 8876 e acessivel pelo mesmo host da tela. Detalhe: ${err?.message || err}`);
    }

    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.ok === false) {
        const msg = data?.error?.message || data?.detail?.error?.message || `Falha API ${response.status}`;
        throw new Error(msg);
    }
    return data;
}
