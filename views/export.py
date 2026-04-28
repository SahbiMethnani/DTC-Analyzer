"""
pages/export.py — Page Export des données
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.export_helpers import to_excel_bytes, to_pdf_bytes
from utils.style import section_title

PDF_COLS = ["DTC", "calculateur", "Kilometrage", "délai_apparition",
            "groupe_apparition", "channel_name", "date"]


def render(filt_dtc: pd.DataFrame, filt_files: pd.DataFrame):
    st.markdown("## Export des données")

    section_title("Sélection des données à exporter")
    export_scope = st.radio(
        "Périmètre", ["Tous les DTC filtrés", "Par fichier spécifique"], horizontal=True
    )

    if export_scope == "Par fichier spécifique" and not filt_files.empty:
        sel_exp_file = st.selectbox(
            "Fichier", filt_files["path"].tolist(),
            format_func=lambda p: p.split("\\")[-1] if "\\" in p else p.split("/")[-1],
        )
        export_df = filt_dtc[filt_dtc["path"] == sel_exp_file]
    else:
        export_df = filt_dtc.copy()

    st.info(f"**{len(export_df)}** lignes prêtes à l'export")
    if not export_df.empty:
        st.dataframe(export_df.head(30), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    # ── Excel ─────────────────────────────────────────────────
    with col1:
        section_title("Export Excel")
        if not export_df.empty:
            st.download_button(
                "⬇️ Télécharger Excel",
                data=to_excel_bytes(export_df),
                file_name=f"dtc_export_{ts}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.info("Aucune donnée à exporter.")

    # ── PDF ───────────────────────────────────────────────────
    with col2:
        section_title("Export PDF")
        if not export_df.empty:
            pdf_df   = export_df[[c for c in PDF_COLS if c in export_df.columns]].head(500)
            pdf_data = to_pdf_bytes(pdf_df, title="Export DTC")
            if pdf_data:
                st.download_button(
                    "⬇️ Télécharger PDF",
                    data=pdf_data,
                    file_name=f"dtc_export_{ts}.pdf",
                    mime="application/pdf",
                )
                st.caption("⚠️ Limité aux 500 premières lignes pour le PDF.")
        else:
            st.info("Aucune donnée à exporter.")

    # ── Export fichiers ───────────────────────────────────────
    st.markdown("---")
    section_title("Export liste des fichiers")
    if not filt_files.empty:
        st.download_button(
            "⬇️ Exporter les fichiers en Excel",
            data=to_excel_bytes(filt_files),
            file_name=f"fichiers_export_{ts}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
