"""
pages/executive_summary/page.py — Halaman Executive Summary
PRD Section 5: bento-grid layout, insight utama dari data CSV.
Shell UI — chart & insight final ditambahkan setelah dataset tersedia.
"""

import streamlit as st
from components.cards import metric_card, chart_card
from components.metric import kpi_row
from pages.executive_summary.filters import render_filters


def render() -> None:
    """Render halaman Executive Summary."""

    st.markdown('<h1 class="page-title">Executive Summary</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Ringkasan insight utama dari dataset kompetisi.</p>',
        unsafe_allow_html=True,
    )

    # ── Filter panel ──────────────────────────────────────────────────────────
    render_filters()

    st.divider()

    # ── KPI Row (placeholder) ─────────────────────────────────────────────────
    kpi_row([
        {"label": "Total Data",      "value": "—",    "format": "raw"},
        {"label": "Periode",         "value": "TBD",  "format": "raw"},
        {"label": "Variabel Utama",  "value": "TBD",  "format": "raw"},
        {"label": "Model Terbaik",   "value": "TBD",  "format": "raw"},
    ])

    st.divider()

    # ── Bento grid (shell) ────────────────────────────────────────────────────
    col_left, col_right = st.columns([2, 1])

    with col_left:
        chart_card("Tren Utama", "Dataset belum tersedia — chart akan ditambahkan setelah data rilis.")
        st.info("📊 Area chart / line chart utama akan ditampilkan di sini.")

    with col_right:
        chart_card("Distribusi", "Placeholder")
        st.info("🥧 Chart distribusi / pie chart akan ditampilkan di sini.")

    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Insight 1", "—", subtitle="TBD setelah dataset tersedia")
    with col2:
        metric_card("Insight 2", "—", subtitle="TBD setelah dataset tersedia")
    with col3:
        metric_card("Insight 3", "—", subtitle="TBD setelah dataset tersedia")
