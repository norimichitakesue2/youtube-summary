"""yt-dlp を使って失敗した字幕を取得し直す。
ブラウザのCookieを借りるためIPブロックを回避できる。

使い方（Chromeを使っている場合）:
    python3 scripts/retry_with_ytdlp.py --browser chrome
    python3 scripts/retry_with_ytdlp.py --browser safari
    python3 scripts/retry_with_ytdlp.py --browser firefox
    python3 scripts/retry_with_ytdlp.py --browser edge
    python3 scripts/retry_with_ytdlp.py --browser brave

YouTubeにログインしているブラウザを指定してください。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import PENDING_DIR, TRANSCRIPTS_DIR


def fetch_via_ytdlp(video_id: str, browser: str) -> tuple[str, str]:
    """yt-dlp で字幕（日本語、なければ英語）を取得し、(text, status) を返す。"""
    url = f"https://www.youtube.com/watch?v={video_id}"
    with tempfile.TemporaryDirectory() as td:
        out_template = str(Path(td) / "sub")
        # まず手動字幕、なければ自動字幕
        for write_flag in ("--write-subs", "--write-auto-subs"):
            cmd = [
                "yt-dlp",
                "--cookies-from-browser",
                browser,
                write_flag,
                "--sub-langs",
                "ja,ja-JP,en",
                "--skip-download",
                "--sub-format",
                "ttml/vtt/srv3",
                "-o",
                out_template,
                url,
            ]
            try:
                r = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=60
                )
            except subprocess.TimeoutExpired:
                continue
            if r.returncode != 0:
                # 字幕がないか、IPブロック
                if "HTTP Error 429" in r.stderr or "Sign in to confirm" in r.stderr:
                    return "", "error: rate_limited_or_login_required"
                continue
            # 出力された字幕ファイルを探す
            files = sorted(Path(td).glob("sub*"))
            if not files:
                continue
            # 言語の優先順
            preferred = None
            for lang in ("ja", "ja-JP", "en"):
                for f in files:
                    if f".{lang}." in f.name:
                        preferred = f
                        break
                if preferred:
                    break
            if not preferred:
                preferred = files[0]
            text = parse_subtitle(preferred)
            if text:
                return text, "ok"
        return "", "no_transcript"


def parse_subtitle(path: Path) -> str:
    """ttml / vtt / srv3 を平文に変換。"""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix == ".vtt" or "WEBVTT" in raw[:200]:
        return parse_vtt(raw)
    # ttml / xml系
    try:
        # 名前空間を雑に剥がす
        cleaned = re.sub(r'xmlns(:\w+)?="[^"]+"', "", raw)
        root = ET.fromstring(cleaned)
        texts = []
        for elem in root.iter():
            if elem.text and elem.text.strip():
                texts.append(elem.text.strip())
        return "\n".join(texts)
    except ET.ParseError:
        return parse_vtt(raw)  # フォールバック


def parse_vtt(raw: str) -> str:
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(("WEBVTT", "NOTE", "STYLE")):
            continue
        if "-->" in line:
            continue
        if re.match(r"^\d+$", line):
            continue
        # タグ除去
        clean = re.sub(r"<[^>]+>", "", line)
        if clean:
            lines.append(clean)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--browser",
        required=True,
        choices=["chrome", "safari", "firefox", "edge", "brave", "chromium", "opera", "vivaldi"],
        help="YouTubeにログインしているブラウザ",
    )
    ap.add_argument("--max", type=int, default=200, help="最大処理件数")
    ap.add_argument("--sleep", type=float, default=1.0, help="リクエスト間隔（秒）")
    args = ap.parse_args()

    targets = []
    for p in sorted(PENDING_DIR.glob("*.json")):
        with p.open("r", encoding="utf-8") as f:
            d = json.load(f)
        status = d.get("transcript_status", "")
        if status not in ("ok", "no_transcript"):
            targets.append((d.get("published_at", ""), p, d))

    targets.sort(reverse=True)
    targets = targets[: args.max]

    if not targets:
        print("再取得対象の動画はありません")
        return

    print(f"対象: {len(targets)} 件 / browser={args.browser}")
    ok = no_t = err = 0
    for i, (pub, p, d) in enumerate(targets):
        if i > 0:
            time.sleep(args.sleep)
        text, status = fetch_via_ytdlp(d["video_id"], args.browser)
        d["transcript"] = text
        d["transcript_status"] = status
        with p.open("w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        if status == "ok":
            (TRANSCRIPTS_DIR / f"{d['video_id']}.txt").write_text(
                text, encoding="utf-8"
            )
            ok += 1
        elif status == "no_transcript":
            no_t += 1
        else:
            err += 1
        marker = "✓" if status == "ok" else ("-" if status == "no_transcript" else "✗")
        print(
            f"  [{i+1}/{len(targets)}] {marker} {pub[:10]} {d['title'][:50]}  ({status[:40]})"
        )

    print(f"\n結果: ok={ok} / no_transcript={no_t} / error={err}")


if __name__ == "__main__":
    main()
