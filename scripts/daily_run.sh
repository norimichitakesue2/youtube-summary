#!/bin/bash
# 毎日の定期実行用スクリプト
# 1. 各チャンネルの新着動画を取得
# 2. 字幕取得失敗分を少しずつ再取得（IPブロック対策で5件/30秒間隔まで）
# 3. （要約は Claude が後段で実施）

set -e
cd "$(dirname "$0")/.."

# --- 依存パッケージの自動ブートストラップ（Claude実行VMは毎回リセットされ、system python3に
#     googleapiclient等が無いため、mnt上の .pylibs_yt に常設して PYTHONPATH で解決する） ---
export PYLIBS_YT="$(pwd)/.pylibs_yt"
export PYTHONPATH="$PYLIBS_YT${PYTHONPATH:+:$PYTHONPATH}"
export TMPDIR="$(pwd)/.pytmp"
mkdir -p "$PYLIBS_YT" "$TMPDIR"
if ! python3 -c "import googleapiclient, youtube_transcript_api" 2>/dev/null; then
  echo "--- 依存パッケージを .pylibs_yt にインストール中 ---"
  python3 -m pip install --target "$PYLIBS_YT" --no-cache-dir \
    google-api-python-client youtube-transcript-api >/dev/null 2>&1 \
    && echo "  インストール完了" || echo "  警告: 依存パッケージのインストールに失敗"
fi

echo "=== $(date) daily_run start ==="

echo "--- 新着取得 ---"
python3 scripts/fetch_pending.py

echo "--- 字幕再取得（失敗分） ---"
python3 scripts/retry_failed_transcripts.py --max 5 --sleep 30 || true

echo "=== done ==="
