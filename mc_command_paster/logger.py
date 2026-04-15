from __future__ import annotations

import logging
import sys


def setup_logger() -> logging.Logger:
    """アプリ全体で利用するロガーを初期化する。"""
    logger = logging.getLogger("mc_command_paster")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger

