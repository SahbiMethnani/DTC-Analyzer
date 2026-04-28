"""
utils/export_helpers.py — Fonctions d'export Excel et PDF
"""
import io
import pandas as pd


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Sérialise un DataFrame en bytes XLSX."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="DTC_Export")
    return buf.getvalue()


def to_pdf_bytes(df: pd.DataFrame, title: str = "Export DTC") -> bytes:
    try:
        from fpdf import FPDF

        # Nettoyage des caractères non supportés par Helvetica
        def sanitize(text: str) -> str:
            return (
                str(text)
                .replace("—", "-")
                .replace("–", "-")
                .replace("'", "'")
                .replace(""", '"')
                .replace(""", '"')
                .replace("…", "...")
                .encode("latin-1", errors="replace")
                .decode("latin-1")
            )

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, sanitize(title), ln=True)
        pdf.set_font("Helvetica", "", 7)
        pdf.ln(3)

        cols  = list(df.columns)
        col_w = min(190 // max(len(cols), 1), 38)

        # En-tête
        pdf.set_fill_color(30, 30, 40)
        pdf.set_text_color(255, 255, 255)
        for c in cols:
            pdf.cell(col_w, 6, sanitize(str(c))[:16], border=1, fill=True)
        pdf.ln()

        # Lignes
        pdf.set_text_color(0, 0, 0)
        for _, row in df.iterrows():
            for c in cols:
                pdf.cell(col_w, 5, sanitize(str(row[c]))[:16], border=1)
            pdf.ln()

        #return pdf.output(dest="S").encode("latin-1")
        return bytes(pdf.output())

    except ImportError:
        import streamlit as st
        st.error(ImportError)
        return b""