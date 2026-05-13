# GitHubにPushする手順（Mac側で実行）

`.gitignore` は整備済み。`.env` / ブラウザプロファイル / 生ツイートJSON / トランスクリプトは含まれません。

## 0. 事前確認

GitHub CLI（`gh`）が入ってなければインストール:

```bash
brew install gh
gh auth login   # GitHub.com → HTTPS → ブラウザ認証
```

## 1. 既存の `.git/` を一掃して再初期化

サンドボックス側で `git init` だけ走っていますが、tmp objects が残っている可能性があるのでクリーンに作り直します。

```bash
cd ~/youtube-summary
rm -rf .git
git init -b main
git config user.email "norimichitakesue2@gmail.com"
git config user.name "takesue"
```

## 2. 念のため危険ファイルが含まれないか確認

```bash
cd ~/youtube-summary
git add .
git status --short | grep -E "(\.env|browser_profile|/tweets/[0-9]|transcripts/|pending_summaries/|x_state\.json|x_fetch\.log)"
# ↑ 何も出なければOK（除外できている）
git ls-files | wc -l   # 70前後のはず
```

## 3. 初回コミット

```bash
git commit -m "Initial commit: YouTube + X daily summary pipeline & reports"
```

## 4. GitHub にPrivateリポジトリ作成 & Push

```bash
gh repo create youtube-summary --private --source=. --remote=origin --push
```

これで `https://github.com/<your-handle>/youtube-summary` がPrivateで作成され、即座にPushされます。

## 5. 今後の運用

日次タスクで `reports/weekly_report_<date>.html` と `reports/index.html`、`data/tweet_summaries/*.json`、`tweets_log.xlsx`、`video_log.xlsx` が更新されます。コミット＆Pushを自動化したい場合は、`scripts/x_daily_run.sh` の末尾あたりに以下を追加するのが手軽です:

```bash
cd ~/youtube-summary
git add -A
git diff --cached --quiet || git commit -m "daily update: $(date +%Y-%m-%d)" && git push origin main
```

または scheduled-task 側に「git commit & push」のステップを足してもOK。

## （オプション）GitHub Pages で見たい場合

Privateリポでも GitHub Pages（Pro/Team プラン）で公開できますが、ツイート本文・著者ハンドル等の二次公開になるのでおすすめはしません。社内・身内共有ならリポジトリの Collaborator 招待で十分です。
