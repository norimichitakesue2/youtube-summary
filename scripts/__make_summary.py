import json, datetime, os

DATE = "2026-05-22"
SRC = f"/sessions/wizardly-ecstatic-euler/mnt/youtube-summary/data/tweets/{DATE}__fetch.json"
DST = f"/sessions/wizardly-ecstatic-euler/mnt/youtube-summary/data/tweet_summaries/{DATE}.json"

with open(SRC, "r", encoding="utf-8") as f:
    tweets = json.load(f)

tweets_sorted = sorted(tweets, key=lambda x: (x.get("likes") or 0), reverse=True)

hot = []
for t in tweets_sorted[:10]:
    hot.append({
        "tweet_id": t.get("tweet_id"),
        "url": t.get("url"),
        "author_handle": t.get("author_handle"),
        "author_name": t.get("author_name"),
        "text": t.get("text"),
        "likes": t.get("likes", 0),
        "retweets": t.get("retweets", 0),
        "replies": t.get("replies", 0),
    })

summary = {
    "date": DATE,
    "n_tweets": len(tweets),
    "summary_3lines": (
        "聖王の厄（闇堕ち）スタイル実装で賛否両論の盛り上がり\n"
        "メイン4話後編・新ガチャ・新イベント「スコアバトル」開始\n"
        "螺旋回廊560階（ジュエルビースト）攻略報告と検証が活発"
    ),
    "key_topics": [
        "聖王[厄]（闇堕ち）スタイル実装",
        "メイン4話後編 こよみ編 バロルディア",
        "新ガチャ（聖王厄・ロロ・ヴァンパイアレディ正月）",
        "新イベント スコアバトル",
        "螺旋回廊560階 ジュエルビースト攻略",
        "ハーフアニバーサリー前のガチャタイミング議論",
        "BOXガチャ期限（明日4時まで）",
    ],
    "positive_themes": [
        "厄スタイル聖王のビジュアル・可愛さに好意的な反応",
        "螺旋560階クリア報告が多数（ロッキー/ミルザ/オアイーブ縛りなど工夫した攻略）",
        "ストーリー進行（メイン4話後編開始）への期待感",
        "ジュエルビースト戦のギミック検証（カウンター/OD条件解明）が盛り上がり",
    ],
    "negative_themes": [
        "聖王闇堕ちに対する拒否反応（神格化キャラへの『お気持ち』論争が再燃）",
        "ハーフアニバ直前のガチャタイミングに様子見・温存推奨の声",
        "オリジナル要素・闇堕ち乱発への批判（『嫌なら辞めろ』論争）",
        "BOXガチャの自動リセット非対応・カタリナの微妙アビリティへの不満",
    ],
    "hot_tweets": hot,
    "summarized_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
}

os.makedirs(os.path.dirname(DST), exist_ok=True)
with open(DST, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("wrote", DST)
print("n_tweets =", summary["n_tweets"])
