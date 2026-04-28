import os
import shutil
import logging
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
import psutil
import pandas as pd
from datetime import datetime
from asammdf import MDF
import time
import signal
import sys
import gc
from collections import defaultdict

# ── Import de la configuration ────────────────────────────────
import config

# ── Logging ──────────────────────────────────────────────────
logging.getLogger("asammdf").setLevel(logging.CRITICAL)

class NoErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.addFilter(NoErrorFilter())
console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logging.basicConfig(level=logging.INFO, handlers=[console_handler])

# ── État global ───────────────────────────────────────────────
TOTAL_FILES_PROCESSED = 0

# ── Pool de connexions ────────────────────────────────────────
def init_db_pool():
    try:
        pool = MySQLConnectionPool(
            pool_name       = config.DB_POOL_NAME,
            pool_size       = config.DB_POOL_SIZE,
            pool_reset_session = True,
            host            = config.DB_HOST,
            database        = config.DB_NAME,
            user            = config.DB_USER,
            password        = config.DB_PASSWORD,
        )
        logging.info("MySQL connection pool successfully initialized.")
        return pool
    except mysql.connector.Error as err:
        logging.error("Error while creating connection pool: %s", err)
        sys.exit(1)

POOL = init_db_pool()

def get_db_connection():
    return POOL.get_connection()

# ── Mémoire ───────────────────────────────────────────────────
def check_memory_usage():
    mem = psutil.virtual_memory()
    if mem.percent > config.MEMORY_THRESHOLD_PERCENT:
        logging.warning("High memory usage: %s%%. Forcing garbage collection.", mem.percent)
        gc.collect()

