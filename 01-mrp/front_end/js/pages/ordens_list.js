import { localGET } from "../api.js";

export async function init() {
    const [ordens, produtos] = await Promise.all([
        localGET("ordens_producao"),
        localGET("produtos")
    ]);

    const produtoNomeById = new Map(produtos.map(p => [String(p.id), p.nome]));
    const tbody = document.querySelector("#tblOrdens tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    ordens.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.id ?? ""}</td>
            <td>${item.numero ?? ""}</td>
            <td>${produtoNomeById.get(String(item.produto_id)) ?? "-"}</td>
            <td>${item.quantidade ?? ""}</td>
            <td>${item.status ?? ""}</td>
            <td>${item.prioridade ?? ""}</td>
            <td>${item.data_prevista ?? ""}</td>
            <td><button class="btn-row-action" type="button" disabled>Visualizar</button></td>
        `;
        tbody.appendChild(tr);
    });
}
