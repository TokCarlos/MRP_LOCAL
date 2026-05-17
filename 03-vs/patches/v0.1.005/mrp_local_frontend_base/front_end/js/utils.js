/* ============================================================
   utils.js - Funcoes utilitarias globais para o sistema JPL
============================================================ */

/* -------------------------------
   1) LOG DE DEBUG (ligar/desligar)
--------------------------------*/
const DEBUG = true;
function logDebug(tag, data) {
    if (DEBUG) console.log(`[DEBUG] ${tag}:`, data);
}


/* -------------------------------
   2) ALERTA PADRONIZADO (toast)
--------------------------------*/
function toast(msg, tipo = "info") {
    alert(msg);
}


/* -------------------------------
   3) FORMATACAO DE DATAS
--------------------------------*/
function formatarDataISO() {
    return new Date().toISOString().split("T")[0];
}

function formatarDataHora() {
    const d = new Date();
    return `${d.toLocaleDateString()} ${d.toLocaleTimeString()}`;
}


/* -------------------------------
   4) STORAGE - ACESSO SEGURO
--------------------------------*/
function storageSet(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function storageGet(key, fallback = null) {
    try {
        const raw = localStorage.getItem(key);
        return raw ? JSON.parse(raw) : fallback;
    } catch {
        return fallback;
    }
}

function storageRemove(key) {
    localStorage.removeItem(key);
}


/* -------------------------------
   5) CARREGAR HTML LOCAL
--------------------------------*/
async function loadHTML(targetId, filePath) {
    try {
        const resp = await fetch(filePath);
        const html = await resp.text();
        document.getElementById(targetId).innerHTML = html;
    } catch (err) {
        console.error("Erro ao carregar HTML:", err);
        toast("Erro ao carregar conteudo.");
    }
}


/* -------------------------------
   6) API ONLINE DESATIVADA NESTA ETAPA
--------------------------------*/
async function apiRequest() {
    console.warn("apiRequest online desativado em v0.1.005. Use js/api.js local.");
    return null;
}


/* -------------------------------
   7) GERAR ID UNICO LOCAL
--------------------------------*/
function gerarIdLocal(prefix = "ID") {
    return `${prefix}_${Math.random().toString(36).substr(2, 9)}`;
}


/* -------------------------------
   8) ROLE / PERMISSOES (helpers)
--------------------------------*/
function userHasPermission(perm) {
    const permissoes = storageGet("permissoes", []);
    return permissoes.includes(perm);
}
