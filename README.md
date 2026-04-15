# mc_command_paster

Minecraftクライアントに対して、テキストファイルに並んだコマンドを1行ずつ自動送信するWindows向けPython CLIツールです。

## 機能
- コマンドファイルを上から順に実行
- 実行シーケンス: `T` でチャット入力を開く -> クリップボード貼り付け(`/`付き) -> Enter
- 送信間隔をミリ秒で指定可能
- `Esc` による緊急停止
- `--dry-run` で送信せず内容確認

## 前提
- Windows
- Python 3.11+

## セットアップ
```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -e .
```

## 実行例
```powershell
python -m mc_command_paster .\examples\commands.txt --delay-ms 500 --countdown 10
```

ドライラン:
```powershell
python -m mc_command_paster .\examples\commands.txt --dry-run --countdown 10 --delay-ms 500
```

## テスト
```powershell
python -m unittest -v
```

Windowsバッチでの実行:
```powershell
.\scripts\run_unittest.bat
.\scripts\run_dry_run.bat
.\scripts\run_boundary_checks.bat
.\scripts\run_all_checks.bat
```

※ バッチのdry-run/境界値チェックは `examples/smoke_commands.txt` を使用します。

## コマンドファイル形式
- 1行1コマンド
- 空行は無視
- `#` で始まる行はコメントとして無視

例:
```text
# setup
say hello
time set day
```

## 安全に使うための注意
- 開始前のカウントダウン中にMinecraftウィンドウを前面にする
- カウントダウンは安全のため最低10秒(デフォルト10秒)
- ディレイは負荷軽減のため最低0.1秒(デフォルト0.5秒)
- 誤送信防止のため、本番前に `--dry-run` で内容を確認する
- 異常時は `Esc` で停止する
- Minecraft側でチャット開始キーが`T`以外の場合は、キー設定を見直す

## ライセンス
- 商用利用: 禁止
- 改変: 可能(クレジット記載必須)
- 再配布: 改変版のみ可能(無改変の再配布は禁止)

詳細は `LICENSE` を参照してください。

クレジット記載例:
```text
Based on mc_command_paster by takumi nakajima. Modified by <your-name>.
```

