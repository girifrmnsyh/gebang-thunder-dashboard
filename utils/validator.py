"""
utils/validator.py — Validasi data & input
"""

import pandas as pd
from typing import Optional


def validate_csv_columns(
    df: pd.DataFrame,
    required_columns: list[str],
    source: str = "dataset",
) -> tuple[bool, list[str]]:
    """
    Periksa apakah DataFrame memiliki semua kolom yang dibutuhkan.
    Return (is_valid, missing_columns).
    """
    missing = [col for col in required_columns if col not in df.columns]
    return (len(missing) == 0, missing)


def validate_dataframe_not_empty(df: pd.DataFrame, source: str = "dataset") -> bool:
    """Return True jika DataFrame tidak kosong."""
    return df is not None and not df.empty


def sanitize_user_input(text: str, max_length: int = 2000) -> str:
    """
    Sanitasi input teks dari user (untuk Ask to Gemini).
    Potong jika terlalu panjang, strip whitespace.
    """
    if not isinstance(text, str):
        return ""
    return text.strip()[:max_length]
