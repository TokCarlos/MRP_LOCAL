// =======================================================
// SEGURANCA LOCAL TEMPORARIA - VALIDACAO DE SESSAO LOCAL
// =======================================================

import { isAuthenticated, logout } from "./auth.js";

function validateAccess() {
    if (!isAuthenticated()) {
        logout();
    }
}

validateAccess();

export {};
