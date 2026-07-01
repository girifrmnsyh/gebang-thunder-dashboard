"""
components/icon.py — render_icon() helper untuk Lucide SVG lokal
PRD Section 6: bundle SVG lokal, bukan fetch dari CDN.
"""

from __future__ import annotations

import streamlit as st
from pathlib import Path

ICON_DIR = Path("assets/icons")


@st.cache_data(show_spinner=False)
def _read_svg(name: str) -> str | None:
    """
    Baca file SVG dari assets/icons/.
    Di-cache oleh Streamlit — tidak re-read disk tiap rerun.
    """
    path = ICON_DIR / f"{name}.svg"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def render_icon(
    name: str,
    size: int = 20,
    color: str | None = None,
    class_name: str = "",
) -> None:
    """
    Render icon Lucide SVG via st.markdown.

    Args:
        name:       Nama file SVG (tanpa ekstensi), misal "home", "bar-chart-2"
        size:       Ukuran dalam pixel (width & height)
        color:      Warna stroke. None = pakai CSS currentColor (inherit dari parent)
        class_name: CSS class tambahan untuk wrapper div
    """
    svg = _read_svg(name)

    if svg is None:
        # Fallback: emoji jika icon tidak ditemukan
        st.markdown(f"<span title='{name}'>□</span>", unsafe_allow_html=True)
        return

    # Inject width, height, color ke SVG
    svg = svg.replace('width="24"', f'width="{size}"')
    svg = svg.replace('height="24"', f'height="{size}"')

    if color:
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')

    wrapper_class = f'gt-icon {class_name}'.strip()
    html = f'<span class="{wrapper_class}" style="display:inline-flex;align-items:center;">{svg}</span>'
    st.markdown(html, unsafe_allow_html=True)


def icon_html(
    name: str,
    size: int = 20,
    color: str | None = None,
) -> str:
    """
    Kembalikan HTML string icon (untuk embed di dalam string HTML lain).
    Tidak memanggil st.markdown — cocok untuk dipakai di dalam f-string HTML.
    """
    svg = _read_svg(name)
    if svg is None:
        return "□"

    svg = svg.replace('width="24"', f'width="{size}"').replace('height="24"', f'height="{size}"')
    if color:
        svg = svg.replace('stroke="currentColor"', f'stroke="{color}"')
    return svg
