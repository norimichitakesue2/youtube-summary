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

# クラッシュ等で残った .git のロック/一時ファイルを掃除（10分以上前のもののみ、
# 同時実行を踏まないように）。接続フォルダでは削除が禁止され rm が無言で失敗する
# ことがあるため、消せない場合は退避(mv)して次回以降の commit を壊さないようにする。
QUARANTINE=".git/_stale_quarantine"
CRUFT=$(find .git \( -name "*.lock" -mmin +10 \) -o \( -name "tmp_obj_*" -mmin +10 \) 2>/dev/null)
if [ -n "$CRUFT" ]; then
    echo "[git_daily_push] stale lock/tmp を掃除:"
    while IFS= read -r f; do
        [ -z "$f" ] && continue
        echo "  - $f"
        rm -f "$f" 2>/dev/null
        if [ -e "$f" ]; then
            # 削除が禁止されている → 退避して無害化
            mkdir -p "$QUARANTINE" 2>/dev/null
            mv -f "$f" "$QUARANTINE/$(basename "$f").$(date +%s).$$" 2>/dev/null || true
        fi
    done <<< "$CRUFT"
fi
# 退避済みファイルは削除が可能になっていれば一掃（できなければ次回に持ち越し）
rm -rf "$QUARANTINE" 2>/dev/null || true

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
