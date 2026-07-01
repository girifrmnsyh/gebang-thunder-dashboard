"""
utils/helper.py — General-purpose helper functions
"""

import hashlib
import streamlit as st


def hash_prompt(prompt: str, context: str = "") -> str:
    """
    Hash prompt + context untuk cache key Gemini response.
    PRD Section 7.1: cache response per query identik.
    """
    raw = f"{prompt.strip()}::{context.strip()}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


def navigate_to(page: str) -> None:
    """
    Navigasi ke halaman lain via query_params.
    PRD Section 5: routing pakai query_params agar link shareable & tahan refresh.
    """
    st.query_params["page"] = page
    st.rerun()


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp nilai ke dalam range [min_val, max_val]."""
    return max(min_val, min(value, max_val))


def truncate_text(text: str, max_chars: int = 200, suffix: str = "...") -> str:
    """Potong teks panjang untuk tampilan card/preview."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + suffix
