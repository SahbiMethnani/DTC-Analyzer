import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import pie_by_calculateur, apply_theme
from components.metrics import metric_card
from utils.style import section_title, CALC_COLORS


def render(filt_dtc: pd.DataFrame, filt_files: pd.DataFrame):
    st.markdown("## Fichiers & DTC")

    tab1, tab2 = st.tabs(["📁 Liste des fichiers", "🔍 DTC par fichier"])

    # ── Tab 1 : liste fichiers ────────────────────────────────
    with tab1:
        section_title("Fichiers d'acquisition")
        if not filt_files.empty:
            display = filt_files.copy()
            display["invalid"] = display["invalid"].map({0: "✅ Valide", 1: "❌ Invalide"})
            display["traité"]  = display["dateprocessed"].apply(
                lambda x: "✅ Oui" if pd.notna(x) else "⏳ Non"
            )
            st.dataframe(
                display[["id", "path", "moyen", "datecreated", "traité", "nbdefaut", "invalid"]],
                use_container_width=True, height=500,
            )
        else:
            st.info("Aucun fichier trouvé.")

    # ── Tab 2 : DTC par fichier ───────────────────────────────
    with tab2:
        section_title("DTC pour un fichier sélectionné")
        if not filt_files.empty:
            sel_file = st.selectbox(
                "Sélectionner un fichier",
                filt_files["path"].tolist(),
                format_func=lambda p: p.split("\\")[-1] if "\\" in p else p.split("/")[-1],
            )
            file_dtc = filt_dtc[filt_dtc["path"] == sel_file] if sel_file else pd.DataFrame()

            if not file_dtc.empty:
                # Mini KPIs
                c1, c2, c3 = st.columns(3)
                with c1:
                    metric_card("DTC total", len(file_dtc))
                with c2:
                    metric_card("Calculateurs", file_dtc["calculateur"].nunique())
                with c3:
                    km_val = int(file_dtc["Kilometrage"].max()) if "Kilometrage" in file_dtc.columns else 0
                    metric_card("Km max", km_val)

                st.markdown("<br>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(
                        pie_by_calculateur(file_dtc, title="Par calculateur"),
                        use_container_width=True,
                    )
                with col2:
                    grp2 = file_dtc.groupby("groupe_apparition").size().reset_index(name="count")
                    fig  = px.bar(
                        grp2, x="groupe_apparition", y="count",
                        color="count",
                        color_continuous_scale=["#252830", "#e8ff3c"],
                        title="Par groupe d'apparition",
                        labels={"groupe_apparition": "Groupe", "count": "DTC"},
                    )
                    fig.update_layout(coloraxis_showscale=False)
                    apply_theme(fig)
                    st.plotly_chart(fig, use_container_width=True)

                section_title("Détail des DTC")
                show_cols = [
                    "DTC", "calculateur", "Kilometrage", "délai_apparition",
                    "groupe_apparition", "channel_name", "date",
                    "status_suivi", "commentaire",
                ]
                st.dataframe(
                    file_dtc[[c for c in show_cols if c in file_dtc.columns]],
                    use_container_width=True, height=400,
                )
            else:
                st.info("Aucun DTC pour ce fichier.")
        else:
            st.info("Aucun fichier disponible.")
