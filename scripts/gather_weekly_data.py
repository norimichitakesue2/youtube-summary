"""1週間分のpending_summariesを集約してJSONを出力する。

使い方:
    python3 scripts/gather_weekly_data.py                       # 直近7日
    python3 scripts/gather_weekly_data.py --until 2026-05-11    # 5/5〜5/11
    python3 scripts/gather_weekly_data.py --days 7 --until 2026-05-11

出力:
    data/weekly_aggregates/week_<until>.json
    （Claudeがこれを読んでナラティブを書く想定）
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import PENDING_DIR, ROOT

AGG_DIR = ROOT / "data" / "weekly_aggregates"
AGG_DIR.mkdir(parents=True, exist_ok=True)


def parse_iso(s: str) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def collect(since: datetime, until: datetime) -> list[dict]:
    """期間内の要約済み動画を集める。"""
    items = []
    for f in PENDING_DIR.glob("*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not d.get("summary_3lines"):
            continue
        pub = parse_iso(d.get("published_at", ""))
        if pub is None:
            continue
        if pub < since or pub > until + timedelta(days=1):
            continue
        items.append(d)
    return items


def build_aggregate(items: list[dict], since: datetime, until: datetime) -> dict:
    # チャンネル別
    by_channel: dict[str, list[dict]] = defaultdict(list)
    for d in items:
        ch = d.get("channel_name") or "(unknown)"
        by_channel[ch].append(d)

    channel_stats = []
    for ch, vids in sorted(by_channel.items(), key=lambda x: -len(x[1])):
        channel_stats.append(
            {
                "channel": ch,
                "n_videos": len(vids),
                "videos": [
                    {
                        "video_id": v["video_id"],
                        "title": v["title"],
                        "published_at": v["published_at"],
                        "url": v.get("url"),
                        "summary_3lines": v.get("summary_3lines", ""),
                        "key_topics": v.get("key_topics") or [],
                        "positive_points": v.get("positive_points") or [],
                        "negative_points": v.get("negative_points") or [],
                    }
                    for v in sorted(vids, key=lambda x: x["published_at"], reverse=True)
                ],
            }
        )

    # トピック頻度
    topic_counter: Counter[str] = Counter()
    topic_videos: dict[str, list[str]] = defaultdict(list)  # topic -> [video_id]
    for d in items:
        for t in d.get("key_topics") or []:
            tk = t.strip()
            if not tk:
                continue
            topic_counter[tk] += 1
            topic_videos[tk].append(d["video_id"])
    top_topics = [
        {"topic": t, "count": c, "video_ids": topic_videos[t]}
        for t, c in topic_counter.most_common(20)
    ]

    # ポジ/ネガ全件
    all_positive = []
    all_negative = []
    for d in items:
        for p in d.get("positive_points") or []:
            all_positive.append(
                {"point": p, "video_id": d["video_id"], "channel": d.get("channel_name")}
            )
        for n in d.get("negative_points") or []:
            all_negative.append(
                {"point": n, "video_id": d["video_id"], "channel": d.get("channel_name")}
            )

    # ピックアップ候補: ポジ+ネガ件数の合計が多い動画上位
    def pn_count(d):
        return len(d.get("positive_points") or []) + len(d.get("negative_points") or [])

    pick_candidates = sorted(items, key=pn_count, reverse=True)[:10]
    pick_brief = [
        {
            "video_id": v["video_id"],
            "title": v["title"],
            "channel": v.get("channel_name"),
            "published_at": v["published_at"],
            "url": v.get("url"),
            "summary_3lines": v.get("summary_3lines", ""),
            "key_topics": v.get("key_topics") or [],
            "n_pos": len(v.get("positive_points") or []),
            "n_neg": len(v.get("negative_points") or []),
            "positive_points": v.get("positive_points") or [],
            "negative_points": v.get("negative_points") or [],
        }
        for v in pick_candidates
    ]

    return {
        "meta": {
            "since": since.strftime("%Y-%m-%d"),
            "until": until.strftime("%Y-%m-%d"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "n_videos": len(items),
            "n_channels": len(by_channel),
            "n_positive_points": len(all_positive),
            "n_negative_points": len(all_negative),
        },
        "channels": channel_stats,
        "top_topics": top_topics,
        "positive_points": all_positive,
        "negative_points": all_negative,
        "pick_candidates": pick_brief,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--until", help="YYYY-MM-DD (default: today)")
    ap.add_argument("--days", type=int, default=7)
    args = ap.parse_args()

    if args.until:
        until = datetime.fromisoformat(args.until).replace(tzinfo=timezone.utc)
    else:
        until = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59, microsecond=0)
    since = (until - timedelta(days=args.days - 1)).replace(hour=0, minute=0, second=0, microsecond=0)

    items = collect(since, until)
    agg = build_aggregate(items, since, until)

    out = AGG_DIR / f"week_{until.strftime('%Y-%m-%d')}.json"
    out.write_text(json.dumps(agg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"集約: {out}")
    print(f"  期間: {agg['meta']['since']} 〜 {agg['meta']['until']}")
    print(f"  動画: {agg['meta']['n_videos']} 本 / チャンネル: {agg['meta']['n_channels']}")
    print(f"  ポジ: {agg['meta']['n_positive_points']} / ネガ: {agg['meta']['n_negative_points']}")
    print(f"  トピック種: {len(agg['top_topics'])}")


if __name__ == "__main__":
    main()
