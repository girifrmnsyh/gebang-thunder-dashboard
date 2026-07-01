"""
components/navbar.py — Dynamic Island Navbar
PRD Section 5: Fixed navbar custom, bukan sidebar Streamlit.
  - Kiri: logo + nomor tim
  - Tengah: 4 menu (Home, Executive Summary, GT Lab, Ask to Gemini)
  - Kanan: toggle light/dark mode
"""

import streamlit as st
from config.constants import PAGE_LABELS
from utils.session import toggle_theme


def render_navbar(active_page: str = "home") -> None:
    """
    Render navbar dynamic island via custom HTML/CSS.
    Navigasi mengubah st.query_params lalu trigger rerun.
    """
    theme = st.session_state.get("theme", "light")
    theme_icon = "☀️" if theme == "dark" else "🌙"
    theme_label = "Mode Terang" if theme == "dark" else "Mode Gelap"

    menu_items = [
        ("home",              "⚡ Beranda"),
        ("executive_summary", "📊 Executive Summary"),
        ("gt_lab",            "🔬 GT Lab"),
        ("ask_gemini",        "✨ Ask to Gemini"),
    ]

    # Render toggle theme sebagai kolom tersembunyi
    cols = st.columns([1, 4, 1])

    with cols[0]:
        st.markdown(
            '<div class="navbar-brand">'
            '<span class="navbar-logo">⚡</span>'
            '<span class="navbar-team">Gebang Thunder</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    with cols[1]:
        nav_cols = st.columns(len(menu_items))
        for i, (page_key, label) in enumerate(menu_items):
            with nav_cols[i]:
                is_active = active_page == page_key
                btn_type = "primary" if is_active else "secondary"
                if st.button(
                    label,
                    key=f"nav_{page_key}",
                    type=btn_type,
                    use_container_width=True,
                ):
                    st.query_params["page"] = page_key
                    st.rerun()

    with cols[2]:
        if st.button(theme_icon, key="theme_toggle", help=theme_label):
            toggle_theme()
            st.rerun()
