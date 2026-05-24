const API_HOST = window.location.hostname || "127.0.0.1";
const API_PROTOCOL = window.location.protocol === "http:" || window.location.protocol === "https:" ? window.location.protocol : "http:";
const API_ORIGIN = `${API_PROTOCOL}//${API_HOST}:8876`;
const API_OP = `${API_ORIGIN}/api/ordens-producao`;
const API_PRODUTOS = `${API_ORIGIN}/api/produtos`;

const state = {
    ordens: [],
    produtosCatalogo: [],
    filtros: { texto: "", status: "", empresa: "" }
};

export async function init() {
    bindBaseEvents();
    await Promise.all([loadOrdens(), loadProdutosCatalogo()]);
    renderOrdens();
}

function bindBaseEvents() {
    const btnNovaOp = document.getElementById("btnNovaOp");
    const filtroTexto = document.getElementById("filtroOpTexto");
    const filtroStatus = document.getElementById("filtroOpStatus");
    const filtroEmpresa = document.getElementById("filtroOpEmpresa");
    const btnLimpar = document.getElementById("btnLimparFiltrosOp");
    const tabela = document.getElementById("tblOrdensProducao");

    if (btnNovaOp) btnNovaOp.addEventListener("click", () => openModalOpCabecalho());
    if (filtroTexto) {
        filtroTexto.addEventListener("input", (event) => {
            state.filtros.texto = event.target.value || "";
            renderOrdens();
        });
    }
    if (filtroStatus) {
        filtroStatus.addEventListener("change", (event) => {
            state.filtros.status = event.target.value || "";
            renderOrdens();
        });
    }
    if (filtroEmpresa) {
        filtroEmpresa.addEventListener("change", (event) => {
            state.filtros.empresa = event.target.value || "";
            renderOrdens();
        });
    }
    if (btnLimpar) {
        btnLimpar.addEventListener("click", () => {
            state.filtros = { texto: "", status: "", empresa: "" };
            if (filtroTexto) filtroTexto.value = "";
            if (filtroStatus) filtroStatus.value = "";
            if (filtroEmpresa) filtroEmpresa.value = "";
            renderOrdens();
        });
    }

    if (tabela) {
        tabela.addEventListener("click", async (event) => {
            const button = event.target.closest("button[data-action]");
            if (!button) return;
            const action = button.dataset.action;
            const opId = Number(button.dataset.opId || 0);
            if (!action || !opId) return;
            try {
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
                }
            } catch (err) {
                alert(getErrorMessage(err));
            }
        });
    }

    bindModalEvents();
}

function bindModalEvents() {
    document.querySelectorAll("[data-close-modal]").forEach((button) => {
        button.addEventListener("click", () => closeModal(button.getAttribute("data-close-modal")));
    });

    const opEntregaTipo = document.getElementById("opEntregaTipo");
    if (opEntregaTipo) opEntregaTipo.addEventListener("change", syncEntregaTipoUi);

    const btnSalvarOp = document.getElementById("btnSalvarOp");
    if (btnSalvarOp) btnSalvarOp.addEventListener("click", saveModalOpCabecalho);

    const btnAdicionarProduto = document.getElementById("btnAdicionarProdutoOp");
    if (btnAdicionarProduto) btnAdicionarProduto.addEventListener("click", addProdutoNaOpAtual);

    const btnSalvarBom = document.getElementById("btnSalvarBomOp");
    if (btnSalvarBom) btnSalvarBom.addEventListener("click", saveBomDaOpAtual);

    const produtosRows = document.getElementById("opProdutosRows");
    if (produtosRows) {
        produtosRows.addEventListener("click", async (event) => {
            const button = event.target.closest("button[data-action]");
            if (!button) return;
            const action = button.dataset.action;
            const opId = Number(document.getElementById("opProdutosId")?.value || 0);
            const opProdutoId = Number(button.dataset.opProdutoId || 0);
            if (!opId || !opProdutoId) return;
            try {
                if (action === "salvar-produto-op") {
                    const qtyInput = document.getElementById(`opProdutoQtd_${opProdutoId}`);
                    const quantidade = Number(qtyInput?.value || 0);
                    await apiPut(`${API_OP}/${opId}/produtos/${opProdutoId}`, { quantidade });
                    await refreshModalProdutos(opId);
                    await refreshOrdens();
                } else if (action === "remover-produto-op") {
                    const ok = window.confirm("Remover este produto da OP?");
                    if (!ok) return;
                    await apiDelete(`${API_OP}/${opId}/produtos/${opProdutoId}`);
                    await refreshModalProdutos(opId);
                    await refreshOrdens();
                }
            } catch (err) {
                alert(getErrorMessage(err));
            }
        });
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
            } catch (err) {
                alert(getErrorMessage(err));
            }
        });
    }
}

