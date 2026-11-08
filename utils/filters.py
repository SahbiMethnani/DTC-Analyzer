
import pandas as pd
from datetime import timedelta


def apply_filters(dtc_df: pd.DataFrame, files_df: pd.DataFrame, filters: dict):
    
    filt_dtc   = dtc_df.copy()
    filt_files = files_df.copy()

    sel_moyen  = filters.get("sel_moyen", "Tous")
    sel_calc   = filters.get("sel_calc", "Tous")
    date_range = filters.get("date_range", ())

    if sel_moyen != "Tous":
        filt_dtc   = filt_dtc[filt_dtc["moyen"] == sel_moyen]
        filt_files = filt_files[filt_files["moyen"] == sel_moyen]

    if sel_calc != "Tous":
        filt_dtc = filt_dtc[filt_dtc["calculateur"] == sel_calc]

    if len(date_range) == 2 and not filt_dtc.empty and "date" in filt_dtc.columns:
        d0 = pd.Timestamp(date_range[0])
        d1 = pd.Timestamp(date_range[1]) + timedelta(days=1)
        filt_dtc = filt_dtc[
            (filt_dtc["date"] >= d0) & (filt_dtc["date"] < d1)
        ]

    return filt_dtc, filt_files
