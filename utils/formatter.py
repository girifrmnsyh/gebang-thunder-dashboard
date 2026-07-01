"""
utils/formatter.py — Format angka & tanggal konvensi Indonesia
PRD Section 3: titik (.) untuk ribuan, koma (,) untuk desimal, DD/MM/YYYY
"""

from __future__ import annotations

from datetime import datetime
from config.constants import DATE_FORMAT, DECIMAL_SEPARATOR, THOUSAND_SEPARATOR


def format_number(value: float | int, decimal_places: int = 2) -> str:
    """
    Format angka dengan konvensi Indonesia.
    Contoh: 1234567.89 → '1.234.567,89'
    """
    try:
        formatted = f"{value:,.{decimal_places}f}"
        # Swap: koma → titik sementara, titik → koma
        formatted = formatted.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
        return formatted
    except (TypeError, ValueError):
        return str(value)


def format_integer(value: int) -> str:
    """
    Format bilangan bulat dengan pemisah ribuan Indonesia.
    Contoh: 1234567 → '1.234.567'
    """
    try:
        formatted = f"{int(value):,}"
        return formatted.replace(",", ".")
    except (TypeError, ValueError):
        return str(value)


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """
    Format persentase.
    Contoh: 0.856 → '85,6%'
    """
    try:
        pct = value * 100 if abs(value) <= 1 else value
        return f"{pct:.{decimal_places}f}%".replace(".", ",")
    except (TypeError, ValueError):
        return str(value)


def format_date(date_obj: datetime | str, input_format: str = "%Y-%m-%d") -> str:
    """
    Format tanggal ke konvensi Indonesia (DD/MM/YYYY).
    Menerima objek datetime atau string.
    """
    try:
        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, input_format)
        return date_obj.strftime(DATE_FORMAT)
    except (TypeError, ValueError):
        return str(date_obj)


def format_currency(value: float, prefix: str = "Rp") -> str:
    """
    Format mata uang Rupiah.
    Contoh: 1500000 → 'Rp 1.500.000'
    """
    return f"{prefix} {format_integer(value)}"
