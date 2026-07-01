"""
pages/ask_gemini/chat.py — Chat UI & interaction logic
PRD Section 7: loading indicator, session history, error handling Bahasa Indonesia.
"""

import streamlit as st
from services.gemini_service import ask_gemini
from pages.ask_gemini.prompts import build_system_prompt
from utils.validator import sanitize_user_input
from utils.session import reset_chat_history


def render_chat_interface() -> None:
    """Render antarmuka chat lengkap."""

    # ── Tombol reset ──────────────────────────────────────────────────────────
    col_title, col_reset = st.columns([4, 1])
    with col_title:
        st.markdown("#### 💬 Percakapan")
    with col_reset:
        if st.button("🗑️ Hapus", key="clear_chat", help="Hapus riwayat percakapan"):
            reset_chat_history()
            st.rerun()

    # ── Tampilkan riwayat chat ────────────────────────────────────────────────
    chat_history: list[dict] = st.session_state.get("chat_history", [])

    chat_container = st.container()
    with chat_container:
        if not chat_history:
            st.markdown(
                '<div class="chat-empty">'
                '✨ Mulai percakapan — tanya apa saja tentang data!'
                '</div>',
                unsafe_allow_html=True,
            )

        for msg in chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ── Input user ─────────────────────────────────────────────────────────────
    user_input = st.chat_input(
        "Tulis pertanyaanmu di sini...",
        key="chat_input",
    )

    if user_input:
        clean_input = sanitize_user_input(user_input)

        if not clean_input:
            st.warning("Pertanyaan tidak boleh kosong.")
            return

        # Tampilkan pesan user
        with st.chat_message("user"):
            st.markdown(clean_input)

        # Simpan ke history
        st.session_state["chat_history"].append({
            "role": "user",
            "content": clean_input,
        })

        # Panggil Gemini dengan loading indicator
        with st.chat_message("assistant"):
            with st.spinner("Sedang berpikir..."):
                system_prompt = build_system_prompt()
                response, success = ask_gemini(
                    user_prompt=clean_input,
                    system_context=system_prompt,
                    use_cache=True,
                )

            st.markdown(response)

            if not success:
                st.caption("⚠️ Respons dari fallback — bukan dari AI.")

        # Simpan respons ke history
        st.session_state["chat_history"].append({
            "role": "model",
            "content": response,
        })
