"""
utils/session.py — Inisialisasi & manajemen st.session_state
PRD Section 5 & 8:
  - filter aktif Executive Summary
  - chat history Ask to Gemini
  - theme (light/dark)
  NOTE: routing halaman pakai st.query_params, bukan session_state
"""

import streamlit as st


DEFAULTS: dict = {
    # Tema UI
    "theme": "dark",

    # Executive Summary — filter aktif
    "exec_filters": {},

    # Ask to Gemini — riwayat chat
    "chat_history": [],          # list of {"role": "user"|"model", "content": str}

    # GT Lab — pilihan model aktif
    "gt_lab_model": "Regression",

    # Skeleton loading flag (per page load)
    "loading": False,
}


def init_session_state() -> None:
    """
    Inisialisasi semua kunci session_state dengan nilai default.
    Dipanggil sekali di app.py sebelum render apapun.
    """
    for key, default in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def reset_chat_history() -> None:
    """Hapus riwayat chat Ask to Gemini."""
    st.session_state["chat_history"] = []


def toggle_theme() -> None:
    """Toggle antara light dan dark mode."""
    current = st.session_state.get("theme", "dark")
    st.session_state["theme"] = "light" if current == "dark" else "dark"


def set_exec_filter(key: str, value) -> None:
    """Set satu filter Executive Summary."""
    st.session_state["exec_filters"][key] = value


def clear_exec_filters() -> None:
    """Reset semua filter Executive Summary."""
    st.session_state["exec_filters"] = {}
