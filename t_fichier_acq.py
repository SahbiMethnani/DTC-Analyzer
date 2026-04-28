import os
import mysql.connector
import logging
import getpass
from datetime import datetime
import time
import signal
import sys

import config

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# ── État global ───────────────────────────────────────────────
existing_files       = set()
username             = getpass.getuser()
inserted_file_count  = 0
start_time           = None
debut_traitement     = None
db_connection_global = None
STOP_CAUSE           = "completed"

# ── t_traitement ──────────────────────────────────────────────
def insert_t_traitement(connection, cursor, debut, fin, cause):
    try:
        cursor.execute(
            "INSERT INTO t_traitement (debut, fin, cause_arret, modulename) VALUES (%s, %s, %s, %s)",
            (debut, fin, cause, config.MODULE_NAME)
        )
        connection.commit()
        logging.info("t_traitement inséré avec cause : %s", cause)
    except mysql.connector.Error as err:
        logging.error("Erreur insertion t_traitement : %s", err)
    except Exception as e:
        logging.error("Erreur inattendue t_traitement : %s", e)

# ── Signal handler ────────────────────────────────────────────
def signal_handler(sig, frame):
    global STOP_CAUSE, debut_traitement, db_connection_global
    STOP_CAUSE = "keyboard interrupted"

    overall_time = time.time() - start_time if start_time else 0
    log_entry = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
        f"Arrêt prématuré après {overall_time:.2f}s, {inserted_file_count} fichiers insérés.\n"
    )
    _write_log(log_entry)
    logging.info(log_entry.strip())

    if db_connection_global and debut_traitement:
        try:
            cursor = db_connection_global.cursor()
            insert_t_traitement(db_connection_global, cursor, debut_traitement, datetime.now(), STOP_CAUSE)
            cursor.close()
        except Exception as e:
            logging.error("Erreur insertion t_traitement (signal) : %s", e)

    sys.exit(0)

