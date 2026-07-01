"""
components/metric.py — Metric display components
"""

import streamlit as st
from utils.formatter import format_number, format_integer, format_percentage


def kpi_row(metrics: list[dict]) -> None:
    """
    Render satu baris KPI cards.

    metrics = list of dict:
      {
        "label": str,
        "value": str | float | int,
        "delta": str | None,
        "delta_ok": bool,   # True = positif (hijau), False = negatif (merah)
        "format": "number" | "integer" | "percentage" | "raw",
      }
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            raw = m.get("value", 0)
            fmt = m.get("format", "raw")

            if fmt == "number":
                display = format_number(raw)
            elif fmt == "integer":
                display = format_integer(raw)
            elif fmt == "percentage":
                display = format_percentage(raw)
            else:
                display = str(raw)

            delta = m.get("delta")
            delta_color = "normal"
            if delta is not None:
                delta_color = "normal" if m.get("delta_ok", True) else "inverse"

            st.metric(
                label=m["label"],
                value=display,
                delta=delta,
                delta_color=delta_color,
            )
