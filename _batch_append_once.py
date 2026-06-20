"""Load workbook once, append all un-logged summaries, save once (atomic)."""
import json, sys, os
from pathlib import Path
sys.path.insert(0, 'scripts')
from lib import PENDING_DIR, LOG_FILE
from append_summary import ensure_workbook, already_logged, fmt_list, COLUMNS
from openpyxl.styles import Alignment

wb, ws = ensure_workbook()
added = skipped = no_summary = 0
for p in sorted(PENDING_DIR.glob("*.json")):
    d = json.load(open(p, encoding="utf-8"))
    if not d.get("summary_3lines"):
        no_summary += 1
        continue
    if already_logged(ws, d.get("video_id", "")):
        skipped += 1
        continue
    row = [
        d.get("published_at", "")[:10],
        d.get("channel_name", ""),
        d.get("title", ""),
        d.get("summary_3lines", ""),
        fmt_list(d.get("positive_points", [])),
        fmt_list(d.get("negative_points", [])),
        fmt_list(d.get("key_topics", [])),
        ", ".join(d.get("tags", [])),
        d.get("url", ""),
        d.get("video_id", ""),
        d.get("summarized_at", ""),
    ]
    ws.append(row)
    nr = ws.max_row
    for i in range(1, len(COLUMNS) + 1):
        ws.cell(row=nr, column=i).alignment = Alignment(wrap_text=True, vertical="top")
    added += 1

tmp = str(LOG_FILE) + ".tmp"
wb.save(tmp)
os.replace(tmp, str(LOG_FILE))
print(f"追記: {added} / 既存スキップ: {skipped} / 未要約: {no_summary}")
