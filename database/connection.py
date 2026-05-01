import os
import streamlit as st
import pandas as pd
import psycopg2


@st.cache_resource
def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            sslmode=os.getenv("DB_SSLMODE", "require")
        )
    except Exception as e:
        st.error(f"❌ Connexion DB impossible : {e}")
        return None


def query(sql, params=None):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()

    try:
        return pd.read_sql(sql, conn, params=params)
    except Exception as e:
        st.error(f"Erreur SQL : {e}")
        return pd.DataFrame()


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
        st.error(f"Erreur SQL : {e}")
        return False