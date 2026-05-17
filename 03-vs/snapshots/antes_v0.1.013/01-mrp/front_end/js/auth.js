// =======================================================
// AUTENTICACAO LOCAL TEMPORARIA - MRP_LOCAL
// =======================================================

const SESSION_KEY = "mrp_local_session";
const LOCAL_USER = "admin";
const LOCAL_PASSWORD = "admin";

function buildSession() {
    return {
        user: LOCAL_USER,
        mode: "LOCAL_TEMPORARIO",
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
            mode: "LOCAL_TEMPORARIO"
        };
    }

    return {
        ok: false,
        error: "Credenciais invalidas"
    };
}
