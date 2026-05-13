"""集約JSON＋ナラティブJSON → reports/weekly_summary_<until>.html

使い方:
    python3 scripts/render_weekly_summary.py --until 2026-05-11
    （data/weekly_aggregates/week_<until>.json と
      data/weekly_narratives/week_<until>.json を読む。
      ナラティブがない場合は集約データだけで簡易レンダ）
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import REPORTS_DIR, ROOT

AGG_DIR = ROOT / "data" / "weekly_aggregates"
NAR_DIR = ROOT / "data" / "weekly_narratives"
NAR_DIR.mkdir(parents=True, exist_ok=True)


CSS = """
:root{
  --bg:#0f172a; --panel:#1e293b; --panel-2:#273449; --text:#e2e8f0;
  --muted:#94a3b8; --accent:#60a5fa; --pos:#34d399; --neg:#f87171;
  --topic:#fbbf24; --weekly:#f59e0b;
}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;background:var(--bg);color:var(--text);line-height:1.7}
header{padding:36px 48px;background:linear-gradient(135deg,#92400e 0%,#7c2d12 50%,#312e81 100%);border-bottom:1px solid #334155}
header h1{margin:0 0 6px;font-size:28px}
header .meta{color:#fbbf24;font-size:14px;font-weight:600}
header .tagline{color:#fef3c7;font-size:15px;margin-top:8px;font-style:italic}
main{padding:32px 48px;max-width:1080px;margin:0 auto}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:32px}
.stat{background:var(--panel);padding:14px 18px;border-radius:8px}
.stat .num{font-size:24px;font-weight:700;color:var(--accent)}
.stat .lbl{font-size:12px;color:var(--muted);margin-top:2px}
section{margin-bottom:36px}
section h2{font-size:20px;color:var(--weekly);border-bottom:2px solid var(--weekly);padding-bottom:6px;margin:0 0 16px;display:flex;align-items:center;gap:8px}
section h2 .emoji{font-size:22px}
.theme{background:var(--panel);padding:16px 20px;border-radius:10px;margin-bottom:12px;border-left:4px solid var(--weekly)}
.theme h3{margin:0 0 6px;font-size:16px;color:var(--text)}
.theme .desc{color:#cbd5e1;font-size:14px;margin:4px 0 8px}
.theme .channels{font-size:12px;color:var(--muted)}
.theme .channels b{color:#cbd5e1}
.topic-list{display:flex;flex-wrap:wrap;gap:8px}
.topic-chip{background:var(--panel);padding:6px 12px;border-radius:18px;font-size:13px;display:inline-flex;align-items:center;gap:6px}
.topic-chip .cnt{background:var(--weekly);color:#1c1917;padding:1px 8px;border-radius:10px;font-size:11px;font-weight:700}
.channel-card{background:var(--panel);padding:14px 18px;border-radius:8px;margin-bottom:10px;display:grid;grid-template-columns:auto 1fr auto;gap:14px;align-items:start}
.channel-card .ch-name{font-weight:600;color:var(--accent);min-width:140px}
.channel-card .ch-text{color:#cbd5e1;font-size:14px}
.channel-card .ch-n{color:var(--muted);font-size:12px;text-align:right;white-space:nowrap}
.bullet-list{list-style:none;padding:0;margin:0}
.bullet-list li{background:var(--panel-2);padding:8px 14px;border-radius:6px;margin-bottom:6px;font-size:14px}
.bullet-list.pos li{border-left:3px solid var(--pos)}
.bullet-list.neg li{border-left:3px solid var(--neg)}
.pick{background:var(--panel);padding:16px 20px;border-radius:10px;margin-bottom:12px}
.pick .pick-head{display:flex;justify-content:space-between;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:6px}
.pick .pick-title{font-size:15px;font-weight:600;color:var(--accent);text-decoration:none}
.pick .pick-title:hover{text-decoration:underline}
.pick .pick-ch{font-size:12px;color:var(--muted)}
.pick .pick-reason{background:#451a03;color:#fed7aa;padding:8px 12px;border-radius:6px;font-size:13px;margin:8px 0;border-left:3px solid var(--weekly)}
.pick .pick-summary{color:#cbd5e1;font-size:13px;white-space:pre-line;margin:6px 0}
.pick .pick-topics{display:flex;flex-wrap:wrap;gap:4px;margin-top:6px}
.pick .pick-topics span{background:var(--panel-2);color:var(--topic);padding:2px 8px;border-radius:10px;font-size:11px}
.footer-links{margin-top:32px;padding-top:16px;border-top:1px solid #334155;font-size:13px;color:var(--muted)}
.footer-links a{color:var(--accent);text-decoration:none;margin-right:14px}
.footer-links a:hover{text-decoration:underline}
"""


def esc(s) -> str:
    return html.escape(str(s) if s is not None else "")


def render_themes(narrative: dict) -> str:
    themes = narrative.get("themes") or []
    if not themes:
        return ""
    parts = []
    for t in themes:
        chs = t.get("channels") or []
        chs_html = (
            f'<div class="channels"><b>関連チャンネル:</b> {esc("、".join(chs))}</div>'
            if chs
            else ""
        )
        parts.append(
            f'<div class="theme">'
            f'<h3>{esc(t.get("title",""))}</h3>'
            f'<div class="desc">{esc(t.get("description",""))}</div>'
            f'{chs_html}'
            f'</div>'
        )
    return f'<section><h2><span class="emoji">🔥</span>今週の話題まとめ</h2>{"".join(parts)}</section>'


def render_topics(agg: dict) -> str:
    topics = agg.get("top_topics") or []
    if not topics:
        return ""
    top = topics[:12]
    chips = "".join(
        f'<span class="topic-chip">{esc(t["topic"])}<span class="cnt">{t["count"]}</span></span>'
        for t in top
    )
    return (
        f'<section><h2><span class="emoji">🏷</span>頻出キートピック Top {len(top)}</h2>'
        f'<div class="topic-list">{chips}</div></section>'
    )


def render_channels(narrative: dict, agg: dict) -> str:
    highlights = {h["channel"]: h["highlight"] for h in (narrative.get("channel_highlights") or [])}
    rows = []
    for c in agg.get("channels") or []:
        ch = c["channel"]
        text = highlights.get(ch, "（ハイライト未生成）")
        rows.append(
            f'<div class="channel-card">'
            f'<div class="ch-name">{esc(ch)}</div>'
            f'<div class="ch-text">{esc(text)}</div>'
            f'<div class="ch-n">{c["n_videos"]} 本</div>'
            f'</div>'
        )
    if not rows:
        return ""
    return (
        f'<section><h2><span class="emoji">📺</span>チャンネル別ハイライト</h2>'
        f'{"".join(rows)}</section>'
    )


def render_themes_posneg(narrative: dict) -> str:
    pos = narrative.get("positive_themes") or []
    neg = narrative.get("negative_themes") or []
    if not pos and not neg:
        return ""
    pos_html = (
        f'<h3 style="font-size:15px;color:var(--pos);margin:8px 0 6px">👍 ポジティブ傾向</h3>'
        f'<ul class="bullet-list pos">{"".join(f"<li>{esc(p)}</li>" for p in pos)}</ul>'
        if pos
        else ""
    )
    neg_html = (
        f'<h3 style="font-size:15px;color:var(--neg);margin:14px 0 6px">👎 ネガティブ傾向</h3>'
        f'<ul class="bullet-list neg">{"".join(f"<li>{esc(n)}</li>" for n in neg)}</ul>'
        if neg
        else ""
    )
    return (
        f'<section><h2><span class="emoji">⚖️</span>今週の共通ポジ／ネガ傾向</h2>'
        f'{pos_html}{neg_html}</section>'
    )


def render_picks(narrative: dict, agg: dict) -> str:
    picks = narrative.get("picks") or []
    if not picks:
        return ""
    by_id = {v["video_id"]: v for v in (agg.get("pick_candidates") or [])}
    parts = []
    for p in picks:
        vid = p.get("video_id")
        v = by_id.get(vid, {})
        url = v.get("url") or (f"https://www.youtube.com/watch?v={vid}" if vid else "#")
        topics_html = ""
        if v.get("key_topics"):
            topics_html = (
                f'<div class="pick-topics">'
                + "".join(f"<span>{esc(t)}</span>" for t in v["key_topics"])
                + "</div>"
            )
        parts.append(
            f'<div class="pick">'
            f'<div class="pick-head">'
            f'<a class="pick-title" href="{esc(url)}" target="_blank">{esc(v.get("title","(タイトル不明)"))}</a>'
            f'<span class="pick-ch">{esc(v.get("channel",""))}</span>'
            f'</div>'
            f'<div class="pick-reason">💡 {esc(p.get("reason",""))}</div>'
            f'<div class="pick-summary">{esc(v.get("summary_3lines",""))}</div>'
            f'{topics_html}'
            f'</div>'
        )
    return (
        f'<section><h2><span class="emoji">⭐</span>注目動画ピックアップ</h2>'
        f'{"".join(parts)}</section>'
    )


def render_html(agg: dict, narrative: dict | None) -> str:
    meta = agg["meta"]
    narrative = narrative or {}
    tagline = narrative.get("tagline", "")
    tagline_html = f'<div class="tagline">{esc(tagline)}</div>' if tagline else ""

    stats_html = (
        f'<div class="stats">'
        f'<div class="stat"><div class="num">{meta["n_videos"]}</div><div class="lbl">動画</div></div>'
        f'<div class="stat"><div class="num">{meta["n_channels"]}</div><div class="lbl">チャンネル</div></div>'
        f'<div class="stat"><div class="num">{meta["n_positive_points"]}</div><div class="lbl">ポジ要素</div></div>'
        f'<div class="stat"><div class="num">{meta["n_negative_points"]}</div><div class="lbl">ネガ要素</div></div>'
        f'</div>'
    )

    body = (
        render_themes(narrative)
        + render_topics(agg)
        + render_channels(narrative, agg)
        + render_themes_posneg(narrative)
        + render_picks(narrative, agg)
    )

    daily_link = f'weekly_report_{meta["until"]}.html'
    footer = (
        f'<div class="footer-links">'
        f'<a href="{daily_link}">📄 同週の日次レポート（個別動画一覧）</a>'
        f'<a href="index.html">🗂 レポート一覧へ戻る</a>'
        f'</div>'
    )

    return f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<title>YouTube週次総括 {meta["since"]}〜{meta["until"]}</title>
<style>{CSS}</style></head>
<body>
<header>
<h1>📌 YouTube 週次総括</h1>
<div class="meta">{meta["since"]} 〜 {meta["until"]}（7日間）</div>
{tagline_html}
</header>
<main>
{stats_html}
{body}
{footer}
</main>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--until", required=True, help="YYYY-MM-DD")
    args = ap.parse_args()

    agg_path = AGG_DIR / f"week_{args.until}.json"
    nar_path = NAR_DIR / f"week_{args.until}.json"
    if not agg_path.exists():
        raise SystemExit(f"集約ファイルがありません: {agg_path}")
    agg = json.loads(agg_path.read_text(encoding="utf-8"))
    narrative = None
    if nar_path.exists():
        narrative = json.loads(nar_path.read_text(encoding="utf-8"))
        print(f"ナラティブ読み込み: {nar_path}")
    else:
        print(f"⚠️  ナラティブなし（{nar_path}）— 集約データのみで簡易レンダ")

    out = REPORTS_DIR / f"weekly_summary_{args.until}.html"
    out.write_text(render_html(agg, narrative), encoding="utf-8")
    print(f"出力: {out}")

    # index も再生成して、新しい weekly_summary が「週次総括」セクションに載るようにする
    # （日次タスクとの実行順序ズレでindexが古くならないように）
    try:
        from generate_weekly_report import render_index
        render_index()
        print("index 再生成: reports/index.html")
    except Exception as e:
        print(f"⚠️  index 再生成失敗（手動で render_index() を実行してください）: {e}")


if __name__ == "__main__":
    main()
