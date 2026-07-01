"""
services/export_service.py — Export data ke Excel / CSV
"""

import io
import pandas as pd
import streamlit as st


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Konversi DataFrame ke bytes CSV (UTF-8 dengan BOM untuk Excel compatibility)."""
    return df.to_csv(index=False).encode("utf-8-sig")


def to_excel_bytes(df: pd.DataFrame, sheet_name: str = "Data") -> bytes:
    """Konversi DataFrame ke bytes Excel (.xlsx)."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    return buffer.getvalue()


def download_button_csv(df: pd.DataFrame, filename: str = "data.csv", label: str = "Unduh CSV") -> None:
    """Render tombol download CSV Streamlit."""
    st.download_button(
        label=label,
        data=to_csv_bytes(df),
        file_name=filename,
        mime="text/csv",
    )


def download_button_excel(df: pd.DataFrame, filename: str = "data.xlsx", label: str = "Unduh Excel") -> None:
    """Render tombol download Excel Streamlit."""
    st.download_button(
        label=label,
        data=to_excel_bytes(df),
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
