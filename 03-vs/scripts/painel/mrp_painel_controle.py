#!/usr/bin/env python3
"""
MRP_LOCAL - Painel Administrativo Local do Servidor
Interface local em tkinter para controle operacional e preparacao de modo automatico.
"""

from __future__ import annotations

import getpass
import hmac
import hashlib
import json
import os
import socket
import subprocess
import sys
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from tkinter import BOTH, DISABLED, END, LEFT, NORMAL, RIGHT, TOP, VERTICAL, Button, Frame, Label, Text, Tk, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def resolve_repo_root() -> Path:
    # 03-vs/scripts/painel -> subir 3 niveis
    return Path(__file__).resolve().parents[3]


class MrpPainel:
    def __init__(self) -> None:
        self.repo_root = resolve_repo_root()
        self.config_dir = self.repo_root / "01-mrp" / "config"
        self.local_config_dir = self.config_dir / "local"
        self.logs_admin_dir = self.repo_root / "01-mrp" / "logs" / "admin"
        self.auth_file = self.local_config_dir / "admin_auth.local.json"
        self.auto_mode_file = self.local_config_dir / "mrp_auto_mode.local.json"
        self.admin_log_file = self.logs_admin_dir / "painel_admin.log"
        self.user_name = getpass.getuser()
        self.port = self._load_port()
        self.root = Tk()
        self.root.title("MRP_LOCAL - Painel Administrativo do Servidor")
        self.root.geometry("980x640")
        self.root.minsize(880, 560)
        self.output: ScrolledText
        self.status_label: Label
        self.admin_status_label: Label
        self._build_ui()
        self.refresh_status()

    def _load_port(self) -> int:
        cfg_path = self.config_dir / "mrp_local.env.json"
        if cfg_path.exists():
            try:
                cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
                return int(cfg.get("frontend", {}).get("port", 8765))
            except Exception:
                return 8765
        return 8765

    def _build_ui(self) -> None:
        header = Label(
            self.root,
            text="MRP_LOCAL - Painel Administrativo do Servidor",
            font=("Segoe UI", 14, "bold"),
        )
        header.pack(anchor="w", padx=12, pady=(12, 6))

        self.status_label = Label(self.root, text="", font=("Segoe UI", 10))
        self.status_label.pack(anchor="w", padx=12, pady=(0, 8))

        top_actions = Frame(self.root)
        top_actions.pack(fill="x", padx=12, pady=4)
        Button(top_actions, text="Abrir Sistema no Navegador", width=30, command=self.open_system).pack(side=LEFT, padx=4)
        Button(top_actions, text="Ver Status", width=18, command=lambda: self.run_service_script("mrp_frontend_status.ps1", "VER_STATUS")).pack(side=LEFT, padx=4)
        Button(top_actions, text="Healthcheck", width=18, command=lambda: self.run_service_script("mrp_frontend_healthcheck.ps1", "HEALTHCHECK")).pack(side=LEFT, padx=4)
        Button(top_actions, text="Sair", width=12, command=self.root.destroy).pack(side=RIGHT, padx=4)

        admin_frame = Frame(self.root)
        admin_frame.pack(fill="x", padx=12, pady=(8, 6))
        self.admin_status_label = Label(admin_frame, text="", fg="#7a3b00", font=("Segoe UI", 10, "bold"))
        self.admin_status_label.pack(anchor="w", pady=(0, 4))

        row1 = Frame(admin_frame)
        row1.pack(fill="x", pady=2)
        Button(row1, text="Iniciar Sistema", width=22, command=lambda: self._admin_action("INICIAR_SISTEMA", lambda: self.run_service_script("mrp_frontend_start.ps1", "INICIAR_SISTEMA"))).pack(side=LEFT, padx=4)
        Button(row1, text="Desativar Sistema", width=22, command=lambda: self._admin_action("DESATIVAR_SISTEMA", lambda: self.run_service_script("mrp_frontend_stop.ps1", "DESATIVAR_SISTEMA"))).pack(side=LEFT, padx=4)
        Button(row1, text="Reiniciar Sistema", width=22, command=lambda: self._admin_action("REINICIAR_SISTEMA", self.restart_system)).pack(side=LEFT, padx=4)
        Button(row1, text="Zerar Execucao", width=22, command=lambda: self._admin_action("ZERAR_EXECUCAO", lambda: self.run_service_script("mrp_zerar_execucao.ps1", "ZERAR_EXECUCAO"))).pack(side=LEFT, padx=4)

        row2 = Frame(admin_frame)
        row2.pack(fill="x", pady=2)
        Button(row2, text="Ativar Modo Automatico", width=22, command=lambda: self._admin_action("ATIVAR_MODO_AUTOMATICO", lambda: self.update_auto_mode(True, "running", False, False, "Ativacao administrativa local"))).pack(side=LEFT, padx=4)
        Button(row2, text="Desativar Modo Automatico", width=22, command=lambda: self._admin_action("DESATIVAR_MODO_AUTOMATICO", lambda: self.update_auto_mode(False, "stopped", False, False, "Desativacao administrativa local"))).pack(side=LEFT, padx=4)
        Button(row2, text="Entrar em Manutencao", width=22, command=lambda: self._admin_action("ENTRAR_MANUTENCAO", lambda: self.update_auto_mode(False, "maintenance", True, False, "Manutencao planejada"))).pack(side=LEFT, padx=4)
        Button(row2, text="Sair da Manutencao", width=22, command=lambda: self._admin_action("SAIR_MANUTENCAO", lambda: self.update_auto_mode(False, "stopped", False, False, "Fim da manutencao"))).pack(side=LEFT, padx=4)

        self.output = ScrolledText(self.root, font=("Consolas", 10), wrap="word")
        self.output.pack(fill=BOTH, expand=True, padx=12, pady=(6, 12))
        self.append_output("Painel iniciado.")
        self.append_output(f"Repositorio: {self.repo_root}")

    def append_output(self, text: str) -> None:
        self.output.insert(END, text + "\n")
        self.output.see(END)

    def _is_port_open(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.7)
            return sock.connect_ex(("127.0.0.1", port)) == 0

    def refresh_status(self) -> None:
        port_open = self._is_port_open(self.port)
        frontend = "ONLINE" if port_open else "OFFLINE"
        self.status_label.configure(text=f"Porta {self.port}: {'ocupada' if port_open else 'livre'} | Frontend: {frontend}")
        if self.auth_file.exists():
            self.admin_status_label.configure(text="Credencial admin local: configurada.")
        else:
            self.admin_status_label.configure(
                text="Credencial admin ainda nao configurada. Rode: python 03-vs/scripts/painel/mrp_admin_auth_setup.py"
            )

    def open_system(self) -> None:
        url = f"http://127.0.0.1:{self.port}"
        webbrowser.open(url, new=1, autoraise=True)
        self.append_output(f"Abrindo navegador: {url}")
        self.log_admin("ABRIR_SISTEMA_NAVEGADOR", "OK", f"url={url}")

    def service_script_path(self, script_name: str) -> Path:
        return self.repo_root / "03-vs" / "scripts" / "servicos" / script_name

    def run_service_script(self, script_name: str, action: str) -> tuple[bool, str]:
        script_path = self.service_script_path(script_name)
        if not script_path.exists():
            msg = f"Script nao encontrado: {script_path}"
            self.append_output(msg)
            self.log_admin(action, "ERRO", msg)
            return False, msg

        cmd = [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script_path),
        ]
        self.append_output(f"> {' '.join(cmd)}")
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        output = (proc.stdout or "") + (proc.stderr or "")
        if output.strip():
            self.append_output(output.rstrip())
        ok = proc.returncode == 0
        self.log_admin(action, "OK" if ok else "ERRO", f"exit_code={proc.returncode}")
        self.refresh_status()
        return ok, output

    def restart_system(self) -> tuple[bool, str]:
        ok_stop, out_stop = self.run_service_script("mrp_frontend_stop.ps1", "RESTART_STOP")
        ok_start, out_start = self.run_service_script("mrp_frontend_start.ps1", "RESTART_START")
        ok = ok_stop and ok_start
        text = out_stop + "\n" + out_start
        self.log_admin("REINICIAR_SISTEMA", "OK" if ok else "ERRO", "stop+start executados")
        return ok, text

    def read_auth_data(self) -> dict | None:
        if not self.auth_file.exists():
            return None
        try:
            return json.loads(self.auth_file.read_text(encoding="utf-8"))
        except Exception:
            return None

    def verify_admin_secret(self, provided: str, data: dict) -> bool:
        try:
            salt = bytes.fromhex(data["salt"])
            iterations = int(data["iterations"])
            expected = str(data["password_hash"]).lower()
        except Exception:
            return False

        digest = hashlib.pbkdf2_hmac("sha256", provided.encode("utf-8"), salt, iterations).hex().lower()
        return secrets_compare(digest, expected)

    def _admin_action(self, action_name: str, func) -> None:
        auth_data = self.read_auth_data()
        if not auth_data:
            message = "Credencial admin local nao configurada. Rode:\npython 03-vs/scripts/painel/mrp_admin_auth_setup.py"
            messagebox.showwarning("Admin nao configurado", message)
            self.append_output(message)
            self.log_admin(action_name, "NEGADO", "credencial_admin_nao_configurada")
            return

        secret = simpledialog.askstring("Autenticacao Admin", "Informe PIN/senha administrativa:", show="*")
        if not secret:
            self.log_admin(action_name, "CANCELADO", "usuario_cancelou_autenticacao")
            return

        if not self.verify_admin_secret(secret, auth_data):
            messagebox.showerror("Falha", "Credencial invalida.")
            self.log_admin(action_name, "NEGADO", "credencial_invalida")
            return

        try:
            result = func()
            if isinstance(result, tuple):
                ok = bool(result[0])
            else:
                ok = bool(result)
            if ok:
                self.append_output(f"[OK] {action_name}")
            else:
                self.append_output(f"[ERRO] {action_name}")
        except Exception as exc:
            self.append_output(f"[ERRO] {action_name}: {exc}")
            self.log_admin(action_name, "ERRO", str(exc))

    def read_auto_mode(self) -> dict:
        if self.auto_mode_file.exists():
            try:
                data = json.loads(self.auto_mode_file.read_text(encoding="utf-8"))
                return data
            except Exception:
                pass
        return {
            "version": "v0.1.049",
            "auto_enabled": False,
            "desired_state": "stopped",
            "maintenance_mode": False,
            "locked": False,
            "last_changed_by": "admin",
            "last_changed_at": "EXEMPLO",
            "reason": "EXEMPLO",
        }

    def update_auto_mode(
        self,
        auto_enabled: bool,
        desired_state: str,
        maintenance_mode: bool,
        locked: bool,
        reason: str,
    ) -> tuple[bool, str]:
        valid_states = {"running", "stopped", "maintenance", "locked"}
        if desired_state not in valid_states:
            msg = f"desired_state invalido: {desired_state}"
            self.append_output(msg)
            return False, msg

        data = self.read_auto_mode()
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
        self.local_config_dir.mkdir(parents=True, exist_ok=True)
        self.auto_mode_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        self.append_output(f"Auto mode atualizado: auto_enabled={data['auto_enabled']} desired_state={data['desired_state']} maintenance_mode={data['maintenance_mode']} locked={data['locked']}")
        self.log_admin("AUTO_MODE_UPDATE", "OK", f"auto_enabled={data['auto_enabled']} desired_state={data['desired_state']} maintenance_mode={data['maintenance_mode']} locked={data['locked']}")
        return True, "ok"

    def log_admin(self, action: str, status: str, result: str) -> None:
        self.logs_admin_dir.mkdir(parents=True, exist_ok=True)
        line = f"{utc_now_iso()} | action={action} | status={status} | user={self.user_name} | result={result}\n"
        with self.admin_log_file.open("a", encoding="utf-8", newline="\n") as f:
            f.write(line)

    def run(self) -> None:
        self.root.mainloop()


def secrets_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)


def main() -> int:
    app = MrpPainel()
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
