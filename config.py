from dotenv import load_dotenv
import os
"""
load_dotenv()   

DB_HOST     = os.getenv("DB_HOST",     "localhost")
DB_NAME     = os.getenv("DB_NAME",     "dtc-analyser")
DB_USER     = os.getenv("DB_USER",     "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_POOL_NAME = os.getenv("DB_POOL_NAME", "mypool")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 5))
DB_PORT      = int(os.getenv("DB_PORT", "3306"))


BATCH_SIZE               = int(os.getenv("BATCH_SIZE",               1))
SCAN_LOG_FILE            = os.getenv("SCAN_LOG_FILE",            "log.txt")
MEMORY_THRESHOLD_PERCENT = int(os.getenv("MEMORY_THRESHOLD_PERCENT", 80))
LOCAL_DIR                = os.getenv("LOCAL_DIR",                "local_files")

KM_CHANNEL       = os.getenv("KM_CHANNEL",       "KILOMETRAGE")
GROUPE_THRESHOLD = int(os.getenv("GROUPE_THRESHOLD", 45))
DB_CONFIG = {
    "host":     DB_HOST,
    "database": DB_NAME,
    "user":     DB_USER,
    "password": DB_PASSWORD,
}

CHECKPOINT_FILE = os.getenv("CHECKPOINT_FILE", "checkpoint.txt")
SCAN_LOG_FILE   = os.getenv("SCAN_LOG_FILE",   "scan_log.txt")

ROOT_DIR    = os.getenv(r"ROOT_DIR",    r"MDF_files")
MDF_FILTER  = os.getenv("MDF_FILTER",  "_")
MODULE_NAME = os.getenv("MODULE_NAME", "mdf_file_scanner")
APP_TITLE    = os.getenv("APP_TITLE", "DTC Dashboard")
APP_DEBUG    = os.getenv("APP_DEBUG", "false").lower() == "true"

JOB1_PATH    = os.getenv("JOB1_PATH", "jobs/job1.exe")
JOB1_LABEL   = os.getenv("JOB1_LABEL", "Job 1 — Acquisition")
JOB2_PATH    = os.getenv("JOB2_PATH", "jobs/job2.exe")
JOB2_LABEL   = os.getenv("JOB2_LABEL", "Job 2 — Traitement")

CONTROL_PASSWORD = os.getenv("CONTROL_PASSWORD", "admin123")
"""

import tomllib
from pathlib import Path

CONFIG_FILE = next(Path(__file__).parent.glob("*.toml"))
with CONFIG_FILE.open("rb") as file:
    config = tomllib.load(file)
if not CONFIG_FILE.exists():
    import streamlit as st
    config = st.secrets


DB_HOST = config["database"].get("host", "localhost")
DB_NAME = config["database"].get("name", "dtc-analyser")
DB_USER = config["database"].get("user", "root")
DB_PASSWORD = config["database"].get("password", "")
DB_POOL_NAME = config["database"].get("pool_name", "mypool")
DB_POOL_SIZE = int(config["database"].get("pool_size", 5))
DB_PORT = int(config["database"].get("port", 3306))

DB_CONFIG = {
    "host": DB_HOST,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "port": DB_PORT,
}


BATCH_SIZE = int(config["processing"].get("batch_size", 1))
MEMORY_THRESHOLD_PERCENT = int(
    config["processing"].get("memory_threshold_percent", 80)
)
GROUPE_THRESHOLD = int(config["processing"].get("groupe_threshold", 45))
KM_CHANNEL = config["processing"].get("km_channel", "KILOMETRAGE")


LOCAL_DIR = config["files"].get("local_dir", "local_files")
ROOT_DIR = config["files"].get("root_dir", "MDF_files")
CHECKPOINT_FILE = config["files"].get("checkpoint_file", "checkpoint.txt")
SCAN_LOG_FILE = config["files"].get("scan_log_file", "scan_log.txt")
MDF_FILTER = config["files"].get("mdf_filter", "_")
MODULE_NAME = config["files"].get("module_name", "mdf_file_scanner")


APP_TITLE = config["application"].get("title", "DTC Dashboard")
APP_DEBUG = bool(config["application"].get("debug", False))


JOB1_PATH = config["jobs"]["job1"].get("path", "jobs/job1.exe")
JOB1_LABEL = config["jobs"]["job1"].get("label", "Job 1 - Acquisition")

JOB2_PATH = config["jobs"]["job2"].get("path", "jobs/job2.exe")
JOB2_LABEL = config["jobs"]["job2"].get("label", "Job 2 - Traitement")


CONTROL_PASSWORD = config["security"].get("control_password", "admin123")
