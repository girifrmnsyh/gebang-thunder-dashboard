"""
services/gemini_service.py — Consumer Gemini API dengan multi-key pooling
PRD Section 7.1 & 7.2

Error handling per tipe:
  - 429 RPM/TPM → retry key yang sama + exponential backoff
  - 429 RPD     → mark_failed, rotate ke key berikutnya
  - invalid key → mark_failed, rotate
  - network     → retry singkat
  - semua key exhausted → graceful fallback message
"""

from __future__ import annotations

import hashlib
import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from utils.key_pool import get_key_pool
from utils.logger import log
from config.settings import GEMINI_MODEL, GEMINI_TEMPERATURE, GEMINI_MAX_TOKENS
from config.constants import ERROR_MESSAGES

MAX_RETRIES = 3  # maksimum rotasi key saat error


@st.cache_data(ttl=1800, show_spinner=False)
def _cached_generate(prompt: str, system_context: str, model_name: str) -> str | None:
    """
    Wrapper yang di-cache: query identik (prompt + context) tidak re-consume quota.
    Cache key otomatis dari argumen fungsi (hashable strings).
    """
    return _generate_uncached(prompt, system_context, model_name)


def _generate_uncached(prompt: str, system_context: str, model_name: str) -> str | None:
    """Eksekusi panggilan API Gemini dengan rotasi key & error handling."""
    pool = get_key_pool()

    for attempt in range(MAX_RETRIES):
        key = pool.get_key()

        if key is None:
            log.warning("Semua Gemini API key exhausted.")
            return None

        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_context,
            )
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=GEMINI_TEMPERATURE,
                    max_output_tokens=GEMINI_MAX_TOKENS,
                ),
            )
            return response.text

        except google_exceptions.ResourceExhausted as e:
            error_str = str(e).lower()
            if "quota" in error_str or "daily" in error_str:
                # RPD — tandai failed, rotate
                pool.mark_failed(key)
                log.warning("RPD tercapai untuk key ini, rotate ke key berikutnya.")
            else:
                # RPM/TPM — backoff lalu coba ulang key yang sama
                log.warning("Rate limit sementara (attempt %d), backoff...", attempt + 1)
                pool.exponential_backoff(attempt)

        except google_exceptions.InvalidArgument:
            pool.mark_failed(key)
            log.error("API key tidak valid, rotate ke key berikutnya.")

        except (google_exceptions.ServiceUnavailable, google_exceptions.DeadlineExceeded):
            log.warning("Layanan Gemini tidak tersedia (attempt %d).", attempt + 1)
            pool.exponential_backoff(attempt, base=5.0, cap=30.0)

        except Exception as e:
            log.error("Error tidak dikenal saat memanggil Gemini: %s", e)
            break

    return None


def ask_gemini(
    user_prompt: str,
    system_context: str = "",
    use_cache: bool = True,
) -> tuple[str, bool]:
    """
    Antarmuka publik untuk memanggil Gemini.

    Return:
        (response_text, is_success)
        response_text: jawaban Gemini, atau pesan error user-friendly
        is_success: True jika berhasil, False jika error/fallback
    """
    pool = get_key_pool()

    if pool.all_exhausted():
        return ERROR_MESSAGES["gemini_all_exhausted"], False

    if use_cache:
        result = _cached_generate(user_prompt, system_context, GEMINI_MODEL)
    else:
        result = _generate_uncached(user_prompt, system_context, GEMINI_MODEL)

    if result is None:
        if pool.all_exhausted():
            return ERROR_MESSAGES["gemini_all_exhausted"], False
        return ERROR_MESSAGES["gemini_busy"], False

    return result, True
