import { localGET } from "../api.js";

export async function init() {
    const data = await localGET("processos");
    const tbody = document.querySelector("#tblProcessos tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    data.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.id ?? ""}</td>
            <td>${item.codigo ?? ""}</td>
            <td>${item.nome ?? ""}</td>
            <td>${item.setor ?? ""}</td>
            <td>${item.tempo_padrao_min ?? ""}</td>
            <td>${item.status ?? ""}</td>
        `;
        tbody.appendChild(tr);
    });
}
