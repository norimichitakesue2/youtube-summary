# YouTube動画 要約自動化システム

指定したYouTubeチャンネルの新着動画を自動で取得し、字幕から「3行要約・キートピック・ポジ要素・ネガ要素」を抽出して、xlsxとHTMLレポートに蓄積していく仕組み。

## 構成

```
youtube-summary/
├── channels.yaml                    # 監視対象チャンネル一覧（ここに追加すれば対象が増える）
├── .env                             # YouTube APIキー（コミット禁止）
├── video_log.xlsx                   # 全動画の蓄積ログ（フィルタ・ソート可）
├── reports/
│   ├── index.html                   # 過去レポート一覧
│   └── weekly_report_YYYY-MM-DD.html
├── data/
│   ├── state.json                   # チャンネル別の最終取得状態
│   ├── transcripts/<video_id>.txt   # 字幕本文（再利用用）
│   └── pending_summaries/           # メタデータ＋字幕＋要約のJSON置き場
└── scripts/
    ├── lib.py                       # 設定読み込み・パス管理
    ├── fetch_pending.py             # 新着動画と字幕を取得 → pending_summaries/
    ├── retry_failed_transcripts.py  # IPブロックで失敗した字幕を少しずつ再取得
    ├── append_summary.py            # 単体の要約JSONを xlsx に追記
    ├── batch_append.py              # 要約済みJSONを一括で xlsx に追記
    ├── generate_weekly_report.py    # 直近期間のHTMLレポート生成
    ├── daily_run.sh                 # 日次実行（新着取得 + 字幕再取得）
    └── weekly_run.sh                # 週次実行（HTMLレポート生成）
```

## 新しいYouTuberを追加する

`channels.yaml` を編集するだけ。

```yaml
channels:
  - name: サンゾーGAMES
    channel_id: UCTnmCbMtBLO1IJ6iwRPkySg
    tags: [ロマサガRS, RPG]
    enabled: true

  # ↓ 追加
  - name: 別のYouTuber
    channel_id: UCxxxxxxxxxxxxxxxxxxxxxx
    tags: [ジャンル]
    enabled: true
```

`channel_id` の調べ方：
1. チャンネルページを開く
2. URLが `youtube.com/channel/UCxxxx` 形式ならその `UCxxxx` 部分
3. `youtube.com/@xxxxx` 形式の場合は、ページソースで "channelId" を検索

## 運用フロー

### 日次（自動）
```bash
bash scripts/daily_run.sh
```
1. `fetch_pending.py` で各チャンネルの新着を取得（state.json で重複防止）
2. `retry_failed_transcripts.py` でIPブロックで失敗した字幕を5件/30秒間隔で再取得

### 要約（Claude が実施）
新規取得した動画（`pending_summaries/*.json` で `summary_3lines` が空のもの）について、
Claude が `transcript` を読んで以下を生成：
- `summary_3lines`: 3行要約
- `key_topics`: キートピック（3〜6個）
- `positive_points`: ポジ要素（褒めてた点）
- `negative_points`: ネガ要素（批判/不満点）

### xlsx反映
```bash
python3 scripts/batch_append.py
```
要約済みJSONを `video_log.xlsx` に一括追記（既存はスキップ）。

### 週次（自動）
```bash
bash scripts/weekly_run.sh
```
直近7日分のHTMLレポートを `reports/weekly_report_YYYY-MM-DD.html` に生成。
任意期間は `python3 scripts/generate_weekly_report.py --since 2026-04-01 --until 2026-04-30`。

## ⚠️ 字幕取得のIPブロックについて

YouTubeはクラウド/データセンターIPからの字幕取得をしばしばブロックする。
本システムが Cowork のサンドボックス内で動く場合、初回の大量取得は失敗しやすい。

**対策**:
1. **日次少量実行**: 新着は1〜3本/日なのでブロックされにくい
2. **段階的リトライ**: `retry_failed_transcripts.py` が日次で5件ずつ再取得を試みる
3. **ローカル実行（推奨）**: ご自宅のMacから実行すれば残留住宅IPなので原則ブロックされない

ローカル実行する場合（macOSのPEP 668対応のため venv 経由）：
```bash
cd /Users/takesue/youtube-summary

# 初回のみ：仮想環境作成 & 依存インストール
python3 -m venv .venv
source .venv/bin/activate
pip install google-api-python-client youtube-transcript-api openpyxl jinja2 pyyaml python-dotenv

# 2回目以降：venvをアクティベートしてから実行
source .venv/bin/activate
bash scripts/daily_run.sh

# 失敗した字幕を一気に取りに行く例（住宅IPでは原則ブロックされない）
python3 scripts/retry_failed_transcripts.py --max 100 --sleep 2
```

## トラブルシュート

### `YOUTUBE_API_KEY が .env に設定されていません`
→ `.env` ファイルに `YOUTUBE_API_KEY=AIza...` の行があるか確認。

