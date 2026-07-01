"""
pages/gt_lab/page.py — GT Lab (Gebang Thunder Lab)
PRD Section 5: modul projection & what-if analysis.
Shell UI pakai dummy data — model & kolom final menyusul setelah dataset tersedia.
"""

import streamlit as st
from config.constants import GT_LAB_MODELS


def render() -> None:
    """Render halaman GT Lab."""

    st.markdown('<h1 class="page-title">⚡ GT Lab</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">Gebang Thunder Lab — Eksplorasi model prediktif & analisis what-if.</p>',
        unsafe_allow_html=True,
    )

    # ── Model selector ────────────────────────────────────────────────────────
    model_type = st.selectbox(
        "Pilih Tipe Model",
        options=GT_LAB_MODELS,
        key="gt_lab_model",
        help="Pilih jenis analisis yang ingin dijalankan.",
    )

    st.divider()

    # ── Router ke sub-modul ───────────────────────────────────────────────────
    if model_type == "Regression":
        from pages.gt_lab.regression import render as render_regression
        render_regression()

    elif model_type == "Classification":
        from pages.gt_lab.classification import render as render_classification
        render_classification()

    elif model_type == "Clustering":
        from pages.gt_lab.clustering import render as render_clustering
        render_clustering()
