// =======================================================
// AUTENTICACAO LOCAL TEMPORARIA - MRP_LOCAL
// =======================================================

import { APP_CONFIG } from "./config.js";

const SESSION_KEY = APP_CONFIG.sessionKey;
const LOCAL_USER = APP_CONFIG.login.usuario;
const LOCAL_PASSWORD = APP_CONFIG.login.senha;

function buildSession() {
    return {
        user: LOCAL_USER,
        mode: APP_CONFIG.authMode,
        createdAt: new Date().toISOString()
    };
}

export function saveSession(session) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function getSession() {
    try {
        const raw = localStorage.getItem(SESSION_KEY);
        return raw ? JSON.parse(raw) : null;
    } catch {
        return null;
    }
}

export function isAuthenticated() {
    const session = getSession();
    return Boolean(session && session.user === LOCAL_USER);
}

export function logout() {
    localStorage.removeItem(SESSION_KEY);
    window.location.href = "login.html";
}

export async function loginUser(user, password) {
    if (user === LOCAL_USER && password === LOCAL_PASSWORD) {
        saveSession(buildSession());
        return {
            ok: true,
            user: LOCAL_USER,
            mode: APP_CONFIG.authMode
        };
    }

    return {
        ok: false,
        error: "Credenciais invalidas"
    };
}
