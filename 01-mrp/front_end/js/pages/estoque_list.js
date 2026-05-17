import { localGET } from "../api.js";

export async function init() {
    const [estoque, produtos] = await Promise.all([
        localGET("estoque"),
        localGET("produtos")
    ]);

    const produtoNomeById = new Map(produtos.map(p => [String(p.id), p.nome]));
    const tbody = document.querySelector("#tblEstoque tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    estoque.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.id ?? ""}</td>
            <td>${produtoNomeById.get(String(item.produto_id)) ?? "-"}</td>
            <td>${item.local ?? ""}</td>
            <td>${item.quantidade ?? ""}</td>
            <td>${item.minimo ?? ""}</td>
            <td>${item.unidade ?? ""}</td>
            <td>${item.status ?? ""}</td>
        `;
        tbody.appendChild(tr);
    });
}
