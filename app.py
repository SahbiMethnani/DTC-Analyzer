import streamlit as st
from utils.style import apply_page_config, apply_selectbox_style, inject_css
from components.sidebar import render_sidebar
from database.loaders import load_files, load_dtc_all
from utils.filters import apply_filters

apply_page_config()
inject_css()
apply_selectbox_style()

files_df  = load_files()
dtc_df    = load_dtc_all()

page, filters = render_sidebar(files_df, dtc_df)
filt_dtc, filt_files = apply_filters(dtc_df, files_df, filters)

if page == "**Vue globale**":
    from views.vue_globale import render
    render(filt_dtc, filt_files)

elif page == "**Fichiers & DTC**":
    from views.fichiers_dtc import render
    render(filt_dtc, filt_files)

elif page == "**Évolution temporelle**":
    from views.evolution_temporelle import render
    render(filt_dtc)

elif page == "**Vue hebdomadaire**":
    from views.vue_hebdomadaire import render
    render(filt_dtc)

elif page == "**Import Excel**":
    from views.import_excel import render
    render()

elif page == "**Export**":
    from views.export import render
    render(filt_dtc, filt_files)

elif page == "**Contrôle**":
    from views.controle import render
    render()
