"""
services/csv_service.py — Load & validasi CSV fixed dari data/
PRD Section 2 & 8: dataset fixed di-commit ke repo, baca sekali pakai cache.
"""

import pandas as pd
import streamlit as st
from pathlib import Path

from config.constants import ERROR_MESSAGES
from utils.logger import log

# Path default dataset
RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")
SAMPLE_DATA_DIR = Path("data/sample")


@st.cache_data(show_spinner=False)
def load_csv(filepath: str | Path, **kwargs) -> pd.DataFrame | None:
    """
    Load CSV dari path yang diberikan.
    Di-cache oleh Streamlit — tidak re-read disk tiap rerun.

    Return DataFrame, atau None jika gagal (dengan log error).
    """
    path = Path(filepath)

    if not path.exists():
        log.error("File tidak ditemukan: %s", path)
        return None

    try:
        df = pd.read_csv(path, **kwargs)
        log.info("Dataset dimuat: %s (%d baris, %d kolom)", path.name, len(df), len(df.columns))
        return df
    except pd.errors.ParserError as e:
        log.error("CSV corrupt atau format tidak valid (%s): %s", path.name, e)
        return None
    except Exception as e:
        log.error("Gagal membaca CSV (%s): %s", path.name, e)
        return None


def get_main_dataset() -> pd.DataFrame | None:
    """
    Load dataset utama dari data/raw/.
    Ubah path ke file CSV aktual saat dataset tersedia.
    """
    # TODO: Ganti dengan nama file CSV aktual dari panitia
    candidates = list(RAW_DATA_DIR.glob("*.csv"))

    if not candidates:
        log.warning("Tidak ada file CSV di data/raw/. Mencoba data/sample/...")
        candidates = list(SAMPLE_DATA_DIR.glob("*.csv"))

    if not candidates:
        log.error("Tidak ada dataset yang tersedia.")
        return None

    return load_csv(candidates[0])


def get_sample_dataset() -> pd.DataFrame | None:
    """Load dummy dataset dari data/sample/ untuk dev/demo."""
    candidates = list(SAMPLE_DATA_DIR.glob("*.csv"))
    if not candidates:
        log.warning("Tidak ada file di data/sample/.")
        return None
    return load_csv(candidates[0])
