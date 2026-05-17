import { localGET } from "../api.js";

const state = {
    dados: [],
    filtros: { pesquisa: "", local: "", status: "", unidade: "" }
};

export async function init() {
    const addBtn = document.getElementById("btnAddEstoque");
    if (addBtn) addBtn.addEventListener("click", () => alert("Cadastro manual fora do escopo desta etapa."));

    state.dados = await carregarDados();
    initFiltros();
    popularFiltros(state.dados);
    renderFiltrados();
}

function normalizeSearchText(value) {
    return String(value || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase()
        .trim();
}

async function carregarDados() {
    const [estoque, produtos] = await Promise.all([localGET("estoque"), localGET("produtos")]);
    const produtoNomeById = new Map(produtos.map(p => [String(p.id), p.nome_oficial || p.nome || ""]));

    const data = (Array.isArray(estoque) ? estoque : []).map((item) => ({
        id: item.id,
        produto_id: item.produto_id,
        produto_nome: item.produto_nome || produtoNomeById.get(String(item.produto_id)) || "-",
        local: item.local || "Almoxarifado",
        quantidade: item.quantidade ?? 0,
        minimo: item.minimo ?? 0,
        unidade: item.unidade || "UN",
        status: item.status || "OK"
    }));
    return data;
}

function initFiltros() {
    const pesquisa = document.getElementById("filtroEstoquePesquisa");
    const local = document.getElementById("filtroEstoqueLocal");
    const status = document.getElementById("filtroEstoqueStatus");
    const unidade = document.getElementById("filtroEstoqueUnidade");
    const limpar = document.getElementById("btnLimparFiltrosEstoque");

    if (pesquisa) pesquisa.addEventListener("input", (e) => { state.filtros.pesquisa = e.target.value || ""; renderFiltrados(); });
    if (local) local.addEventListener("change", (e) => { state.filtros.local = e.target.value || ""; renderFiltrados(); });
    if (status) status.addEventListener("change", (e) => { state.filtros.status = e.target.value || ""; renderFiltrados(); });
    if (unidade) unidade.addEventListener("change", (e) => { state.filtros.unidade = e.target.value || ""; renderFiltrados(); });
    if (limpar) limpar.addEventListener("click", () => {
        state.filtros = { pesquisa: "", local: "", status: "", unidade: "" };
        if (pesquisa) pesquisa.value = "";
        if (local) local.value = "";
        if (status) status.value = "";
        if (unidade) unidade.value = "";
        renderFiltrados();
    });
}

function popularFiltros(dados) {
    const local = document.getElementById("filtroEstoqueLocal");
    const status = document.getElementById("filtroEstoqueStatus");
    const unidade = document.getElementById("filtroEstoqueUnidade");
    if (local) fillSelect(local, "Todos os Locais", [...new Set(dados.map(d => d.local).filter(Boolean))].sort());
    if (status) fillSelect(status, "Todos os Status", [...new Set(dados.map(d => d.status).filter(Boolean))].sort());
    if (unidade) fillSelect(unidade, "Todas as Unidades", [...new Set(dados.map(d => d.unidade).filter(Boolean))].sort());
}

function fillSelect(select, defaultLabel, values) {
    select.innerHTML = "";
    const d = document.createElement("option");
    d.value = "";
    d.textContent = defaultLabel;
    select.appendChild(d);
    values.forEach((v) => {
        const o = document.createElement("option");
        o.value = v;
        o.textContent = v;
        select.appendChild(o);
    });
}

function aplicarFiltros(dados) {
    const pesquisa = normalizeSearchText(state.filtros.pesquisa);
    return dados.filter((item) => {
        const texto = normalizeSearchText([item.produto_nome, item.local, item.status, item.unidade].join(" "));
        const mPesquisa = !pesquisa || texto.includes(pesquisa);
        const mLocal = !state.filtros.local || item.local === state.filtros.local;
        const mStatus = !state.filtros.status || item.status === state.filtros.status;
        const mUnidade = !state.filtros.unidade || item.unidade === state.filtros.unidade;
        return mPesquisa && mLocal && mStatus && mUnidade;
    });
}

function renderFiltrados() {
    const filtrados = aplicarFiltros(state.dados);
    renderTabela(filtrados);
    updateContador(filtrados.length, state.dados.length);
}

function updateContador(exibidos, total) {
    const el = document.getElementById("contadorEstoque");
    if (!el) return;
    el.textContent = exibidos ? `Exibindo ${exibidos} de ${total} registros de estoque` : "0 registros de estoque encontrados";
}

function renderTabela(dados) {
    const tbody = document.querySelector("#tblEstoque tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (!dados.length) {
        const tr = document.createElement("tr");
        tr.className = "sistema-empty-row";
        tr.innerHTML = `<td colspan="8" class="sistema-empty-msg">Nenhum registro encontrado com os filtros atuais.</td>`;
        tbody.appendChild(tr);
        return;
    }

    dados.forEach((item) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="col-meta-1">${item.id ?? ""}</td>
            <td class="col-principal">${item.produto_nome ?? ""}</td>
            <td class="col-meta-1">${item.local ?? ""}</td>
            <td class="col-meta-2">${item.quantidade ?? ""}</td>
            <td class="col-meta-2">${item.minimo ?? ""}</td>
            <td class="col-meta-2">${item.unidade ?? ""}</td>
            <td class="col-meta-3">${item.status ?? ""}</td>
            <td class="col-acao"><button class="btn-row-action" type="button" onclick="alert('Futuro: editar')">Editar</button></td>
        `;
        tbody.appendChild(tr);
    });
}
