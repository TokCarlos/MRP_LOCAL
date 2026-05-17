// =======================================================
// ADAPTADOR LOCAL TEMPORARIO - DADOS MOCKADOS
// =======================================================

import { APP_CONFIG } from "./config.js";

const STORAGE_KEY = APP_CONFIG.mockStorageKey;

const seedData = {
    produtos: [
        { id: 1, nome: "Produto Exemplo A" },
        { id: 2, nome: "Produto Exemplo B" },
        { id: 3, nome: "Produto Exemplo C" }
    ],
    ordens_producao: [
        { id: 1, produto_id: 1, status: "EM_TESTE", quantidade: 10 },
        { id: 2, produto_id: 2, status: "RASCUNHO", quantidade: 5 }
    ],
    estoque: [
        { id: 1, produto_id: 1, quantidade: 25 },
        { id: 2, produto_id: 2, quantidade: 12 },
        { id: 3, produto_id: 3, quantidade: 7 }
    ],
    processos: [
        { id: 1, nome: "Corte" },
        { id: 2, nome: "Montagem" },
        { id: 3, nome: "Conferencia" }
    ]
};

function clone(value) {
    return JSON.parse(JSON.stringify(value));
}

function loadDb() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) return JSON.parse(raw);
    } catch {
        // Recria a base mockada quando houver dado local invalido.
    }

    const initialData = clone(seedData);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(initialData));
    return initialData;
}

function saveDb(db) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
}

function applyParams(rows, params) {
    const entries = Object.entries(params || {});
    if (!entries.length) return rows;

    return rows.filter(row => entries.every(([key, value]) => String(row[key]) === String(value)));
}

export async function localGET(table, params = {}) {
    const db = loadDb();
    const rows = Array.isArray(db[table]) ? db[table] : [];
    return clone(applyParams(rows, params));
}

export async function localINSERT(table, data) {
    const db = loadDb();
    const rows = Array.isArray(db[table]) ? db[table] : [];
    const nextId = rows.reduce((max, row) => Math.max(max, Number(row.id) || 0), 0) + 1;
    const record = { id: nextId, ...data };

    db[table] = [...rows, record];
    saveDb(db);

    return clone(record);
}
