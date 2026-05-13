---
name: x-summary-daily
description: 前日のXツイート（ローカルMacが取得済み）を集約サマリしてtweets_log.xlsxに追記
---

Xツイートの日次サマリ生成タスクです。`/Users/takesue/youtube-summary/` で作業してください。

## 前提
ローカルMac側で `x_daily_run.sh` が朝9時に動いて、`data/tweets/<YYYY-MM-DD>__fetch.json` を生成している想定。

## 実行手順

### Step 1: 今日のツイートデータを確認
```bash
cd /Users/takesue/youtube-summary
TODAY=$(date +%Y-%m-%d)
ls -la data/tweets/${TODAY}__fetch.json data/tweet_summaries/${TODAY}.json 2>/dev/null
```

### Step 2: 既にサマリ済みならスキップ
data/tweet_summaries/<TODAY>.json が既に存在すればスキップして「既にサマリ済み」と報告してから Step 5 に進む。

### Step 3: ツイートデータを読んで集約サマリを生成
data/tweets/<TODAY>__fetch.json を読み込み、以下のフィールドを持つサマリJSONを `data/tweet_summaries/<TODAY>.json` に保存：

```json
{
  "date": "YYYY-MM-DD",
  "n_tweets": ツイート総数,
  "summary_3lines": "1行目（〜40字）\n2行目\n3行目",
  "key_topics": ["話題1", "話題2", ...],
  "positive_themes": ["...", "..."],
  "negative_themes": ["...", "..."],
  "hot_tweets": [
    {"tweet_id":"...", "url":"...", "author_handle":"...", "author_name":"...", "text":"...", "likes":N, "retweets":N, "replies":N},
    ...
  ],
  "summarized_at": "ISO8601 UTC"
}
```

**ポイント**:
- ツイート大量時はlikes降順で TOP100程度を読みテーマ抽出
- ポジ/ネガは「ロマサガRSのキャラ・性能・運営対応・ガチャ・コラボ・イベント」への評価
- 公式（@romasaga_rs）のお知らせがあれば key_topics に含める

### Step 4: xlsxに追記
```bash
cd /Users/takesue/youtube-summary
python3 scripts/x_append_summary.py $(date +%Y-%m-%d)
```

### Step 5: 統合HTMLレポートを再生成（YouTube＋X）
```bash
cd /Users/takesue/youtube-summary
python3 scripts/generate_weekly_report.py --days 7
```
これで `reports/weekly_report_<today>.html` が直近7日分のYouTube動画＋Xサマリで更新されます。
（YouTube側の youtube-summary-daily が10:00、こちらが10:30なので、こちらの実行時に「YouTubeも今日のぶんが反映済みのHTML」が確定する）

### Step 6: 結果報告
- 取得ツイート数、ポジ要素／ネガ要素の代表的なものを2〜3個ずつ
- リンク:
  - [tweets_log.xlsx](computer:///Users/takesue/youtube-summary/tweets_log.xlsx)
  - [統合レポート（HTML）](computer:///Users/takesue/youtube-summary/reports/weekly_report_<YYYY-MM-DD>.html) ※`ls reports/weekly_report_*.html | tail -1` で最新確認

### Step 7: GitHubに自動Push（当日反映）
生成されたサマリ・xlsx・統合HTMLレポートをGitHubに反映する。`scripts/git_daily_push.sh` は変更がなければ静かに終了する。
```bash
cd /Users/takesue/youtube-summary
bash scripts/git_daily_push.sh
```
push成功／失敗／変更なしの結果をStep 6の報告末尾に1行で添える（例: 「GitHub: pushed (daily update: 2026-05-13)」「GitHub: 変更なし」「GitHub: push失敗、次回再試行」）。

エラー（ツイートデータがない、空など）の場合は静かに報告のみ。
