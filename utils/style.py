"""
utils/style.py — CSS global, thème Plotly et helpers de mise en page
"""
import streamlit as st

# ── Palette de couleurs ───────────────────────────────────────
COLORS = {
    "bg":       "#0d0f14",
    "surface":  "#161920",
    "border":   "#252830",
    "accent":   "#e8ff3c",
    "accent2":  "#3ce8ff",
    "accent3":  "#ff3c6e",
    "text":     "#e2e5ee",
    "muted":    "#6b7080",
}

CALC_COLORS = {
    "ECU": "#e8ff3c",
    "TCU": "#3ce8ff",
    "BCM": "#60a5fa",
    "CCM": "#f87171",
    "CGW": "#fbbf24",
    "VCU": "#a78bfa",
}

TYPE_COLORS = {
    "P": "#4ade80",
    "C": "#f87171",
    "B": "#60a5fa",
    "U": "#fbbf24",
}

# ── Thème Plotly partagé ──────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(22,25,32,0.6)",
    font=dict(family="DM Sans", color="#e2e5ee"),
    xaxis=dict(gridcolor="#252830", linecolor="#252830"),
    yaxis=dict(gridcolor="#252830", linecolor="#252830"),
    colorway=["#e8ff3c", "#3ce8ff", "#ff3c6e", "#a78bfa", "#fb923c", "#34d399"],
    margin=dict(l=20, r=20, t=40, b=20),
)


def apply_page_config():
    """Configure la page Streamlit."""
    import config
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_css():
    """Injecte le CSS personnalisé."""
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:      #0d0f14;
    --surface: #161920;
    --border:  #252830;
    --accent:  #e8ff3c;
    --accent2: #3ce8ff;
    --accent3: #ff3c6e;
    --text:    #e2e5ee;
    --muted:   #6b7080;
}

[data-testid="stSidebar"] * { color: #ffffff !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
h1, h2, h3, h4 { font-family: 'Space Mono', monospace; }

/* ── Cartes métriques ─────────────────────────────────────── */
.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.metric-val {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
}
.metric-label {
    font-size: 0.75rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 6px;
}

/* ── Titres de section ────────────────────────────────────── */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    border-left: 3px solid var(--accent);
    padding-left: 10px;
    margin-bottom: 16px;
}

/* ── Badges ───────────────────────────────────────────────── */
.badge { display:inline-block; padding:2px 10px; border-radius:20px; font-size:0.72rem; font-family:'Space Mono',monospace; }
.badge-p { background:#1a2e1a; color:#4ade80; border:1px solid #4ade8055; }
.badge-c { background:#2e1a1a; color:#f87171; border:1px solid #f8717155; }
.badge-b { background:#1a1f2e; color:#60a5fa; border:1px solid #60a5fa55; }
.badge-u { background:#2e261a; color:#fbbf24; border:1px solid #fbbf2455; }

/* ── Boutons ──────────────────────────────────────────────── */
.stButton > button {
    background: var(--accent) !important;
    color: #0d0f14 !important;
    border: none !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    transition: opacity .2s;
}
.stButton > button:hover { opacity: 0.85; }

/* ── Bouton danger ────────────────────────────────────────── */
.btn-danger > button {
    background: var(--accent3) !important;
    color: #fff !important;
}

/* ── Job card ─────────────────────────────────────────────── */
.job-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.job-card-running { border-color: var(--accent2); }
.job-card-success { border-color: #4ade80; }
.job-card-error   { border-color: var(--accent3); }

/* ── Inputs ───────────────────────────────────────────────── */
/* ── Inputs — Select / Multiselect ───────────────────────── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}

/* ── Date input ───────────────────────────────────────────── */
[data-testid="stDateInput"] > div,
[data-testid="stDateInputField"] {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
[data-testid="stDateInput"] input,
[data-testid="stDateInputField"] input {
    background: var(--surface) !important;
    color: var(--text) !important;
    caret-color: var(--accent) !important;
}
[data-testid="stDateInput"] input::placeholder,
[data-testid="stDateInputField"] input::placeholder {
    color: var(--muted) !important;
    opacity: 1 !important;
}
[data-testid="stDateInput"] span,
[data-testid="stDateInputField"] span {
    color: var(--muted) !important;
}
[data-testid="stDateInput"] svg,
[data-testid="stDateInputField"] svg {
    fill: var(--muted) !important;
    stroke: var(--muted) !important;
}
[data-baseweb="calendar"],
[data-baseweb="calendar"] > div,
[data-baseweb="calendarHeader"],
[data-baseweb="monthHeader"],
[data-baseweb="weekdayHeader"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
/* Tous les textes du calendrier */
[data-baseweb="calendar"] *,
[data-baseweb="calendar"] div,
[data-baseweb="calendar"] span,
[data-baseweb="calendar"] button {
    color: var(--text) !important;
    background-color: var(--surface) !important;
}
/* Mois + année (April 2026) */
[data-baseweb="calendar"] [data-baseweb="select"] *,
[data-baseweb="calendar"] h4,
[data-baseweb="calendar"] h5 {
    color: var(--accent) !important;
    background: var(--surface) !important;
}
/* Jours de la semaine (Mo Tu We...) */
[data-baseweb="calendar"] [aria-label],
[data-baseweb="weekday"] {
    color: var(--muted) !important;
    background: var(--surface) !important;
}
/* Jour sélectionné */
[data-baseweb="calendar"] [aria-selected="true"],
[data-baseweb="calendar"] [aria-selected="true"] * {
    background: var(--accent) !important;
    color: #0d0f14 !important;
    border-radius: 6px !important;
}
/* Hover */
[data-baseweb="calendar"] button:hover,
[data-baseweb="calendar"] button:hover * {
    background: rgba(232,255,60,0.15) !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}
/* Flèches navigation */
[data-baseweb="calendar"] [aria-label="previous month"],
[data-baseweb="calendar"] [aria-label="next month"] {
    color: var(--accent) !important;
    background: transparent !important;
}
[data-baseweb="calendar"] [aria-selected="true"] {
    background: var(--accent) !important;
    color: #0d0f14 !important;
    border-radius: 6px !important;
}
[data-baseweb="calendar"] button:hover {
    background: rgba(232,255,60,0.15) !important;
    border-radius: 6px !important;
}

/* ── Text input / Password ──────────────────────────────── */
[data-testid="stTextInput"] input {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: var(--muted) !important;
    opacity: 1 !important;
}
[data-testid="stTabs"] button {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important;
}
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
.stAlert { border-radius: 10px; }
div[data-testid="stHorizontalBlock"] { gap: 16px; }

/* ── Terminal output ──────────────────────────────────────── */
.terminal-box {
    background: #050608;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #4ade80;
    max-height: 280px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-all;
}
.terminal-box.err { color: #f87171; }
</style>
""", unsafe_allow_html=True)


def section_title(text: str):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def hex_to_rgba(hex_color: str, alpha: float = 0.09) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"
