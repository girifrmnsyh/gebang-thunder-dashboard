"""
components/cards.py — Reusable card components
PRD Section 5: bento-grid cards (long & short) untuk Executive Summary.
"""

from __future__ import annotations

import streamlit as st


def metric_card(
    title: str,
    value: str,
    delta: str | None = None,
    delta_positive: bool = True,
    icon: str = "",
    subtitle: str = "",
) -> None:
    """
    Card metrik tunggal dengan nilai utama + delta opsional.
    Mirip komponen metric Streamlit tapi dengan styling custom.
    """
    delta_class = "positive" if delta_positive else "negative"
    delta_html = (
        f'<span class="card-delta {delta_class}">{delta}</span>'
        if delta else ""
    )
    icon_html = f'<span class="card-icon">{icon}</span>' if icon else ""
    subtitle_html = f'<p class="card-subtitle">{subtitle}</p>' if subtitle else ""

    html = f"""
    <div class="gt-card metric-card">
        <div class="card-header">
            {icon_html}
            <span class="card-title">{title}</span>
        </div>
        <div class="card-value">{value}</div>
        {delta_html}
        {subtitle_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def insight_card(
    title: str,
    body: str,
    tag: str = "",
    wide: bool = False,
) -> None:
    """
    Card narasi insight dengan teks variatif (bukan plain caption).
    wide=True untuk card lebar di bento-grid.
    """
    tag_html = f'<span class="card-tag">{tag}</span>' if tag else ""
    card_class = "gt-card insight-card wide" if wide else "gt-card insight-card"

    html = f"""
    <div class="{card_class}">
        <div class="card-header">
            {tag_html}
            <h3 class="card-title">{title}</h3>
        </div>
        <p class="card-body">{body}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def chart_card(title: str, subtitle: str = "") -> None:
    """
    Wrapper header untuk card yang berisi chart Plotly.
    Gunakan di dalam container/column sebelum st.plotly_chart().
    """
    subtitle_html = f'<p class="card-subtitle">{subtitle}</p>' if subtitle else ""
    html = f"""
    <div class="chart-card-header">
        <h3 class="card-title">{title}</h3>
        {subtitle_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
