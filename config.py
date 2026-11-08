from dotenv import load_dotenv
import os

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