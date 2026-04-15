from __future__ import annotations

import ctypes
import logging
import time
from dataclasses import dataclass

from .command_loader import CommandList
from .input_sender import send_command_input

VK_ESCAPE = 0x1B


@dataclass(frozen=True)
class ExecutionOptions:
    delay_ms: int = 500
    countdown_seconds: int = 10
    dry_run: bool = False


def _is_escape_pressed() -> bool:
    return (ctypes.windll.user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000) != 0


def _sleep_with_escape_check(delay_ms: int) -> bool:
    step = 0.05
    target = delay_ms / 1000.0
    elapsed = 0.0
    while elapsed < target:
        if _is_escape_pressed():
            return False
        current = min(step, target - elapsed)
        time.sleep(current)
        elapsed += current
    return True


def execute_commands(command_list: CommandList, options: ExecutionOptions, logger: logging.Logger) -> int:
    """コマンド実行全体の制御を行い、終了コードを返す。"""
    logger.info(
        "実行準備: 件数=%d, delay=%dms, dry_run=%s",
        len(command_list.items),
        options.delay_ms,
        str(options.dry_run).lower(),
    )

    for i in range(options.countdown_seconds, 0, -1):
        logger.warning("%d秒後に開始します。Minecraftを前面にしてください。(Escで停止)", i)
        time.sleep(1)
        if _is_escape_pressed():
            logger.warning("開始前にEscが押されたため中止しました")
            return 2

    for index, command in enumerate(command_list.items, start=1):
        if _is_escape_pressed():
            logger.warning("Esc検知: %d件目で停止しました", index)
            return 2

        if options.dry_run:
            logger.info("[DRY-RUN] %d/%d: %s", index, len(command_list.items), command)
        else:
            try:
                send_command_input(command)
                logger.info("送信成功 %d/%d", index, len(command_list.items))
            except Exception as exc:  # noqa: BLE001
                logger.error("送信失敗 %d/%d: %s", index, len(command_list.items), exc)
                return 1

        if not _sleep_with_escape_check(options.delay_ms):
            logger.warning("待機中にEscを検知したため停止しました")
            return 2

    logger.info("全コマンドの処理が完了しました")
    return 0

