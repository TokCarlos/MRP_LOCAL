import { localGET } from "../api.js";

const SEED_PATH = "data/produtos_seed.json";
const API_HOST = window.location.hostname || "127.0.0.1";
const API_PROTOCOL = window.location.protocol === "http:" || window.location.protocol === "https:" ? window.location.protocol : "http:";
const API_ORIGIN = `${API_PROTOCOL}//${API_HOST}:8876`;
const BASE_API = `${API_ORIGIN}/api/produtos`;
const PLACEHOLDER = "img/ui/placeholders/produto_placeholder.svg";
const EMPRESAS = [
    { key: "jpl", nome: "JPL" },
    { key: "aco", nome: "Aço" },
    { key: "tcr", nome: "TCR" }
];
const BOM_GRUPOS = ["tubos", "chapas", "insumos"];
const BOM_GRUPO_LABELS = {
    tubos: "TUBOS",
    chapas: "CHAPAS",
    insumos: "INSUMOS"
};
const SESSION_KEY = "mrp_local_session";
const ADMIN_USERS = new Set(["admin", "administrador"]);

function getLocalSession() {
    try {
        return JSON.parse(localStorage.getItem(SESSION_KEY) || "{}");
    } catch {
        return {};
    }
}

function hasAdminToken(value) {
    const normalized = String(value || "").trim().toLowerCase();
    return normalized === "admin" || normalized === "administrador" || normalized === "grupo_admin";
}

function isAdminUser() {
    const session = getLocalSession();
    if (ADMIN_USERS.has(String(session.user || "").trim().toLowerCase())) return true;
    if (hasAdminToken(session.role) || hasAdminToken(session.perfil) || hasAdminToken(session.grupo)) return true;
    if (Array.isArray(session.grupos) && session.grupos.some(hasAdminToken)) return true;
    if (Array.isArray(session.permissions) && session.permissions.some(hasAdminToken)) return true;
    return false;
}

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

const bomState = { produtoSelecionado: null, itens: [], ultimaAtualizacao: null, historico: [] };
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

function parseBomDate(value) {
    if (!value) return null;
    const raw = String(value).trim();
    if (!raw) return null;
    const date = new Date(raw);
    return Number.isNaN(date.getTime()) ? null : date;
}

function formatBomDate(value) {
    const date = parseBomDate(value);
    if (!date) return "sem registro";
    const dias = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SAB"];
    const dd = String(date.getDate()).padStart(2, "0");
    const mm = String(date.getMonth() + 1).padStart(2, "0");
    const yyyy = String(date.getFullYear());
    const hh = String(date.getHours()).padStart(2, "0");
    const min = String(date.getMinutes()).padStart(2, "0");
    return `${dias[date.getDay()]} - ${dd}/${mm}/${yyyy} - ${hh}:${min}`;
}

function setBomUltimaAtualizacao(value) {
    bomState.ultimaAtualizacao = value || null;
    const btn = document.getElementById("btnBomHistorico");
    if (btn) btn.textContent = `Última atualização: ${formatBomDate(value)}`;
}

function bomAcaoLabel(value) {
    const map = {
        ADICIONADO: "ADICIONADO",
        MODIFICADO: "MODIFICADO",
        REMOVIDO: "REMOVIDO",
        BOM_ATUALIZADA: "BOM ATUALIZADA",
        HISTORICO_LIMPO: "HISTÓRICO LIMPO"
    };
    const key = String(value || "").trim().toUpperCase();
    return map[key] || key || "-";
}

