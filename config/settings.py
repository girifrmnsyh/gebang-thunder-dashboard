"""
config/settings.py — Global application settings
"""

APP_CONFIG = {
    "title": "Gebang Thunder Dashboard",
    "icon": "⚡",
    "version": "1.0.0",
    "team": "Gebang Thunder",
    "karya": "Ready to Take Off",
    "year": 2026,
}

# Halaman valid untuk routing
VALID_PAGES = ["home", "executive_summary", "gt_lab", "ask_gemini"]
DEFAULT_PAGE = "home"

# Gemini model default (Flash tier — tersedia di free tier 2026)
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_TEMPERATURE = 0.4
GEMINI_MAX_TOKENS = 2048

# Cache TTL (detik)
CSV_CACHE_TTL = 3600       # 1 jam
GEMINI_CACHE_TTL = 1800    # 30 menit
ICON_CACHE_TTL = None      # indefinite (file statis)
