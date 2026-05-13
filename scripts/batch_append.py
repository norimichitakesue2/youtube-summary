"""data/pending_summaries/*.json のうち summary_3lines が入っているものを
video_log.xlsx に一括追記する。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import PENDING_DIR
from append_summary import append


def main():
    files = sorted(PENDING_DIR.glob("*.json"))
    added = skipped = no_summary = 0
    for p in files:
        with p.open("r", encoding="utf-8") as f:
            d = json.load(f)
        if not d.get("summary_3lines"):
            no_summary += 1
            continue
        if append(d):
            added += 1
        else:
            skipped += 1
    print(
        f"追記: {added} / 既存スキップ: {skipped} / 未要約: {no_summary} / 合計: {len(files)}"
    )


if __name__ == "__main__":
    main()
