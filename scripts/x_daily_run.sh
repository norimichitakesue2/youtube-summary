#!/bin/bash
# Xツイート取得（ローカルMacで実行する想定）
# launchd または手動で起動
#
# 必要な環境: venv にPlaywrightがインストール済み、x_login.py 実行済み

set -e
cd "$(dirname "$0")/.."

echo "=== $(date) x_daily_run start ==="

# venv をアクティベート
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

python3 scripts/x_fetch.py --hours 24

# カープトーク用（失敗してもロマサガ側・git pushは止めない）
python3 scripts/x_fetch.py --hours 24 --targets x_targets_carp.yaml --out-dir data/carp_tweets \
    || echo "[warn] carp fetch failed"

# 自動 commit & push（変更があるときだけ／失敗しても本体は止めない）
bash scripts/git_daily_push.sh || true

echo "=== done ==="
