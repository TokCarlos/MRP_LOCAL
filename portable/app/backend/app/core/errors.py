from __future__ import annotations


class BackendError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 500) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


class SeedNotFoundError(BackendError):
    def __init__(self, seed_path: str) -> None:
        super().__init__("seed_not_found", f"Seed de produtos nao encontrado: {seed_path}", 500)


class SeedInvalidError(BackendError):
    def __init__(self, message: str) -> None:
        super().__init__("seed_invalid", message, 500)


class AdapterError(BackendError):
    def __init__(self, message: str) -> None:
        super().__init__("adapter_failed", message, 500)

