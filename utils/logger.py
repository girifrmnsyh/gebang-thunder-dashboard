"""
utils/logger.py — Konfigurasi logging terpusat
"""

import logging
import sys


def setup_logger(name: str = "gt_dashboard", level: int = logging.INFO) -> logging.Logger:
    """
    Setup dan kembalikan logger dengan formatter yang rapi.
    Dipanggil sekali di app.py atau di modul yang butuh logging.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # sudah dikonfigurasi sebelumnya

    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Logger default yang bisa langsung di-import
log = setup_logger()
