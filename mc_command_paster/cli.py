from __future__ import annotations

import argparse
from pathlib import Path

from .command_loader import load_commands
from .execution_controller import ExecutionOptions, execute_commands
from .logger import setup_logger

MIN_COUNTDOWN_SECONDS = 10
MIN_DELAY_MS = 100
DEFAULT_DELAY_MS = 500


def build_parser() -> argparse.ArgumentParser:
    """CLI引数パーサーを構築する。"""
    parser = argparse.ArgumentParser(description="Minecraft command paster")
    parser.add_argument("command_file", type=Path, help="1行1コマンドのテキストファイル")
    parser.add_argument(
        "--delay-ms",
        type=int,
        default=DEFAULT_DELAY_MS,
        help=f"コマンド間隔(ミリ秒, 最低{MIN_DELAY_MS})",
    )
    parser.add_argument(
        "--countdown",
        type=int,
        default=MIN_COUNTDOWN_SECONDS,
        help=f"開始前カウントダウン(秒, 最低{MIN_COUNTDOWN_SECONDS})",
    )
    parser.add_argument("--dry-run", action="store_true", help="送信せずに内容だけ表示")
    return parser


def run(argv: list[str] | None = None) -> int:
    """アプリのエントリーポイント。"""
    logger = setup_logger()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.delay_ms < MIN_DELAY_MS:
        logger.error("--delay-ms は%d以上を指定してください", MIN_DELAY_MS)
        return 1

    if args.countdown < MIN_COUNTDOWN_SECONDS:
        logger.error("--countdown は%d以上を指定してください", MIN_COUNTDOWN_SECONDS)
        return 1

    try:
        command_list = load_commands(args.command_file)
    except Exception as exc:  # noqa: BLE001
        logger.error("コマンドファイル読み込み失敗: %s", exc)
        return 1

    if not command_list.items:
        logger.warning("有効なコマンドが見つからなかったため終了します")
        return 0

    options = ExecutionOptions(
        delay_ms=args.delay_ms,
        countdown_seconds=args.countdown,
        dry_run=args.dry_run,
    )
    return execute_commands(command_list, options, logger)

