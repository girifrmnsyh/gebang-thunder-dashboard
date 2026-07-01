"""
utils/key_pool.py — Multi-key rotation untuk Gemini API
PRD Section 7.1

Strategi:
  - Round-robin get_key()
  - mark_failed() untuk skip key yang kena daily limit (RPD)
  - Retry dengan exponential backoff untuk rate limit sementara (RPM/TPM)
  - Graceful fallback kalau semua key exhausted
"""

from __future__ import annotations

import time
import logging
import streamlit as st

logger = logging.getLogger(__name__)


@st.cache_resource
def get_key_pool() -> "KeyPool":
    """Singleton KeyPool, di-cache sebagai resource (tidak re-init saat rerun)."""
    return KeyPool()


class KeyPool:
    """
    Pool rotasi API key Gemini.
    Key di-load dari st.secrets["gemini"]["api_keys"].
    """

    def __init__(self) -> None:
        try:
            raw_keys: list[str] = st.secrets["gemini"]["api_keys"]
        except (KeyError, AttributeError):
            logger.warning("Gemini API keys tidak ditemukan di secrets.")
            raw_keys = []

        self._keys: list[str] = [k.strip() for k in raw_keys if k.strip()]
        self._failed: set[str] = set()       # key yang kena RPD / error permanen
        self._index: int = 0                 # pointer round-robin
        self._call_counts: dict[str, int] = {k: 0 for k in self._keys}

    # ── Public API ─────────────────────────────────────────────────────────────

    def get_key(self) -> str | None:
        """
        Ambil key berikutnya (round-robin), skip key yang sudah di-mark failed.
        Return None jika semua key exhausted.
        """
        available = [k for k in self._keys if k not in self._failed]
        if not available:
            return None

        key = available[self._index % len(available)]
        self._index = (self._index + 1) % len(available)
        self._call_counts[key] = self._call_counts.get(key, 0) + 1

        # Log alias (bukan full key) untuk keamanan
        alias = self._alias(key)
        logger.debug("Menggunakan key %s (total panggilan: %d)", alias, self._call_counts[key])
        return key

    def mark_failed(self, key: str) -> None:
        """
        Tandai key sebagai gagal (kena RPD / error permanen).
        Key ini dilewati sampai app di-restart.
        """
        alias = self._alias(key)
        logger.warning("Key %s ditandai gagal (RPD/permanen).", alias)
        self._failed.add(key)

    def all_exhausted(self) -> bool:
        """True jika tidak ada key yang masih bisa dipakai."""
        return all(k in self._failed for k in self._keys) or not self._keys

    def available_count(self) -> int:
        """Jumlah key yang masih aktif."""
        return sum(1 for k in self._keys if k not in self._failed)

    # ── Internal helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _alias(key: str) -> str:
        """Mask key untuk logging — tampilkan hanya 4 karakter terakhir."""
        return f"sk-...{key[-4:]}" if len(key) > 4 else "sk-****"

    @staticmethod
    def exponential_backoff(attempt: int, base: float = 10.0, cap: float = 60.0) -> None:
        """Sleep dengan exponential backoff untuk retry RPM/TPM."""
        delay = min(base * (2 ** attempt), cap)
        logger.info("Backoff %.1f detik (attempt %d)...", delay, attempt)
        time.sleep(delay)
