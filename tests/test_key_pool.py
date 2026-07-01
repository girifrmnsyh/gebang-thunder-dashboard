"""
tests/test_key_pool.py — Unit tests untuk KeyPool
PRD Section 8: tests/ minimal cover key rotation logic.
"""

import pytest
from unittest.mock import patch, MagicMock


# ── Mock streamlit.secrets sebelum import KeyPool ───────────────────────────
@pytest.fixture(autouse=True)
def mock_streamlit(monkeypatch):
    """Mock st.secrets dan st.cache_resource agar bisa ditest tanpa Streamlit."""
    mock_st = MagicMock()
    mock_st.secrets = {
        "gemini": {
            "api_keys": ["key_aaa", "key_bbb", "key_ccc"]
        }
    }
    # st.cache_resource jadi passthrough decorator
    mock_st.cache_resource = lambda func: func

    monkeypatch.setattr("utils.key_pool.st", mock_st)


def make_pool():
    """Buat KeyPool fresh (bypass cache untuk testing)."""
    from utils.key_pool import KeyPool
    return KeyPool()


class TestKeyPool:

    def test_initial_available_count(self):
        pool = make_pool()
        assert pool.available_count() == 3

    def test_get_key_returns_key(self):
        pool = make_pool()
        key = pool.get_key()
        assert key in ["key_aaa", "key_bbb", "key_ccc"]

    def test_round_robin_rotation(self):
        pool = make_pool()
        keys_fetched = [pool.get_key() for _ in range(6)]
        # Harus ada lebih dari 1 unique key yang dikembalikan
        assert len(set(keys_fetched)) > 1

    def test_mark_failed_reduces_available(self):
        pool = make_pool()
        pool.mark_failed("key_aaa")
        assert pool.available_count() == 2

    def test_mark_failed_skips_key(self):
        pool = make_pool()
        pool.mark_failed("key_aaa")
        for _ in range(10):
            key = pool.get_key()
            assert key != "key_aaa", "Key yang di-mark failed tidak boleh dikembalikan"

    def test_all_exhausted_when_all_failed(self):
        pool = make_pool()
        pool.mark_failed("key_aaa")
        pool.mark_failed("key_bbb")
        pool.mark_failed("key_ccc")
        assert pool.all_exhausted() is True

    def test_get_key_returns_none_when_exhausted(self):
        pool = make_pool()
        pool.mark_failed("key_aaa")
        pool.mark_failed("key_bbb")
        pool.mark_failed("key_ccc")
        assert pool.get_key() is None

    def test_alias_masks_key(self):
        assert KeyPool._alias("abcdef1234") == "sk-...1234"

    def test_alias_short_key(self):
        assert KeyPool._alias("ab") == "sk-****"


def test_alias_standalone():
    from utils.key_pool import KeyPool
    assert KeyPool._alias("my-super-secret-key-XYZ") == "sk-...-XYZ"
