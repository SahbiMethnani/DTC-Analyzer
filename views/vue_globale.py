import streamlit as st
import pandas as pd
from components.metrics import kpi_row
from components.charts import (
    pie_by_calculateur, bar_top_dtc, bar_per_file,
    bar_dtc_type, scatter_km,
)
from utils.style import section_title


def render(filt_dtc: pd.DataFrame, filt_files: pd.DataFrame):
    st.markdown("## Vue globale")

    # ── KPIs ─────────────────────────────────────────────────
    kpi_row([
        ("Fichiers total",     len(filt_files)),
        ("Fichiers traités",   int(filt_files["dateprocessed"].notna().sum()) if not filt_files.empty else 0),
        ("Fichiers invalides", int(filt_files["invalid"].sum()) if not filt_files.empty else 0),
        ("DTC total",          len(filt_dtc)),
        ("Calculateurs",       filt_dtc["calculateur"].nunique() if not filt_dtc.empty else 0),
    ])

    # ── Rangée 1 : répartition globale ───────────────────────
    col1, col2 = st.columns(2)

    with col1:
        section_title("Répartition DTC par calculateur")
        if not filt_dtc.empty:
            st.plotly_chart(pie_by_calculateur(filt_dtc), use_container_width=True)
        else:
            st.info("Aucune donnée")

    with col2:
        section_title("Top 15 DTC les plus fréquents")
        if not filt_dtc.empty:
            st.plotly_chart(bar_top_dtc(filt_dtc), use_container_width=True)
        else:
            st.info("Aucune donnée")

    # ── Rangée 2 : DTC par fichier ────────────────────────────
    section_title("DTC par fichier (top 20)")
    if not filt_dtc.empty:
        st.plotly_chart(bar_per_file(filt_dtc), use_container_width=True)

    # ── Rangée 3 : type & kilométrage ────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        section_title("Répartition par type DTC (préfixe)")
        if not filt_dtc.empty:
            st.plotly_chart(bar_dtc_type(filt_dtc), use_container_width=True)

    with col4:
        section_title("Kilométrage vs DTC détectés")
        if not filt_dtc.empty:
            st.plotly_chart(scatter_km(filt_dtc), use_container_width=True)
