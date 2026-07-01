"""
components/sidebar.py — Sidebar helper (untuk filter/panel)
PRD: Sidebar bukan navigasi utama (navbar custom yang dipakai untuk itu),
tapi bisa dipakai untuk panel filter atau setting tambahan per halaman.
"""

import streamlit as st


def hide_default_sidebar() -> None:
    """Sembunyikan sidebar Streamlit default via CSS."""
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="collapsedControl"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def filter_sidebar(title: str = "Filter") -> None:
    """
    Sidebar filter opsional — hanya tampil jika dipanggil dari page tertentu.
    """
    with st.sidebar:
        st.markdown(f"### {title}")
        st.divider()
        # Placeholder — filter spesifik diimplementasi di page masing-masing
        st.caption("Filter tersedia setelah dataset dimuat.")
