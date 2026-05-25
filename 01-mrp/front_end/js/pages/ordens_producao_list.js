const API_HOST = window.location.hostname || "127.0.0.1";
const API_PROTOCOL = window.location.protocol === "http:" || window.location.protocol === "https:" ? window.location.protocol : "http:";
const API_ORIGIN = `${API_PROTOCOL}//${API_HOST}:8876`;
const API_OP = `${API_ORIGIN}/api/ordens-producao`;
const API_OP_KANBAN = `${API_OP}/kanban`;
const API_PRODUTOS = `${API_ORIGIN}/api/produtos`;
const API_PRODUTOS_BASES = `${API_PRODUTOS}/bases`;

const STATUS_PROCESSO_OPTIONS = ["PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "PAUSADO"];
const STATUS_KANBAN_OPTIONS = ["NAO_INICIADO", "EM_ANDAMENTO", "CONCLUIDO"];
const PROCESSOS_OP_OPTIONS = [
    { key: "corte", nome: "Corte" },
    { key: "dobra", nome: "Dobra" },
    { key: "montagem_solda", nome: "Montagem/Solda" },
    { key: "solda", nome: "Solda" },
    { key: "acabamento", nome: "Acabamento" },
    { key: "pintura", nome: "Pintura" },
    { key: "sublimacao", nome: "Sublimação" },
    { key: "montagem", nome: "Montagem" },
    { key: "teste", nome: "Teste" },
    { key: "expedicao", nome: "Expedição" },
];

const state = {
    kanban: null,
    produtosCatalogo: [],
    basesCatalogo: [],
    opProdutosSelecionados: [],
    opProdutosOriginais: [],
    filtros: { texto: "", status: "", empresa: "" },
    opKanbanCtx: null,
    opPularCtx: null,
    opBomCtx: null,
};

function parseQuantidadeProduto(value) {
    const raw = String(value ?? "").trim();
    if (!/^\d+$/.test(raw)) return null;
    const qtd = Number.parseInt(raw, 10);
    return qtd > 0 ? qtd : null;
}

function sanitizeQuantidadeProdutoInput(input) {
    if (!input) return;
    const onlyDigits = String(input.value || "").replace(/\D+/g, "");
    if (input.value !== onlyDigits) input.value = onlyDigits;
}

export async function init() {
    bindBaseEvents();
    await Promise.all([loadKanban(), loadProdutosCatalogo(), loadBasesCatalogo()]);
    renderKanban();
}

function bindBaseEvents() {
    const btnNovaOp = document.getElementById("btnNovaOp");
    const filtroTexto = document.getElementById("filtroOpTexto");
    const filtroStatus = document.getElementById("filtroOpStatus");
    const filtroEmpresa = document.getElementById("filtroOpEmpresa");
    const btnLimpar = document.getElementById("btnLimparFiltrosOp");
    const kanbanBoard = document.getElementById("opKanbanBoard");

    if (btnNovaOp) btnNovaOp.addEventListener("click", () => openModalOpCabecalho());

    if (filtroTexto) {
        filtroTexto.addEventListener("input", (event) => {
            state.filtros.texto = event.target.value || "";
            renderKanban();
        });
    }
    if (filtroStatus) {
        filtroStatus.addEventListener("change", (event) => {
            state.filtros.status = event.target.value || "";
            renderKanban();
        });
    }
    if (filtroEmpresa) {
        filtroEmpresa.addEventListener("change", (event) => {
            state.filtros.empresa = event.target.value || "";
            renderKanban();
        });
    }
    if (btnLimpar) {
        btnLimpar.addEventListener("click", () => {
            state.filtros = { texto: "", status: "", empresa: "" };
            if (filtroTexto) filtroTexto.value = "";
            if (filtroStatus) filtroStatus.value = "";
            if (filtroEmpresa) filtroEmpresa.value = "";
            renderKanban();
        });
    }

    if (kanbanBoard) {
        kanbanBoard.addEventListener("click", async (event) => {
            const actionButton = event.target.closest("button[data-action]");
            const card = event.target.closest(".op-kanban-card");
            const opId = Number((actionButton?.dataset.opId || card?.dataset.opId || 0));
            if (!opId) return;

            try {
                if (!actionButton && card) {
                    await openModalOpKanbanOperacional(opId);
                    return;
                }
                if (!actionButton) return;

                const action = actionButton.dataset.action;
                if (action === "menu-toggle") {
                    openModalOpAcoesCard(card);
                    return;
                }
                await handleOpAction(action, opId);
            } catch (err) {
                setInlineError("opKanbanFeedback", getErrorMessage(err));
            }
        });
    }

    bindModalEvents();
}

function bindModalEvents() {
    document.querySelectorAll("[data-close-modal]").forEach((button) => {
        button.addEventListener("click", () => closeModal(button.getAttribute("data-close-modal")));
    });

    const opModeloAta = document.getElementById("opModeloAta");
    if (opModeloAta) opModeloAta.addEventListener("change", () => {
        syncAtaEmpresaUi();
        renderProdutosDisponiveisOp();
    });
    const opProdutoBusca = document.getElementById("opProdutoBusca");
    if (opProdutoBusca) opProdutoBusca.addEventListener("input", renderProdutosDisponiveisOp);

    const btnSalvarOp = document.getElementById("btnSalvarOp");
    if (btnSalvarOp) btnSalvarOp.addEventListener("click", saveModalOpCabecalho);

    const opAcoesCardBody = document.getElementById("opAcoesCardBody");
    if (opAcoesCardBody) {
        opAcoesCardBody.addEventListener("click", async (event) => {
            const button = event.target.closest("button[data-action]");
            if (!button) return;
            const opId = Number(button.dataset.opId || 0);
            if (!opId) return;
            try {
                clearInlineError("opAcoesErro");
                closeModal("modalOpAcoesCard");
                await handleOpAction(button.dataset.action, opId);
            } catch (err) {
                setInlineError("opKanbanFeedback", getErrorMessage(err));
            }
        });
    }

    const opCardStatusSelect = document.getElementById("opCardStatusSelect");
    if (opCardStatusSelect) {
        opCardStatusSelect.addEventListener("change", async (event) => {
            const statusDestino = String(event.target.value || "");
            if (!STATUS_KANBAN_OPTIONS.includes(statusDestino)) return;
            const ctx = state.opKanbanCtx;
            if (!ctx?.opId) return;
            try {
                clearInlineError("opKanbanErro");
                await setKanbanStatus(ctx.opId, statusDestino, ctx.processoKey);
                await refreshKanban();
                await openModalOpKanbanOperacional(ctx.opId);
            } catch (err) {
                setInlineError("opKanbanErro", getErrorMessage(err));
            }
        });
    }

    const btnOpCardPularEtapa = document.getElementById("btnOpCardPularEtapa");
    if (btnOpCardPularEtapa) {
        btnOpCardPularEtapa.addEventListener("click", () => {
            const ctx = state.opKanbanCtx;
            if (!ctx?.opId) return;
            openModalOpPularEtapa(ctx.opId, ctx.processoKey);
        });
    }

    const btnConfirmarPuloEtapa = document.getElementById("btnConfirmarPuloEtapa");
    if (btnConfirmarPuloEtapa) {
        btnConfirmarPuloEtapa.addEventListener("click", confirmPularEtapaModal);
    }

    const btnConfirmarCancelamento = document.getElementById("btnConfirmarCancelamentoOp");
    if (btnConfirmarCancelamento) {
        btnConfirmarCancelamento.addEventListener("click", () => resolverConfirmacaoCancelamento(true));
    }
    const btnVoltarCancelamento = document.getElementById("btnVoltarCancelamentoOp");
    if (btnVoltarCancelamento) {
        btnVoltarCancelamento.addEventListener("click", () => resolverConfirmacaoCancelamento(false));
    }

    const opProdutoLista = document.getElementById("opProdutoLista");
    if (opProdutoLista) {
        opProdutoLista.addEventListener("click", (event) => {
            const button = event.target.closest("button[data-action='adicionar-produto-guiado']");
            if (!button) return;
            const produtoId = Number(button.dataset.produtoId || 0);
            const input = document.getElementById(`opQtdProduto_${produtoId}`);
            sanitizeQuantidadeProdutoInput(input);
            const qtd = parseQuantidadeProduto(input?.value);
            if (qtd === null) {
                alert("Quantidade do produto deve ser um número inteiro maior que zero.");
                return;
            }
            addProdutoSelecionadoGuiado(produtoId, qtd);
        });
    }
    const opProdutosSelecionados = document.getElementById("opProdutosSelecionados");
    if (opProdutosSelecionados) {
        opProdutosSelecionados.addEventListener("click", (event) => {
            const toggle = event.target.closest("button[data-action='toggle-selecionados']");
            if (toggle) {
                toggleProdutosSelecionados(toggle);
                return;
            }
            const button = event.target.closest("button[data-action='remover-produto-guiado']");
            if (!button) return;
            removeProdutoSelecionadoGuiado(Number(button.dataset.produtoId || 0));
        });
        opProdutosSelecionados.addEventListener("input", (event) => {
            const input = event.target.closest("input[data-action='qtd-produto-guiado']");
            if (!input) return;
            sanitizeQuantidadeProdutoInput(input);
            const qtd = parseQuantidadeProduto(input.value);
            if (qtd !== null) updateProdutoSelecionadoQtd(Number(input.dataset.produtoId || 0), qtd);
        });
    }

    const opKanbanProdutosRows = document.getElementById("opKanbanProdutosRows");
    if (opKanbanProdutosRows) {
        opKanbanProdutosRows.addEventListener("input", (event) => {
            const input = event.target.closest("input[data-action='qtd-op-kanban']");
            if (!input) return;
            sanitizeQuantidadeProdutoInput(input);
        });
        opKanbanProdutosRows.addEventListener("change", async (event) => {
            const input = event.target.closest("input[data-action='qtd-op-kanban']");
            if (!input) return;
            const opProdutoId = Number(input.dataset.opProdutoId || 0);
            if (!opProdutoId) return;
            try {
                await saveKanbanProdutoQuantidade(opProdutoId, input);
            } catch (err) {
                setInlineError("opKanbanErro", getErrorMessage(err));
            }
        });
    }

    const btnOpCardEditar = document.getElementById("btnOpCardEditar");
    if (btnOpCardEditar) {
        btnOpCardEditar.addEventListener("click", async () => {
            const ctx = state.opKanbanCtx;
            if (!ctx?.opId) return;
            closeModal("modalOpKanbanOperacional");
            await openModalOpCabecalho(ctx.opId);
        });
    }

    const opBomProdutosRows = document.getElementById("opBomProdutosRows");
    if (opBomProdutosRows) {
        opBomProdutosRows.addEventListener("click", async (event) => {
            const button = event.target.closest("button[data-action='abrir-bom-op-produto']");
            if (!button) return;
            const opProdutoId = Number(button.dataset.opProdutoId || 0);
            if (!opProdutoId) return;
            try {
                await openModalOpBomDetalhe(opProdutoId);
            } catch (err) {
                setInlineError("opKanbanFeedback", getErrorMessage(err));
            }
        });
    }

    const btnVoltarBomProdutos = document.getElementById("btnVoltarBomProdutos");
    if (btnVoltarBomProdutos) {
        btnVoltarBomProdutos.addEventListener("click", () => toggleBomViews(false));
    }

    const processosRows = document.getElementById("opProcessosRows");
    if (processosRows) {
        processosRows.addEventListener("click", async (event) => {
            const button = event.target.closest("button[data-action='salvar-processo-op']");
            if (!button) return;
            const opId = Number(document.getElementById("opProcessosId")?.value || 0);
            const processoId = Number(button.dataset.processoId || 0);
            if (!opId || !processoId) return;
            try {
                const qtd = Number(document.getElementById(`opProcessoQtd_${processoId}`)?.value || 0);
                const status = document.getElementById(`opProcessoStatus_${processoId}`)?.value || "PENDENTE";
                const observacao = document.getElementById(`opProcessoObs_${processoId}`)?.value || null;
                await apiPut(`${API_OP}/${opId}/processos/${processoId}`, {
                    quantidade_concluida: qtd,
                    status,
                    observacao
                });
                await openModalOpProcessos(opId);
                await refreshKanban();
            } catch (err) {
                alert(getErrorMessage(err));
            }
        });
    }
}

async function loadKanban() {
    const data = await apiGet(API_OP_KANBAN);
    state.kanban = data && typeof data === "object" ? data : { processos: [] };
    syncFiltroOptions();
}

async function loadProdutosCatalogo() {
    const data = await apiGet(API_PRODUTOS);
    state.produtosCatalogo = Array.isArray(data) ? data : [];
    syncProdutosCatalogoSelect();
}

async function loadBasesCatalogo() {
    const data = await apiGet(API_PRODUTOS_BASES);
    state.basesCatalogo = Array.isArray(data) ? data : [];
    syncAtaOptions();
}

async function refreshKanban() {
    await loadKanban();
    renderKanban();
}

function getAllKanbanCards() {
    const processos = Array.isArray(state.kanban?.processos) ? state.kanban.processos : [];
    const flat = [];
    processos.forEach((processo) => {
        const statusRows = Array.isArray(processo.status) ? processo.status : [];
        statusRows.forEach((statusRow) => {
            const ordens = Array.isArray(statusRow.ordens) ? statusRow.ordens : [];
            ordens.forEach((ordem) => {
                flat.push({
                    ...ordem,
                    _processo_key: processo.processo_key,
                    _processo_nome: processo.processo_nome,
                    _status_key: statusRow.status_key
                });
            });
        });
    });
    return flat;
}

function syncFiltroOptions() {
    const allCards = getAllKanbanCards();
    const statusSelect = document.getElementById("filtroOpStatus");
    const empresaSelect = document.getElementById("filtroOpEmpresa");
    if (statusSelect) {
        setSelectOptions(
            statusSelect,
            "Todos os status",
            [...new Set(allCards.map((card) => card.status_op).filter(Boolean))]
        );
        statusSelect.value = state.filtros.status || "";
    }
    if (empresaSelect) {
        setSelectOptions(
            empresaSelect,
            "Todas as empresas",
            [...new Set(allCards.map((card) => card.empresa_nome).filter(Boolean))]
        );
        empresaSelect.value = state.filtros.empresa || "";
    }
}

function syncProdutosCatalogoSelect() {
    const select = document.getElementById("opProdutoCatalogo");
    if (!select) return;
    select.innerHTML = "";
    const defaultOpt = document.createElement("option");
    defaultOpt.value = "";
    defaultOpt.textContent = "Selecione um produto";
    select.appendChild(defaultOpt);

    state.produtosCatalogo.forEach((item) => {
        const option = document.createElement("option");
        option.value = String(item.id);
        option.textContent = `${item.produto_key || item.id} - ${item.nome_oficial || "-"}`;
        select.appendChild(option);
    });
    renderProdutosDisponiveisOp();
}

function syncAtaOptions() {
    const select = document.getElementById("opModeloAta");
    if (!select) return;
    const previous = select.value || "";
    select.innerHTML = "";
    const opts = [{ value: "", label: "Selecione a ATA" }, { value: "especial", label: "ESPECIAL - Todos os produtos" }];
    state.basesCatalogo
        .filter((base) => base.ativo !== false && Number(base.ativo ?? 1) !== 0)
        .forEach((base) => {
            opts.push({
                value: String(base.ata_key || ""),
                label: `${base.ata_nome || base.ata_key || "ATA"} | ${base.empresa_nome || base.empresa_key || ""}`,
                empresa: base.empresa_nome || base.empresa_key || "",
                numero_ata: base.numero_ata || ""
            });
        });
    opts.forEach((item) => {
        const opt = document.createElement("option");
        opt.value = item.value;
        opt.textContent = item.label;
        if (item.empresa) opt.dataset.empresa = item.empresa;
        if (item.numero_ata) opt.dataset.numeroAta = item.numero_ata;
        select.appendChild(opt);
    });
    if ([...select.options].some((opt) => opt.value === previous)) select.value = previous;
    syncAtaEmpresaUi();
}

function getSelectedAtaOption() {
    const select = document.getElementById("opModeloAta");
    return select?.options?.[select.selectedIndex] || null;
}

function syncAtaEmpresaUi() {
    // Empresa permanece automática no backend pela ATA selecionada; não existe campo visual para preenchimento.
}

function getProdutosFiltradosParaOp() {
    const ataKey = String(document.getElementById("opModeloAta")?.value || "").toLowerCase();
    const termo = normalizeSearchText(document.getElementById("opProdutoBusca")?.value || "");
    if (!ataKey) return [];
    return state.produtosCatalogo.filter((produto) => {
        if (!produto || produto.ativo === false) return false;
        const produtoAta = String(produto.ata_key || "").toLowerCase();
        const matchAta = ataKey === "especial" || produtoAta === ataKey;
        const hay = normalizeSearchText(`${produto.item_ata || ""} ${produto.nome_oficial || ""} ${produto.produto_key || ""} ${produto.empresa || ""}`);
        return matchAta && (!termo || hay.includes(termo));
    });
}

function renderProdutosDisponiveisOp() {
    const container = document.getElementById("opProdutoLista");
    if (!container) return;
    const ataKey = String(document.getElementById("opModeloAta")?.value || "").toLowerCase();
    if (!ataKey) {
        container.innerHTML = `<div class="op-kanban-empty op-produto-lista-vazia">Selecione uma ATA para listar os produtos.</div>`;
        renderProdutosSelecionadosOp();
        return;
    }
    const produtos = getProdutosFiltradosParaOp();
    if (!produtos.length) {
        container.innerHTML = `<div class="op-kanban-empty op-produto-lista-vazia">Nenhum produto para a ATA/filtro atual.</div>`;
        renderProdutosSelecionadosOp();
        return;
    }
    container.innerHTML = produtos.map((produto) => {
        const jaSelecionado = state.opProdutosSelecionados.some((item) => Number(item.produto_id) === Number(produto.id));
        const img = resolveProdutoImagemFonte(produto);
        const imgHtml = img ? `<img src="${escapeHtml(resolveMediaUrl(img))}" alt="" loading="lazy">` : `<div class="op-produto-card-sem-img">SEM IMAGEM</div>`;
        const ataInfo = ataKey === "especial"
            ? `<div class="op-produto-card-ata">${escapeHtml(produto.arp || produto.ata_key || "-")} | ${escapeHtml(produto.empresa || "-")}</div>`
            : "";
        return `
            <article class="op-produto-card ${jaSelecionado ? "selecionado" : ""}">
                <div class="op-produto-card-img">${imgHtml}<span>${escapeHtml(produto.item_ata || "-")}</span></div>
                <div class="op-produto-card-body">
                    <strong>${escapeHtml(produto.nome_oficial || produto.produto_key || "-")}</strong>
                    ${ataInfo}
                    <div class="op-produto-card-actions">
                        <input id="opQtdProduto_${produto.id}" type="text" inputmode="numeric" pattern="[0-9]*" value="1">
                        <button class="btn-row-action" type="button" data-action="adicionar-produto-guiado" data-produto-id="${produto.id}">${jaSelecionado ? "Atualizar" : "Adicionar"}</button>
                    </div>
                </div>
            </article>`;
    }).join("");
    renderProdutosSelecionadosOp();
}

function renderProdutosSelecionadosOp() {
    const container = document.getElementById("opProdutosSelecionados");
    if (!container) return;
    const totalItens = state.opProdutosSelecionados.length;
    const totalQtd = state.opProdutosSelecionados.reduce((acc, item) => acc + (parseQuantidadeProduto(item.quantidade) || 0), 0);
    if (!totalItens) {
        container.innerHTML = `
            <div class="op-selecionados-compacto vazio">
                <button class="op-selecionados-toggle" type="button" data-action="toggle-selecionados" aria-expanded="false">
                    <span>Itens adicionados na OP</span>
                    <strong>0 itens</strong>
                </button>
                <div class="op-selecionados-hint">Adicione produtos pela tabela abaixo após selecionar a ATA.</div>
            </div>`;
        return;
    }
    container.innerHTML = `
        <div class="op-selecionados-compacto" data-expanded="false">
            <button class="op-selecionados-toggle" type="button" data-action="toggle-selecionados" aria-expanded="false">
                <span>Itens adicionados na OP</span>
                <strong>${totalItens} item(ns) | ${totalQtd} un.</strong>
            </button>
            <div class="table-responsive op-selecionados-tabela-wrap hidden">
                <table class="preview-table sistema-table op-selecionados-tabela">
                    <thead>
                        <tr>
                            <th>ITEM</th>
                            <th>IMAGEM</th>
                            <th>PRODUTO</th>
                            <th>ATA</th>
                            <th>QTD</th>
                            <th>AÇÃO</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${state.opProdutosSelecionados.map((item) => {
                            const imgHtml = item.imagem_src
                                ? `<img src="${escapeHtml(resolveMediaUrl(item.imagem_src))}" alt="" loading="lazy">`
                                : `<span class="op-sem-img-mini">SEM IMAGEM</span>`;
                            return `
                                <tr>
                                    <td>${escapeHtml(item.item_ata || "-")}</td>
                                    <td class="op-selecionado-img">${imgHtml}</td>
                                    <td class="col-principal">${escapeHtml(item.nome_oficial || item.produto_key || "-")}</td>
                                    <td>${escapeHtml(item.ata_label || item.ata_key || "-")}</td>
                                    <td><input type="text" inputmode="numeric" pattern="[0-9]*" value="${escapeHtml(item.quantidade || 1)}" data-action="qtd-produto-guiado" data-produto-id="${item.produto_id}"></td>
                                    <td><button class="btn-row-action" type="button" data-action="remover-produto-guiado" data-produto-id="${item.produto_id}">Remover</button></td>
                                </tr>`;
                        }).join("")}
                    </tbody>
                </table>
            </div>
        </div>`;
}

function toggleProdutosSelecionados(button) {
    const box = button.closest(".op-selecionados-compacto");
    if (!box || box.classList.contains("vazio")) return;
    const wrap = box.querySelector(".op-selecionados-tabela-wrap");
    const expanded = box.dataset.expanded === "true";
    box.dataset.expanded = expanded ? "false" : "true";
    button.setAttribute("aria-expanded", expanded ? "false" : "true");
    if (wrap) wrap.classList.toggle("hidden", expanded);
}

function addProdutoSelecionadoGuiado(produtoId, quantidade) {
    if (!produtoId) return;
    const produto = state.produtosCatalogo.find((item) => Number(item.id) === Number(produtoId));
    if (!produto) return;
    const qtd = Number.isInteger(quantidade) && quantidade > 0 ? quantidade : 1;
    const current = state.opProdutosSelecionados.find((item) => Number(item.produto_id) === Number(produtoId));
    if (current) {
        current.quantidade = qtd;
    } else {
        state.opProdutosSelecionados.push({
            produto_id: Number(produto.id),
            produto_key: produto.produto_key || "",
            item_ata: produto.item_ata || "",
            nome_oficial: produto.nome_oficial || "",
            ata_key: produto.ata_key || "",
            ata_label: produto.arp || produto.ata_key || "",
            imagem_src: resolveProdutoImagemFonte(produto),
            quantidade: qtd
        });
    }
    renderProdutosDisponiveisOp();
}

function removeProdutoSelecionadoGuiado(produtoId) {
    state.opProdutosSelecionados = state.opProdutosSelecionados.filter((item) => Number(item.produto_id) !== Number(produtoId));
    renderProdutosDisponiveisOp();
}

function updateProdutoSelecionadoQtd(produtoId, quantidade) {
    const current = state.opProdutosSelecionados.find((item) => Number(item.produto_id) === Number(produtoId));
    if (current && Number.isInteger(quantidade) && quantidade > 0) current.quantidade = quantidade;
}

function resolveMediaUrl(path) {
    const raw = String(path || "").trim().replace(/\\/g, "/");
    if (!raw) return "";
    if (/^(https?:)?\/\//i.test(raw) || raw.startsWith("data:")) return raw;
    const clean = raw.replace(/^\/+/, "");
    if (clean.startsWith("media/")) return `${API_ORIGIN}/${clean}`;
    return clean;
}

function resolveProdutoImagemFonte(item) {
    if (!item || typeof item !== "object") return "";
    const imagemObj = item.imagem;
    const imagemFromObj = imagemObj && typeof imagemObj === "object"
        ? (imagemObj.preview || imagemObj.url || imagemObj.path || "")
        : "";
    const imagemRaw = item.imagem_path
        || item.produto_imagem_path
        || item.imagem_url
        || imagemFromObj
        || (typeof imagemObj === "string" ? imagemObj : "")
        || "";
    return String(imagemRaw || "").trim();
}

function clearInlineError(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = "";
    el.classList.add("hidden");
}

function setInlineError(id, message) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = message || "Falha ao processar a operação.";
    el.classList.remove("hidden");
}

function setSelectOptions(select, defaultLabel, values) {
    select.innerHTML = "";
    const defaultOpt = document.createElement("option");
    defaultOpt.value = "";
    defaultOpt.textContent = defaultLabel;
    select.appendChild(defaultOpt);

    [...values].sort().forEach((value) => {
        const opt = document.createElement("option");
        opt.value = String(value);
        opt.textContent = String(value);
        select.appendChild(opt);
    });
}

function normalizeSearchText(value) {
    return String(value || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

function applyFiltros(cards) {
    const texto = normalizeSearchText(state.filtros.texto);
    return cards.filter((card) => {
        const termo = normalizeSearchText(`${card.numero_op || ""} ${card.cliente || ""} ${card.obra || ""}`);
        const matchTexto = !texto || termo.includes(texto);
        const matchStatus = !state.filtros.status || String(card.status_op || "") === state.filtros.status;
        const matchEmpresa = !state.filtros.empresa || String(card.empresa_nome || "") === state.filtros.empresa;
        return matchTexto && matchStatus && matchEmpresa;
    });
}

function renderKanban() {
    const container = document.getElementById("opKanbanBoard");
    if (!container) return;

    const processos = Array.isArray(state.kanban?.processos) ? state.kanban.processos : [];
    if (!processos.length) {
        container.innerHTML = `<div class="op-kanban-empty">Nenhuma OP disponivel para o Kanban.</div>`;
        updateContador(0, 0);
        return;
    }

    const allCards = getAllKanbanCards();
    const filtered = applyFiltros(allCards);
    const allowedIds = new Set(filtered.map((item) => Number(item.id || 0)));

    const html = processos.map((processo) => renderKanbanProcess(processo, allowedIds)).join("");
    container.innerHTML = html || `<div class="op-kanban-empty">Nenhuma OP encontrada com os filtros atuais.</div>`;

    updateContador(filtered.length, allCards.length);
}

function renderKanbanProcess(processo, allowedIds) {
    const statusRows = Array.isArray(processo.status) ? processo.status : [];
    let totalProcesso = 0;

    const statusHtml = statusRows.map((statusRow) => {
        const rawCards = Array.isArray(statusRow.ordens) ? statusRow.ordens : [];
        const cards = rawCards.filter((card) => allowedIds.has(Number(card.id || 0)));
        totalProcesso += cards.length;

        const cardsHtml = cards.length
            ? cards.map((card) => renderCard(card)).join("")
            : `<div class="op-kanban-empty">Sem cards</div>`;

        return `
            <div class="op-kanban-status-row" data-status="${escapeHtml(statusRow.status_key || "")}">
                <div class="op-kanban-status-label">${escapeHtml(statusRow.status_nome || "-")}</div>
                <div class="op-kanban-cards-row">
                    ${cardsHtml}
                </div>
            </div>
        `;
    }).join("");

    return `
        <section class="op-kanban-process" data-processo-key="${escapeHtml(processo.processo_key || "")}">
            <header class="op-kanban-process-header">
                <h3>${escapeHtml(processo.processo_nome || "-")}</h3>
                <span class="op-kanban-process-count">${totalProcesso} OP(s)</span>
            </header>
            ${statusHtml}
        </section>
    `;
}

function renderCard(card) {
    const prazoClass = getPrazoClass(card.prazo_status);
    const entrega = card.data_entrega_valor || "NAO DEFINIDO";
    const prazo = card.prazo_label ? `<div class="op-card-prazo ${prazoClass}">${escapeHtml(card.prazo_label)}</div>` : "";
    const statusLabel = getStatusLabel(card.status_processo_macro);
    const statusClass = getStatusClass(card.status_processo_macro);

    return `
        <article class="op-kanban-card" data-op-id="${Number(card.id || 0)}">
            <div class="op-card-header">
                <div class="op-card-numero">OP ${escapeHtml(card.numero_op || "-")}</div>
                <button class="op-card-menu-btn" type="button" aria-label="Ações" data-action="menu-toggle" data-op-id="${card.id}">⋯</button>
            </div>
            <div class="op-card-cliente">${escapeHtml(card.cliente || "-")}</div>
            <div class="op-card-obra">${escapeHtml(card.obra || "-")}</div>
            <div class="op-card-entrega">Entrega: ${escapeHtml(entrega)}</div>
            ${prazo}
            <span class="op-card-status-pill ${statusClass}">${escapeHtml(statusLabel)}</span>
        </article>
    `;
}

function getPrazoClass(prazoStatus) {
    if (prazoStatus === "ok") return "op-prazo-ok";
    if (prazoStatus === "hoje") return "op-prazo-hoje";
    if (prazoStatus === "atrasado") return "op-prazo-atrasado";
    return "op-prazo-indefinido";
}

function getStatusLabel(statusKey) {
    if (statusKey === "EM_ANDAMENTO") return "Em Andamento";
    if (statusKey === "CONCLUIDO") return "Concluído";
    return "Não Iniciado";
}

function getStatusClass(statusKey) {
    if (statusKey === "EM_ANDAMENTO") return "status-em-andamento";
    if (statusKey === "CONCLUIDO") return "status-concluido";
    return "status-nao-iniciado";
}


async function handleOpAction(action, opId) {
    if (action === "abrir" || action === "produtos") {
        await openModalOpProdutos(opId);
    } else if (action === "editar") {
        await openModalOpCabecalho(opId);
    } else if (action === "bom") {
        await openModalOpBom(opId);
    } else if (action === "processos") {
        await openModalOpProcessos(opId);
    } else if (action === "historico") {
        await openModalOpHistorico(opId);
    } else if (action === "cancelar-op") {
        await cancelarOp(opId);
    }
}

let resolverCancelamentoOp = null;
let opCancelamentoPendente = 0;

function confirmarCancelamentoOp(opId) {
    opCancelamentoPendente = Number(opId || 0);
    const mensagem = document.getElementById("opCancelarMensagem");
    if (mensagem) mensagem.textContent = `Cancelar a OP ${opCancelamentoPendente}? Ela sairá do Kanban ativo e ficará registrada como CANCELADA.`;
    openModal("modalOpCancelarConfirm");
    return new Promise((resolve) => {
        resolverCancelamentoOp = resolve;
    });
}

function resolverConfirmacaoCancelamento(confirmado) {
    closeModal("modalOpCancelarConfirm");
    const resolver = resolverCancelamentoOp;
    resolverCancelamentoOp = null;
    opCancelamentoPendente = 0;
    if (typeof resolver === "function") resolver(Boolean(confirmado));
}

function getProcessoNomeByKey(processoKey) {
    const raw = String(processoKey || "").trim().toLowerCase();
    const found = PROCESSOS_OP_OPTIONS.find((item) => item.key === raw);
    return found?.nome || raw || "-";
}

function getKanbanStatusFromCard(card) {
    const value = String(card?._status_key || card?.status_processo_macro || "").trim().toUpperCase();
    return STATUS_KANBAN_OPTIONS.includes(value) ? value : "NAO_INICIADO";
}

function getKanbanStatusLabel(statusKey) {
    if (statusKey === "EM_ANDAMENTO") return "Em Andamento";
    if (statusKey === "CONCLUIDO") return "Concluído";
    return "Não Iniciado";
}

function openModalOpPularEtapa(opId, processoOrigem) {
    const processoAtual = String(processoOrigem || "").trim().toLowerCase();
    state.opPularCtx = { opId: Number(opId), processoOrigem: processoAtual };
    const resumo = document.getElementById("opPularResumo");
    const inputAtual = document.getElementById("opPularProcessoAtual");
    const selectDestino = document.getElementById("opPularProcessoDestino");
    if (resumo) resumo.textContent = `Selecione a próxima etapa da OP ${opId}.`;
    if (inputAtual) inputAtual.value = getProcessoNomeByKey(processoAtual);
    if (selectDestino) {
        selectDestino.innerHTML = "";
        PROCESSOS_OP_OPTIONS
            .filter((item) => item.key !== processoAtual)
            .forEach((item) => {
                const opt = document.createElement("option");
                opt.value = item.key;
                opt.textContent = item.nome;
                selectDestino.appendChild(opt);
            });
    }
    clearInlineError("opPularErro");
    openModal("modalOpPularProcesso");
}

async function confirmPularEtapaModal() {
    const ctx = state.opPularCtx;
    if (!ctx?.opId || !ctx?.processoOrigem) return;
    const selectDestino = document.getElementById("opPularProcessoDestino");
    const processoDestino = String(selectDestino?.value || "").trim().toLowerCase();
    if (!processoDestino) {
        setInlineError("opPularErro", "Selecione a próxima etapa.");
        return;
    }
    if (processoDestino === ctx.processoOrigem) {
        setInlineError("opPularErro", "A próxima etapa deve ser diferente da etapa atual.");
        return;
    }
    try {
        clearInlineError("opPularErro");
        await apiPost(`${API_OP}/${ctx.opId}/kanban/pular`, {
            processo_origem: ctx.processoOrigem,
            processo_destino: processoDestino,
            status_destino: "NAO_INICIADO",
        });
        closeModal("modalOpPularProcesso");
        await refreshKanban();
        await openModalOpKanbanOperacional(ctx.opId);
    } catch (err) {
        setInlineError("opPularErro", getErrorMessage(err));
    }
}

async function setKanbanStatus(opId, statusDestino, processoKey = null) {
    const payload = { status_destino: statusDestino };
    if (processoKey) payload.processo_key = String(processoKey).toLowerCase();
    await apiPost(`${API_OP}/${opId}/kanban/status`, payload);
}

async function cancelarOp(opId) {
    const confirmado = await confirmarCancelamentoOp(opId);
    if (!confirmado) return;
    try {
        await apiDelete(`${API_OP}/${opId}`);
        await refreshKanban();
    } catch (err) {
        setInlineError("opKanbanFeedback", getErrorMessage(err));
    }
}

function updateContador(exibidos, total) {
    const contador = document.getElementById("opContador");
    if (!contador) return;
    contador.textContent = exibidos
        ? `Exibindo ${exibidos} de ${total} ordens no Kanban`
        : "0 ordens encontradas no Kanban";
}

function openModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modal.classList.remove("hidden");
    modal.setAttribute("aria-hidden", "false");
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (!modal) return;
    modal.classList.add("hidden");
    modal.setAttribute("aria-hidden", "true");
}

async function openModalOpProcessos(opId) {
    document.getElementById("opProcessosId").value = String(opId);
    const rows = await apiGet(`${API_OP}/${opId}/processos`);
    const tbody = document.getElementById("opProcessosRows");
    if (!tbody) return;
    tbody.innerHTML = "";
    const list = Array.isArray(rows) ? rows : [];
    if (!list.length) {
        tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="7" class="sistema-empty-msg">Nenhum processo registrado.</td></tr>`;
    } else {
        list.forEach((item) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td class="col-principal">${escapeHtml(item.nome_produto || "-")}</td>
                <td class="col-meta-2">${escapeHtml(item.processo_nome || "-")}</td>
                <td class="col-meta-2">${escapeHtml(item.quantidade_planejada || 0)}</td>
                <td class="col-meta-2"><input id="opProcessoQtd_${item.id}" type="number" min="0" step="0.01" value="${escapeHtml(item.quantidade_concluida || 0)}"></td>
                <td class="col-meta-2">${escapeHtml(item.quantidade_falta || 0)}</td>
                <td class="col-meta-2">
                    <select id="opProcessoStatus_${item.id}">
                        ${buildStatusProcessoOptions(item.status)}
                    </select>
                    <input id="opProcessoObs_${item.id}" type="text" value="${escapeHtml(item.observacao || "")}" placeholder="Observacao">
                </td>
                <td class="col-acao">
                    <button class="btn-row-action" type="button" data-action="salvar-processo-op" data-processo-id="${item.id}">Salvar</button>
                </td>
            `;
            tbody.appendChild(tr);
        });
    }
    openModal("modalOpProcessos");
}

