import { localGET } from "../api.js";

const state = {
    dados: [],
    filtros: { pesquisa: "", setor: "", status: "" }
};

export async function init() {
    const addBtn = document.getElementById("btnAddProcesso");
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
    const data = await localGET("processos");
    if (Array.isArray(data) && data.length) return data;
    return [
        { id: 1, codigo: "PROC-001", nome: "Corte", setor: "Produção", tempo_padrao_min: 30, status: "ATIVO" },
        { id: 2, codigo: "PROC-002", nome: "Solda", setor: "Produção", tempo_padrao_min: 45, status: "ATIVO" },
        { id: 3, codigo: "PROC-003", nome: "Dobra", setor: "Produção", tempo_padrao_min: 25, status: "ATIVO" },
        { id: 4, codigo: "PROC-004", nome: "Pintura", setor: "Acabamento", tempo_padrao_min: 40, status: "ATIVO" },
        { id: 5, codigo: "PROC-005", nome: "Montagem", setor: "Montagem", tempo_padrao_min: 55, status: "ATIVO" },
        { id: 6, codigo: "PROC-006", nome: "Expedição", setor: "Logística", tempo_padrao_min: 20, status: "ATIVO" }
    ];
}

function initFiltros() {
    const pesquisa = document.getElementById("filtroProcessoPesquisa");
    const setor = document.getElementById("filtroProcessoSetor");
    const status = document.getElementById("filtroProcessoStatus");
    const limpar = document.getElementById("btnLimparFiltrosProcesso");

    if (pesquisa) pesquisa.addEventListener("input", (e) => { state.filtros.pesquisa = e.target.value || ""; renderFiltrados(); });
    if (setor) setor.addEventListener("change", (e) => { state.filtros.setor = e.target.value || ""; renderFiltrados(); });
    if (status) status.addEventListener("change", (e) => { state.filtros.status = e.target.value || ""; renderFiltrados(); });
    if (limpar) limpar.addEventListener("click", () => {
        state.filtros = { pesquisa: "", setor: "", status: "" };
        if (pesquisa) pesquisa.value = "";
        if (setor) setor.value = "";
        if (status) status.value = "";
        renderFiltrados();
    });
}

function popularFiltros(dados) {
    const setor = document.getElementById("filtroProcessoSetor");
    const status = document.getElementById("filtroProcessoStatus");
    if (setor) fillSelect(setor, "Todos os Setores", [...new Set(dados.map(d => d.setor).filter(Boolean))].sort());
    if (status) fillSelect(status, "Todos os Status", [...new Set(dados.map(d => d.status).filter(Boolean))].sort());
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
        const texto = normalizeSearchText([item.codigo, item.nome, item.setor, item.status].join(" "));
        const mPesquisa = !pesquisa || texto.includes(pesquisa);
        const mSetor = !state.filtros.setor || item.setor === state.filtros.setor;
        const mStatus = !state.filtros.status || item.status === state.filtros.status;
        return mPesquisa && mSetor && mStatus;
    });
}

function renderFiltrados() {
    const filtrados = aplicarFiltros(state.dados);
    renderTabela(filtrados);
    updateContador(filtrados.length, state.dados.length);
}

function updateContador(exibidos, total) {
    const el = document.getElementById("contadorProcessos");
    if (!el) return;
    el.textContent = exibidos ? `Exibindo ${exibidos} de ${total} processos` : "0 processos encontrados";
}

function renderTabela(dados) {
    const tbody = document.querySelector("#tblProcessos tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    if (!dados.length) {
        const tr = document.createElement("tr");
        tr.className = "sistema-empty-row";
        tr.innerHTML = `<td colspan="7" class="sistema-empty-msg">Nenhum registro encontrado com os filtros atuais.</td>`;
        tbody.appendChild(tr);
        return;
    }

    dados.forEach((item) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td class="col-meta-1">${item.id ?? ""}</td>
            <td class="col-meta-2">${item.codigo ?? ""}</td>
            <td class="col-principal">${item.nome ?? ""}</td>
            <td class="col-meta-1">${item.setor ?? ""}</td>
            <td class="col-meta-2">${item.tempo_padrao_min ?? ""}</td>
            <td class="col-meta-3">${item.status ?? ""}</td>
            <td class="col-acao"><button class="btn-row-action" type="button" onclick="alert('Futuro: editar')">Editar</button></td>
        `;
        tbody.appendChild(tr);
    });
}
