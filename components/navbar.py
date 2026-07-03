# components/navbar.py — Dynamic Island Navbar (Minimalist Redesign)
# PRD Section 5: Fixed navbar custom, bukan sidebar Streamlit.
# - Kiri : logo (gebang-thunder-logo.svg, warna #2563EB) + nama tim + nomor tim
# - Tengah: 4 menu (Home, Summary, Analytics, ThunderChat) — teks only, no icon
# - Kanan : light/dark toggle dengan sun.svg & moon.svg
# - Style  : pill/rounded card, glassmorphic, Inter font
#
# Theme Toggle Strategy:
# Navbar toggle button → set URL param ?theme=dark/light&page=...
# → app.py rerun → _handle_theme_param() baca & update session_state
# st.rerun() HANYA dipanggil jika theme benar-benar berubah (fix blank-page bug).

import base64
import os
import re
import textwrap
import streamlit as st


# ── SVG helpers ───────────────────────────────────────────────────────────────

def _read_svg(path: str) -> str:
    """Baca file SVG dan kembalikan kontennya sebagai string."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def _colorize_svg(svg_content: str, color: str) -> str:
    """
    Ganti stroke="currentColor" dan fill="currentColor" di SVG
    dengan warna eksplisit agar tampil benar saat digunakan sebagai <img src>.
    Browser tidak mewarisi currentColor dari CSS ketika SVG dimuat via <img>.
    """
    if not svg_content:
        return ""
    result = svg_content
    result = re.sub(r'stroke="currentColor"', f'stroke="{color}"', result)
    result = re.sub(r'fill="currentColor"', f'fill="{color}"', result)
    return result


def _svg_to_b64(svg_content: str) -> str:
    """Encode SVG string ke base64 data URI."""
    if not svg_content:
        return ""
    encoded = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def _colored_svg_uri(path: str, color: str) -> str:
    """Baca SVG, warnai dengan `color`, lalu kembalikan sebagai data URI base64."""
    raw = _read_svg(path)
    colored = _colorize_svg(raw, color)
    return _svg_to_b64(colored)


# ── Theme param handler ───────────────────────────────────────────────────────

def _handle_theme_param() -> None:
    """
    Baca ?theme= dari query_params, update session_state jika ada,
    lalu hapus param dari URL.

    BUG FIX: st.rerun() hanya dipanggil jika theme benar-benar BERUBAH.
    Sebelumnya rerun() selalu dipanggil saat ?theme= ada di URL,
    menyebabkan infinite rerun / blank page.
    """
    theme_param = st.query_params.get("theme", None)
    if theme_param not in ("light", "dark"):
        return  # Tidak ada param theme — tidak perlu apa-apa

    current = st.session_state.get("theme", "light")
    theme_changed = current != theme_param

    if theme_changed:
        st.session_state["theme"] = theme_param

    # Hapus param theme dari URL setelah diproses (selalu hapus agar URL bersih)
    params = dict(st.query_params)
    params.pop("theme", None)
    st.query_params.update(params)

    # Rerun HANYA jika theme benar-benar berubah
    if theme_changed:
        st.rerun()


# ── Main render ───────────────────────────────────────────────────────────────

def render_navbar(active_page: str = "home") -> None:
    """Render navbar dynamic island via pure HTML/CSS."""
    _handle_theme_param()

    theme = st.session_state.get("theme", "light")
    next_theme = "dark" if theme == "light" else "light"

    # ── Direktori icons ───────────────────────────────────────────────────────
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icons_dir = os.path.join(base_dir, "assets", "icons")

    # ── Logo: inject warna #2563EB langsung ke SVG ────────────────────────────
    # Pendekatan ini lebih andal daripada CSS filter karena <img> tidak mewarisi
    # currentColor dari DOM parent.
    logo_color = "#2563EB"  # Primary blue, konsisten di light dan dark
    logo_uri = _colored_svg_uri(os.path.join(icons_dir, "gebang-thunder-logo.svg"), logo_color)

    # ── Toggle icons: warna disesuaikan dengan tema ───────────────────────────
    if theme == "light":
        # Light mode → tombol toggle menampilkan moon (untuk switch ke dark)
        # Warna moon abu-abu (#6B7280) agar kontras di atas background putih
        toggle_icon_uri = _colored_svg_uri(os.path.join(icons_dir, "moon.svg"), "#6B7280")
        toggle_tooltip  = "Ganti ke Mode Gelap"
    else:
        # Dark mode → tombol toggle menampilkan sun (untuk switch ke light)
        # Warna sun kuning/amber (#FBBF24) agar kontras di atas background gelap
        toggle_icon_uri = _colored_svg_uri(os.path.join(icons_dir, "sun.svg"), "#FBBF24")
        toggle_tooltip  = "Ganti ke Mode Terang"

    # ── CSS tokens berdasarkan tema aktif ─────────────────────────────────────
    if theme == "dark":
        css_navbar_bg        = "rgba(18, 18, 20, 0.80)"
        css_navbar_border    = "rgba(255, 255, 255, 0.10)"
        css_navbar_shadow    = ("0 4px 32px rgba(0, 0, 0, 0.60), "
                                "0 1px 0 rgba(255, 255, 255, 0.06) inset")
        css_text_primary     = "#FAFAFA"
        css_text_secondary   = "#A1A1AA"
        css_primary          = "#3B82F6"
        css_hover_bg         = "rgba(59, 130, 246, 0.14)"
        css_toggle_bg        = "rgba(255, 255, 255, 0.08)"
        css_toggle_border    = "rgba(255, 255, 255, 0.14)"
        css_toggle_hover_bg  = "rgba(59, 130, 246, 0.20)"
        css_toggle_hover_bdr = "rgba(59, 130, 246, 0.65)"
        css_active_underline = "#3B82F6"
        css_divider          = "rgba(255, 255, 255, 0.10)"
    else:
        css_navbar_bg        = "rgba(255, 255, 255, 0.80)"
        css_navbar_border    = "rgba(0, 0, 0, 0.08)"
        css_navbar_shadow    = ("0 4px 24px rgba(0, 0, 0, 0.08), "
                                "0 1px 0 rgba(255, 255, 255, 0.95) inset")
        css_text_primary     = "#111827"
        css_text_secondary   = "#6B7280"
        css_primary          = "#2563EB"
        css_hover_bg         = "rgba(37, 99, 235, 0.07)"
        css_toggle_bg        = "rgba(0, 0, 0, 0.04)"
        css_toggle_border    = "rgba(0, 0, 0, 0.10)"
        css_toggle_hover_bg  = "rgba(37, 99, 235, 0.08)"
        css_toggle_hover_bdr = "rgba(37, 99, 235, 0.50)"
        css_active_underline = "#2563EB"
        css_divider          = "rgba(0, 0, 0, 0.08)"

    # ── Build menu HTML ───────────────────────────────────────────────────────
    menu_items = [
        ("home",              "Home"),
        ("executive_summary", "Summary"),
        ("gt_lab",            "Analytics"),
        ("ask_gemini",        "ThunderChat"),
    ]

    menu_html_parts = []
    for page_key, label in menu_items:
        is_active  = active_page == page_key
        active_cls = "nav-link--active" if is_active else ""
        menu_html_parts.append(
            f'<a class="nav-link {active_cls.strip()}" href="?page={page_key}" target="_self">{label}</a>'
        )
    menu_html = "\n          ".join(menu_html_parts)

    # Toggle URL: pertahankan page param yang aktif saat toggle theme
    toggle_href = f"?page={active_page}&theme={next_theme}"

    # ── Render navbar HTML ────────────────────────────────────────────────────
    navbar_html = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');

      /* ── Wrapper: fixed centered floating pill ─────────────────── */
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

      /* ── Pill card (Dynamic Island) ────────────────────────────── */
      .gt-navbar {{
        pointer-events: all;
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 7px 12px;
        background: {css_navbar_bg};
        border: 1px solid {css_navbar_border};
        border-radius: 9999px;
        box-shadow: {css_navbar_shadow};
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        white-space: nowrap;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        transition: box-shadow 0.25s ease;
      }}

      /* ── Brand kiri ─────────────────────────────────────────────── */
      .gt-navbar__brand {{
        display: flex;
        align-items: center;
        gap: 7px;
        flex-shrink: 0;
        text-decoration: none !important;
      }}

      .gt-navbar__logo {{
        width: 20px;
        height: 20px;
        flex-shrink: 0;
        display: block;
      }}

      .gt-navbar__brand-text {{
        display: flex;
        flex-direction: column;
        gap: 0;
        line-height: 1.15;
      }}

      .gt-navbar__team-name {{
        font-size: 12.5px;
        font-weight: 600;
        color: {css_text_primary};
        letter-spacing: -0.01em;
      }}

      .gt-navbar__team-id {{
        font-size: 10px;
        font-weight: 400;
        color: {css_text_secondary};
        letter-spacing: 0.01em;
      }}

      /* Divider tipis antara brand dan nav */
      .gt-navbar__divider {{
        width: 1px;
        height: 18px;
        background: {css_divider};
        flex-shrink: 0;
      }}

      /* ── Nav links tengah ───────────────────────────────────────── */
      .gt-navbar__nav {{
        display: flex;
        align-items: center;
        gap: 2px;
      }}

      .nav-link {{
        font-family: 'Inter', sans-serif;
        font-size: 13.5px;
        font-weight: 500;
        color: {css_text_primary};
        text-decoration: none !important;
        padding: 5px 11px;
        border-radius: 9999px;
        transition: background 0.15s ease, color 0.15s ease, font-weight 0.1s ease;
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

      /* Active state: bold + background tint + underline primer */
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
        opacity: 0.9;
      }}

      /* ── Theme toggle kanan ─────────────────────────────────────── */
      .gt-navbar__toggle {{
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        border-radius: 9999px;
        border: 1px solid {css_toggle_border};
        background: {css_toggle_bg};
        cursor: pointer;
        transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
        padding: 0;
        text-decoration: none !important;
        color: inherit;
      }}

      .gt-navbar__toggle:hover {{
        background: {css_toggle_hover_bg};
        border-color: {css_toggle_hover_bdr};
        transform: scale(1.10);
        text-decoration: none !important;
      }}

      .gt-navbar__toggle:active {{
        transform: scale(0.93);
      }}

      .gt-navbar__toggle-icon {{
        width: 14px;
        height: 14px;
        display: block;
        flex-shrink: 0;
      }}

      /* ── Streamlit: padding atas agar konten tidak tertimpa navbar ── */
      [data-testid="stAppViewContainer"] > section:first-child,
      [data-testid="stAppViewContainer"] > div:first-child {{
        padding-top: 80px !important;
      }}
    </style>

    <div class="gt-navbar-wrapper">
      <nav class="gt-navbar">

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

        <div class="gt-navbar__divider"></div>

        <div class="gt-navbar__nav">
          {menu_html}
        </div>

        <a href="{toggle_href}"
           target="_self"
           class="gt-navbar__toggle"
           title="{toggle_tooltip}"
           id="gt-theme-toggle-btn">
          <img src="{toggle_icon_uri}"
               alt="Toggle theme"
               class="gt-navbar__toggle-icon"
               width="14" height="14" />
        </a>

      </nav>
    </div>
    """
    
    # INI KUNCI UTAMANYA: textwrap.dedent wajib ada agar HTML tidak jadi Code Block
    st.markdown(textwrap.dedent(navbar_html), unsafe_allow_html=True)