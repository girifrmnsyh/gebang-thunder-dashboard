"""
pages/gt_lab/classification.py — Shell Classification module
"""

import streamlit as st


def render() -> None:
    st.markdown("### 🎯 Classification Analysis")
    st.info(
        "Shell UI Classification — form & chart akan diisi setelah dataset tersedia."
    )

    with st.form("classification_form"):
        st.markdown("#### Input What-If")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Fitur 1 (TBD)", value=0.0, key="clf_feat1")
            st.number_input("Fitur 2 (TBD)", value=0.0, key="clf_feat2")
        with col2:
            st.number_input("Fitur 3 (TBD)", value=0.0, key="clf_feat3")
            st.selectbox("Kategori (TBD)", options=["—"], key="clf_cat")

        submitted = st.form_submit_button("Klasifikasikan", type="primary")
        if submitted:
            st.warning("⏳ Model belum tersedia — implementasi menyusul setelah dataset rilis.")

    st.divider()
    st.markdown("#### Hasil Klasifikasi")
    st.info("📊 Confusion matrix & classification report akan ditampilkan di sini.")
