import { localGET } from "../api.js";

export async function init() {

    const produtos = await localGET("produtos");
    const ordens = await localGET("ordens_producao");
    const estoque = await localGET("estoque");

    document.getElementById("kpi-produtos").innerText = produtos.length;
    document.getElementById("kpi-ordens").innerText = ordens.length;
    document.getElementById("kpi-estoque").innerText = estoque.length;
}
