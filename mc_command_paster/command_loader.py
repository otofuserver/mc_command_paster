from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommandList:
    items: list[str]


def load_commands(file_path: Path) -> CommandList:
    """コマンドファイルを読み込み、空行とコメント行を除外する。"""
    if not file_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    commands: list[str] = []
    with file_path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            commands.append(stripped)

    return CommandList(items=commands)

