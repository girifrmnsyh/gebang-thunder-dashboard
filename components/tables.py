"""
components/tables.py — Styled data table components
"""

from __future__ import annotations

import pandas as pd
import streamlit as st


def styled_table(
    df: pd.DataFrame,
    title: str = "",
    max_rows: int = 100,
    use_container_width: bool = True,
) -> None:
    """
    Render DataFrame sebagai tabel interaktif.
    """
    if title:
        st.markdown(f"<h4 class='table-title'>{title}</h4>", unsafe_allow_html=True)

    if df is None or df.empty:
        st.info("Tidak ada data untuk ditampilkan.")
        return

    display_df = df.head(max_rows)
    st.dataframe(display_df, use_container_width=use_container_width)

    if len(df) > max_rows:
        st.caption(f"Menampilkan {max_rows} dari {len(df):,} baris.")


def summary_table(
    data: dict[str, str | int | float],
    title: str = "",
) -> None:
    """
    Render dict key-value sebagai tabel ringkasan dua kolom.
    Berguna untuk menampilkan statistik atau metadata singkat.
    """
    if title:
        st.markdown(f"<h4 class='table-title'>{title}</h4>", unsafe_allow_html=True)

    df = pd.DataFrame(list(data.items()), columns=["Keterangan", "Nilai"])
    st.dataframe(df, use_container_width=True, hide_index=True)
