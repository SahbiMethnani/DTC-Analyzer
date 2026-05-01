"""
database/loaders.py — Chargement des données avec mise en cache Streamlit
"""
import pandas as pd
import streamlit as st
from database.connection import query


@st.cache_data(ttl=120)
def load_files() -> pd.DataFrame:
    """Charge tous les fichiers d'acquisition."""
    return query("""
        SELECT id, path, moyen, datecreated, dateprocessed,
               nbdefaut, invalid
        FROM t_acq_files
        ORDER BY datecreated DESC
    """)


@st.cache_data(ttl=120)
def load_dtc_all() -> pd.DataFrame:
    """
    Charge tous les DTC avec jointures sur fichiers et canaux.
    Parse la colonne 'date' au format %Y-%m-%d-%H-%M-%S.
    """
    df = query("""
        SELECT d.id, d.date, d.DTC, d.calculateur, d.Kilometrage,
               d.delai_apparition, d.groupe_apparition,
               d.status_suivi, d.commentaire,
               d.id_t_acq_files,
               c.L_CHANNELS AS channel_name,
               f.path, f.moyen
        FROM t_dtc d
        JOIN t_acq_files f ON d.id_t_acq_files = f.id
        JOIN t_channel   c ON d.Channel = c.id
        ORDER BY d.date DESC
    """)

    if not df.empty and "date" in df.columns:
        df["date"] = pd.to_datetime(
            df["date"], format="%Y-%m-%d-%H-%M-%S", errors="coerce"
        )
    return df


@st.cache_data(ttl=120)
def load_channels() -> pd.DataFrame:
    """Charge la table des canaux."""
    return query("SELECT id, L_CHANNELS FROM t_channel")
