import { localGET } from "../api.js";

const state = {
    dados: [],
    filtros: { pesquisa: "", status: "", prioridade: "" }
};

export async function init() {
    const addBtn = document.getElementById("btnAddOrdem");
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
    const [ordens, produtos] = await Promise.all([localGET("ordens_producao"), localGET("produtos")]);
    const produtoNomeById = new Map(produtos.map(p => [String(p.id), p.nome_oficial || p.nome || ""]));

    return (Array.isArray(ordens) ? ordens : []).map((item, index) => ({
        id: item.id ?? index + 1,
        numero: item.numero || `OP-${String(index + 1).padStart(4, "0")}/2026`,
        produto_id: item.produto_id,
        produto_nome: item.produto_nome || produtoNomeById.get(String(item.produto_id)) || "-",
        quantidade: item.quantidade ?? 0,
        prioridade: item.prioridade || "NORMAL",
        status: item.status || "PLANEJADA",
        data_prevista: item.data_prevista || ""
    }));
}

function initFiltros() {
    const pesquisa = document.getElementById("filtroOrdemPesquisa");
    const status = document.getElementById("filtroOrdemStatus");
    const prioridade = document.getElementById("filtroOrdemPrioridade");
    const limpar = document.getElementById("btnLimparFiltrosOrdem");

    if (pesquisa) pesquisa.addEventListener("input", (e) => { state.filtros.pesquisa = e.target.value || ""; renderFiltrados(); });
    if (status) status.addEventListener("change", (e) => { state.filtros.status = e.target.value || ""; renderFiltrados(); });
    if (prioridade) prioridade.addEventListener("change", (e) => { state.filtros.prioridade = e.target.value || ""; renderFiltrados(); });
    if (limpar) limpar.addEventListener("click", () => {
        state.filtros = { pesquisa: "", status: "", prioridade: "" };
        if (pesquisa) pesquisa.value = "";
        if (status) status.value = "";
        if (prioridade) prioridade.value = "";
        renderFiltrados();
    });
}

function popularFiltros(dados) {
    const status = document.getElementById("filtroOrdemStatus");
    const prioridade = document.getElementById("filtroOrdemPrioridade");
    if (status) fillSelect(status, "Todos os Status", [...new Set(dados.map(d => d.status).filter(Boolean))].sort());
    if (prioridade) fillSelect(prioridade, "Todas as Prioridades", [...new Set(dados.map(d => d.prioridade).filter(Boolean))].sort());
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
        const texto = normalizeSearchText([item.numero, item.produto_nome, item.status, item.prioridade, item.data_prevista].join(" "));
        const mPesquisa = !pesquisa || texto.includes(pesquisa);
        const mStatus = !state.filtros.status || item.status === state.filtros.status;
        const mPrioridade = !state.filtros.prioridade || item.prioridade === state.filtros.prioridade;
        return mPesquisa && mStatus && mPrioridade;
    });
}

function renderFiltrados() {
    const filtrados = aplicarFiltros(state.dados);
    renderTabela(filtrados);
    updateContador(filtrados.length, state.dados.length);
}

function updateContador(exibidos, total) {
    const el = document.getElementById("contadorOrdens");
    if (!el) return;
    el.textContent = exibidos ? `Exibindo ${exibidos} de ${total} ordens de produção` : "0 ordens de produção encontradas";
}

function renderTabela(dados) {
    const tbody = document.querySelector("#tblOrdens tbody");
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
            <td class="col-meta-2">${item.numero ?? ""}</td>
            <td class="col-principal">${item.produto_nome ?? ""}</td>
            <td class="col-meta-1">${item.quantidade ?? ""}</td>
            <td class="col-meta-2">${item.prioridade ?? ""}</td>
            <td class="col-meta-3">${item.status ?? ""}</td>
            <td class="col-meta-2">${item.data_prevista ?? ""}</td>
            <td class="col-acao"><button class="btn-row-action" type="button" onclick="alert('Futuro: editar')">Editar</button></td>
        `;
        tbody.appendChild(tr);
    });
}
