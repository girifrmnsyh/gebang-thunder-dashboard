"""
app.py — Entrypoint & Query Params Router
Gebang Thunder Dashboard — Ready to Take Off

Routing menggunakan st.query_params agar URL shareable dan state tetap
terjaga saat browser di-refresh (bukan hanya st.session_state).
"""

import streamlit as st

from config.settings import APP_CONFIG
from utils.session import init_session_state
from components.navbar import render_navbar

# ── Konfigurasi halaman Streamlit ─────────────────────────────────────────────
st.set_page_config(
    page_title=APP_CONFIG["title"],
    page_icon=APP_CONFIG["icon"],
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inisialisasi session state ────────────────────────────────────────────────
init_session_state()

# ── Baca query param untuk routing halaman ───────────────────────────────────
VALID_PAGES = ["home", "executive_summary", "gt_lab", "ask_gemini"]
page_param = st.query_params.get("page", "home")

if page_param not in VALID_PAGES:
    page_param = "home"
    st.query_params["page"] = "home"

# ── Inject CSS global ─────────────────────────────────────────────────────────
def load_css(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles/main.css")
load_css("styles/cards.css")
load_css("styles/sidebar.css")
load_css("styles/typography.css")

# Inject dynamic theme variables based on session state
from config.theme import get_active_tokens
theme_mode = st.session_state.get("theme", "light")
t = get_active_tokens()
theme_css = f"""
<style>
:root {{
  --bg:           {t['background']};
  --bg-secondary: {t['secondary_background']};
  --card:         {t['card']};
  --border:       {t['border']};
  --primary:      {t['primary']};
  --primary-rgb:  {t['primary_rgb']};
  --hover:        {t['hover']};
  --text-primary: {t['text_primary']};
  --text-secondary: {t['text_secondary']};
}}
</style>
<script>
// Set data-theme attribute pada root element agar CSS selector [data-theme='dark'] bekerja
(function() {{
  var mode = "{theme_mode}";
  document.documentElement.setAttribute('data-theme', mode);
  document.body.setAttribute('data-theme', mode);
  // Tambahkan/hapus class dark pada body sebagai fallback
  if (mode === 'dark') {{
    document.documentElement.classList.add('dark');
    document.body.classList.add('dark');
  }} else {{
    document.documentElement.classList.remove('dark');
    document.body.classList.remove('dark');
  }}
}})();
</script>
"""
st.markdown(theme_css, unsafe_allow_html=True)

# ── Render navbar (fixed, dynamic island style) ───────────────────────────────
render_navbar(active_page=page_param)

# ── Router: render page sesuai query param ───────────────────────────────────
if page_param == "home":
    from pages.home.page import render as render_home
    render_home()

elif page_param == "executive_summary":
    from pages.executive_summary.page import render as render_exec
    render_exec()

elif page_param == "gt_lab":
    from pages.gt_lab.page import render as render_gtlab
    render_gtlab()

elif page_param == "ask_gemini":
    from pages.ask_gemini.page import render as render_ask
    render_ask()
