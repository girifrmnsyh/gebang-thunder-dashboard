"""
pages/executive_summary/charts.py — Chart implementations Executive Summary
Diisi setelah dataset & analisis final tersedia (PRD Section 9).
"""

import plotly.express as px
import pandas as pd
from config.theme import get_active_tokens, get_plotly_layout
import streamlit as st


def placeholder_chart(title: str = "Chart") -> None:
    """Placeholder chart sampai data tersedia."""
    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_annotation(
        text="Chart akan tersedia setelah dataset rilis",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14),
    )
    t = get_active_tokens()
    fig.update_layout(
        title=title,
        **get_plotly_layout(st.session_state.get("theme", "dark")),
        height=300,
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Chart functions (tambahkan setelah dataset tersedia) ─────────────────────

def trend_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str = "Tren") -> None:
    """Line/area chart tren utama."""
    fig = px.area(df, x=x_col, y=y_col, title=title)
    fig.update_layout(**get_plotly_layout(st.session_state.get("theme", "dark")))
    st.plotly_chart(fig, use_container_width=True)


def distribution_chart(df: pd.DataFrame, col: str, title: str = "Distribusi") -> None:
    """Histogram distribusi."""
    fig = px.histogram(df, x=col, title=title)
    fig.update_layout(**get_plotly_layout(st.session_state.get("theme", "dark")))
    st.plotly_chart(fig, use_container_width=True)