function buildStatusProcessoOptions(selected) {
    return STATUS_PROCESSO_OPTIONS
        .map((value) => `<option value="${value}" ${value === selected ? "selected" : ""}>${value}</option>`)
        .join("");
}

async function openModalOpHistorico(opId) {
    document.getElementById("opHistoricoId").value = String(opId);
    const rows = await apiGet(`${API_OP}/${opId}/historico`);
    const tbody = document.getElementById("opHistoricoRows");
    if (!tbody) return;
    tbody.innerHTML = "";
    const list = Array.isArray(rows) ? rows : [];
    if (!list.length) {
        tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="4" class="sistema-empty-msg">Sem historico para esta OP.</td></tr>`;
    } else {
        list.forEach((item) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td class="col-meta-2">${escapeHtml(formatDateTime(item.created_at))}</td>
                <td class="col-meta-2">${escapeHtml(item.acao || "-")}</td>
                <td class="col-meta-2">${escapeHtml(item.entidade || "-")}</td>
                <td class="col-principal">${escapeHtml(item.detalhe || "-")}</td>
            `;
            tbody.appendChild(tr);
        });
    }
    openModal("modalOpHistorico");
}

function toggleBomViews(showDetalhe) {
    const produtosView = document.getElementById("opBomProdutosView");
    const detalheView = document.getElementById("opBomDetalheView");
    const btnVoltar = document.getElementById("btnVoltarBomProdutos");
    if (produtosView) produtosView.classList.toggle("hidden", Boolean(showDetalhe));
    if (detalheView) detalheView.classList.toggle("hidden", !showDetalhe);
    if (btnVoltar) btnVoltar.classList.toggle("hidden", !showDetalhe);
}

