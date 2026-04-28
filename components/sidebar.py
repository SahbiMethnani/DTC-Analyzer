"""
components/sidebar.py — Rendu de la barre latérale + filtres globaux
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.style import section_title


PAGES = [
    "📊 Vue globale",
    "📁 Fichiers & DTC",
    "📈 Évolution temporelle",
    "📅 Vue hebdomadaire",
    "📥 Import Excel",
    "📤 Export",
    "⚙️ Contrôle",
]


def render_sidebar(files_df: pd.DataFrame, dtc_df: pd.DataFrame) -> tuple[str, dict]:
    """
    Affiche la sidebar et retourne (page_sélectionnée, dict_filtres).
    """
    with st.sidebar:
        st.markdown("# 🚗 DTC<br>Dashboard", unsafe_allow_html=True)
        st.markdown("---")

        section_title("Navigation")
        page = st.radio("Navigation", PAGES, label_visibility="collapsed")

        st.markdown("---")
        section_title("Filtres globaux")

        # Filtre moyen
        moyens = (
            ["Tous"] + sorted(files_df["moyen"].dropna().unique().tolist())
            if not files_df.empty
            else ["Tous"]
        )
        sel_moyen = st.selectbox("Moyen", moyens)

        # Filtre calculateur
        calcs = (
            ["Tous"] + sorted(dtc_df["calculateur"].dropna().unique().tolist())
            if not dtc_df.empty
            else ["Tous"]
        )
        sel_calc = st.selectbox("Calculateur", calcs)

        # Filtre date
        if not dtc_df.empty and "date" in dtc_df.columns and dtc_df["date"].notna().any():
            min_d = dtc_df["date"].min().date()
            max_d = dtc_df["date"].max().date()
        else:
            min_d = max_d = datetime.today().date()

        date_range = st.date_input(
            "Période", value=(min_d, max_d), min_value=min_d, max_value=max_d
        )

        st.markdown("---")
        if st.button("🔄 Rafraîchir"):
            st.cache_data.clear()
            st.rerun()

    filters = {
        "sel_moyen":  sel_moyen,
        "sel_calc":   sel_calc,
        "date_range": date_range,
    }
    return page, filters
