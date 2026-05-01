import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import apply_theme
from utils.style import section_title, CALC_COLORS, PLOTLY_THEME


DAY_ORDER = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]


def render(filt_dtc: pd.DataFrame):
    st.markdown("## Vue hebdomadaire des DTC")

    if filt_dtc.empty or filt_dtc["date"].isna().all():
        st.info("Pas de données disponibles.")
        return

    # Ajout des colonnes temporelles
    tmp = filt_dtc.copy()
    tmp["semaine"]       = tmp["date"].dt.isocalendar().week.astype(int)
    tmp["annee"]         = tmp["date"].dt.isocalendar().year.astype(int)
    tmp["annee_semaine"] = tmp["annee"].astype(str) + "-S" + tmp["semaine"].astype(str).str.zfill(2)
    tmp["jour_semaine"]  = tmp["date"].dt.day_name()

    # ── Barres par semaine ────────────────────────────────────
    section_title("DTC par semaine")
    weekly = tmp.groupby(["annee_semaine", "calculateur"]).size().reset_index(name="count")
    fig = px.bar(
        weekly.sort_values("annee_semaine"),
        x="annee_semaine", y="count",
        color="calculateur", color_discrete_map=CALC_COLORS,
        labels={"annee_semaine": "Semaine", "count": "DTC", "calculateur": "Calc."},
        barmode="stack",
    )
    apply_theme(fig)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # ── Heatmap semaine × jour ────────────────────────────────
    section_title("Heatmap — Semaine × Jour")
    heat = tmp.groupby(["annee_semaine", "jour_semaine"]).size().reset_index(name="count")
    heat_pivot = heat.pivot(index="annee_semaine", columns="jour_semaine", values="count").fillna(0)
    heat_pivot = heat_pivot.reindex(columns=[d for d in DAY_ORDER if d in heat_pivot.columns])
    fig2 = px.imshow(
        heat_pivot,
        color_continuous_scale=["#0d0f14", "#e8ff3c"],
        aspect="auto",
        labels=dict(x="Jour", y="Semaine", color="DTC"),
    )
    apply_theme(fig2)
    st.plotly_chart(fig2, use_container_width=True)

    # ── Top semaines ──────────────────────────────────────────
    section_title("Semaines avec le plus de DTC")
    top_w = (
        tmp.groupby("annee_semaine").size()
        .reset_index(name="total")
        .sort_values("total", ascending=False)
        .head(10)
    )
    fig3 = px.bar(
        top_w, x="annee_semaine", y="total",
        color="total",
        color_continuous_scale=["#252830", "#ff3c6e"],
        labels={"annee_semaine": "Semaine", "total": "DTC"},
    )
    fig3.update_layout(coloraxis_showscale=False)
    apply_theme(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    # ── Tableau récap ─────────────────────────────────────────
    section_title("Récapitulatif hebdomadaire")
    recap = (
        tmp.groupby("annee_semaine")
        .agg(
            nb_dtc      = ("dtc",          "count"),
            nb_fichiers = ("path",         "nunique"),
            calculateurs= ("calculateur",  lambda x: ", ".join(x.unique())),
            km_max      = ("kilometrage",  "max"),
        )
        .reset_index()
        .sort_values("annee_semaine", ascending=False)
    )
    st.dataframe(recap, use_container_width=True)
