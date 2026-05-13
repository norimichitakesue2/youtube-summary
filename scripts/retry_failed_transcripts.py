"""字幕取得に失敗しているpending JSONを少しずつ再取得する。

YouTubeはクラウド系IPからの字幕取得を制限することがあるので、
1回の実行では少数だけ・間隔をあけて取得する。
日次の自動実行で少しずつ未取得分が埋まる想定。

使い方:
    python3 scripts/retry_failed_transcripts.py            # デフォルト最大5件、間隔30秒
    python3 scripts/retry_failed_transcripts.py --max 3 --sleep 60
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import PENDING_DIR, TRANSCRIPTS_DIR
from fetch_pending import fetch_transcript


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=5, help="1回の実行で再取得する最大件数")
    ap.add_argument("--sleep", type=int, default=30, help="リクエスト間隔（秒）")
    args = ap.parse_args()

    # 失敗中（ok でも no_transcript でもない）の中から、古いものから順に再取得
    targets = []
    for p in sorted(PENDING_DIR.glob("*.json")):
        with p.open("r", encoding="utf-8") as f:
            d = json.load(f)
        status = d.get("transcript_status", "")
        if status not in ("ok", "no_transcript"):
            targets.append((d.get("published_at", ""), p, d))

    targets.sort(reverse=True)  # 新しい順に試行
    targets = targets[: args.max]

    if not targets:
        print("再取得対象の動画はありません")
        return

    print(f"再取得対象: {len(targets)} 件（最大 {args.max} 件まで）")
    ok = no_t = err = 0
    for i, (pub, p, d) in enumerate(targets):
        if i > 0:
            print(f"  ({args.sleep}秒待機)")
            time.sleep(args.sleep)
        text, status = fetch_transcript(d["video_id"])
        d["transcript"] = text
        d["transcript_status"] = status
        with p.open("w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        if status == "ok":
            (TRANSCRIPTS_DIR / f"{d['video_id']}.txt").write_text(text, encoding="utf-8")
            ok += 1
        elif status == "no_transcript":
            no_t += 1
        else:
            err += 1
        print(f"  {pub[:10]} {d['title'][:40]} → {status[:50]}")

    print(f"\n結果: ok={ok} / no_transcript={no_t} / error={err}")


if __name__ == "__main__":
    main()
