"""
config/constants.py — Application-wide constants
"""

# ── Halaman & navigasi ────────────────────────────────────────────────────────
PAGE_LABELS = {
    "home": "Beranda",
    "executive_summary": "Executive Summary",
    "gt_lab": "GT Lab",
    "ask_gemini": "Ask to Gemini",
}

# ── GT Lab — model types ──────────────────────────────────────────────────────
GT_LAB_MODELS = ["Regression", "Classification", "Clustering"]

# ── Format angka & tanggal (konvensi Indonesia) ───────────────────────────────
DATE_FORMAT = "%d/%m/%Y"
DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = "."

# ── Error messages (Bahasa Indonesia, user-friendly) ─────────────────────────
ERROR_MESSAGES = {
    "csv_not_found": "Dataset tidak ditemukan. Hubungi tim pengembang.",
    "csv_corrupt": "Dataset tidak dapat dibaca. Format file mungkin tidak valid.",
    "gemini_busy": "Maaf, sistem AI sedang sibuk. Coba beberapa saat lagi ya.",
    "gemini_quota": "Batas permintaan harian tercapai. Coba lagi besok.",
    "gemini_all_exhausted": (
        "Semua kapasitas AI saat ini telah habis. "
        "Silakan coba lagi nanti atau hubungi tim kami."
    ),
    "gemini_invalid_key": "Konfigurasi API tidak valid. Hubungi tim pengembang.",
    "gemini_network": "Koneksi ke layanan AI gagal. Periksa koneksi internetmu.",
    "generic": "Terjadi kesalahan. Coba muat ulang halaman.",
}
