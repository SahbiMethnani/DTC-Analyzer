"""
components/metrics.py — Composant de carte métrique HTML
"""
import streamlit as st


def metric_card(label: str, value, col=None):
    """
    Affiche une carte métrique stylisée.
    Si col est fourni, l'affiche dans ce contexte de colonne.
    """
    html = f"""
    <div class="metric-card">
        <div class="metric-val">{value:,}</div>
        <div class="metric-label">{label}</div>
    </div>"""
    ctx = col if col else st
    ctx.markdown(html, unsafe_allow_html=True)


def kpi_row(items: list[tuple]):
    """
    Affiche une rangée de KPI.
    items : liste de (label, valeur)
    """
    cols = st.columns(len(items))
    for col, (label, val) in zip(cols, items):
        with col:
            metric_card(label, val)
    st.markdown("<br>", unsafe_allow_html=True)
