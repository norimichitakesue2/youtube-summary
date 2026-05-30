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

# クラッシュ等で残ったロックファイルを掃除（10分以上前のもののみ削除して
# 同時実行を踏まないようにする）
STALE_LOCKS=$(find .git -name "*.lock" -mmin +10 2>/dev/null)
if [ -n "$STALE_LOCKS" ]; then
    echo "[git_daily_push] stale lock を削除:"
    echo "$STALE_LOCKS" | sed 's/^/  - /'
    echo "$STALE_LOCKS" | xargs -r rm -f
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
# .github_token があれば PAT 認証で push（Cowork sandbox からの非対話 push 用）
TOKEN_FILE=".github_token"
if [ -f "$TOKEN_FILE" ]; then
    TOKEN=$(tr -d '[:space:]\r\n' < "$TOKEN_FILE")
    REMOTE_URL=$(git remote get-url origin)
    # https://github.com/owner/repo.git → https://x-access-token:TOKEN@github.com/owner/repo.git
    AUTH_URL=$(printf '%s' "$REMOTE_URL" | sed "s#https://github.com/#https://x-access-token:${TOKEN}@github.com/#")
    if git push "$AUTH_URL" HEAD:main 2>&1 | sed "s#${TOKEN}#***#g"; then
        echo "[git_daily_push] push 成功: $MSG"
    else
        echo "[git_daily_push] push 失敗（次回再試行）"
    fi
    unset TOKEN AUTH_URL
else
    if git push origin main 2>&1; then
        echo "[git_daily_push] push 成功: $MSG"
    else
        echo "[git_daily_push] push 失敗（.github_token 未設定の可能性。次回再試行）"
    fi
fi
