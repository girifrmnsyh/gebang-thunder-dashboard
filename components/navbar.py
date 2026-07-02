"""
components/navbar.py — Dynamic Island Navbar (Minimalist Redesign)
PRD Section 5: Fixed navbar custom, bukan sidebar Streamlit.
  - Kiri : logo (gebang-thunder-logo.svg, warna primary) + nama tim + nomor tim
  - Tengah: 4 menu (Home, Summary, Analytics, ThunderChat) — teks only, no icon
  - Kanan : light/dark toggle dengan sun.svg & moon.svg
  - Style  : pill/rounded card, thin border shadow, Inter font

Theme Toggle Strategy:
  Karena navbar di-render via st.markdown (pure HTML), tombol toggle tidak bisa
  langsung trigger Streamlit rerun. Solusi: navbar toggle button set URL param
  ?theme=dark/light → app.py baca param ini saat rerun dan update session_state.
  Ini lebih reliable daripada JS click injection.
"""

import base64
import os
import streamlit as st
from utils.session import toggle_theme


def _read_svg(path: str) -> str:
    """Baca file SVG dan kembalikan kontennya sebagai string."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def _svg_to_b64(svg_content: str) -> str:
    """Encode SVG string ke base64 data URI."""
    if not svg_content:
        return ""
    encoded = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def _handle_theme_param() -> None:
    """
    Baca ?theme= dari query_params, update session_state jika ada,
    lalu hapus param dari URL agar tidak muncul permanen.
    Dipanggil di awal render_navbar.
    """
    theme_param = st.query_params.get("theme", None)
    if theme_param in ("light", "dark"):
        current = st.session_state.get("theme", "light")
        if current != theme_param:
            st.session_state["theme"] = theme_param
        # Hapus param theme dari URL setelah diproses
        params = dict(st.query_params)
        params.pop("theme", None)
        st.query_params.update(params)
        st.rerun()


def render_navbar(active_page: str = "home") -> None:
    """
    Render navbar dynamic island via pure HTML/CSS.
    Theme toggle menggunakan URL param strategy:
      - Klik toggle button → navigate ke ?theme=dark/light&page=...
      - App.py rerun → _handle_theme_param() baca & update session_state
    """

    # Handle incoming theme param (dari klik toggle sebelumnya)
    _handle_theme_param()

    theme = st.session_state.get("theme", "light")
    next_theme = "dark" if theme == "light" else "light"

    # ── Baca SVG icons ────────────────────────────────────────────────────────
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icons_dir = os.path.join(base_dir, "assets", "icons")

    logo_uri = _svg_to_b64(_read_svg(os.path.join(icons_dir, "gebang-thunder-logo.svg")))
    sun_uri  = _svg_to_b64(_read_svg(os.path.join(icons_dir, "sun.svg")))
    moon_uri = _svg_to_b64(_read_svg(os.path.join(icons_dir, "moon.svg")))

    # Light mode → tampilkan moon (switch ke dark) | Dark mode → tampilkan sun (switch ke light)
    toggle_icon_uri = moon_uri if theme == "light" else sun_uri
    toggle_tooltip  = "Ganti ke Mode Gelap" if theme == "light" else "Ganti ke Mode Terang"

    # ── Menu items ────────────────────────────────────────────────────────────
    menu_items = [
        ("home",              "Home"),
        ("executive_summary", "Summary"),
        ("gt_lab",            "Analytics"),
        ("ask_gemini",        "ThunderChat"),
    ]

    # ── Build menu HTML ───────────────────────────────────────────────────────
    menu_html_parts = []
    for page_key, label in menu_items:
        is_active = active_page == page_key
        active_class = "nav-link--active" if is_active else ""
        menu_html_parts.append(
            f'<a class="nav-link {active_class.strip()}" href="?page={page_key}">{label}</a>'
        )
    menu_html = "\n      ".join(menu_html_parts)

    # Toggle URL: pertahankan page param yang aktif saat toggle theme
    toggle_href = f"?page={active_page}&theme={next_theme}"

    # ── Render navbar HTML ────────────────────────────────────────────────────
    navbar_html = f"""
<div class="gt-navbar-wrapper">
  <nav class="gt-navbar">

    <!-- LEFT: Brand -->
    <div class="gt-navbar__brand">
      <img class="gt-navbar__logo"
           src="{logo_uri}"
           alt="Gebang Thunder Logo"
           width="20" height="20" />
      <div class="gt-navbar__brand-text">
        <span class="gt-navbar__team-name">Gebang Thunder</span>
        <span class="gt-navbar__team-id">SSDC2026017</span>
      </div>
    </div>

    <!-- CENTER: Navigation links -->
    <div class="gt-navbar__nav">
      {menu_html}
    </div>

    <!-- RIGHT: Theme toggle via URL param navigation -->
    <a href="{toggle_href}"
       class="gt-navbar__toggle"
       title="{toggle_tooltip}"
       id="gt-theme-toggle-btn">
      <img src="{toggle_icon_uri}"
           alt="Toggle theme"
           class="gt-navbar__toggle-icon"
           width="15" height="15" />
    </a>

  </nav>
</div>
"""
    st.markdown(navbar_html, unsafe_allow_html=True)