### `IpBlocked` エラーが連発する
→ サンドボックスIPがブロックされている。`retry_failed_transcripts.py` を時間をあけて何度か実行するか、ローカルから実行。

ローカル実行も `IpBlocked` / HTTP 429 で失敗する場合、`yt-dlp` + `curl_cffi` でブラウザ偽装する経路が使えるかもしれません。手順：

```bash
cd /Users/takesue/youtube-summary
source .venv/bin/activate

# 初回のみ（既に入ってれば不要）
pip install "yt-dlp[default,curl-cffi]"

# 1本テスト（成功すれば /tmp/test.ja.ttml が出来る）
python3 -m yt_dlp --impersonate chrome --cookies-from-browser chrome --write-auto-subs --sub-langs ja --skip-download --sub-format ttml -o '/tmp/test.%(ext)s' 'https://www.youtube.com/watch?v=【適当なvideo_id】'

# 成功したらバッチ実行
python3 scripts/retry_with_ytdlp.py --browser chrome
```

それでもダメなら、IPベースでブロックされている可能性が高い。テザリングで別IPに切り替える / VPN経由 / 時間を置く（数時間〜半日）のいずれかで回避を試す。

### 字幕がない動画
→ `transcript_status: "no_transcript"` で記録される。要約はスキップされる（音声からの転写は別途必要）。

### 動画が漏れる
→ `state.json` を編集して該当チャンネルの `last_published_at` を遡るか、`fetch_pending.py --since 2026-04-01` で期間指定して再取得。

## YouTube Data API クォータ

- 無料枠: 10,000ユニット/日
- `playlistItems.list` = 1ユニット（50件取得につき）
- 数チャンネル・日次運用なら100ユニット/日も使わない

---

# X（Twitter）モジュール

Xから #ロマサガRS 関連投稿を収集し、日次・週次でポジ/ネガ集約サマリを生成する。

## 構成（追加分）

```
youtube-summary/
├── x_targets.yaml                 # 追跡対象（アカウント・ハッシュタグ・キーワード）
├── tweets_log.xlsx                # 日次サマリの蓄積
├── data/
│   ├── x_state.json               # X ログイン状態（gitignore）
│   ├── tweets/<YYYY-MM-DD>__fetch.json  # 日次取得結果
│   └── tweet_summaries/<YYYY-MM-DD>.json # 集約サマリ
├── reports/
│   ├── x_index.html
│   ├── x_daily_<date>.html
│   └── x_weekly_<date>.html
└── scripts/
    ├── x_login.py                 # 初回ログイン保存
    ├── x_fetch.py                 # ツイート取得（Playwright）
    ├── x_append_summary.py        # サマリJSON→xlsx追記
    ├── generate_x_report.py       # HTMLレポート生成
    ├── x_daily_run.sh             # ローカル日次実行スクリプト
    └── launchd/com.takesue.youtube-summary.x-fetch.plist
```

## 初回セットアップ

```bash
cd /Users/takesue/youtube-summary
source .venv/bin/activate
pip install playwright
playwright install chromium

# Xにログイン（ブラウザが立ち上がる）
python3 scripts/x_login.py
```

## ローカル定期実行（毎朝9時）

```bash
cp scripts/launchd/com.takesue.youtube-summary.x-fetch.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.takesue.youtube-summary.x-fetch.plist
```

確認：
```bash
launchctl list | grep youtube-summary
```

ログ：`data/x_fetch.log`

アンインストール：
```bash
launchctl unload ~/Library/LaunchAgents/com.takesue.youtube-summary.x-fetch.plist
rm ~/Library/LaunchAgents/com.takesue.youtube-summary.x-fetch.plist
```

## 自動運用フロー

1. **9:00** ローカルMac で launchd → `x_fetch.py` 実行 → `data/tweets/today.json` 保存
2. **10:30** Coworkで `x-summary-daily` タスク → サマリ生成 → `data/tweet_summaries/today.json` & xlsx追記
3. **月曜10:30** Coworkで `x-summary-weekly` タスク → 週次HTMLレポート生成

## 追跡対象を増やす

`x_targets.yaml` を編集するだけ。

```yaml
accounts:
  - name: 別アカウント
    handle: another_handle
    enabled: true

hashtags:
  - tag: "#ロマサガ"
    enabled: true

keywords:
  - query: "ロマサガRS ガチャ"
    enabled: true
```

## トラブルシュート

### 「先に scripts/x_login.py を実行してください」
→ data/x_state.json がない。`python3 scripts/x_login.py` 再実行。

### ログイン状態が切れた
→ `python3 scripts/x_login.py` 再実行で状態を更新。

### Playwrightがブラウザ見つからない
→ `playwright install chromium` を実行。

### 取得件数が少ない
→ 1ターゲットあたりデフォルト100件上限。`x_targets.yaml` の `defaults.max_per_target` を増やす。

### XのUI変更で壊れる
→ `scripts/x_fetch.py` のセレクタ（`article[data-testid="tweet"]` など）を最新のXのDOMに合わせて修正。
