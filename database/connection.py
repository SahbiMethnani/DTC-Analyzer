import streamlit as st
import pandas as pd
import config


@st.cache_resource
def get_pool():
    try:
        from mysql.connector.pooling import MySQLConnectionPool
        return MySQLConnectionPool(
            pool_name          = config.DB_POOL_NAME,
            pool_size          = config.DB_POOL_SIZE,
            pool_reset_session = True,
            host               = config.DB_HOST,
            port               = config.DB_PORT,
            database           = config.DB_NAME,
            user               = config.DB_USER,
            password           = config.DB_PASSWORD,
        )
    except Exception as e:
        st.error(f"❌ Connexion DB impossible : {e}")
        return None


def query(sql: str, params=None) -> pd.DataFrame:
    
    pool = get_pool()
    if pool is None:
        return pd.DataFrame()
    try:
        conn = pool.get_connection()
        df   = pd.read_sql(sql, conn, params=params)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erreur SQL (query) : {e}")
        return pd.DataFrame()


def execute(sql: str, params=None) -> bool:
    
    pool = get_pool()
    if pool is None:
        return False
    try:
        conn = pool.get_connection()
        cur  = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erreur SQL (execute) : {e}")
        return False
