# tests/test_utils.py
"""Tests unitaires — utilitaires DTC Dashboard"""
import pandas as pd
from utils.filters import apply_filters


def _make_dtc():
    return pd.DataFrame({
        "date":        pd.to_datetime(["2024-01-10", "2024-02-15", "2024-03-20"]),
        "calculateur": ["ECU", "TCU", "ECU"],
        "moyen":       ["A", "B", "A"],
        "DTC":         ["P0100", "C0200", "P0300"],
        "Kilometrage": [1000, 2000, 3000],
        "path":        ["f1", "f2", "f1"],
    })

def _make_files():
    return pd.DataFrame({
        "moyen":         ["A", "B"],
        "dateprocessed": [None, "2024-02-15"],
        "invalid":       [0, 1],
    })


def test_filter_no_filter():
    dtc, files = apply_filters(_make_dtc(), _make_files(), {
        "sel_moyen": "Tous", "sel_calc": "Tous", "date_range": ()
    })
    assert len(dtc) == 3


def test_filter_by_moyen():
    dtc, files = apply_filters(_make_dtc(), _make_files(), {
        "sel_moyen": "A", "sel_calc": "Tous", "date_range": ()
    })
    assert all(dtc["moyen"] == "A")
    assert len(dtc) == 2


def test_filter_by_calculateur():
    dtc, files = apply_filters(_make_dtc(), _make_files(), {
        "sel_moyen": "Tous", "sel_calc": "ECU", "date_range": ()
    })
    assert all(dtc["calculateur"] == "ECU")


def test_filter_by_date():
    from datetime import date
    dtc, files = apply_filters(_make_dtc(), _make_files(), {
        "sel_moyen": "Tous", "sel_calc": "Tous",
        "date_range": (date(2024, 1, 1), date(2024, 1, 31))
    })
    assert len(dtc) == 1
    assert dtc.iloc[0]["DTC"] == "P0100"