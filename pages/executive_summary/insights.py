"""
pages/executive_summary/insights.py — Insight text & narrative components
Data table & brief insight disiapkan manual oleh product owner (PRD Section 1).
"""

import streamlit as st


def render_insight_block(title: str, body: str, highlight: str = "") -> None:
    """
    Render blok insight narasi dengan highlight opsional.
    Dipakai di bento-grid card.
    """
    highlight_html = (
        f'<span class="insight-highlight">{highlight}</span>'
        if highlight else ""
    )
    html = f"""
    <div class="insight-block">
        <h4 class="insight-title">{title}</h4>
        {highlight_html}
        <p class="insight-body">{body}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ── Insight data (diisi oleh product owner setelah dataset tersedia) ──────────

INSIGHTS: list[dict] = [
    # Contoh format:
    # {
    #     "title": "Temuan Utama",
    #     "highlight": "42% peningkatan",
    #     "body": "Terjadi peningkatan signifikan pada periode Q2...",
    # },
]


def render_all_insights() -> None:
    """Render semua insight dari list INSIGHTS."""
    if not INSIGHTS:
        st.info("💡 Insight akan ditambahkan setelah dataset & analisis tersedia.")
        return

    for ins in INSIGHTS:
        render_insight_block(
            title=ins.get("title", ""),
            body=ins.get("body", ""),
            highlight=ins.get("highlight", ""),
        )
