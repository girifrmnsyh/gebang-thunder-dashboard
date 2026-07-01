"""
components/modal.py — Dialog/modal placeholder
Streamlit belum punya native modal yang robust.
Implementasi via st.expander atau st.dialog (Streamlit >= 1.36).
"""

import streamlit as st
from contextlib import contextmanager


@contextmanager
def confirm_dialog(title: str, message: str, confirm_label: str = "Ya, Lanjutkan"):
    """
    Dialog konfirmasi sederhana menggunakan st.expander.
    Gunakan sebagai context manager:

        with confirm_dialog("Hapus Data", "Apakah kamu yakin?") as confirmed:
            if confirmed:
                do_something()
    """
    with st.expander(f"⚠️ {title}", expanded=True):
        st.warning(message)
        confirmed = st.button(confirm_label, key=f"modal_confirm_{title[:10]}", type="primary")
    yield confirmed


def info_banner(message: str, type: str = "info") -> None:
    """
    Tampilkan banner informasi.
    type: 'info' | 'success' | 'warning' | 'error'
    """
    fn = getattr(st, type, st.info)
    fn(message)
