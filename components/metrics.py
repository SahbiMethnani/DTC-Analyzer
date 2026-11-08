
import streamlit as st


def metric_card(label: str, value, col=None):
    
    html = f"""
    <div class="metric-card">
        <div class="metric-val">{value:,}</div>
        <div class="metric-label">{label}</div>
    </div>"""
    ctx = col if col else st
    ctx.markdown(html, unsafe_allow_html=True)


def kpi_row(items: list[tuple]):
    
    cols = st.columns(len(items))
    for col, (label, val) in zip(cols, items):
        with col:
            metric_card(label, val)
    st.markdown("<br>", unsafe_allow_html=True)
