"""
pages/controle.py — Page Contrôle (protégée par mot de passe)
  • Édition des variables .env
  • Lancement des deux jobs .exe avec suivi en temps réel
"""
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime

import streamlit as st

import config
from utils.style import section_title

# ── Chemin absolu vers le fichier .env ────────────────────────
ENV_PATH = Path(__file__).parent.parent / ".env"

# Clés du .env éditables depuis l'interface (label, clé env, type)
ENV_FIELDS = [
    # ── Base de données ──────────────────────────────────────
    ("DB_HOST",          "Hôte MySQL",                  "text"),
    ("DB_NAME",          "Nom de la base",              "text"),
    ("DB_USER",          "Utilisateur MySQL",           "text"),
    ("DB_PASSWORD",      "Mot de passe MySQL",          "password"),
    ("DB_PORT",          "Port MySQL",                  "text"),
    ("DB_POOL_SIZE",     "Taille du pool de connexions","text"),
    # ── Jobs ─────────────────────────────────────────────────
    ("JOB1_PATH",        "Chemin job 1 (.exe)",         "text"),
    ("JOB1_LABEL",       "Libellé job 1",               "text"),
    ("JOB2_PATH",        "Chemin job 2 (.exe)",         "text"),
    ("JOB2_LABEL",       "Libellé job 2",               "text"),
    # ── Application ──────────────────────────────────────────
    ("APP_TITLE",        "Titre de l'application",      "text"),
    ("APP_DEBUG",        "Mode debug (true/false)",     "text"),
]


# ═══════════════════════════════════════════════════════════════
# HELPERS — .env
# ═══════════════════════════════════════════════════════════════

def _read_env() -> dict[str, str]:
    """Lit le fichier .env et retourne un dict clé→valeur (sans commentaires)."""
    env = {}
    if not ENV_PATH.exists():
        return env
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip()
    return env


def _write_env(new_values: dict[str, str]):
    """
    Met à jour le fichier .env en conservant les commentaires et
    en ajoutant les clés manquantes à la fin.
    """
    if not ENV_PATH.exists():
        ENV_PATH.write_text("", encoding="utf-8")

    lines   = ENV_PATH.read_text(encoding="utf-8").splitlines()
    updated = set()
    result  = []

    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.split("=", 1)[0].strip()
            if key in new_values:
                result.append(f"{key}={new_values[key]}")
                updated.add(key)
            else:
                result.append(line)
        else:
            result.append(line)

    # Clés absentes du fichier → on les ajoute à la fin
    for key, val in new_values.items():
        if key not in updated:
            result.append(f"{key}={val}")

    ENV_PATH.write_text("\n".join(result) + "\n", encoding="utf-8")


# ═══════════════════════════════════════════════════════════════
# HELPERS — Jobs
# ═══════════════════════════════════════════════════════════════

