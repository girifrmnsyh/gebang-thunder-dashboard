"""
services/cache_service.py — Utilitas cache tambahan
"""

import streamlit as st
import hashlib


def make_cache_key(*args) -> str:
    """Buat cache key dari argumen arbitrari."""
    raw = "::".join(str(a) for a in args)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


@st.cache_data(ttl=3600, show_spinner=False)
def cached_computation(key: str, func, *args):
    """
    Generic cache wrapper.
    CATATAN: func harus deterministik untuk hasil yang konsisten.
    """
    return func(*args)