signal.signal(signal.SIGINT,  signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# ── Helpers log ───────────────────────────────────────────────
def _write_log(entry: str):
    try:
        with open(config.SCAN_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        logging.error("Erreur écriture log : %s", e)

def log_directory_scan(directory):
    _write_log(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Répertoire scanné : {directory}\n")
    logging.info("[dir]: %s", directory)

def log_file_insertion(entity, insertion_date):
    _write_log(f"{insertion_date} - Fichier inséré : {entity.file_path}\n")

# ── Checkpoint ────────────────────────────────────────────────
def update_checkpoint(entity):
    try:
        with open(config.CHECKPOINT_FILE, "w", encoding="utf-8") as f:
            f.write(f"{entity.file_path} | {entity.creation_date}\n")
        logging.info("Checkpoint mis à jour : %s", entity.file_path)
    except Exception as e:
        logging.error("Erreur checkpoint : %s", e)

# ── Entité MDF ────────────────────────────────────────────────
class MdfEntity:
    def __init__(self, file_path, moyen, creation_date, nbdefaut=0):
        self.file_path     = file_path
        self.moyen         = moyen
        self.creation_date = creation_date
        self.nbdefaut      = nbdefaut

def extract_moyen(file_path):
    normalized = os.path.normpath(file_path)
    prefix     = os.path.normpath(config.ROOT_DIR)

    relative = normalized[len(prefix):].lstrip(os.sep) if normalized.startswith(prefix) else normalized
    folder   = relative.split(os.sep)[0]
    parts    = folder.split('_')

    if len(parts) >= 3:
        try:
            return f"{parts[2]}_{parts[-1].lstrip('-')}"
        except Exception:
            return parts[2]
    return None

# ── Insertion DB ──────────────────────────────────────────────
def insert_file_into_db(entity, db_connection):
    global inserted_file_count
    cursor = db_connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO t_acq_files (path, moyen, datecreated, nbdefaut, invalid) VALUES (%s, %s, %s, %s, %s)",
            (entity.file_path, entity.moyen, entity.creation_date, entity.nbdefaut, False)
        )
        db_connection.commit()
        inserted_file_count += 1
        update_checkpoint(entity)
    except mysql.connector.Error as err:
        logging.error("Erreur MySQL pour %s : %s", entity.file_path, err)
    except Exception as e:
        logging.error("Erreur insertion %s : %s", entity.file_path, e)
    finally:
        cursor.close()

# ── Scan répertoire ───────────────────────────────────────────
def process_directory(root_dir, db_connection):
    global STOP_CAUSE
    dir_queue = [root_dir]

    while dir_queue:
        current_dir = dir_queue.pop(0)
        log_directory_scan(current_dir)
        try:
            with os.scandir(current_dir) as entries:
                for entry in entries:
                    full_path = entry.path
                    if entry.is_file() and entry.name.lower().endswith('.mdf'):
                        if config.MDF_FILTER not in full_path:
                            continue
                        if full_path in existing_files:
                            continue
                        existing_files.add(full_path)
                        logging.info("[nouveau_fichier_trouvé]: %s", full_path)

                        try:
                            creation_date = datetime.fromtimestamp(
                                os.path.getctime(full_path)
                            ).strftime('%Y-%m-%d %H:%M:%S')
                        except Exception as e:
                            creation_date = "Unknown"
                            logging.error("Erreur timestamp %s : %s", full_path, e)

                        entity = MdfEntity(full_path, extract_moyen(full_path), creation_date)
                        insert_file_into_db(entity, db_connection)
                        log_file_insertion(entity, creation_date)

                    elif entry.is_dir():
                        dir_queue.append(entry.path)

        except PermissionError:
            logging.error("Permission refusée : %s", current_dir)
            STOP_CAUSE = "permission error"
        except Exception as e:
            logging.error("Erreur scan %s : %s", current_dir, e)
            STOP_CAUSE = "scan error"

# ── Main ──────────────────────────────────────────────────────
def main():
    global start_time, debut_traitement, db_connection_global, STOP_CAUSE

    start_time       = time.time()
    debut_traitement = datetime.now()
    db_connection    = None

    logging.info("Démarrage du scan MDF...")
    logging.info("Début : %s", debut_traitement.strftime('%Y-%m-%d %H:%M:%S'))

    try:
        db_connection = mysql.connector.connect(**config.DB_CONFIG)
        db_connection_global = db_connection

        if not db_connection.is_connected():
            logging.error("Connexion DB impossible.")
            STOP_CAUSE = "db connection failed"
            return

        cursor = db_connection.cursor()
        cursor.execute("SELECT path FROM t_acq_files")
        for row in cursor.fetchall():
            existing_files.add(row[0])
        logging.info("%s fichiers existants chargés.", len(existing_files))
        cursor.close()

    except mysql.connector.Error as err:
        logging.error("Erreur MySQL chargement : %s", err)
        STOP_CAUSE = "mysql error"
        return
    except Exception as e:
        logging.error("Erreur chargement : %s", e)
        STOP_CAUSE = "loading error"
        return

    try:
        process_directory(config.ROOT_DIR, db_connection)
        STOP_CAUSE = "completed"
    except KeyboardInterrupt:
        STOP_CAUSE = "keyboard interrupted"
        logging.info("Interrompu par l'utilisateur.")
    except Exception as e:
        logging.error("Erreur critique : %s", e)
        STOP_CAUSE = "critical error"
    finally:
        fin_traitement = datetime.now()
        execution_time = time.time() - start_time

        logging.info("Durée : %.2f secondes", execution_time)
        logging.info("Fin : %s", fin_traitement.strftime('%Y-%m-%d %H:%M:%S'))
        logging.info("Cause : %s", STOP_CAUSE)

        if db_connection and db_connection.is_connected():
            try:
                cursor = db_connection.cursor()
                insert_t_traitement(db_connection, cursor, debut_traitement, fin_traitement, STOP_CAUSE)
                cursor.close()
            except Exception as e:
                logging.error("Erreur t_traitement final : %s", e)
            db_connection.close()
            logging.info("Connexion DB fermée.")

        _write_log(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
            f"Résumé : {inserted_file_count} fichiers insérés, "
            f"{execution_time:.2f}s, cause : {STOP_CAUSE}.\n"
        )
        logging.info("Traitement terminé.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        signal_handler(None, None)