def _run_job(job_key: int, exe_path: str):
    """
    Lance un exécutable dans un thread séparé.
    Stocke l'état dans st.session_state sous job{N}_*.
    """
    sk_status = f"job{job_key}_status"
    sk_stdout = f"job{job_key}_stdout"
    sk_stderr = f"job{job_key}_stderr"
    sk_start  = f"job{job_key}_start"

    st.session_state[sk_status] = "running"
    st.session_state[sk_stdout] = ""
    st.session_state[sk_stderr] = ""
    st.session_state[sk_start]  = datetime.now()

    def _target():
        try:
            proc = subprocess.Popen(
                [exe_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(Path(exe_path).parent),
            )
            stdout, stderr = proc.communicate()
            st.session_state[sk_stdout] = stdout
            st.session_state[sk_stderr] = stderr
            st.session_state[sk_status] = (
                "success" if proc.returncode == 0 else "error"
            )
        except FileNotFoundError:
            st.session_state[sk_stderr] = f"❌ Exécutable introuvable : {exe_path}"
            st.session_state[sk_status] = "error"
        except Exception as exc:
            st.session_state[sk_stderr] = f"❌ Erreur : {exc}"
            st.session_state[sk_status] = "error"

    t = threading.Thread(target=_target, daemon=True)
    t.start()


def _init_job_state(key: int):
    for suffix, default in [("status", "idle"), ("stdout", ""), ("stderr", ""), ("start", None)]:
        if f"job{key}_{suffix}" not in st.session_state:
            st.session_state[f"job{key}_{suffix}"] = default


def _job_card(job_key: int, label: str, exe_path: str):
    """Affiche la carte d'un job avec bouton de lancement et résultats."""
    _init_job_state(job_key)

    status  = st.session_state[f"job{job_key}_status"]
    stdout  = st.session_state[f"job{job_key}_stdout"]
    stderr  = st.session_state[f"job{job_key}_stderr"]
    started = st.session_state[f"job{job_key}_start"]

    # Couleur de bordure selon état
    border_class = {
        "idle":    "",
        "running": "job-card-running",
        "success": "job-card-success",
        "error":   "job-card-error",
    }.get(status, "")

    # ── En-tête de la carte ───────────────────────────────────
    st.markdown(
        f'<div class="job-card {border_class}">',
        unsafe_allow_html=True,
    )

    c_title, c_badge, c_btn = st.columns([3, 1, 1])

    with c_title:
        icon = {"idle":"⏸️","running":"⚙️","success":"✅","error":"❌"}.get(status,"⏸️")
        st.markdown(f"**{icon} {label}**")
        st.caption(f"`{exe_path}`")
        if started:
            st.caption(f"Démarré le {started.strftime('%d/%m/%Y à %H:%M:%S')}")

    with c_badge:
        badge_styles = {
            "idle":    ("⬜ Inactif",  "#6b7080", "#1a1a2e"),
            "running": ("🔄 En cours", "#3ce8ff", "#0d1f2e"),
            "success": ("✅ Succès",   "#4ade80", "#0d2e1a"),
            "error":   ("❌ Erreur",   "#f87171", "#2e0d0d"),
        }
        txt, color, bg = badge_styles.get(status, badge_styles["idle"])
        st.markdown(
            f'<div style="background:{bg};color:{color};border:1px solid {color}55;'
            f'border-radius:20px;padding:4px 12px;font-size:0.78rem;'
            f'font-family:\'Space Mono\',monospace;text-align:center;margin-top:8px">'
            f'{txt}</div>',
            unsafe_allow_html=True,
        )

    with c_btn:
        is_running = status == "running"
        if st.button(
            "▶ Lancer" if not is_running else "⏳ En cours…",
            key=f"btn_job{job_key}",
            disabled=is_running,
        ):
            _run_job(job_key, exe_path)
            st.rerun()

    # ── Sortie console ────────────────────────────────────────
    if stdout or stderr:
        st.markdown("<br>", unsafe_allow_html=True)
        if stdout:
            st.markdown(
                f'<div class="terminal-box">{_escape_html(stdout)}</div>',
                unsafe_allow_html=True,
            )
        if stderr:
            st.markdown(
                f'<div class="terminal-box err">{_escape_html(stderr)}</div>',
                unsafe_allow_html=True,
            )

    # Bouton clear
    if status in ("success", "error"):
        if st.button("🗑 Réinitialiser", key=f"clear_job{job_key}"):
            for suffix in ("status","stdout","stderr","start"):
                st.session_state[f"job{job_key}_{suffix}"] = (
                    "idle" if suffix == "status" else ("" if suffix != "start" else None)
                )
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Auto-refresh si job en cours
    if status == "running":
        time.sleep(1)
        st.rerun()


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
    )


# ═══════════════════════════════════════════════════════════════
# AUTHENTIFICATION
# ═══════════════════════════════════════════════════════════════