function resolveImageSrc(value, version = "") {
    const raw = String(value || "").trim().replace(/\\/g, "/");
    if (!raw) return PLACEHOLDER;
    if (/^(https?:)?\/\//i.test(raw) || raw.startsWith("data:")) return raw;
    const clean = raw.replace(/^\/+/, "");
    if (clean.startsWith("media/")) {
        const suffix = version ? `?v=${encodeURIComponent(version)}` : "";
        return `${API_ORIGIN}/${clean}${suffix}`;
    }
    return clean;
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
        if (!isAdminUser() && !toBoolean(produto.ativo ?? true)) return false;
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
        const itemNumero = String(p.item_ata ?? p.itemAta ?? p.item ?? p.numero_item ?? p.numero ?? id).trim() || String(id);
        const officialImagePath = p.imagem_path || p.imagem_url || "";
        const previewImagePath = p?.imagem?.preview || "";
        const imagePath = officialImagePath || previewImagePath || PLACEHOLDER;
        const fallbackImagePath = officialImagePath && previewImagePath ? previewImagePath : PLACEHOLDER;
        const preview = resolveImageSrc(imagePath, p.updated_at || "");
        const previewFallback = resolveImageSrc(fallbackImagePath, "");
        const arp = String(p.arp || "").trim();
        const ataNumeroRaw = String(p.ata_numero || p.ata || "").trim();
        const ataNumero = arp.includes(ataNumeroRaw) || !ataNumeroRaw
            ? arp
            : `${arp} ${ataNumeroRaw}`.trim();
        const empresa = p.empresa || "";
        const produtoAtivo = toBoolean(p.ativo ?? true);
        const admin = isAdminUser();
        const rowClasses = produtoAtivo ? "" : "produto-desativado";
        const toggleLabel = produtoAtivo ? "Desativar" : "Ativar";
        const statusBadge = produtoAtivo ? "" : `<span class="produto-status-desativado">Desativado</span>`;

        tr.className = rowClasses;

        const safeId = escapeHtml(id);
        const safeItemNumero = escapeHtml(itemNumero);
        const safePreview = escapeHtml(preview);
        const safePlaceholder = escapeHtml(PLACEHOLDER);
        const safePreviewFallback = escapeHtml(previewFallback);
        const safeAtaNumero = escapeHtml(ataNumero);
        const safeNome = escapeHtml(nome);
        const safeEmpresa = escapeHtml(empresa);

        tr.innerHTML = `
            <td class="col-id" data-label="ID">${safeId}</td>
            <td class="col-preview" data-label="PREVIEW">
                <img class="produto-preview js-produto-preview" data-action="zoom-image" data-image="${safePreview}" data-fallback="${safePreviewFallback}" src="${safePreview}" alt="Preview demo" width="56" height="32" loading="lazy" onerror="this.onerror=null;this.src=this.dataset.fallback || '${safePlaceholder}';">
                <span class="produto-preview-item-numero">Nº ${safeItemNumero}</span>
            </td>
            <td class="col-ata-numero" data-label="ATA + Nº">${safeAtaNumero}</td>
            <td class="col-produto" data-label="PRODUTO">${safeNome}${statusBadge}</td>
            <td class="col-empresa" data-label="EMPRESA">${safeEmpresa}</td>
            <td class="col-acao" data-label="AÇÃO">
                <div class="prod-actions">
                    <button class="btn-row-action js-btn-bom" data-action="open-bom" type="button" data-produto-id="${safeId}">BOM</button>
                    <button class="btn-row-action" data-action="edit-produto" type="button" data-produto-id="${safeId}">Editar</button>
                    ${admin ? `<button class="btn-row-action btn-toggle-produto" data-action="toggle-produto" type="button" data-produto-id="${safeId}">${toggleLabel}</button>` : ""}
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
            const src = img.currentSrc || img.src || img.dataset.image || PLACEHOLDER;
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
    setBomUltimaAtualizacao(await fetchBomUltimaAtualizacao(produto.id));
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
    closeBomHistoricoModal();
    bomState.produtoSelecionado = null;
    bomState.historico = [];
    setBomUltimaAtualizacao(null);
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

function normalizeBomGrupo(value) {
    const grupo = String(value || "").trim().toLowerCase();
    return BOM_GRUPOS.includes(grupo) ? grupo : "tubos";
}

function getFirstFilled(...values) {
    for (const value of values) {
        if (value === 0) return "0";
        if (value === null || value === undefined) continue;
        const text = String(value).trim();
        if (text) return text;
    }
    return "";
}

function normalizeBomItem(row = {}) {
    const grupo = normalizeBomGrupo(row.grupo);
    const material = getFirstFilled(row.material, row.item_nome, row.descricao, row.nome);
    const tamanho = getFirstFilled(row.tamanho, grupo === "insumos" ? "" : row.unidade);
    const unidade = getFirstFilled(row.unidade, grupo === "insumos" ? row.tamanho : "");
    return {
        ...row,
        grupo,
        cod: getFirstFilled(row.cod, row.codigo, row.id),
        material,
        dim1: getFirstFilled(row.dim1, row.dimensao1, row.observacao),
        dim2: getFirstFilled(row.dim2, row.dimensao2),
        espessura: getFirstFilled(row.espessura, row.esp),
        revestimento: getFirstFilled(row.revestimento, row.resvestimento),
        tamanho,
        unidade,
        quantidade: row.quantidade ?? row.qtd ?? ""
    };
}

function getBomMedidaValue(item) {
    const normalized = normalizeBomItem(item);
    return normalized.grupo === "insumos" ? normalized.unidade : normalized.tamanho;
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
    rows.map(normalizeBomItem).forEach((row) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${escapeHtml(row.cod || "-")}</td>
            <td>${escapeHtml(row.material || "-")}</td>
            <td>${escapeHtml(row.dim1 || "-")}</td>
            <td>${escapeHtml(row.dim2 || "-")}</td>
            <td>${escapeHtml(row.espessura || "-")}</td>
            <td>${escapeHtml(row.revestimento || "-")}</td>
            <td>${escapeHtml(getBomMedidaValue(row) || "-")}</td>
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
        const query = isAdminUser() ? "?include_inactive=1" : "";
        const data = await api("GET", query);
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
        if (data.ok && Array.isArray(data.data)) return data.data;
        if (data.ok && Array.isArray(data.data?.itens)) {
            setBomUltimaAtualizacao(data.data.ultima_atualizacao_bom || data.data.ultima_atualizacao || null);
            return data.data.itens;
        }
        return [];
    } catch {
        return [];
    }
}

async function fetchBomUltimaAtualizacao(produtoId) {
    try {
        const data = await api("GET", `/${produtoId}/bom/ultima-atualizacao`);
        if (data.ok) return data.data?.ultima_atualizacao_bom || data.data?.ultima_atualizacao || null;
    } catch {
        return null;
    }
    return null;
}

async function fetchBomHistorico(produtoId) {
    try {
        const data = await api("GET", `/${produtoId}/bom/historico`);
        if (data.ok && Array.isArray(data.data)) return data.data;
        if (data.ok && Array.isArray(data.data?.items)) return data.data.items;
    } catch {
        return [];
    }
    return [];
}

async function reloadData() {
    produtosState.produtos = await loadProdutosSeed();
    produtosState.bases = await fetchBases();
    popularFiltros(produtosState.produtos);
}

function bindModalEvents() {
    initBomModalDrag();
    initBomHistoricoModalDrag();
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

    const btnBomHistorico = document.getElementById("btnBomHistorico");
    if (btnBomHistorico) {
        btnBomHistorico.onclick = () => openBomHistoricoModal();
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
    resetBomModalPosition();
    openModal("modalBom");
}

function resetBomModalPosition() {
    const content = document.querySelector("#modalBom .modal-content");
    if (!content) return;
    content.style.left = "";
    content.style.top = "";
    content.style.transform = "";
}

function initFloatingModalDrag(modalId) {
    const modal = document.getElementById(modalId);
    const content = modal?.querySelector(".modal-content");
    const handle = modal?.querySelector(`[data-drag-modal='${modalId}']`);
    if (!modal || !content || !handle || handle.dataset.dragBound === "1") return;
    handle.dataset.dragBound = "1";

    let dragging = false;
    let offsetX = 0;
    let offsetY = 0;

    const startDrag = (event) => {
        if (event.button !== undefined && event.button !== 0) return;
        const target = event.target;
        if (target instanceof HTMLElement && target.closest("button, input, select, textarea")) return;
        const rect = content.getBoundingClientRect();
        dragging = true;
        offsetX = event.clientX - rect.left;
        offsetY = event.clientY - rect.top;
        content.style.left = `${rect.left}px`;
        content.style.top = `${rect.top}px`;
        content.style.transform = "none";
        content.classList.add("is-dragging");
        event.preventDefault();
    };

    const moveDrag = (event) => {
        if (!dragging) return;
        const maxLeft = Math.max(8, window.innerWidth - content.offsetWidth - 8);
        const maxTop = Math.max(8, window.innerHeight - content.offsetHeight - 8);
        const nextLeft = Math.min(Math.max(8, event.clientX - offsetX), maxLeft);
        const nextTop = Math.min(Math.max(8, event.clientY - offsetY), maxTop);
        content.style.left = `${nextLeft}px`;
        content.style.top = `${nextTop}px`;
    };

    const endDrag = () => {
        if (!dragging) return;
        dragging = false;
        content.classList.remove("is-dragging");
    };

    handle.addEventListener("mousedown", startDrag);
    document.addEventListener("mousemove", moveDrag);
    document.addEventListener("mouseup", endDrag);
}

function initBomModalDrag() {
    initFloatingModalDrag("modalBom");
}

function initBomHistoricoModalDrag() {
    initFloatingModalDrag("modalBomHistorico");
}

function resetBomHistoricoModalPosition() {
    const content = document.querySelector("#modalBomHistorico .modal-content");
    if (!content) return;
    content.style.left = "";
    content.style.top = "";
    content.style.transform = "";
}

function closeBomHistoricoModal() {
    const modal = document.getElementById("modalBomHistorico");
    if (!modal) return;
    modal.classList.add("hidden");
    modal.setAttribute("aria-hidden", "true");
    if (uiState.modalOpen === "modalBomHistorico") {
        uiState.modalOpen = null;
        document.body.style.overflow = "";
    }
}

function renderBomHistoricoRows(rows) {
    const tbody = document.getElementById("bomHistoricoRows");
    if (!tbody) return;
    tbody.innerHTML = "";
    if (!rows.length) {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td colspan="6">Sem histórico registrado para este produto.</td>`;
        tbody.appendChild(tr);
        return;
    }
    rows.forEach((row) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${escapeHtml(formatBomDate(row.created_at || row.data_hora))}</td>
            <td>${escapeHtml(bomAcaoLabel(row.acao))}</td>
            <td>${escapeHtml(String(row.grupo || "-").toUpperCase())}</td>
            <td>${escapeHtml(row.cod || "-")}</td>
            <td>${escapeHtml(row.material || "-")}</td>
            <td>${escapeHtml(row.detalhe || "-")}</td>
        `;
        tbody.appendChild(tr);
    });
}

async function openBomHistoricoModal() {
    if (!bomState.produtoSelecionado) return;
    const titulo = document.getElementById("bomHistoricoProdutoTitulo");
    if (titulo) {
        const produto = bomState.produtoSelecionado;
        titulo.textContent = `Produto selecionado: ID ${produto.id || "-"} | ${produto.nome_oficial || produto.nome || "-"}`;
    }
    try {
        bomState.historico = await fetchBomHistorico(bomState.produtoSelecionado.id);
        renderBomHistoricoRows(bomState.historico);
        resetBomHistoricoModalPosition();
        openModal("modalBomHistorico");
    } catch (err) {
        reportUiError("Erro ao abrir histórico da BOM", err);
    }
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

function updateBomRowMedidaField(tr) {
    const input = tr.querySelector(".bom-medida");
    if (input) input.placeholder = "";
}

function addBomRow(row = null) {
    const tbody = document.getElementById("bomEditRows");
    if (!tbody) return;
    const normalized = normalizeBomItem(row || {});
    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td><input class="bom-id" type="hidden" value="${escapeHtml(normalized.id || "")}"><select class="bom-grupo">${BOM_GRUPOS.map((g) => `<option value="${g}">${BOM_GRUPO_LABELS[g]}</option>`).join("")}</select></td>
        <td><input class="bom-cod" type="text" value="${escapeHtml(normalized.cod || "")}"></td>
        <td><input class="bom-material" type="text" value="${escapeHtml(normalized.material || "")}"></td>
        <td><input class="bom-dim1" type="text" value="${escapeHtml(normalized.dim1 || "")}"></td>
        <td><input class="bom-dim2" type="text" value="${escapeHtml(normalized.dim2 || "")}"></td>
        <td><input class="bom-espessura" type="text" value="${escapeHtml(normalized.espessura || "")}"></td>
        <td><input class="bom-revestimento" type="text" value="${escapeHtml(normalized.revestimento || "")}"></td>
        <td><input class="bom-medida" type="text" value="${escapeHtml(getBomMedidaValue(normalized) || "")}"></td>
        <td><input class="bom-quantidade" type="number" step="0.01" value="${escapeHtml(normalized.quantidade ?? "")}"></td>
        <td><button type="button" class="btn-row-action" data-action="remove-bom-row">Remover</button></td>
    `;
    tbody.appendChild(tr);
    const g = tr.querySelector(".bom-grupo");
    if (g) {
        g.value = normalized.grupo;
        g.addEventListener("change", () => updateBomRowMedidaField(tr));
    }
    updateBomRowMedidaField(tr);
    const rm = tr.querySelector("[data-action='remove-bom-row']");
    if (rm) rm.addEventListener("click", () => tr.remove());
}

function collectBomFormRows() {
    const tbody = document.getElementById("bomEditRows");
    if (!tbody) return [];
    const rows = [...tbody.querySelectorAll("tr")];
    return rows
        .map((tr, idx) => {
            const bomIdRaw = tr.querySelector(".bom-id")?.value || "";
            const bomId = bomIdRaw ? Number(bomIdRaw) : null;
            const grupo = normalizeBomGrupo(tr.querySelector(".bom-grupo")?.value || "");
            const cod = tr.querySelector(".bom-cod")?.value?.trim() || null;
            const material = tr.querySelector(".bom-material")?.value?.trim() || "";
            const dim1 = tr.querySelector(".bom-dim1")?.value?.trim() || null;
            const dim2 = tr.querySelector(".bom-dim2")?.value?.trim() || null;
            const espessura = tr.querySelector(".bom-espessura")?.value?.trim() || null;
            const revestimento = tr.querySelector(".bom-revestimento")?.value?.trim() || null;
            const medida = tr.querySelector(".bom-medida")?.value?.trim() || null;
            const qtdRaw = tr.querySelector(".bom-quantidade")?.value || "";
            if (!material || !BOM_GRUPOS.includes(grupo)) return null;
            const tamanho = grupo === "insumos" ? null : medida;
            const unidade = grupo === "insumos" ? medida : null;
            return {
                id: Number.isFinite(bomId) ? bomId : null,
                grupo,
                cod,
                material,
                dim1,
                dim2,
                espessura,
                revestimento,
                tamanho,
                unidade,
                quantidade: qtdRaw === "" ? null : Number(qtdRaw),
                ordem: idx + 1,
                item_nome: material,
                observacao: dim1
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
