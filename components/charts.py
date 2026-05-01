"""
components/charts.py — Helpers Plotly réutilisables
"""
import plotly.express as px
import plotly.graph_objects as go
from utils.style import PLOTLY_THEME, CALC_COLORS, TYPE_COLORS, hex_to_rgba


def apply_theme(fig):
    """Applique le thème sombre partagé à n'importe quelle figure Plotly."""
    fig.update_layout(**PLOTLY_THEME)
    return fig


def pie_by_calculateur(df, hole: float = 0.55, title: str = ""):
    grp = df.groupby("calculateur").size().reset_index(name="count")
    fig = px.pie(
        grp, names="calculateur", values="count",
        color="calculateur", color_discrete_map=CALC_COLORS,
        hole=hole, title=title,
    )
    fig.update_traces(textposition="outside", textinfo="label+percent")
    return apply_theme(fig)


def bar_top_dtc(df, n: int = 15):
    top = df["dtc"].value_counts().head(n).reset_index()
    top.columns = ["DTC", "Occurrences"]
    fig = px.bar(
        top, x="Occurrences", y="DTC", orientation="h",
        color="Occurrences",
        color_continuous_scale=["#252830", "#e8ff3c"],
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    return apply_theme(fig)


def bar_per_file(df, top_n: int = 20):
    per_file = df.groupby("path").size().reset_index(name="count")
    per_file["fichier"] = per_file["path"].apply(
        lambda p: p.split("\\")[-1] if "\\" in p else p.split("/")[-1]
    )
    per_file = per_file.nlargest(top_n, "count")
    fig = px.bar(
        per_file, x="fichier", y="count",
        color="count",
        color_continuous_scale=["#161920", "#3ce8ff"],
        labels={"count": "DTC", "fichier": ""},
    )
    fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-35)
    return apply_theme(fig)


def bar_dtc_type(df):
    tmp = df.copy()
    tmp["type"] = tmp["dtc"].str[0]
    grp = tmp.groupby("type").size().reset_index(name="count")
    fig = px.bar(
        grp, x="type", y="count",
        color="type", color_discrete_map=TYPE_COLORS,
        labels={"type": "Type DTC", "count": "Occurrences"},
    )
    return apply_theme(fig)


def scatter_km(df):
    km_grp = df.groupby("kilometrage").size().reset_index(name="count")
    fig = px.scatter(
        km_grp, x="kilometrage", y="count",
        size="count", color="count",
        color_continuous_scale=["#252830", "#ff3c6e"],
        labels={"count": "DTC", "kilometrage": "Kilométrage (km)"},
    )
    fig.update_layout(coloraxis_showscale=False)
    return apply_theme(fig)


def area_global_ts(ts_df):
    fig = px.area(
        ts_df, x="date", y="count",
        labels={"date": "Date", "count": "Nombre de DTC"},
        color_discrete_sequence=["#e8ff3c"],
    )
    fig.update_traces(fill="tozeroy", line_width=2, fillcolor="rgba(232,255,60,0.12)")
    return apply_theme(fig)


def line_by_calc(calc_ts):
    fig = px.line(
        calc_ts, x="date", y="count", color="calculateur",
        color_discrete_map=CALC_COLORS,
        labels={"date": "Date", "count": "DTC", "calculateur": "Calculateur"},
        markers=True,
    )
    fig.update_traces(line_width=2)
    return apply_theme(fig)
