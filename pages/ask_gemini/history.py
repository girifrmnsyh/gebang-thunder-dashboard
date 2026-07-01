"""
pages/ask_gemini/history.py — Chat history panel
"""

import streamlit as st


def render_chat_history() -> None:
    """
    Render panel riwayat chat singkat di sidebar/kolom info.
    Menampilkan jumlah pesan & tombol hapus.
    """
    history: list[dict] = st.session_state.get("chat_history", [])

    st.markdown("---")
    st.markdown("#### 🕐 Riwayat")

    if not history:
        st.caption("Belum ada percakapan.")
        return

    user_msgs = [m for m in history if m["role"] == "user"]
    st.caption(f"{len(user_msgs)} pertanyaan dalam sesi ini.")

    # Preview 3 pertanyaan terakhir
    recent = user_msgs[-3:]
    for i, msg in enumerate(reversed(recent)):
        preview = msg["content"][:60] + ("..." if len(msg["content"]) > 60 else "")
        st.markdown(f"- _{preview}_")
