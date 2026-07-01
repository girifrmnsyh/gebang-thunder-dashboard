"""
config/theme.py — Single source of truth untuk design token warna
Dipakai untuk:
  - Inject custom CSS (via st.markdown)
  - Warna chart Plotly (ngikut tema aktif)

PRD Section 6 — Color Palette
"""

import streamlit as st

# ── Token warna per tema ───────────────────────────────────────────────────────
TOKENS = {
    "light": {
        "background":           "#FFFFFF",
        "secondary_background": "#FAFAFA",
        "card":                 "#FFFFFF",
        "border":               "#E5E7EB",
        "primary":              "#2563EB",
        "primary_rgb":          "37, 99, 235",
        "hover":                "#EFF6FF",
        "text_primary":         "#111827",
        "text_secondary":       "#6B7280",
    },
    "dark": {
        "background":           "#09090B",
        "secondary_background": "#131316",
        "card":                 "#18181B",
        "border":               "#27272A",
        "primary":              "#3B82F6",
        "primary_rgb":          "59, 130, 246",
        "hover":                "rgba(59,130,246,0.12)",
        "text_primary":         "#FAFAFA",
        "text_secondary":       "#A1A1AA",
    },
}


def get_tokens(mode: str = "light") -> dict:
    """Kembalikan dict token warna sesuai mode ('light' / 'dark')."""
    return TOKENS.get(mode, TOKENS["light"])


def get_active_tokens() -> dict:
    """Baca mode dari session_state, kembalikan token yang sesuai."""
    mode = st.session_state.get("theme", "light")
    return get_tokens(mode)


def get_plotly_layout(mode: str = "light") -> dict:
    """
    Kembalikan dict layout Plotly yang sudah disesuaikan dengan color tokens.
    Gunakan sebagai: fig.update_layout(**get_plotly_layout())
    """
    t = get_tokens(mode)
    return {
        "paper_bgcolor": t["card"],
        "plot_bgcolor":  t["card"],
        "font":          {"color": t["text_primary"], "family": "Inter, sans-serif"},
        "xaxis":         {"gridcolor": t["border"], "linecolor": t["border"]},
        "yaxis":         {"gridcolor": t["border"], "linecolor": t["border"]},
        "margin":        {"l": 16, "r": 16, "t": 32, "b": 16},
    }
