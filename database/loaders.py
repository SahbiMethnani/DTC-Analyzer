
import pandas as pd
import streamlit as st

from database.connection import query

@st.cache_data(ttl=300, show_spinner=False)
def load_files() -> pd.DataFrame:

    return query("""
        SELECT
            id,
            path,
            moyen,
            datecreated,
            dateprocessed,
            nbdefaut,
            invalid
        FROM t_acq_files
        ORDER BY datecreated DESC
    """)

@st.cache_data(ttl=120, show_spinner=False)
def load_dtc_all() -> pd.DataFrame:

    df = query("""
        SELECT
            d.id,
            d.date,
            d.DTC,
            d.calculateur,
            d.Kilometrage,
            d.délai_apparition,
            d.groupe_apparition,
            d.status_suivi,
            d.commentaire,
            d.id_t_acq_files,
            c.L_CHANNELS AS channel_name,
            f.path,
            f.moyen
        FROM t_dtc d
        INNER JOIN t_acq_files f
            ON f.id = d.id_t_acq_files
        INNER JOIN t_channel c
            ON c.id = d.Channel
        ORDER BY d.date DESC
    """)

    if df.empty:
        return df

    df["date"] = pd.to_datetime(
        df["date"],
        format="%Y-%m-%d-%H-%M-%S",
        errors="coerce"
    )

    return df



@st.cache_data(ttl=120, show_spinner=False)
def load_dtc_page(limit: int = 500, offset: int = 0):

    limit = max(1, min(int(limit), 5000))
    offset = max(0, int(offset))

    df = query("""
        SELECT
            d.id,
            d.date,
            d.DTC,
            d.calculateur,
            d.Kilometrage,
            d.délai_apparition,
            d.groupe_apparition,
            d.status_suivi,
            d.commentaire,
            d.id_t_acq_files,
            c.L_CHANNELS AS channel_name,
            f.path,
            f.moyen
        FROM t_dtc d
        INNER JOIN t_acq_files f
            ON f.id = d.id_t_acq_files
        INNER JOIN t_channel c
            ON c.id = d.Channel
        ORDER BY d.date DESC, d.id DESC
        LIMIT %s OFFSET %s
    """, (limit, offset))

    if not df.empty:
        df["date"] = pd.to_datetime(
            df["date"],
            format="%Y-%m-%d-%H-%M-%S",
            errors="coerce"
        )

    return df


@st.cache_data(ttl=120, show_spinner=False)
def count_dtc():

    df = query("""
        SELECT COUNT(*) AS total
        FROM t_dtc
    """)

    if df.empty:
        return 0

    return int(df.iloc[0]["total"])

@st.cache_data(ttl=1800, show_spinner=False)
def load_channels() -> pd.DataFrame:

    return query("""
        SELECT id, L_CHANNELS
        FROM t_channel
        ORDER BY L_CHANNELS
    """)