def _auth_wall() -> bool:
    """
    Affiche le formulaire de mot de passe.
    Retourne True si l'utilisateur est authentifié.
    """
    if st.session_state.get("ctrl_authenticated"):
        return True

    st.markdown("## ⚙️ Contrôle")
    st.markdown("<br>", unsafe_allow_html=True)

    # Carte de connexion centrée
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown("""
        <div class="metric-card" style="text-align:center">
            <div style="font-size:2.5rem;margin-bottom:12px">🔒</div>
            <div class="metric-label" style="margin-bottom:20px">
                Accès restreint — Authentification requise
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        pwd = st.text_input("Mot de passe", type="password", key="ctrl_pwd_input",
                            placeholder="Saisir le mot de passe…")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔓 Connexion", use_container_width=True):
                if pwd == config.CONTROL_PASSWORD:
                    st.session_state["ctrl_authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Mot de passe incorrect.")
        with col_b:
            if st.button("↩️ Retour", use_container_width=True):
                st.session_state["ctrl_authenticated"] = False

    return False


# ═══════════════════════════════════════════════════════════════
# RENDER PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def render():
    if not _auth_wall():
        return

    st.markdown("## ⚙️ Contrôle")

    # Bouton de déconnexion discret
    if st.button("🔒 Se déconnecter", key="ctrl_logout"):
        st.session_state["ctrl_authenticated"] = False
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    tab_jobs, tab_env = st.tabs(["▶ Exécution des Jobs", "🛠 Variables d'environnement"])

    # ══════════════════════════════════════════════════════════
    # TAB 1 : JOBS
    # ══════════════════════════════════════════════════════════
    with tab_jobs:
        section_title("Lancement des jobs")

        st.info(
            "Chaque job s'exécute de manière asynchrone. "
            "La sortie console apparaît une fois le job terminé."
        )
        st.markdown("<br>", unsafe_allow_html=True)

        _job_card(
            job_key  = 1,
            label    = config.JOB1_LABEL,
            exe_path = config.JOB1_PATH,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        _job_card(
            job_key  = 2,
            label    = config.JOB2_LABEL,
            exe_path = config.JOB2_PATH,
        )

    # ══════════════════════════════════════════════════════════
    # TAB 2 : ÉDITEUR .env
    # ══════════════════════════════════════════════════════════
    with tab_env:
        section_title("Édition du fichier .env")

        if not ENV_PATH.exists():
            st.warning(f"⚠️ Fichier .env introuvable à : `{ENV_PATH}`")
            st.info("Créez un fichier .env à la racine du projet (copiez .env.example).")

        current = _read_env()

        st.markdown(
            f'<div style="color:#6b7080;font-size:0.78rem;margin-bottom:16px">'
            f'📄 Chemin : <code>{ENV_PATH}</code></div>',
            unsafe_allow_html=True,
        )

        # ── Formulaire d'édition ──────────────────────────────
        new_values: dict[str, str] = {}

        # Groupe DB
        section_title("Base de données")
        db_fields = [(k,l,t) for k,l,t in ENV_FIELDS if k.startswith("DB_")]
        col1, col2 = st.columns(2)
        for i, (key, label, field_type) in enumerate(db_fields):
            col = col1 if i % 2 == 0 else col2
            with col:
                if field_type == "password":
                    new_values[key] = st.text_input(
                        label, value=current.get(key, ""),
                        type="password", key=f"env_{key}",
                    )
                else:
                    new_values[key] = st.text_input(
                        label, value=current.get(key, ""),
                        key=f"env_{key}",
                    )

        st.markdown("<br>", unsafe_allow_html=True)

        # Groupe Jobs
        section_title("Chemins des Jobs")
        job_fields = [(k,l,t) for k,l,t in ENV_FIELDS if k.startswith("JOB")]
        col3, col4 = st.columns(2)
        for i, (key, label, _) in enumerate(job_fields):
            col = col3 if i % 2 == 0 else col4
            with col:
                new_values[key] = st.text_input(
                    label, value=current.get(key, ""), key=f"env_{key}",
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Groupe App
        section_title("Application")
        app_fields = [(k,l,t) for k,l,t in ENV_FIELDS if k.startswith("APP_")]
        col5, col6 = st.columns(2)
        for i, (key, label, _) in enumerate(app_fields):
            col = col5 if i % 2 == 0 else col6
            with col:
                new_values[key] = st.text_input(
                    label, value=current.get(key, ""), key=f"env_{key}",
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Boutons d'action ──────────────────────────────────
        col_save, col_preview, col_reset = st.columns([1, 1, 2])

        with col_save:
            if st.button("💾 Sauvegarder .env", use_container_width=True):
                try:
                    _write_env(new_values)
                    st.success("✅ Fichier .env mis à jour avec succès !")
                    st.info(
                        "♻️ Relancez l'application ou cliquez sur **Rafraîchir** "
                        "dans la sidebar pour que les nouvelles valeurs soient prises en compte."
                    )
                except Exception as e:
                    st.error(f"❌ Erreur lors de la sauvegarde : {e}")

        with col_preview:
            if st.button("👁 Aperçu .env", use_container_width=True):
                st.session_state["show_env_preview"] = not st.session_state.get(
                    "show_env_preview", False
                )

        # ── Aperçu brut du fichier .env ───────────────────────
        if st.session_state.get("show_env_preview") and ENV_PATH.exists():
            st.markdown("<br>", unsafe_allow_html=True)
            section_title("Contenu actuel du fichier .env")
            raw = ENV_PATH.read_text(encoding="utf-8")
            # Masque les mots de passe dans l'aperçu
            masked_lines = []
            for line in raw.splitlines():
                if "PASSWORD" in line.upper() and "=" in line:
                    key_part = line.split("=", 1)[0]
                    masked_lines.append(f"{key_part}=••••••••")
                else:
                    masked_lines.append(line)
            st.markdown(
                f'<div class="terminal-box" style="color:#e8ff3c">'
                f'{_escape_html(chr(10).join(masked_lines))}</div>',
                unsafe_allow_html=True,
            )
