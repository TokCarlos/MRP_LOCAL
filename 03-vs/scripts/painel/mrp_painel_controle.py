#!/usr/bin/env python3
from __future__ import annotations

import getpass
import hashlib
import hmac
import json
import socket
import subprocess
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from tkinter import END, Tk, Toplevel, messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def resolve_repo_root() -> Path:
    # 03-vs/scripts/painel/mrp_painel_controle.py -> subir 3 niveis
    return Path(__file__).resolve().parents[3]


class AdminAuthDialog(Toplevel):
    def __init__(self, parent: Tk) -> None:
        super().__init__(parent)
        self.title("Autenticacao Administrativa")
        self.resizable(False, False)
        self.result: str | None = None
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        frm = ttk.Frame(self, padding=14)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Informe PIN/senha administrativa local").grid(row=0, column=0, columnspan=2, sticky="w")
        self.entry = ttk.Entry(frm, show="*", width=36)
        self.entry.grid(row=1, column=0, columnspan=2, pady=(8, 10))
        self.entry.focus_set()

        ttk.Button(frm, text="Cancelar", command=self.cancel).grid(row=2, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(frm, text="Confirmar", command=self.confirm).grid(row=2, column=1, sticky="ew")

    def confirm(self) -> None:
        val = self.entry.get().strip()
        self.result = val if val else None
        self.destroy()

    def cancel(self) -> None:
        self.result = None
        self.destroy()


class MrpPainel:
    def __init__(self) -> None:
        self.repo_root = resolve_repo_root()
        self.config_dir = self.repo_root / "01-mrp" / "config"
        self.local_dir = self.config_dir / "local"
        self.logs_admin_dir = self.repo_root / "01-mrp" / "logs" / "admin"
        self.auth_file = self.local_dir / "admin_auth.local.json"
        self.auto_mode_file = self.local_dir / "mrp_auto_mode.local.json"
        self.log_file = self.logs_admin_dir / "painel_admin.log"
        self.user_name = getpass.getuser()
        self.port = self._load_port()
        self.admin_unlocked = False

        self.root = Tk()
        self.root.title("MRP_LOCAL - Painel Administrativo do Servidor")
        self.root.geometry("1080x720")
        self.root.minsize(960, 640)

        self.style = ttk.Style(self.root)
        self._configure_style()

        self.status_vars: dict[str, ttk.Label] = {}
        self.output: ScrolledText | None = None
        self.admin_buttons: list[ttk.Button] = []
        self.admin_status: ttk.Label | None = None

        self._build_ui()
        self.refresh_status_card()

    def _configure_style(self) -> None:
        themes = self.style.theme_names()
        theme = "vista" if "vista" in themes else "clam"
        self.style.theme_use(theme)

        bg = "#101419"
        card = "#1a212a"
        accent = "#2b7cff"
        fg = "#e8eef7"
        muted = "#9fb0c5"

        self.root.configure(bg=bg)
        self.style.configure("TFrame", background=bg)
        self.style.configure("Card.TFrame", background=card, relief="flat")
        self.style.configure("Head.TLabel", background=bg, foreground=fg, font=("Segoe UI", 18, "bold"))
        self.style.configure("SubHead.TLabel", background=bg, foreground=muted, font=("Segoe UI", 10))
        self.style.configure("CardTitle.TLabel", background=card, foreground=fg, font=("Segoe UI", 11, "bold"))
        self.style.configure("CardText.TLabel", background=card, foreground=muted, font=("Segoe UI", 10))
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        self.style.map("Accent.TButton", background=[("active", accent), ("!disabled", accent)])
        self.style.configure("TButton", font=("Segoe UI", 10))

    def _build_ui(self) -> None:
        root_pad = ttk.Frame(self.root, padding=14)
        root_pad.pack(fill="both", expand=True)

        header = ttk.Frame(root_pad)
        header.pack(fill="x", pady=(0, 10))
        ttk.Label(header, text="MRP_LOCAL", style="Head.TLabel").pack(anchor="w")
        ttk.Label(header, text="Painel Administrativo do Servidor", style="SubHead.TLabel").pack(anchor="w")
        ttk.Label(header, text=f"Raiz detectada: {self.repo_root}", style="SubHead.TLabel").pack(anchor="w", pady=(2, 0))

        cards = ttk.Frame(root_pad)
        cards.pack(fill="x")

        status_card = ttk.Frame(cards, style="Card.TFrame", padding=12)
        status_card.pack(fill="x", pady=(0, 10))
        ttk.Label(status_card, text="Status Operacional", style="CardTitle.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))
        for i, key in enumerate(("Porta 8765", "Frontend", "Modo Automatico", "Manutencao")):
            ttk.Label(status_card, text=key + ":", style="CardText.TLabel").grid(row=i + 1, column=0, sticky="w", padx=(0, 8), pady=1)
            lbl = ttk.Label(status_card, text="-", style="CardText.TLabel")
            lbl.grid(row=i + 1, column=1, sticky="w", pady=1)
            self.status_vars[key] = lbl

        body = ttk.Frame(root_pad)
        body.pack(fill="both", expand=True)

        left = ttk.Frame(body)
        left.pack(side="left", fill="y", padx=(0, 10))
        right = ttk.Frame(body)
        right.pack(side="left", fill="both", expand=True)

        user_card = ttk.Frame(left, style="Card.TFrame", padding=12)
        user_card.pack(fill="x", pady=(0, 10))
        ttk.Label(user_card, text="Acoes de Usuario", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Button(user_card, text="Abrir Sistema no Navegador", command=self.open_system).pack(fill="x", pady=2)
        ttk.Button(user_card, text="Ver Status", command=lambda: self.run_service("mrp_frontend_status.ps1", "VER_STATUS")).pack(fill="x", pady=2)
        ttk.Button(user_card, text="Healthcheck", command=lambda: self.run_service("mrp_frontend_healthcheck.ps1", "HEALTHCHECK")).pack(fill="x", pady=2)
        ttk.Button(user_card, text="Sair", command=self.root.destroy).pack(fill="x", pady=2)

        admin_card = ttk.Frame(left, style="Card.TFrame", padding=12)
        admin_card.pack(fill="x")
        ttk.Label(admin_card, text="Acoes Administrativas", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))
        self.admin_status = ttk.Label(admin_card, text="", style="CardText.TLabel")
        self.admin_status.pack(anchor="w", pady=(0, 8))
        ttk.Button(admin_card, text="Entrar como Admin", command=self.admin_login, style="Accent.TButton").pack(fill="x", pady=(0, 8))

        def add_admin_btn(text: str, fn):
            b = ttk.Button(admin_card, text=text, command=fn)
            b.pack(fill="x", pady=2)
            self.admin_buttons.append(b)

        add_admin_btn("Iniciar Sistema", lambda: self.admin_action("INICIAR", lambda: self.run_service("mrp_frontend_start.ps1", "INICIAR")))
        add_admin_btn("Desativar Sistema", lambda: self.admin_action("DESATIVAR", lambda: self.run_service("mrp_frontend_stop.ps1", "DESATIVAR")))
        add_admin_btn("Reiniciar Sistema", lambda: self.admin_action("REINICIAR", self.restart_service))
        add_admin_btn("Zerar Execucao", lambda: self.admin_action("ZERAR", lambda: self.run_service("mrp_zerar_execucao.ps1", "ZERAR")))
        add_admin_btn("Ativar Modo Automatico", lambda: self.admin_action("AUTO_ON", lambda: self.update_auto_mode(True, "running", False, False, "Ativacao admin local")))
        add_admin_btn("Desativar Modo Automatico", lambda: self.admin_action("AUTO_OFF", lambda: self.update_auto_mode(False, "stopped", False, False, "Desativacao admin local")))
        add_admin_btn("Entrar em Manutencao", lambda: self.admin_action("MANUT_ON", lambda: self.update_auto_mode(False, "maintenance", True, False, "Manutencao admin local")))
        add_admin_btn("Sair da Manutencao", lambda: self.admin_action("MANUT_OFF", lambda: self.update_auto_mode(False, "stopped", False, False, "Fim manutencao admin local")))

        self.output = ScrolledText(right, font=("Consolas", 10), wrap="word", bg="#0f151d", fg="#dbe8f9", insertbackground="#dbe8f9", borderwidth=0)
        self.output.pack(fill="both", expand=True)
        self.append("Painel iniciado.")
        self.append(f"Raiz detectada: {self.repo_root}")
        self.append("Painel local do servidor - nao e interface de usuario final.")
        self.set_admin_enabled(False)

    def append(self, text: str) -> None:
        if not self.output:
            return
        self.output.insert(END, text + "\n")
        self.output.see(END)

    def _load_port(self) -> int:
        p = self.config_dir / "mrp_local.env.json"
        if p.exists():
            try:
                cfg = json.loads(p.read_text(encoding="utf-8"))
                return int(cfg.get("frontend", {}).get("port", 8765))
            except Exception:
                return 8765
        return 8765

    def _port_open(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.6)
            return s.connect_ex(("127.0.0.1", self.port)) == 0

    def _read_auto_mode(self) -> dict:
        default = {
            "version": "v0.1.049",
            "auto_enabled": False,
            "desired_state": "stopped",
            "maintenance_mode": False,
            "locked": False,
            "last_changed_by": "admin",
            "last_changed_at": "EXEMPLO",
            "reason": "EXEMPLO",
        }
        if self.auto_mode_file.exists():
            try:
                data = json.loads(self.auto_mode_file.read_text(encoding="utf-8"))
                default.update(data)
            except Exception:
                pass
        return default

    def refresh_status_card(self) -> None:
        is_open = self._port_open()
        auto = self._read_auto_mode()
        self.status_vars["Porta 8765"].configure(text="ocupada" if is_open else "livre")
        self.status_vars["Frontend"].configure(text="ONLINE" if is_open else "OFFLINE")
        self.status_vars["Modo Automatico"].configure(text="ATIVO" if auto.get("auto_enabled") else "DESATIVADO")
        self.status_vars["Manutencao"].configure(text="SIM" if auto.get("maintenance_mode") else "NAO")

        if self.auth_file.exists():
            self.admin_status.configure(text="Credencial admin local configurada.")
        else:
            self.admin_status.configure(text="Credencial admin ausente. Rode: python 03-vs/scripts/painel/mrp_admin_auth_setup.py")
            self.set_admin_enabled(False)

    def open_system(self) -> None:
        url = f"http://127.0.0.1:{self.port}"
        webbrowser.open(url, new=1, autoraise=True)
        self.append(f"Abrindo: {url}")
        self.log_admin("ABRIR_SISTEMA", "OK", url)

    def _ps_script(self, name: str) -> Path:
        return self.repo_root / "03-vs" / "scripts" / "servicos" / name

    def run_service(self, script_name: str, action: str) -> tuple[bool, str]:
        p = self._ps_script(script_name)
        if not p.exists():
            msg = f"Script nao encontrado: {p}"
            self.append(msg)
            self.log_admin(action, "ERRO", msg)
            return False, msg

        cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(p)]
        self.append("> " + " ".join(cmd))
        cp = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        combined = ((cp.stdout or "") + (cp.stderr or "")).strip()
        if combined:
            self.append(combined)
        ok = cp.returncode == 0
        self.log_admin(action, "OK" if ok else "ERRO", f"exit={cp.returncode}")
        self.refresh_status_card()
        return ok, combined

    def restart_service(self) -> tuple[bool, str]:
        ok1, t1 = self.run_service("mrp_frontend_stop.ps1", "RESTART_STOP")
        ok2, t2 = self.run_service("mrp_frontend_start.ps1", "RESTART_START")
        ok = ok1 and ok2
        self.log_admin("REINICIAR", "OK" if ok else "ERRO", "stop+start")
        return ok, f"{t1}\n{t2}"

    def set_admin_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for b in self.admin_buttons:
            b.configure(state=state)
        self.admin_unlocked = enabled

    def admin_login(self) -> None:
        if not self.auth_file.exists():
            messagebox.showwarning(
                "Credencial nao configurada",
                "Credencial admin local ainda nao configurada.\nRode:\npython 03-vs/scripts/painel/mrp_admin_auth_setup.py",
            )
            self.log_admin("ADMIN_LOGIN", "NEGADO", "credencial_inexistente")
            return
        data = self._read_auth()
        if not data:
            messagebox.showerror("Erro", "Falha ao ler credencial admin local.")
            self.log_admin("ADMIN_LOGIN", "ERRO", "falha_leitura_credencial")
            return

        dlg = AdminAuthDialog(self.root)
        self.root.wait_window(dlg)
        secret = dlg.result
        if not secret:
            self.log_admin("ADMIN_LOGIN", "CANCELADO", "cancelado")
            return
        if self._verify_secret(secret, data):
            self.set_admin_enabled(True)
            self.admin_status.configure(text="Sessao admin ativa.")
            self.append("[OK] Sessao admin desbloqueada.")
            self.log_admin("ADMIN_LOGIN", "OK", "autenticado")
        else:
            messagebox.showerror("Falha", "Credencial invalida.")
            self.log_admin("ADMIN_LOGIN", "NEGADO", "credencial_invalida")

    def admin_action(self, action: str, fn) -> None:
        if not self.admin_unlocked:
            messagebox.showwarning("Bloqueado", "Acao administrativa bloqueada. Use 'Entrar como Admin'.")
            self.log_admin(action, "NEGADO", "admin_nao_autenticado")
            return
        try:
            ok, _ = fn()
            self.append(f"[{'OK' if ok else 'ERRO'}] {action}")
        except Exception as exc:
            self.append(f"[ERRO] {action}: {exc}")
            self.log_admin(action, "ERRO", str(exc))

    def _read_auth(self) -> dict | None:
        try:
            return json.loads(self.auth_file.read_text(encoding="utf-8"))
        except Exception:
            return None

    def _verify_secret(self, provided: str, data: dict) -> bool:
        try:
            salt = bytes.fromhex(str(data["salt"]))
            iterations = int(data["iterations"])
            expected = str(data["password_hash"])
        except Exception:
            return False
        got = hashlib.pbkdf2_hmac("sha256", provided.encode("utf-8"), salt, iterations).hex()
        return hmac.compare_digest(got, expected)

    def update_auto_mode(self, auto_enabled: bool, desired_state: str, maintenance_mode: bool, locked: bool, reason: str) -> tuple[bool, str]:
        valid = {"running", "stopped", "maintenance", "locked"}
        if desired_state not in valid:
            return False, "desired_state invalido"

        data = self._read_auto_mode()
        data.update(
            {
                "version": "v0.1.049",
                "auto_enabled": bool(auto_enabled),
                "desired_state": desired_state,
                "maintenance_mode": bool(maintenance_mode),
                "locked": bool(locked),
                "last_changed_by": self.user_name,
                "last_changed_at": utc_now_iso(),
                "reason": reason,
            }
        )
        self.local_dir.mkdir(parents=True, exist_ok=True)
        self.auto_mode_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        self.log_admin("AUTO_MODE_UPDATE", "OK", f"{desired_state}|auto={auto_enabled}|maint={maintenance_mode}|locked={locked}")
        self.refresh_status_card()
        return True, "ok"

    def log_admin(self, action: str, status: str, result: str) -> None:
        self.logs_admin_dir.mkdir(parents=True, exist_ok=True)
        line = f"{utc_now_iso()} | action={action} | status={status} | user={self.user_name} | result={result}\n"
        with self.log_file.open("a", encoding="utf-8", newline="\n") as f:
            f.write(line)

    def run(self) -> int:
        self.root.mainloop()
        return 0


def main() -> int:
    app = MrpPainel()
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
