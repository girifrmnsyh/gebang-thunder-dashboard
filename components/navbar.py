# components/navbar.py — Dynamic Island Navbar (Minimalist Redesign)
# PRD Section 5: Fixed navbar custom, bukan sidebar Streamlit.
# - Kiri : logo (gebang-thunder-logo.svg, warna primary) + nama tim + nomor tim
# - Tengah: 4 menu (Home, Summary, Analytics, ThunderChat) — teks only, no icon
# - Kanan : light/dark toggle dengan sun.svg & moon.svg
# - Style  : pill/rounded card, thin border shadow, Inter font
#
# Theme Toggle Strategy:
# Karena navbar di-render via st.markdown (pure HTML), tombol toggle tidak bisa
# langsung trigger Streamlit rerun. Solusi: navbar toggle button set URL param
# ?theme=dark/light → app.py baca param ini saat rerun dan update session_state.
# Ini lebih reliable daripada JS click injection.

import base64
import os
import textwrap
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
    """Render navbar dynamic island via pure HTML/CSS."""
    _handle_theme_param()

    theme = st.session_state.get("theme", "light")
    next_theme = "dark" if theme == "light" else "light"

    # ── Baca SVG icons ────────────────────────────────────────────────────────
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icons_dir = os.path.join(base_dir, "assets", "icons")

    logo_uri = _svg_to_b64(_read_svg(os.path.join(icons_dir, "gebang-thunder-logo.svg")))
    sun_uri  = _svg_to_b64(_read_svg(os.path.join(icons_dir, "sun.svg")))
    moon_uri = _svg_to_b64(_read_svg(os.path.join(icons_dir, "moon.svg")))

    toggle_icon_uri = moon_uri if theme == "light" else sun_uri
    toggle_tooltip  = "Ganti ke Mode Gelap" if theme == "light" else "Ganti ke Mode Terang"

    # ── CSS tokens berdasarkan tema aktif ─────────────────────────────────────
    if theme == "dark":
        css_navbar_bg         = "rgba(18, 18, 20, 0.72)"
        css_navbar_border     = "rgba(255, 255, 255, 0.10)"
        css_navbar_shadow     = ("0 4px 32px rgba(0, 0, 0, 0.55), "
                                 "0 1px 0 rgba(255, 255, 255, 0.06) inset")
        css_text_primary      = "#FAFAFA"
        css_text_secondary    = "#A1A1AA"
        css_primary           = "#3B82F6"
        css_hover_bg          = "rgba(59, 130, 246, 0.12)"
        css_toggle_bg         = "rgba(255, 255, 255, 0.06)"
        css_toggle_border     = "rgba(255, 255, 255, 0.12)"
        css_toggle_hover_bg   = "rgba(59, 130, 246, 0.18)"
        css_toggle_hover_bdr  = "rgba(59, 130, 246, 0.6)"
        css_toggle_icon_filter = "brightness(0) invert(0.75) saturate(0)"
        css_logo_filter       = ("brightness(0) saturate(100%) invert(45%) sepia(80%) "
                                 "saturate(600%) hue-rotate(200deg) brightness(110%) contrast(100%)")
        css_active_underline  = "#3B82F6"
    else:
        css_navbar_bg         = "rgba(255, 255, 255, 0.75)"
        css_navbar_border     = "rgba(0, 0, 0, 0.08)"
        css_navbar_shadow     = ("0 4px 24px rgba(0, 0, 0, 0.08), "
                                 "0 1px 0 rgba(255, 255, 255, 0.9) inset")
        css_text_primary      = "#111827"
        css_text_secondary    = "#6B7280"
        css_primary           = "#2563EB"
        css_hover_bg          = "rgba(37, 99, 235, 0.07)"
        css_toggle_bg         = "rgba(0, 0, 0, 0.04)"
        css_toggle_border     = "rgba(0, 0, 0, 0.10)"
        css_toggle_hover_bg   = "rgba(37, 99, 235, 0.08)"
        css_toggle_hover_bdr  = "rgba(37, 99, 235, 0.5)"
        css_toggle_icon_filter = ("brightness(0) saturate(100%) invert(49%) sepia(7%) "
                                   "saturate(497%) hue-rotate(182deg) brightness(90%) contrast(90%)")
        css_logo_filter        = ("brightness(0) saturate(100%) invert(21%) sepia(95%) "
                                  "saturate(1800%) hue-rotate(216deg) brightness(98%) contrast(97%)")
        css_active_underline  = "#2563EB"

    # ── Build menu HTML ───────────────────────────────────────────────────────
    menu_items = [
        ("home",              "Home"),
        ("executive_summary", "Summary"),
        ("gt_lab",            "Analytics"),
        ("ask_gemini",        "ThunderChat"),
    ]

    menu_html_parts = []
    for page_key, label in menu_items:
        is_active = active_page == page_key
        active_class = "nav-link--active" if is_active else ""
        menu_html_parts.append(
            f'<a class="nav-link {active_class.strip()}" href="?page={page_key}">{label}</a>'
        )
    menu_html = "\n      ".join(menu_html_parts)

    toggle_href = f"?page={active_page}&theme={next_theme}"

    # ── Render navbar HTML ────────────────────────────────────────────────────
    navbar_html = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

      .gt-navbar-wrapper {{
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 99999;
        width: max-content;
        max-width: calc(100vw - 48px);
        pointer-events: none;
      }}

      .gt-navbar {{
        pointer-events: all;
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 8px 14px;
        background: {css_navbar_bg};
        border: 1px solid {css_navbar_border};
        border-radius: 9999px;
        box-shadow: {css_navbar_shadow};
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        white-space: nowrap;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        transition: box-shadow 0.25s ease, background 0.25s ease;
      }}

      .gt-navbar:hover {{
        box-shadow: {css_navbar_shadow}, 0 0 0 1px {css_primary}22;
      }}

      .gt-navbar__brand {{
        display: flex;
        align-items: center;
        gap: 8px;
        flex-shrink: 0;
        text-decoration: none !important;
      }}

      .gt-navbar__logo {{
        width: 20px;
        height: 20px;
        flex-shrink: 0;
        filter: {css_logo_filter};
        transition: filter 0.2s ease;
      }}

      .gt-navbar__brand-text {{
        display: flex;
        flex-direction: column;
        gap: 0;
        line-height: 1.2;
      }}

      .gt-navbar__team-name {{
        font-size: 13px;
        font-weight: 600;
        color: {css_text_primary};
        letter-spacing: -0.01em;
      }}

      .gt-navbar__team-id {{
        font-size: 10.5px;
        font-weight: 400;
        color: {css_text_secondary};
        letter-spacing: 0.01em;
      }}

      .gt-navbar__brand::after {{
        content: '';
        display: block;
        width: 1px;
        height: 20px;
        background: {css_navbar_border};
        margin-left: 4px;
      }}

      .gt-navbar__nav {{
        display: flex;
        align-items: center;
        gap: 2px;
      }}

      .nav-link {{
        font-family: 'Inter', sans-serif;
        font-size: 13.5px;
        font-weight: 450;
        color: {css_text_secondary};
        text-decoration: none !important;
        padding: 5px 11px;
        border-radius: 9999px;
        transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        letter-spacing: -0.01em;
        display: inline-block;
      }}

      .nav-link:hover {{
        font-weight: 600;
        color: {css_text_primary};
        background: {css_hover_bg};
        text-decoration: none !important;
      }}

      .nav-link--active {{
        font-weight: 700;
        color: {css_text_primary};
        background: {css_hover_bg};
      }}

      .nav-link--active::after {{
        content: '';
        position: absolute;
        bottom: 3px;
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 22px);
        height: 2px;
        background: {css_active_underline};
        border-radius: 2px;
        opacity: 0.85;
      }}

      .gt-navbar__toggle {{
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 9999px;
        border: 1px solid {css_toggle_border};
        background: {css_toggle_bg};
        cursor: pointer;
        transition: background 0.18s ease, border-color 0.18s ease, transform 0.18s ease;
        padding: 0;
        text-decoration: none !important;
        color: inherit;
        margin-left: 2px;
      }}

      .gt-navbar__toggle:hover {{
        background: {css_toggle_hover_bg};
        border-color: {css_toggle_hover_bdr};
        transform: scale(1.08);
        text-decoration: none !important;
      }}

      .gt-navbar__toggle:active {{
        transform: scale(0.95);
      }}

      .gt-navbar__toggle-icon {{
        width: 15px;
        height: 15px;
        display: block;
        flex-shrink: 0;
        filter: {css_toggle_icon_filter};
        transition: filter 0.2s ease;
      }}

      [data-testid="stAppViewContainer"] > section:first-child,
      [data-testid="stAppViewContainer"] > div:first-child {{
        padding-top: 80px !important;
      }}
    </style>

    <div class="gt-navbar-wrapper">
      <nav class="gt-navbar">
        <div class="gt-navbar__brand">
          <img class="gt-navbar__logo" src="{logo_uri}" alt="Gebang Thunder Logo" width="20" height="20" />
          <div class="gt-navbar__brand-text">
            <span class="gt-navbar__team-name">Gebang Thunder</span>
            <span class="gt-navbar__team-id">SSDC2026017</span>
          </div>
        </div>
        <div class="gt-navbar__nav">
          {menu_html}
        </div>
        <a href="{toggle_href}" class="gt-navbar__toggle" title="{toggle_tooltip}" id="gt-theme-toggle-btn">
          <img src="{toggle_icon_uri}" alt="Toggle theme" class="gt-navbar__toggle-icon" width="15" height="15" />
        </a>
      </nav>
    </div>
    """

    # KUNCI PERBAIKAN: Gunakan textwrap.dedent() untuk menghapus spasi awal (indentasi)
    # yang menyebabkan Streamlit membacanya sebagai Markdown Code Block
    st.markdown(textwrap.dedent(navbar_html), unsafe_allow_html=True)