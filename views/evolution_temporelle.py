"""
pages/evolution_temporelle.py — Page Évolution temporelle
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from components.charts import area_global_ts, line_by_calc, apply_theme
from utils.style import section_title, PLOTLY_THEME, TYPE_COLORS, CALC_COLORS, hex_to_rgba


_pd_version = tuple(int(x) for x in pd.__version__.split(".")[:2])
FREQ_MAP = {
    "Jour":    "D",
    "Semaine": "W",
    "Mois":    "ME" if _pd_version >= (2, 2) else "M",
}

def render(filt_dtc: pd.DataFrame):
    st.markdown("## Évolution temporelle des DTC")

    if filt_dtc.empty or filt_dtc["date"].isna().all():
        st.info("Pas de données temporelles disponibles.")
        return

    # ── Granularité ───────────────────────────────────────────
    granularity = st.radio("Granularité", list(FREQ_MAP.keys()), horizontal=True)
    freq = FREQ_MAP[granularity]

    # ── Courbe globale ────────────────────────────────────────
    section_title("Courbe d'évolution globale")
    ts = filt_dtc.set_index("date").resample(freq).size().reset_index(name="count")
    st.plotly_chart(area_global_ts(ts), use_container_width=True)

    # ── Par calculateur ───────────────────────────────────────
    section_title("Évolution par calculateur")
    calc_ts = (
        filt_dtc.set_index("date")
        .groupby("calculateur")
        .resample(freq)
        .size()
        .reset_index(name="count")
    )
    st.plotly_chart(line_by_calc(calc_ts), use_container_width=True)

    # ── Par type DTC ──────────────────────────────────────────
    section_title("Évolution par type de DTC (P / C / B / U)")
    tmp = filt_dtc.copy()
    tmp["type"] = tmp["DTC"].str[0]
    type_ts = (
        tmp.set_index("date")
        .groupby("type")
        .resample(freq)
        .size()
        .reset_index(name="count")
    )

    fig3 = make_subplots(
        rows=2, cols=2,
        subplot_titles=["P — Powertrain", "C — Chassis", "B — Body", "U — Network"],
        shared_xaxes=False,
    )
    for t, (r, c) in zip(["P", "C", "B", "U"], [(1,1),(1,2),(2,1),(2,2)]):
        sub = type_ts[type_ts["type"] == t]
        fig3.add_trace(
            go.Scatter(
                x=sub["date"], y=sub["count"],
                mode="lines+markers", name=t,
                line=dict(color=TYPE_COLORS.get(t, "#e2e5ee"), width=2),
                fill="tozeroy",
                fillcolor=hex_to_rgba(TYPE_COLORS.get(t, "#e2e5ee"), alpha=0.09),
            ),
            row=r, col=c,
        )
    fig3.update_layout(**PLOTLY_THEME, showlegend=False, height=500)
    fig3.update_xaxes(gridcolor="#252830", linecolor="#252830")
    fig3.update_yaxes(gridcolor="#252830", linecolor="#252830")
    st.plotly_chart(fig3, use_container_width=True)

    # ── Délai d'apparition ────────────────────────────────────
    section_title("Distribution du délai d'apparition")
    fig4 = px.histogram(
        filt_dtc, x="délai_apparition", nbins=50,
        color="calculateur", color_discrete_map=CALC_COLORS,
        labels={"délai_apparition": "Délai (s)", "count": "Fréquence"},
        barmode="overlay", opacity=0.75,
    )
    apply_theme(fig4)
    st.plotly_chart(fig4, use_container_width=True)