async function loadOrdens() {
    const data = await apiGet(API_OP);
    state.ordens = Array.isArray(data) ? data : [];
    syncFiltroOptions();
}

async function loadProdutosCatalogo() {
    const data = await apiGet(API_PRODUTOS);
    state.produtosCatalogo = Array.isArray(data) ? data : [];
    syncProdutosCatalogoSelect();
}

function syncFiltroOptions() {
    const statusSelect = document.getElementById("filtroOpStatus");
    const empresaSelect = document.getElementById("filtroOpEmpresa");
    if (statusSelect) {
        setSelectOptions(
            statusSelect,
            "Todos os status",
            [...new Set(state.ordens.map((row) => row.status).filter(Boolean))]
        );
        statusSelect.value = state.filtros.status || "";
    }
    if (empresaSelect) {
        setSelectOptions(
            empresaSelect,
            "Todas as empresas",
            [...new Set(state.ordens.map((row) => row.empresa_nome).filter(Boolean))]
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

function applyFiltros(ordens) {
    const texto = normalizeSearchText(state.filtros.texto);
    return ordens.filter((row) => {
        const termo = normalizeSearchText(
            `${row.numero_op || ""} ${row.cliente || ""} ${row.obra || ""} ${row.status || ""} ${row.empresa_nome || ""}`
        );
        const matchTexto = !texto || termo.includes(texto);
        const matchStatus = !state.filtros.status || row.status === state.filtros.status;
        const matchEmpresa = !state.filtros.empresa || row.empresa_nome === state.filtros.empresa;
        return matchTexto && matchStatus && matchEmpresa;
    });
}

function renderOrdens() {
    const tbody = document.querySelector("#tblOrdensProducao tbody");
    if (!tbody) return;
    const rows = applyFiltros(state.ordens);
    tbody.innerHTML = "";

    if (!rows.length) {
        tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="7" class="sistema-empty-msg">Nenhuma OP encontrada com os filtros atuais.</td></tr>`;
        updateContador(0, state.ordens.length);
        return;
    }

    rows.forEach((item) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="col-meta-1">${escapeHtml(item.numero_op || "-")}</td>
            <td class="col-meta-2">${escapeHtml(item.empresa_nome || "-")}</td>
            <td class="col-principal col-op-principal">
                <strong>${escapeHtml(item.cliente || "-")}</strong><br>
                <span>${escapeHtml(item.obra || "-")}</span>
            </td>
            <td class="col-meta-2">${escapeHtml(item.data_entrega_valor || "-")}</td>
            <td class="col-meta-3"><span class="op-status-tag">${escapeHtml(item.status || "-")}</span></td>
            <td class="col-meta-2">${escapeHtml(item.total_produtos || 0)} / ${escapeHtml(item.total_unidades || 0)}</td>
            <td class="col-acao">
                <div class="op-row-actions">
                    <button class="btn-row-action" type="button" data-action="abrir" data-op-id="${item.id}">Abrir</button>
                    <button class="btn-row-action" type="button" data-action="editar" data-op-id="${item.id}">Editar</button>
                    <button class="btn-row-action" type="button" data-action="produtos" data-op-id="${item.id}">Produtos</button>
                    <button class="btn-row-action" type="button" data-action="bom" data-op-id="${item.id}">BOM</button>
                    <button class="btn-row-action" type="button" data-action="processos" data-op-id="${item.id}">Processos</button>
                    <button class="btn-row-action" type="button" data-action="historico" data-op-id="${item.id}">Histórico</button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
    updateContador(rows.length, state.ordens.length);
}

function updateContador(exibidos, total) {
    const contador = document.getElementById("opContador");
    if (!contador) return;
    contador.textContent = exibidos
        ? `Exibindo ${exibidos} de ${total} ordens de produção`
        : "0 ordens de produção encontradas";
}

async function refreshOrdens() {
    await loadOrdens();
    renderOrdens();
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

async function openModalOpCabecalho(opId = null) {
    clearModalOpCabecalho();
    if (opId) {
        const detail = await apiGet(`${API_OP}/${opId}`);
        const cabecalho = detail?.cabecalho || {};
        document.getElementById("tituloModalOp").textContent = `Editar OP ${cabecalho.numero_op || opId}`;
        document.getElementById("opId").value = String(opId);
        document.getElementById("opCliente").value = cabecalho.cliente || "";
        document.getElementById("opObra").value = cabecalho.obra || "";
        document.getElementById("opModelo").value = cabecalho.modelo || "";
        document.getElementById("opTipo").value = cabecalho.tipo || "";
        document.getElementById("opMaterial").value = cabecalho.material || "";
        document.getElementById("opSolicitante").value = cabecalho.solicitante || "";
        document.getElementById("opStatus").value = cabecalho.status || "RASCUNHO";
        document.getElementById("opEntregaTipo").value = cabecalho.data_entrega_tipo || "TEXTO";
        document.getElementById("opEntregaData").value = cabecalho.data_entrega_data || "";
        document.getElementById("opEntregaValor").value = cabecalho.data_entrega_valor || "";
        document.getElementById("opObservacoes").value = cabecalho.observacoes || "";
    }
    syncEntregaTipoUi();
    openModal("modalOpCabecalho");
}

function clearModalOpCabecalho() {
    document.getElementById("tituloModalOp").textContent = "Nova OP";
    document.getElementById("opId").value = "";
    document.getElementById("opCliente").value = "";
    document.getElementById("opObra").value = "";
    document.getElementById("opModelo").value = "";
    document.getElementById("opTipo").value = "";
    document.getElementById("opMaterial").value = "";
    document.getElementById("opSolicitante").value = "";
    document.getElementById("opStatus").value = "RASCUNHO";
    document.getElementById("opEntregaTipo").value = "TEXTO";
    document.getElementById("opEntregaData").value = "";
    document.getElementById("opEntregaValor").value = "NÃO DEFINIDO";
    document.getElementById("opObservacoes").value = "";
}

function syncEntregaTipoUi() {
    const tipo = document.getElementById("opEntregaTipo")?.value || "TEXTO";
    const blocoData = document.getElementById("blocoEntregaData");
    const blocoTexto = document.getElementById("blocoEntregaTexto");
    if (!blocoData || !blocoTexto) return;
    if (tipo === "DATA") {
        blocoData.classList.remove("hidden");
        blocoTexto.classList.add("hidden");
    } else {
        blocoData.classList.add("hidden");
        blocoTexto.classList.remove("hidden");
    }
}

async function saveModalOpCabecalho() {
    try {
        const opId = Number(document.getElementById("opId").value || 0);
        const payload = {
            cliente: fieldValue("opCliente"),
            obra: fieldValue("opObra"),
            modelo: fieldValue("opModelo"),
            tipo: fieldValue("opTipo"),
            material: fieldValue("opMaterial"),
            solicitante: fieldValue("opSolicitante"),
            status: fieldValue("opStatus"),
            data_entrega_tipo: fieldValue("opEntregaTipo"),
            data_entrega_data: fieldValue("opEntregaData"),
            data_entrega_valor: fieldValue("opEntregaValor"),
            observacoes: fieldValue("opObservacoes")
        };
        if (payload.data_entrega_tipo === "DATA" && !payload.data_entrega_data) {
            throw new Error("Informe a data de entrega.");
        }
        if (payload.data_entrega_tipo === "TEXTO" && !payload.data_entrega_valor) {
            payload.data_entrega_valor = "NÃO DEFINIDO";
        }

        if (opId) {
            await apiPut(`${API_OP}/${opId}`, payload);
        } else {
            await apiPost(API_OP, payload);
        }
        closeModal("modalOpCabecalho");
        await refreshOrdens();
    } catch (err) {
        alert(getErrorMessage(err));
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
        tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="4" class="sistema-empty-msg">Nenhum produto vinculado nesta OP.</td></tr>`;
        return;
    }
    rows.forEach((item) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="col-principal">${escapeHtml(item.nome_produto || item.produto_key || "-")}</td>
            <td class="col-meta-2">${escapeHtml(item.item_ata || "-")}</td>
            <td class="col-meta-2"><input id="opProdutoQtd_${item.id}" type="number" min="0.01" step="0.01" value="${escapeHtml(item.quantidade || 1)}"></td>
            <td class="col-acao">
                <div class="op-row-actions">
                    <button class="btn-row-action" type="button" data-action="salvar-produto-op" data-op-produto-id="${item.id}">Salvar</button>
                    <button class="btn-row-action" type="button" data-action="remover-produto-op" data-op-produto-id="${item.id}">Remover</button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function addProdutoNaOpAtual() {
    try {
        const opId = Number(document.getElementById("opProdutosId")?.value || 0);
        const produtoId = Number(document.getElementById("opProdutoCatalogo")?.value || 0);
        const quantidade = Number(document.getElementById("opProdutoQuantidade")?.value || 0);
        if (!opId) throw new Error("OP inválida.");
        if (!produtoId) throw new Error("Selecione um produto.");
        if (!(quantidade > 0)) throw new Error("Quantidade inválida.");
        await apiPost(`${API_OP}/${opId}/produtos`, { produto_id: produtoId, quantidade });
        await refreshModalProdutos(opId);
        await refreshOrdens();
    } catch (err) {
        alert(getErrorMessage(err));
    }
}

async function openModalOpBom(opId) {
    document.getElementById("opBomId").value = String(opId);
    const rows = await apiGet(`${API_OP}/${opId}/bom`);
    const tbody = document.getElementById("opBomRows");
    if (!tbody) return;
    tbody.innerHTML = "";
    const list = Array.isArray(rows) ? rows : [];
    if (!list.length) {
        tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="7" class="sistema-empty-msg">BOM não encontrada para esta OP.</td></tr>`;
    } else {
        list.forEach((item) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td class="col-principal">${escapeHtml(item.nome_produto || "-")}</td>
                <td class="col-meta-2">${escapeHtml((item.grupo || "").toUpperCase())}</td>
                <td class="col-meta-2">${escapeHtml(item.cod || "-")}</td>
                <td class="col-principal">${escapeHtml(item.material || "-")}</td>
                <td class="col-meta-2"><input class="opBomQtdUnit" data-bom-id="${item.id}" type="number" min="0" step="0.0001" value="${escapeHtml(item.quantidade_unitaria || 0)}"></td>
                <td class="col-meta-2">${escapeHtml(item.quantidade_produto || 0)}</td>
                <td class="col-meta-2">${escapeHtml(item.quantidade_total || 0)}</td>
            `;
            tbody.appendChild(tr);
        });
    }
    openModal("modalOpBom");
}

async function saveBomDaOpAtual() {
    try {
        const opId = Number(document.getElementById("opBomId")?.value || 0);
        if (!opId) throw new Error("OP inválida.");
        const itens = [...document.querySelectorAll(".opBomQtdUnit")]
            .map((input) => ({
                id: Number(input.getAttribute("data-bom-id") || 0),
                quantidade_unitaria: Number(input.value || 0)
            }))
            .filter((item) => item.id > 0);
        await apiPut(`${API_OP}/${opId}/bom`, { itens });
        await openModalOpBom(opId);
    } catch (err) {
        alert(getErrorMessage(err));
    }
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
                    <input id="opProcessoObs_${item.id}" type="text" value="${escapeHtml(item.observacao || "")}" placeholder="Observação">
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
    const list = ["PENDENTE", "EM_ANDAMENTO", "CONCLUIDO", "PAUSADO"];
    return list
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
        tbody.innerHTML = `<tr class="sistema-empty-row"><td colspan="4" class="sistema-empty-msg">Sem histórico para esta OP.</td></tr>`;
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
    const fallback = "Falha ao processar a operação.";
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
        throw new Error(detail || "Erro de integração com backend.");
    }
    return payload.data;
}
