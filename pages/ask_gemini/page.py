"""
pages/ask_gemini/page.py — Halaman Ask to Gemini
PRD Section 5 & 7: conversational AI grounded ke dataset fixed.
Key differentiator vs kompetitor.
"""

import streamlit as st
from pages.ask_gemini.chat import render_chat_interface
from pages.ask_gemini.history import render_chat_history


def render() -> None:
    """Render halaman Ask to Gemini."""

    st.markdown('<h1 class="page-title">✨ Ask to Gemini</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="page-subtitle">'
        'Tanya apa saja tentang data — AI menjawab berdasarkan dataset kompetisi.'
        '</p>',
        unsafe_allow_html=True,
    )

    # ── Layout: chat di kiri, history di kanan (opsional) ─────────────────────
    col_main, col_info = st.columns([3, 1])

    with col_main:
        render_chat_interface()

    with col_info:
        st.markdown("#### 📋 Info")
        st.markdown(
            """
            **Model:** Gemini Flash  
            **Bahasa:** Indonesia (default)  
            **Grounding:** Dataset kompetisi  

            ---
            💡 **Tips:**  
            - Tanya spesifik soal data  
            - Gunakan pertanyaan yang jelas  
            - AI hanya menjawab dari data yang tersedia
            """
        )
        render_chat_history()
