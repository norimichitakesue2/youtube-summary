"""各チャンネルの新着動画を取得し、字幕とメタデータを pending_summaries/ に保存。

使い方:
    python3 scripts/fetch_pending.py            # 各チャンネルの新着のみ（state.jsonベース）
    python3 scripts/fetch_pending.py --since 2026-01-25  # 指定日以降を遡って取得
    python3 scripts/fetch_pending.py --channel UCxxxx --since 2026-01-25  # 特定chのみ

保存形式: data/pending_summaries/<channel_id>__<video_id>.json
   {
     "video_id": "...",
     "channel_id": "...",
     "channel_name": "...",
     "title": "...",
     "published_at": "ISO8601",
     "url": "https://www.youtube.com/watch?v=...",
     "transcript": "字幕全文（取得失敗時は空文字）",
     "transcript_status": "ok" | "no_transcript" | "error: ..."
   }
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import (
    PENDING_DIR,
    TRANSCRIPTS_DIR,
    get_api_key,
    load_channels,
    load_state,
    save_state,
)


def fetch_uploads(youtube, channel_id: str, since_iso: str) -> list[dict]:
    """指定チャンネルの uploads playlist から since_iso 以降の動画一覧を返す。"""
    uploads_playlist = "UU" + channel_id[2:]
    items = []
    page_token = None
    while True:
        resp = (
            youtube.playlistItems()
            .list(
                part="snippet,contentDetails",
                playlistId=uploads_playlist,
                maxResults=50,
                pageToken=page_token,
            )
            .execute()
        )
        for it in resp.get("items", []):
            published = it["contentDetails"]["videoPublishedAt"]
            if published < since_iso:
                # uploads は新しい順なので、since より古いのが出たら以降は不要
                return items
            items.append(
                {
                    "video_id": it["contentDetails"]["videoId"],
                    "title": it["snippet"]["title"],
                    "published_at": published,
                }
            )
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return items


_API = YouTubeTranscriptApi()


def fetch_transcript(video_id: str) -> tuple[str, str]:
    """字幕を取得して (text, status) を返す。"""
    try:
        tl = _API.list(video_id)
        try:
            t = tl.find_transcript(["ja", "ja-JP"])
        except NoTranscriptFound:
            try:
                t = tl.find_generated_transcript(["ja", "ja-JP"])
            except NoTranscriptFound:
                try:
                    t = tl.find_transcript(["en"])
                except NoTranscriptFound:
                    t = next(iter(tl))
        fetched = t.fetch()
        text = "\n".join(s.text for s in fetched if getattr(s, "text", None))
        return text, "ok"
    except (TranscriptsDisabled, NoTranscriptFound):
        return "", "no_transcript"
    except VideoUnavailable:
        return "", "error: video_unavailable"
    except Exception as e:  # noqa: BLE001
        return "", f"error: {type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="ISO日付。指定なしは state.json から再開（初回は7日前）")
    ap.add_argument("--channel", help="特定 channel_id のみ処理")
    args = ap.parse_args()

    try:
        youtube = build("youtube", "v3", developerKey=get_api_key())
    except Exception:
        # 一部環境では静的ディスカバリ文書が同梱されずビルドに失敗するためリモート取得にフォールバック
        youtube = build("youtube", "v3", developerKey=get_api_key(), static_discovery=False)
    state = load_state()
    channels = load_channels()
    if args.channel:
        channels = [c for c in channels if c["channel_id"] == args.channel]

    total_new = 0
    for ch in channels:
        cid = ch["channel_id"]
        ch_state = state.setdefault(cid, {})
        last = ch_state.get("last_published_at")

        if args.since:
            since = (
                args.since
                if "T" in args.since
                else args.since + "T00:00:00Z"
            )
        elif last:
            since = last
        else:
            since = (
                datetime.now(timezone.utc).replace(microsecond=0).isoformat()[:10]
                + "T00:00:00Z"
            )

        print(f"[{ch['name']}] since={since}")
        videos = fetch_uploads(youtube, cid, since)
        # state.json で既に処理済みのは除外
        processed: set[str] = set(ch_state.get("processed_video_ids", []))
        new_videos = [v for v in videos if v["video_id"] not in processed]
        print(f"  取得 {len(videos)} 件 / 新規 {len(new_videos)} 件")

        for v in new_videos:
            text, status = fetch_transcript(v["video_id"])
            payload = {
                "video_id": v["video_id"],
                "channel_id": cid,
                "channel_name": ch["name"],
                "tags": ch.get("tags", []),
                "title": v["title"],
                "published_at": v["published_at"],
                "url": f"https://www.youtube.com/watch?v={v['video_id']}",
                "transcript": text,
                "transcript_status": status,
            }
            out = PENDING_DIR / f"{cid}__{v['video_id']}.json"
            with out.open("w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            # 字幕単体も保存（後で再利用するかも）
            if status == "ok":
                (TRANSCRIPTS_DIR / f"{v['video_id']}.txt").write_text(
                    text, encoding="utf-8"
                )
            print(f"  + {v['published_at'][:10]} {v['title'][:40]}  [{status}]")
            total_new += 1

        if videos:
            ch_state["last_published_at"] = max(v["published_at"] for v in videos)
            ch_state["processed_video_ids"] = sorted(
                processed | {v["video_id"] for v in new_videos}
            )[-500:]  # 直近500件だけ保持

    save_state(state)
    print(f"\n合計 {total_new} 件の新規動画を pending_summaries/ に保存しました")


if __name__ == "__main__":
    main()
