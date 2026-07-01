"""
pages/gt_lab/regression.py — Shell Regression module
"""

import streamlit as st


def render() -> None:
    st.markdown("### 📈 Regression Analysis")
    st.info(
        "Shell UI Regression — form what-if & chart akan diisi setelah dataset tersedia. "
        "Kolom/fitur menyusul dari dataset panitia."
    )

    with st.form("regression_form"):
        st.markdown("#### Input What-If")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Fitur 1 (TBD)", value=0.0, key="reg_feat1")
            st.number_input("Fitur 2 (TBD)", value=0.0, key="reg_feat2")
        with col2:
            st.number_input("Fitur 3 (TBD)", value=0.0, key="reg_feat3")
            st.number_input("Fitur 4 (TBD)", value=0.0, key="reg_feat4")

        submitted = st.form_submit_button("Prediksi", type="primary")
        if submitted:
            st.warning("⏳ Model belum tersedia — implementasi menyusul setelah dataset rilis.")

    st.divider()
    st.markdown("#### Visualisasi Model")
    st.info("📊 Scatter plot actual vs predicted akan ditampilkan di sini.")
