import streamlit as st


COLORS = {
    "bg":       "#12151a",
    "surface":  "#1a1e25",
    "surface2": "#222730",
    "border":   "#2c323d",
    "accent":   "#ffb224",
    "accent2":  "#4fd1c5",
    "accent3":  "#ff5d5d",
    "success":  "#4ade80",
    "text":     "#e8eaee",
    "muted":    "#8a93a3",
}

CALC_COLORS = {
    "ECU": "#ffb224",
    "TCU": "#4fd1c5",
    "BCM": "#60a5fa",
    "CCM": "#f87171",
    "CGW": "#a3e635",
    "VCU": "#c084fc",
}

TYPE_COLORS = {
    "P": "#4ade80",
    "C": "#f87171",
    "B": "#60a5fa",
    "U": "#c084fc",
}

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(26,30,37,0.6)",
    font=dict(family="Barlow, sans-serif", color=COLORS["text"], size=13),
    xaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"],
               zerolinecolor=COLORS["border"]),
    yaxis=dict(gridcolor=COLORS["border"], linecolor=COLORS["border"],
               zerolinecolor=COLORS["border"]),
    colorway=["#ffb224", "#4fd1c5", "#60a5fa", "#c084fc", "#a3e635", "#f87171"],
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["muted"])),
    hoverlabel=dict(bgcolor=COLORS["surface2"], bordercolor=COLORS["border"],
                    font=dict(family="Barlow, sans-serif", color=COLORS["text"])),
    margin=dict(l=20, r=20, t=40, b=20),
)


def apply_page_config():
    import config
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=None,
        layout="wide",
        initial_sidebar_state="expanded",
    )


def hex_to_rgba(hex_color: str, alpha: float = 0.09) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _root_css() -> str:
    c = COLORS
    return f"""
:root {{
    --bg: {c['bg']};
    --surface: {c['surface']};
    --surface-2: {c['surface2']};
    --border: {c['border']};
    --accent: {c['accent']};
    --accent-soft: {hex_to_rgba(c['accent'], 0.14)};
    --accent2: {c['accent2']};
    --accent3: {c['accent3']};
    --success: {c['success']};
    --text: {c['text']};
    --muted: {c['muted']};
}}
"""


def _badge_css() -> str:
    return "\n".join(
        f".badge-{k.lower()} {{ background:{hex_to_rgba(col, 0.12)}; "
        f"color:{col}; border:1px solid {hex_to_rgba(col, 0.38)}; }}"
        for k, col in TYPE_COLORS.items()
    )


_STATIC_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Barlow', sans-serif;
    font-size: 16px;
    line-height: 1.5;
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 2.2rem; max-width: 1400px; }

h1, h2, h3, h4 {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
    color: var(--text) !important;
}
h1 { font-size: 2.4rem !important; }
h2 { font-size: 1.8rem !important; }
h3 { font-size: 1.4rem !important; }

a { color: var(--accent2) !important; }

:is(button, a, input, textarea, [role="tab"], [role="option"]):focus-visible {
    outline: 2px solid var(--accent) !important;
    outline-offset: 2px;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] :is(p, span, label, li, h1, h2, h3, h4) {
    color: var(--text) !important;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: var(--muted) !important;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 22px;
}
.metric-val {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.8rem;
    font-weight: 600;
    color: var(--accent);
    line-height: 1;
    font-variant-numeric: tabular-nums;
}
.metric-label {
    font-size: 0.9rem;
    color: var(--muted);
    margin-top: 8px;
}
.metric-card.ok  .metric-val { color: var(--success); }
.metric-card.bad .metric-val { color: var(--accent3); }

[data-testid="stMetric"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
}
[data-testid="stMetricValue"] {
    font-family: 'Barlow Condensed', sans-serif;
    font-variant-numeric: tabular-nums;
}
[data-testid="stMetricLabel"] * { color: var(--muted) !important; }

.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    padding-bottom: 8px;
    margin: 8px 0 18px;
    border-bottom: 1px solid var(--border);
}

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
}

.stButton > button,
[data-testid="stDownloadButton"] > button {
    background: var(--accent) !important;
    color: #1a1204 !important;
    border: none !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    padding: 9px 20px !important;
    transition: background .15s, transform .15s;
}
.stButton > button:hover,
[data-testid="stDownloadButton"] > button:hover {
    background: #ffc247 !important;
}
.stButton > button:active { transform: translateY(1px); }
.stButton > button:disabled {
    background: var(--surface-2) !important;
    color: var(--muted) !important;
}

