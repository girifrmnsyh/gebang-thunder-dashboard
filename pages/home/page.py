"""
pages/home/page.py — Halaman Beranda
PRD Section 5: Hero section — judul karya, deskripsi, tanggal pembuatan.
Visual: subtle gradient + glassmorphism.
"""

import streamlit as st
from datetime import date


def render() -> None:
    """Render halaman Home."""

    st.markdown(
        """
        <div class="hero-section">
            <div class="hero-badge">⚡ Gebang Thunder</div>
            <h1 class="hero-title">Ready to Take Off</h1>
            <p class="hero-subtitle">
                Dashboard analitik data interaktif untuk kompetisi — 
                menampilkan insight mendalam, eksplorasi model prediktif, 
                dan tanya-jawab AI yang grounded ke data.
            </p>
            <div class="hero-meta">
                <span class="hero-tag">📅 2026</span>
                <span class="hero-tag">📊 Data Analytics</span>
                <span class="hero-tag">🤖 Gemini AI</span>
                <span class="hero-tag">🐍 Streamlit</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Feature overview cards ─────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    features = [
        ("📊", "Executive Summary", "Insight utama & visualisasi dari dataset kompetisi."),
        ("🔬", "GT Lab",            "Eksplorasi model prediktif: Regression, Classification, Clustering."),
        ("✨", "Ask to Gemini",     "Tanya apa saja tentang data — dijawab AI secara real-time."),
        ("🎨", "Design System",     "UI minimalis, clean, futuristic — referensi shadcn & Apple."),
    ]

    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <h3 class="feature-title">{title}</h3>
                    <p class="feature-desc">{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
