"""
pages/gt_lab/clustering.py — Shell Clustering module
"""

import streamlit as st


def render() -> None:
    st.markdown("### 🔵 Clustering Analysis")
    st.info("Shell UI Clustering — visualisasi cluster akan diisi setelah dataset tersedia.")

    n_clusters = st.slider("Jumlah Cluster (K)", min_value=2, max_value=10, value=3, key="n_clusters")

    if st.button("Jalankan Clustering", type="primary", key="run_clustering"):
        st.warning("⏳ Model belum tersedia — implementasi menyusul setelah dataset rilis.")

    st.divider()
    st.markdown("#### Visualisasi Cluster")
    st.info("📊 Scatter plot cluster (PCA/t-SNE) akan ditampilkan di sini.")

    st.markdown("#### Elbow Method")
    st.info("📈 Elbow curve untuk pemilihan K optimal akan ditampilkan di sini.")
