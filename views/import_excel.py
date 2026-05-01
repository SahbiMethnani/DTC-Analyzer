import streamlit as st
import pandas as pd
from database.connection import execute
from utils.export_helpers import to_excel_bytes
from utils.style import section_title


REQUIRED_COLS = [
    "date", "calculateur", "Kilometrage", "délai_apparition",
    "groupe_apparition", "status_suivi", "commentaire",
    "id_t_acq_files", "Channel", "DTC",
]

INSERT_SQL = """
    INSERT INTO t_dtc
    (date, calculateur, Kilometrage, délai_apparition, groupe_apparition,
     status_suivi, commentaire, id_t_acq_files, Channel, DTC)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""


def _row_params(row):
    return (
        str(row.get("date", ""))[:25],
        str(row.get("calculateur", "")),
        int(row.get("Kilometrage", 0) or 0),
        float(row.get("délai_apparition", 0) or 0),
        str(row.get("groupe_apparition", "")),
        str(row.get("status_suivi", ""))   if pd.notna(row.get("status_suivi"))  else None,
        str(row.get("commentaire", ""))    if pd.notna(row.get("commentaire"))   else None,
        int(row.get("id_t_acq_files", 0)),
        int(row.get("Channel", 0)),
        str(row.get("DTC", "")),
    )


def render():
    st.markdown("## Import DTC depuis Excel")

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Colonnes attendues dans le fichier Excel</div><br>
        <code style="color:#000000">{" | ".join(REQUIRED_COLS)}</code>
    </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Déposer le fichier Excel", type=["xlsx", "xls"])

    if uploaded:
        try:
            xl = pd.read_excel(uploaded)
            st.success(f"✅ Fichier lu : {len(xl)} lignes, {len(xl.columns)} colonnes")

            section_title("Aperçu")
            st.dataframe(xl.head(20), use_container_width=True)

            missing = [c for c in REQUIRED_COLS if c not in xl.columns]
            if missing:
                st.error(f"Colonnes manquantes : {', '.join(missing)}")
            else:
                if st.button("⬆️ Insérer dans la base de données"):
                    _do_insert(xl)
                    st.cache_data.clear()

        except Exception as e:
            st.error(f"Erreur lecture fichier : {e}")

    # Template téléchargeable
    st.markdown("---")
    section_title("Télécharger un template")
    template = pd.DataFrame(columns=REQUIRED_COLS)
    st.download_button(
        "⬇️ Template Excel",
        data=to_excel_bytes(template),
        file_name="template_dtc.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


def _do_insert(xl: pd.DataFrame):
    success_count = 0
    errors        = []
    progress      = st.progress(0)

    for i, row in xl.iterrows():
        ok = execute(INSERT_SQL, _row_params(row))
        if ok:
            success_count += 1
        else:
            errors.append(i)
        progress.progress((i + 1) / len(xl))

    st.success(f"✅ {success_count}/{len(xl)} lignes insérées.")
    if errors:
        st.warning(f"⚠️ Erreurs sur les lignes : {errors[:10]}{'...' if len(errors) > 10 else ''}")
