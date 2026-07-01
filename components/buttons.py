"""
components/buttons.py — Custom button components
"""

import streamlit as st


def primary_button(label: str, key: str, icon: str = "", **kwargs) -> bool:
    """Tombol primary dengan ikon opsional. Return True jika diklik."""
    full_label = f"{icon} {label}".strip() if icon else label
    return st.button(full_label, key=key, type="primary", **kwargs)


def secondary_button(label: str, key: str, icon: str = "", **kwargs) -> bool:
    """Tombol secondary. Return True jika diklik."""
    full_label = f"{icon} {label}".strip() if icon else label
    return st.button(full_label, key=key, type="secondary", **kwargs)


def danger_button(label: str, key: str, icon: str = "⚠️", **kwargs) -> bool:
    """Tombol destruktif (konfirmasi tindakan berisiko). Return True jika diklik."""
    full_label = f"{icon} {label}".strip()
    return st.button(full_label, key=key, **kwargs)
