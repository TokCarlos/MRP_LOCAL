// =======================================================
// ADAPTADOR LOCAL TEMPORARIO - DADOS MOCKADOS
// =======================================================

import { APP_CONFIG } from "./config.js";

const STORAGE_KEY = APP_CONFIG.mockStorageKey;

const seedData = {
    produtos: [
        {
            id: 1,
            codigo: "PRD-001",
            nome: "Produto Exemplo A",
            unidade: "UN",
            categoria: "Linha A",
            status: "ATIVO"
        },
        {
            id: 2,
            codigo: "PRD-002",
            nome: "Produto Exemplo B",
            unidade: "UN",
            categoria: "Linha B",
            status: "ATIVO"
        },
        {
            id: 3,
            codigo: "PRD-003",
            nome: "Produto Exemplo C",
            unidade: "CJ",
            categoria: "Linha C",
            status: "REVISAO"
        }
    ],
    ordens_producao: [
        {
            id: 1,
            numero: "OP-0001",
            produto_id: 1,
            quantidade: 10,
            status: "EM_TESTE",
            prioridade: "ALTA",
            data_prevista: "2026-05-20"
        },
        {
            id: 2,
            numero: "OP-0002",
            produto_id: 2,
            quantidade: 5,
            status: "RASCUNHO",
            prioridade: "MEDIA",
            data_prevista: "2026-05-23"
        }
    ],
    estoque: [
        {
            id: 1,
            produto_id: 1,
            local: "ALMOX-A1",
            quantidade: 25,
            minimo: 10,
            unidade: "UN",
            status: "OK"
        },
        {
            id: 2,
            produto_id: 2,
            local: "ALMOX-B1",
            quantidade: 12,
            minimo: 8,
            unidade: "UN",
            status: "ATENCAO"
        },
        {
            id: 3,
            produto_id: 3,
            local: "ALMOX-C2",
            quantidade: 7,
            minimo: 5,
            unidade: "CJ",
            status: "OK"
        }
    ],
    processos: [
        {
            id: 1,
            codigo: "PRC-001",
            nome: "Corte",
            setor: "Producao",
            tempo_padrao_min: 15,
            status: "ATIVO"
        },
        {
            id: 2,
            codigo: "PRC-002",
            nome: "Montagem",
            setor: "Producao",
            tempo_padrao_min: 30,
            status: "ATIVO"
        },
        {
            id: 3,
            codigo: "PRC-003",
            nome: "Conferencia",
            setor: "Qualidade",
            tempo_padrao_min: 12,
            status: "ATIVO"
        }
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