# ── Logging fichier ───────────────────────────────────────────
def log_new_file(file_path, dtc_count=None, km=None, timestamp=None, invalid=False):
    try:
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if invalid:
            entry = f"{now_str} - Invalid file: {file_path} | invalid: 1"
        else:
            entry = (f"{now_str} - Processed file: {file_path} | "
                     f"DTC detected: {dtc_count} | Kilometrage: {km} | invalid: 0")
        with open(config.SCAN_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        logging.info(entry)
    except Exception as e:
        logging.error("Error writing to scan log for %s: %s", file_path, e)

# ── Signal SIGINT ─────────────────────────────────────────────
def signal_handler(sig, frame):
    global TOTAL_FILES_PROCESSED
    logging.info("Signal reçu. Fichiers traités : %s", TOTAL_FILES_PROCESSED)
    try:
        with open(config.SCAN_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n--- Interrupted ---\nTotal: {TOTAL_FILES_PROCESSED}\n---\n\n")
    except Exception as e:
        logging.error("Error writing interruption stats: %s", e)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ── Conversion DTC ────────────────────────────────────────────
def convert_hex_to_bit_and_back(hex_value: str, mask: int) -> str:
    try:
        return format(int(hex_value, 16) & mask, 'X')
    except (TypeError, ValueError) as e:
        logging.warning("convert_hex_to_bit_and_back error %s: %s", hex_value, e)
        return "0"

def convert_formula(hex_value: str) -> str:
    try:
        return format((int(hex_value, 16) & 48) >> 4, 'X')
    except (TypeError, ValueError) as e:
        logging.warning("convert_formula error %s: %s", hex_value, e)
        return "0"

def to_dtc(v) -> str:
    try:
        v_int = int(v) if v is not None else None
        if v_int is None:
            return "P00000-00"
        dtc = format(v_int, 'X').zfill(6)
    except (TypeError, ValueError) as e:
        logging.warning("to_dtc error for value %s: %s", v, e)
        return "P00000-00"
    vv  = convert_formula(dtc[:2]) + convert_hex_to_bit_and_back(dtc[:2], 15)
    b   = int(dtc[:2], 16) >> 6
    prefix = ["P", "C", "B", "U"][b] if b < 4 else "P"
    code = prefix + vv + dtc[2:]
    return code[:5] + "-" + code[5:7]

def deduce_calculator(dtc_code: str) -> str:
    if not dtc_code or len(dtc_code) < 5:
        return "Unknown type"
    prefix = dtc_code[0].upper()
    mapping = {"B": "BCM", "C": "CCM", "U": "CGW"}
    if prefix == "P":
        return "TCU" if dtc_code[1:3] == "07" else "ECU"
    return mapping.get(prefix, "VCU")

# ── Requêtes DB ───────────────────────────────────────────────
def get_mdf_file_paths_batch(cursor, offset):
    try:
        cursor.execute(
            "SELECT id, path FROM t_acq_files WHERE dateprocessed IS NULL LIMIT %s OFFSET %s",
            (config.BATCH_SIZE, offset)
        )
        return {row[1]: row[0] for row in cursor.fetchall()}
    except mysql.connector.Error as err:
        logging.error("MySQL error fetching MDF files: %s", err)
        return {}

def get_channels(cursor):
    try:
        cursor.execute("SELECT id, L_CHANNELS FROM t_channel")
        channels = {}
        for ch_id, names in cursor.fetchall():
            for name in names.split(";"):
                name = name.strip()
                if name and name not in channels:
                    channels[name] = ch_id
        return channels
    except mysql.connector.Error as err:
        logging.error("MySQL error fetching channels: %s", err)
        return {}

def update_file_invalid(file_path, connection, cursor):
    try:
        cursor.execute("UPDATE t_acq_files SET invalid = 1 WHERE path = %s", (file_path,))
        connection.commit()
    except mysql.connector.Error as err:
        logging.error("Error marking file invalid %s: %s", file_path, err)

def mark_file_as_processed(file_path, connection, cursor):
    cursor.execute(
        "UPDATE t_acq_files SET dateprocessed = %s WHERE path = %s",
        (datetime.now().strftime('%Y-%m-%d'), file_path)
    )
    connection.commit()

def update_nbdefaut_for_file(file_id, connection, cursor):
    try:
        cursor.execute("SELECT COUNT(*) FROM t_dtc WHERE id_t_acq_files = %s", (file_id,))
        count = cursor.fetchone()[0] or 0
        cursor.execute("UPDATE t_acq_files SET nbdefaut = %s WHERE id = %s", (count, file_id))
        connection.commit()
        return count
    except mysql.connector.Error as err:
        logging.error("Error updating DTC count for file %s: %s", file_id, err)
        return 0

def insert_records(records, cursor, connection):
    if not records:
        return 0
    try:
        cursor.executemany('''
            INSERT INTO t_dtc
            (date, calculateur, Kilometrage, délai_apparition, groupe_apparition,
             status_suivi, commentaire, id_t_acq_files, Channel, DTC)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''', [(r['date'], r['calculateur'], r['Kilometrage'], r['délai_apparition'],
               r['groupe_apparition'], r['status_suivi'], r['commentaire'],
               r['id_t_acq_files'], r['Channel'], r['DTC']) for r in records])
        connection.commit()
        logging.info("Inserted %s records into t_dtc", len(records))
        return len(records)
    except mysql.connector.Error as err:
        logging.error("Error inserting records: %s", err)
        return 0

# ── Parsing MDF ───────────────────────────────────────────────
def calculate_elapsed_time(start, current) -> float:
    return (current - start).total_seconds()

def assign_groupe_apparition(records):
    grouped = defaultdict(list)
    for rec in records:
        grouped[rec['Channel']].append(rec)
    result = []
    for recs in grouped.values():
        recs.sort(key=lambda r: r['délai_apparition'])
        group, start_t = 1, recs[0]['délai_apparition']
        recs[0]['groupe_apparition'] = "G1"
        for i in range(1, len(recs)):
            if (recs[i]['délai_apparition'] - start_t) <= config.GROUPE_THRESHOLD:
                recs[i]['groupe_apparition'] = f"G{group}"
            else:
                group += 1
                recs[i]['groupe_apparition'] = f"G{group}"
                start_t = recs[i]['délai_apparition']
        result.extend(recs)
    return result

def parse_mdf_file(file_path, file_id, channels_dict, use_signal=False):
    mdf = None
    try:
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"Permission refusée : {file_path}")
        mdf = MDF(file_path, memory_map=True)
        available = list(mdf.channels_db.keys())

        # Kilométrage
        df_km = mdf.to_dataframe(channels=[config.KM_CHANNEL])
        df_km = df_km.loc[:, ~df_km.columns.duplicated()]
        df_km.index = pd.to_datetime(df_km.index, unit='s', errors='coerce')
        df_km.dropna(subset=[config.KM_CHANNEL], inplace=True)
        max_km = df_km[config.KM_CHANNEL].max()
        if pd.isnull(max_km) or max_km == 0:
            logging.warning("Kilométrage nul dans %s", file_path)
            return []
        max_km_int = int(float(max_km))

        records = []

        if not use_signal:
            req_channels = [ch for ch in channels_dict if ch in available] + [config.KM_CHANNEL]
            df = mdf.to_dataframe(channels=req_channels)
            df = df.loc[:, ~df.columns.duplicated()]
            df.index = pd.to_datetime(df.index, unit='s', errors='coerce')

        for ch_name, ch_id in channels_dict.items():
            if ch_name not in available:
                continue

            def make_record(elapsed, val):
                try:
                    dtc = to_dtc(val)
                except Exception as ex:
                    logging.warning("DTC conversion error %s in %s: %s", val, file_path, ex)
                    dtc = "P00000-00"
                return {
                    'date': datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
                    'calculateur': deduce_calculator(dtc),
                    'Kilometrage': max_km_int,
                    'délai_apparition': round(elapsed, 2),
                    'groupe_apparition': None,
                    'status_suivi': None,
                    'commentaire': None,
                    'id_t_acq_files': file_id,
                    'Channel': ch_id,
                    'DTC': dtc,
                }

            if use_signal:
                try:
                    sig = mdf.get(ch_name)
                    if sig is None:
                        continue
                    last = None
                    for t, val in zip(sig.timestamps, sig.samples):
                        if last is None or val != last:
                            elapsed = calculate_elapsed_time(sig.timestamps[0], t)
                            if elapsed > 0:
                                records.append(make_record(elapsed, val))
                        last = val
                except Exception as ex:
                    logging.warning("Signal mode error for %s: %s", ch_name, ex)
            else:
                if ch_name not in df.columns:
                    continue
                last = None
                for idx, row in df.iterrows():
                    try:
                        val = row[ch_name] if pd.notnull(row[ch_name]) else None
                    except Exception:
                        continue
                    if val is None:
                        continue
                    if last is None or val != last:
                        elapsed = calculate_elapsed_time(df.index[0], idx)
                        if elapsed > 0:
                            records.append(make_record(elapsed, val))
                    last = val

        return assign_groupe_apparition(records) if records else []

    except PermissionError as pe:
        logging.error("Permission refusée %s: %s", file_path, pe)
        raise
    except Exception as e:
        logging.error("Erreur parsing %s: %s", file_path, e)
        return []
    finally:
        if mdf:
            try:
                mdf.close()
            except Exception:
                pass
        gc.collect()

# ── Traitement d'un fichier ───────────────────────────────────
def process_file(file_path, file_id, connection, cursor, channels_dict, use_signal=False):
    global TOTAL_FILES_PROCESSED
    os.makedirs(config.LOCAL_DIR, exist_ok=True)
    local_path = os.path.join(config.LOCAL_DIR, os.path.basename(file_path))

    try:
        shutil.copy(file_path, local_path)
        logging.info("Fichier copié : %s", local_path)
    except Exception as e:
        logging.error("Erreur copie %s: %s", file_path, e)
        return

    try:
        records = parse_mdf_file(local_path, file_id, channels_dict, use_signal)
        if records:
            insert_records(records, cursor, connection)
        dtc_count = update_nbdefaut_for_file(file_id, connection, cursor)
        mark_file_as_processed(file_path, connection, cursor)
        ts = records[0]['date'] if records else datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        km = records[0]['Kilometrage'] if records else 0
        log_new_file(file_path, dtc_count=dtc_count, km=km, timestamp=ts)
    except Exception as exc:
        update_file_invalid(file_path, connection, cursor)
        logging.error("Fichier invalide %s: %s", file_path, exc)
        log_new_file(file_path, invalid=True)
    finally:
        TOTAL_FILES_PROCESSED += 1
        logging.info("Total traités : %s", TOTAL_FILES_PROCESSED)
        try:
            os.remove(local_path)
        except Exception as e:
            logging.error("Erreur suppression %s: %s", local_path, e)
        gc.collect()
        check_memory_usage()

# ── Boucle principale ─────────────────────────────────────────
def process_all_files():
    connection = get_db_connection()
    cursor = connection.cursor()
    channels_dict = get_channels(cursor)
    offset, start_total = 0, time.time()

    while True:
        batch = get_mdf_file_paths_batch(cursor, offset)
        if not batch:
            break
        logging.info("Batch de %s fichiers (offset %s)", len(batch), offset)
        for file_path, file_id in batch.items():
            try:
                process_file(file_path, file_id, connection, cursor, channels_dict)
            except Exception as e:
                logging.error("Erreur inattendue %s: %s", file_path, e)
            finally:
                check_memory_usage()
        #offset += config.BATCH_SIZE

    total_time = time.time() - start_total
    stats = (f"Processing Statistics:\n"
             f" - Total files processed: {TOTAL_FILES_PROCESSED}\n"
             f" - Total processing time: {total_time:.2f} seconds\n")
    logging.info(stats)
    print(stats)
    try:
        with open(config.SCAN_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n--- Scan Statistics ---\n"
                    f"Completed in {total_time:.2f}s for {TOTAL_FILES_PROCESSED} files.\n"
                    f"---\n\n")
    except Exception as e:
        logging.error("Error writing stats: %s", e)
    cursor.close()
    if connection.is_connected():
        connection.close()

if __name__ == "__main__":
    try:
        process_all_files()
    except KeyboardInterrupt:
        logging.info("Interruption. Total traités : %s", TOTAL_FILES_PROCESSED)
        sys.exit(0)