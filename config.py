import os
import streamlit as st

# ─────────────────────────────────────────────
# Helper : récupérer secrets (Streamlit ou .env)
# ─────────────────────────────────────────────
def get_secret(key, section=None, default=None):
    try:
        if section:
            return st.secrets[section][key]
        return st.secrets[key]
    except Exception:
        return os.getenv(key, default)

# ─────────────────────────────────────────────
# Base de données (Supabase PostgreSQL)
# ─────────────────────────────────────────────
DB_HOST = get_secret("host", "database", "localhost")
DB_NAME = get_secret("name", "database", "postgres")
DB_USER = get_secret("user", "database", "postgres")
DB_PASSWORD = get_secret("password", "database", "")
DB_PORT = int(get_secret("port", "database", 5432))
DB_SSLMODE = get_secret("sslmode", "database", "require")

DB_POOL_SIZE = int(get_secret("pool_size", "database", 5))

DATABASE_URL = get_secret("DATABASE_URL", default=None)

DB_CONFIG = {
    "host": DB_HOST,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "port": DB_PORT,
    "sslmode": DB_SSLMODE
}

# ─────────────────────────────────────────────
# Application
# ─────────────────────────────────────────────
APP_TITLE = get_secret("title", "application", "DTC Dashboard")
APP_DEBUG = str(get_secret("debug", "application", "false")).lower() == "true"

# ─────────────────────────────────────────────
# Jobs
# ─────────────────────────────────────────────
JOB1_PATH = get_secret("job1_path", "jobs", "jobs/job1.exe")
JOB1_LABEL = get_secret("job1_label", "jobs", "Job 1 — Acquisition")

JOB2_PATH = get_secret("job2_path", "jobs", "jobs/job2.exe")
JOB2_LABEL = get_secret("job2_label", "jobs", "Job 2 — Traitement")

# ─────────────────────────────────────────────
# Sécurité
# ─────────────────────────────────────────────
CONTROL_PASSWORD = get_secret("control_password", "security", "admin123")

# ─────────────────────────────────────────────
# MDF / Scan (optionnel local)
# ─────────────────────────────────────────────
KM_CHANNEL = os.getenv("KM_CHANNEL", "KILOMETRAGE")
GROUPE_THRESHOLD = int(os.getenv("GROUPE_THRESHOLD", 45))

ROOT_DIR = os.getenv("ROOT_DIR", "MDF_files")
MDF_FILTER = os.getenv("MDF_FILTER", "_")
MODULE_NAME = os.getenv("MODULE_NAME", "mdf_file_scanner")

CHECKPOINT_FILE = os.getenv("CHECKPOINT_FILE", "checkpoint.txt")
SCAN_LOG_FILE = os.getenv("SCAN_LOG_FILE", "scan_log.txt")

# ─────────────────────────────────────────────
# Batch / perf
# ─────────────────────────────────────────────
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1))
MEMORY_THRESHOLD_PERCENT = int(os.getenv("MEMORY_THRESHOLD_PERCENT", 80))
LOCAL_DIR = os.getenv("LOCAL_DIR", "local_files")