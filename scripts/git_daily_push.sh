#!/bin/bash
# 日次の自動 commit & push
# 変更があるときだけコミット＆Push。失敗してもデイリーパイプライン本体は止めない（set -e セーフ）
set -u

cd "$(dirname "$0")/.."

# git リポジトリでない場合はスキップ
if [ ! -d .git ]; then
    echo "[git_daily_push] .git なし、スキップ"
    exit 0
fi

# 変更がなければ何もしない
git add -A
if git diff --cached --quiet; then
    echo "[git_daily_push] 変更なし、スキップ"
    exit 0
fi

MSG="daily update: $(date +%Y-%m-%d)"
git commit -m "$MSG" || {
    echo "[git_daily_push] commit 失敗"
    exit 0
}

# Push（失敗しても日次本体は止めない）
if git push origin main 2>&1; then
    echo "[git_daily_push] push 成功: $MSG"
else
    echo "[git_daily_push] push 失敗（次回再試行）"
fi