.btn-secondary > div > button,
.btn-secondary button {
    background: transparent !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
}
.btn-secondary button:hover { background: var(--surface-2) !important; }
.btn-danger button {
    background: var(--accent3) !important;
    color: #fff !important;
}

.job-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--border);
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 14px;
}
.job-card-running { border-left-color: var(--accent2); }
.job-card-success { border-left-color: var(--success); }
.job-card-error   { border-left-color: var(--accent3); }

.stSelectbox > div > div,
.stMultiSelect > div > div,
[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
[data-baseweb="tag"] {
    background: var(--accent-soft) !important;
    color: var(--accent) !important;
}
[data-baseweb="tag"] * { color: var(--accent) !important; }

[data-baseweb="popover"] > div,
[data-baseweb="menu"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border);
    border-radius: 8px !important;
}
[data-baseweb="menu"] li,
[role="option"] { color: var(--text) !important; }
[data-baseweb="menu"] li:hover,
[role="option"]:hover,
[role="option"][aria-selected="true"] {
    background: var(--accent-soft) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
textarea {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    caret-color: var(--accent) !important;
}
[data-testid="stTextInput"] input::placeholder,
textarea::placeholder {
    color: var(--muted) !important;
    opacity: 1 !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

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
[data-testid="stDateInput"] svg,
[data-testid="stDateInputField"] svg {
    fill: var(--muted) !important;
}

[data-baseweb="calendar"],
[data-baseweb="calendar"] > div,
[data-baseweb="calendarHeader"],
[data-baseweb="monthHeader"],
[data-baseweb="weekdayHeader"] {
    background: var(--surface-2) !important;
    border-radius: 10px !important;
}
[data-baseweb="calendar"] { border: 1px solid var(--border) !important; }
[data-baseweb="calendar"] :is(div, span, button) {
    color: var(--text) !important;
    background-color: transparent !important;
}
[data-baseweb="calendar"] :is(h4, h5),
[data-baseweb="calendar"] [data-baseweb="select"] * {
    color: var(--accent) !important;
}
[data-baseweb="weekday"],
[data-baseweb="calendar"] [aria-label] { color: var(--muted) !important; }
[data-baseweb="calendar"] button:hover {
    background-color: var(--accent-soft) !important;
    border-radius: 6px !important;
}
[data-baseweb="calendar"] [aria-selected="true"],
[data-baseweb="calendar"] [aria-selected="true"] * {
    background-color: var(--accent) !important;
    color: #1a1204 !important;
    border-radius: 6px !important;
}

[data-baseweb="tab-list"] { border-bottom: 1px solid var(--border); gap: 4px; }
[data-baseweb="tab"] {
    font-family: 'Barlow', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: var(--muted) !important;
    background: transparent !important;
}
[data-baseweb="tab"][aria-selected="true"] { color: var(--text) !important; }
[data-baseweb="tab-highlight"] { background-color: var(--accent) !important; height: 3px !important; }
[data-baseweb="tab-border"] { background-color: transparent !important; }

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}
[data-testid="stExpander"] {
    background: var(--surface);
    border: 1px solid var(--border) !important;
    border-radius: 10px;
}
.stAlert { border-radius: 10px; }
div[data-testid="stHorizontalBlock"] { gap: 16px; }
hr { border-color: var(--border) !important; }

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 6px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

.terminal-box {
    background: #0b0d10;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.55;
    color: var(--success);
    max-height: 280px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-all;
}
.terminal-box.err { color: var(--accent3); }

@media (max-width: 640px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .metric-val { font-size: 2.2rem; }
    h1 { font-size: 1.9rem !important; }
}

@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
}
"""


def inject_css():
    st.markdown(
        f"<style>{_root_css()}\n{_badge_css()}\n{_STATIC_CSS}</style>",
        unsafe_allow_html=True,
    )


def section_title(text: str):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def metric_card(label: str, value, state: str = ""):
    st.markdown(
        f'<div class="metric-card {state}">'
        f'<div class="metric-val">{value}</div>'
        f'<div class="metric-label">{label}</div></div>',
        unsafe_allow_html=True,
    )
def apply_selectbox_style():
    st.markdown("""
    <style>
    /* Champ Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #2563eb !important;
    }

    /* Texte du champ */
    div[data-baseweb="select"] span {
        color: white !important;
    }

    /* Menu déroulant */
    div[data-baseweb="popover"] ul {
        background-color: #2563eb !important;
    }

    /* Options */
    div[data-baseweb="popover"] li {
        background-color: #2563eb !important;
        color: white !important;
    }

    /* Option survolée */
    div[data-baseweb="popover"] li:hover {
        background-color: #1d4ed8 !important;
        color: white !important;
    }

    /* Option sélectionnée */
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #1e40af !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)