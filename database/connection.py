import streamlit as st
import pandas as pd
import psycopg2

from config import DB_CONFIG


# ─────────────────────────────────────────────
# Connexion DB (cache Streamlit)
# ─────────────────────────────────────────────
@st.cache_resource
def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG.get("port", 5432),
            sslmode=DB_CONFIG.get("sslmode", "require")
        )
        return conn

    except Exception as e:
        st.error(f"❌ Connexion DB impossible : {e}")
        return None


# ─────────────────────────────────────────────
# SELECT
# ─────────────────────────────────────────────
def query(sql, params=None):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()

    try:
        return pd.read_sql(sql, conn, params=params)

    except Exception as e:
        st.error(f"❌ Erreur SQL : {e}")
        return pd.DataFrame()


# ─────────────────────────────────────────────
# INSERT / UPDATE / DELETE
# ─────────────────────────────────────────────
def execute(sql, params=None):
    conn = get_connection()
    if conn is None:
        return False

    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        cur.close()
        return True

    except Exception as e:
        st.error(f"❌ Erreur SQL : {e}")
        return False