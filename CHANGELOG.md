# CHANGELOG

## [Unreleased]
### Added
- 開発計画書 `docs/development-plan.md` を追加
- コミットメッセージ指針 `.github/git-commit-instructions.md` を拡張
- Python版CLI初期実装を追加
  - コマンドファイル読込
  - ドライラン
  - 送信シーケンス(`T`でチャット入力を開く -> `/`付きコマンドを貼り付け -> Enter)
  - Esc緊急停止
- Pythonパッケージ定義 `pyproject.toml` と最小テスト `tests/test_smoke.py` を追加
- Windows向けテスト実行バッチを追加
  - `scripts/run_unittest.bat`
  - `scripts/run_dry_run.bat`
  - `scripts/run_boundary_checks.bat`
  - `scripts/run_all_checks.bat`
- バッチ検証用の軽量サンプル `examples/smoke_commands.txt` を追加
- 独自ライセンス `LICENSE` を追加
  - 商用利用NG
  - 改変OK(クレジット必須)
  - 再配布は改変版のみOK(無改変の再配布NG)

### Changed
- READMEをPython実行手順に更新
- カウントダウンの最低値とデフォルト値を10秒に変更
- ディレイの最低値を0.1秒(100ms)に変更(デフォルト値は0.5秒/500msを維持)

### Fixed
- Minecraftでコマンド入力欄が開かない場合がある不具合を修正
  - 開始操作を`/`文字入力から`T`キー送信へ変更
  - 貼り付け文字列を`/`付きコマンドへ変更

### Removed
- C実装(`src/*.c`, `src/*.h`)と`CMakeLists.txt`を削除
