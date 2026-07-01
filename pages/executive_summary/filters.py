"""
pages/executive_summary/filters.py — Filter component Executive Summary
"""

import streamlit as st
from utils.session import set_exec_filter, clear_exec_filters


def render_filters() -> None:
    """
    Render filter panel untuk Executive Summary.
    Filter spesifik (kolom, range) ditambahkan setelah dataset tersedia.
    """
    with st.expander("🔍 Filter Data", expanded=False):
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.selectbox(
                "Kategori",
                options=["Semua"],
                key="filter_category",
                help="Filter berdasarkan kategori — tersedia setelah dataset dimuat.",
            )

        with col2:
            st.selectbox(
                "Periode",
                options=["Semua"],
                key="filter_period",
                help="Filter berdasarkan periode waktu.",
            )

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)  # spacer vertikal
            if st.button("Reset", key="filter_reset", use_container_width=True):
                clear_exec_filters()
                st.rerun()
