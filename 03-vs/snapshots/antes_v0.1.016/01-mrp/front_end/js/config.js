// =======================================================
// CONFIGURACAO DO FRONT-END - MRP_LOCAL
// =======================================================

export const APP_CONFIG = {
    ambiente: "TESTE_HOME",
    authMode: "LOCAL_TEMPORARIO",
    dataMode: "MOCK_LOCAL",
    sessionKey: "mrp_local_session",
    mockStorageKey: "mrp_local_mock_db",
    login: {
        usuario: "admin",
        senha: "admin"
    },
    api: {
        baseUrl: "",
        useMock: true
    },
    flags: {
        debug: true
    }
};
