#!/bin/bash
# 毎日の定期実行用スクリプト
# 1. 各チャンネルの新着動画を取得
# 2. 字幕取得失敗分を少しずつ再取得（IPブロック対策で5件/30秒間隔まで）
# 3. （要約は Claude が後段で実施）

set -e
cd "$(dirname "$0")/.."

echo "=== $(date) daily_run start ==="

echo "--- 新着取得 ---"
python3 scripts/fetch_pending.py

echo "--- 字幕再取得（失敗分） ---"
python3 scripts/retry_failed_transcripts.py --max 5 --sleep 30 || true

echo "=== done ==="