async function saveKanbanProdutoQuantidade(opProdutoId, inputElement) {
    const ctx = state.opKanbanCtx;
    if (!ctx?.opId) return;
    sanitizeQuantidadeProdutoInput(inputElement);
    const quantidade = parseQuantidadeProduto(inputElement?.value);
    if (quantidade === null) {
        setInlineError("opKanbanErro", "Quantidade deve ser inteiro positivo.");
        if (inputElement) inputElement.value = String(inputElement.dataset.previousValue || "1");
        return;
    }
    clearInlineError("opKanbanErro");
    await apiPut(`${API_OP}/${ctx.opId}/produtos/${opProdutoId}`, { quantidade });
    await refreshKanban();
    await openModalOpKanbanOperacional(ctx.opId);
}

async function renderOpKanbanProdutos(opId) {
    const tbody = document.getElementById("opKanbanProdutosRows");
    if (!tbody) return;
    const detail = await apiGet(`${API_OP}/${opId}`);
    const rows = Array.isArray(detail?.produtos) ? detail.produtos : [];
    tbody.innerHTML = "";
    if (!rows.length) {
        tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="5" class="sistema-empty-msg">Nenhum produto vinculado nesta OP.</td></tr>`;
        return;
    }
    rows.forEach((item) => {
        const imgSource = resolveProdutoImagemFonte(item);
        const imgHtml = imgSource
            ? `<img src="${escapeHtml(resolveMediaUrl(imgSource))}" alt="" loading="lazy">`
            : `<span class="op-sem-img-mini">SEM IMAGEM</span>`;
        const quantidade = parseQuantidadeProduto(item.quantidade) || 1;
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="op-kanban-produto-img">${imgHtml}</td>
            <td>${escapeHtml(item.item_ata || "-")}</td>
            <td class="col-principal">${escapeHtml(item.nome_produto || item.produto_key || "-")}</td>
            <td>${escapeHtml(item.ata_nome || item.ata_key || "-")}</td>
            <td>
                <input
                    type="text"
                    inputmode="numeric"
                    pattern="[0-9]*"
                    value="${escapeHtml(quantidade)}"
                    data-action="qtd-op-kanban"
                    data-op-produto-id="${Number(item.id || 0)}"
                    data-previous-value="${escapeHtml(quantidade)}"
                >
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function openModalOpKanbanOperacional(opId) {
    const card = getAllKanbanCards().find((item) => Number(item.id || 0) === Number(opId));
    if (!card) throw new Error("OP nao encontrada no Kanban.");
    const processoKey = String(card._processo_key || card.processo_macro_key || "corte").toLowerCase();
    state.opKanbanCtx = { opId: Number(opId), processoKey };

    const titulo = document.getElementById("opKanbanTitulo");
    const resumo = document.getElementById("opKanbanResumo");
    const processoAtual = document.getElementById("opKanbanProcessoAtual");
    const statusSelect = document.getElementById("opCardStatusSelect");
    if (titulo) titulo.textContent = `Operacao da OP ${card.numero_op || opId}`;
    if (resumo) resumo.textContent = `${card.cliente || "-"} | ${card.obra || "-"} | Entrega: ${card.data_entrega_valor || "NAO DEFINIDO"}`;
    if (processoAtual) processoAtual.textContent = `Processo atual: ${getProcessoNomeByKey(processoKey)}`;
    if (statusSelect) statusSelect.value = getKanbanStatusFromCard(card);
    clearInlineError("opKanbanErro");
    await renderOpKanbanProdutos(opId);
    openModal("modalOpKanbanOperacional");
}

function mapOpProdutoToSelecionado(item) {
    return {
        op_produto_id: Number(item.id || 0),
        produto_id: Number(item.produto_id || 0),
        produto_key: item.produto_key || "",
        item_ata: item.item_ata || "",
        nome_oficial: item.nome_produto || item.produto_key || "",
        ata_key: item.ata_key || "",
        ata_label: item.ata_nome || item.ata_key || "",
        imagem_src: resolveProdutoImagemFonte(item),
        quantidade: parseQuantidadeProduto(item.quantidade) || 1,
    };
}

async function openModalOpCabecalho(opId = null) {
    clearModalOpCabecalho();
    const btnSalvar = document.getElementById("btnSalvarOp");
    if (btnSalvar) btnSalvar.textContent = opId ? "Salvar alteracoes" : "Salvar OP";

    if (opId) {
        const detail = await apiGet(`${API_OP}/${opId}`);
        const cabecalho = detail?.cabecalho || {};
        const produtos = Array.isArray(detail?.produtos) ? detail.produtos : [];
        document.getElementById("tituloModalOp").textContent = `Editar OP ${cabecalho.numero_op || opId}`;
        document.getElementById("opId").value = String(opId);
        document.getElementById("opCliente").value = cabecalho.cliente || "";
        document.getElementById("opObra").value = cabecalho.obra || "";
        document.getElementById("opSolicitante").value = cabecalho.solicitante || "";
        document.getElementById("opStatus").value = cabecalho.status || "RASCUNHO";
        document.getElementById("opDataEntregaInput").value = cabecalho.data_entrega_valor || "NAO DEFINIDO";
        document.getElementById("opObservacoes").value = cabecalho.observacoes || "";
        syncAtaOptions();
        const ataSelect = document.getElementById("opModeloAta");
        if (ataSelect && cabecalho.ata_key) ataSelect.value = cabecalho.ata_key;
        state.opProdutosSelecionados = produtos.map(mapOpProdutoToSelecionado);
        state.opProdutosOriginais = state.opProdutosSelecionados.map((item) => ({
            op_produto_id: Number(item.op_produto_id || 0),
            produto_id: Number(item.produto_id || 0),
            quantidade: parseQuantidadeProduto(item.quantidade) || 1,
        }));
    }

    document.getElementById("opBlocoProdutosGuiados")?.classList.remove("hidden");
    clearInlineError("opCabecalhoErro");
    syncAtaEmpresaUi();
    renderProdutosDisponiveisOp();
    openModal("modalOpCabecalho");
}

function clearModalOpCabecalho() {
    document.getElementById("tituloModalOp").textContent = "Nova OP";
    document.getElementById("opId").value = "";
    document.getElementById("opCliente").value = "";
    document.getElementById("opObra").value = "";
    document.getElementById("opSolicitante").value = "";
    document.getElementById("opStatus").value = "RASCUNHO";
    document.getElementById("opDataEntregaInput").value = "NAO DEFINIDO";
    document.getElementById("opObservacoes").value = "";
    const ata = document.getElementById("opModeloAta");
    if (ata) ata.value = "";
    const busca = document.getElementById("opProdutoBusca");
    if (busca) busca.value = "";
    state.opProdutosSelecionados = [];
    state.opProdutosOriginais = [];
    document.getElementById("opBlocoProdutosGuiados")?.classList.remove("hidden");
    clearInlineError("opCabecalhoErro");
    syncAtaEmpresaUi();
    renderProdutosSelecionadosOp();
}

async function sincronizarProdutosEdicaoOp(opId) {
    const selecionados = state.opProdutosSelecionados.map((item) => ({
        op_produto_id: Number(item.op_produto_id || 0),
        produto_id: Number(item.produto_id || 0),
        quantidade: parseQuantidadeProduto(item.quantidade),
    }));
    const invalid = selecionados.find((item) => item.quantidade === null || item.produto_id <= 0);
    if (invalid) throw new Error("Todos os itens da OP devem ter quantidade inteira positiva.");

    const originais = Array.isArray(state.opProdutosOriginais) ? state.opProdutosOriginais : [];
    const originalById = new Map(
        originais
            .filter((item) => Number(item.op_produto_id || 0) > 0)
            .map((item) => [Number(item.op_produto_id), parseQuantidadeProduto(item.quantidade) || 1])
    );

    const selecionadosOriginais = new Set();
    for (const item of selecionados) {
        if (item.op_produto_id > 0) {
            selecionadosOriginais.add(item.op_produto_id);
            const qtdOriginal = originalById.get(item.op_produto_id);
            if (qtdOriginal !== item.quantidade) {
                await apiPut(`${API_OP}/${opId}/produtos/${item.op_produto_id}`, { quantidade: item.quantidade });
            }
            continue;
        }
        await apiPost(`${API_OP}/${opId}/produtos`, { produto_id: item.produto_id, quantidade: item.quantidade });
    }

    for (const original of originais) {
        const opProdutoId = Number(original.op_produto_id || 0);
        if (opProdutoId > 0 && !selecionadosOriginais.has(opProdutoId)) {
            await apiDelete(`${API_OP}/${opId}/produtos/${opProdutoId}`);
        }
    }
}

async function saveModalOpCabecalho() {
    try {
        clearInlineError("opCabecalhoErro");
        const opId = Number(document.getElementById("opId").value || 0);
        const ataSelect = document.getElementById("opModeloAta");
        const selectedAtaOption = getSelectedAtaOption();
        const payload = {
            cliente: fieldValue("opCliente"),
            obra: fieldValue("opObra"),
            solicitante: fieldValue("opSolicitante"),
            status: fieldValue("opStatus") || "RASCUNHO",
            data_entrega_input: fieldValue("opDataEntregaInput") || "NAO DEFINIDO",
            observacoes: fieldValue("opObservacoes"),
            ata_key: ataSelect?.value || null,
            ata_nome: selectedAtaOption?.textContent?.split("|")[0]?.replace("ESPECIAL - Todos os produtos", "ESPECIAL")?.trim() || null,
            numero_ata: selectedAtaOption?.dataset?.numeroAta || null,
        };

        if (!payload.ata_key) throw new Error("Selecione o MODELO ATA.");
        if (!state.opProdutosSelecionados.length) throw new Error("Selecione ao menos um item/aparelho.");

        if (opId) {
            await apiPut(`${API_OP}/${opId}`, payload);
            await sincronizarProdutosEdicaoOp(opId);
        } else {
            const payloadCreate = {
                ...payload,
                produtos: state.opProdutosSelecionados.map((item) => ({
                    produto_id: Number(item.produto_id),
                    quantidade: parseQuantidadeProduto(item.quantidade) || 1,
                })),
            };
            await apiPost(API_OP, payloadCreate);
        }

        closeModal("modalOpCabecalho");
        await refreshKanban();
        if (opId) await openModalOpKanbanOperacional(opId);
    } catch (err) {
        setInlineError("opCabecalhoErro", getErrorMessage(err));
    }
}

async function openModalOpProdutos(opId) {
    document.getElementById("opProdutosId").value = String(opId);
    await refreshModalProdutos(opId);
    openModal("modalOpProdutos");
}

async function refreshModalProdutos(opId) {
    const detail = await apiGet(`${API_OP}/${opId}`);
    const rows = Array.isArray(detail?.produtos) ? detail.produtos : [];
    const tbody = document.getElementById("opProdutosRows");
    if (!tbody) return;
    tbody.innerHTML = "";
    if (!rows.length) {
        tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="6" class="sistema-empty-msg">Nenhum produto vinculado nesta OP.</td></tr>`;
        return;
    }
    rows.forEach((item) => {
        const imgSource = resolveProdutoImagemFonte(item);
        const imgHtml = imgSource
            ? `<img src="${escapeHtml(resolveMediaUrl(imgSource))}" alt="" loading="lazy">`
            : `<span class="op-sem-img-mini">SEM IMAGEM</span>`;
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="op-kanban-produto-img">${imgHtml}</td>
            <td>${escapeHtml(item.item_ata || "-")}</td>
            <td class="col-principal">${escapeHtml(item.nome_produto || item.produto_key || "-")}</td>
            <td>${escapeHtml(item.ata_nome || item.ata_key || "-")}</td>
            <td>${escapeHtml(parseQuantidadeProduto(item.quantidade) || 1)}</td>
            <td>-</td>
        `;
        tbody.appendChild(tr);
    });
}

async function openModalOpBom(opId) {
    const detail = await apiGet(`${API_OP}/${opId}`);
    const produtos = Array.isArray(detail?.produtos) ? detail.produtos : [];
    state.opBomCtx = { opId, produtos, bomRows: null };
    document.getElementById("opBomId").value = String(opId);
    const resumo = document.getElementById("opBomResumo");
    const cabecalho = detail?.cabecalho || {};
    if (resumo) resumo.textContent = `OP ${cabecalho.numero_op || opId} | ${cabecalho.cliente || "-"} | ${cabecalho.obra || "-"}`;

    const tbody = document.getElementById("opBomProdutosRows");
    if (tbody) {
        tbody.innerHTML = "";
        if (!produtos.length) {
            tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="6" class="sistema-empty-msg">Nenhum aparelho vinculado nesta OP.</td></tr>`;
        } else {
            produtos.forEach((item) => {
                const imgSource = resolveProdutoImagemFonte(item);
                const imgHtml = imgSource
                    ? `<img src="${escapeHtml(resolveMediaUrl(imgSource))}" alt="" loading="lazy">`
                    : `<span class="op-sem-img-mini">SEM IMAGEM</span>`;
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td class="op-kanban-produto-img">${imgHtml}</td>
                    <td>${escapeHtml(item.item_ata || "-")}</td>
                    <td class="col-principal">${escapeHtml(item.nome_produto || item.produto_key || "-")}</td>
                    <td>${escapeHtml(item.ata_nome || item.ata_key || "-")}</td>
                    <td>${escapeHtml(parseQuantidadeProduto(item.quantidade) || 1)}</td>
                    <td><button class="btn-row-action" type="button" data-action="abrir-bom-op-produto" data-op-produto-id="${Number(item.id || 0)}">Ver BOM</button></td>
                `;
                tbody.appendChild(tr);
            });
        }
    }

    toggleBomViews(false);
    openModal("modalOpBom");
}

async function openModalOpBomDetalhe(opProdutoId) {
    const ctx = state.opBomCtx;
    if (!ctx?.opId) throw new Error("Contexto da BOM nao carregado.");
    if (!Array.isArray(ctx.bomRows)) {
        ctx.bomRows = await apiGet(`${API_OP}/${ctx.opId}/bom`);
    }
    const produto = (ctx.produtos || []).find((item) => Number(item.id || 0) === Number(opProdutoId));
    const qtdProduto = parseQuantidadeProduto(produto?.quantidade) || 1;
    const titulo = document.getElementById("opBomDetalheTitulo");
    if (titulo) titulo.textContent = `BOM detalhada - ${produto?.nome_produto || produto?.produto_key || "Produto"}`;

    const tbody = document.getElementById("opBomRows");
    if (!tbody) return;
    const rows = (Array.isArray(ctx.bomRows) ? ctx.bomRows : []).filter((item) => Number(item.op_produto_id || 0) === Number(opProdutoId));
    tbody.innerHTML = "";
    if (!rows.length) {
        tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="6" class="sistema-empty-msg">Sem itens de BOM para este aparelho.</td></tr>`;
    } else {
        rows.forEach((item) => {
            const qtdUnit = Number(item.quantidade_unitaria);
            const qtdOp = Number(item.quantidade_produto);
            const total = Number.isFinite(qtdUnit) && Number.isFinite(qtdOp) ? (qtdUnit * qtdOp) : item.quantidade_total;
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${escapeHtml(item.cod || "-")}</td>
                <td class="col-principal">${escapeHtml(item.material || "-")}</td>
                <td>${escapeHtml(item.unidade || "-")}</td>
                <td>${escapeHtml(item.quantidade_unitaria ?? "-")}</td>
                <td>${escapeHtml(qtdProduto)}</td>
                <td>${escapeHtml(total ?? "-")}</td>
            `;
            tbody.appendChild(tr);
        });
    }
    toggleBomViews(true);
}

function openModalOpAcoesCard(cardElement) {
    if (!cardElement) return;
    const opId = Number(cardElement.dataset.opId || 0);
    if (!opId) return;
    const card = getAllKanbanCards().find((item) => Number(item.id || 0) === opId) || {};
    const titulo = document.getElementById("opAcoesTitulo");
    const resumo = document.getElementById("opAcoesResumo");
    const body = document.getElementById("opAcoesCardBody");
    clearInlineError("opAcoesErro");
    if (titulo) titulo.textContent = `OP ${card.numero_op || opId}`;
    if (resumo) resumo.textContent = `${card.cliente || "-"} | ${card.obra || "-"} | Entrega: ${card.data_entrega_valor || "NAO DEFINIDO"}`;
    if (body) {
        body.innerHTML = `
            <table class="preview-table sistema-table op-acoes-table">
                <tbody>
                    <tr><th>OP</th><td>${escapeHtml(card.numero_op || "-")}</td><th>Status</th><td>${escapeHtml(getStatusLabel(card.status_processo_macro))}</td></tr>
                    <tr><th>Cliente</th><td>${escapeHtml(card.cliente || "-")}</td><th>Obra</th><td>${escapeHtml(card.obra || "-")}</td></tr>
                    <tr><th>Empresa</th><td>${escapeHtml(card.empresa_nome || "-")}</td><th>Entrega</th><td>${escapeHtml(card.data_entrega_valor || "NAO DEFINIDO")}</td></tr>
                    <tr><th>Processo</th><td>${escapeHtml(card._processo_nome || "-")}</td><th>Prazo</th><td>${escapeHtml(card.prazo_label || "-")}</td></tr>
                </tbody>
            </table>
            <div class="op-acoes-grupo">
                <h4>Consultas administrativas</h4>
                <div class="op-acoes-grid">
                    <button class="btn-row-action" type="button" data-action="abrir" data-op-id="${opId}">Produtos da OP</button>
                    <button class="btn-row-action" type="button" data-action="bom" data-op-id="${opId}">BOM</button>
                    <button class="btn-row-action" type="button" data-action="processos" data-op-id="${opId}">Processos</button>
                    <button class="btn-row-action" type="button" data-action="historico" data-op-id="${opId}">Historico</button>
                </div>
            </div>
            <div class="op-acoes-danger-zone">
                <button class="btn-row-action op-btn-danger" type="button" data-action="cancelar-op" data-op-id="${opId}">Cancelar OP</button>
            </div>`;
    }
    openModal("modalOpAcoesCard");
}

function fieldValue(id) {
    const element = document.getElementById(id);
    return element ? (element.value || "").trim() : "";
}

function formatDateTime(value) {
    if (!value) return "-";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return String(value);
    const dd = String(date.getDate()).padStart(2, "0");
    const mm = String(date.getMonth() + 1).padStart(2, "0");
    const yyyy = String(date.getFullYear());
    const hh = String(date.getHours()).padStart(2, "0");
    const min = String(date.getMinutes()).padStart(2, "0");
    return `${dd}/${mm}/${yyyy} ${hh}:${min}`;
}

function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function getErrorMessage(error) {
    const fallback = "Falha ao processar a operacao.";
    if (!error) return fallback;
    if (typeof error === "string") return error;
    if (error.message) return error.message;
    return fallback;
}

async function apiGet(url) {
    return request(url, { method: "GET" });
}

async function apiPost(url, body) {
    return request(url, { method: "POST", body });
}

async function apiPut(url, body) {
    return request(url, { method: "PUT", body });
}

async function apiDelete(url) {
    return request(url, { method: "DELETE" });
}

async function request(url, { method, body } = {}) {
    const response = await fetch(url, {
        method: method || "GET",
        headers: { "Content-Type": "application/json" },
        body: body ? JSON.stringify(body) : undefined
    });
    let payload = null;
    try {
        payload = await response.json();
    } catch {
        payload = null;
    }
    if (!response.ok || !payload || payload.ok !== true) {
        const detail = payload?.detail?.error?.message || payload?.error?.message || payload?.detail || response.statusText;
        throw new Error(detail || "Erro de integracao com backend.");
    }
    return payload.data;
}
