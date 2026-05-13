"""Xツイート要約のHTMLレポートを生成する。

使い方:
    python3 scripts/generate_x_report.py --daily              # 直近1日
    python3 scripts/generate_x_report.py --weekly             # 直近7日
    python3 scripts/generate_x_report.py --since 2026-04-01 --until 2026-04-30

出力:
    reports/x_daily_<YYYY-MM-DD>.html  または
    reports/x_weekly_<YYYY-MM-DD>.html
    reports/x_index.html  ← 過去Xレポート一覧
"""
from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMMARIES_DIR = ROOT / "data" / "tweet_summaries"
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>Xツイートサマリ {since} 〜 {until}</title>
<style>
  :root {{
    --bg: #0f172a;
    --panel: #1e293b;
    --panel-2: #273449;
    --text: #e2e8f0;
    --muted: #94a3b8;
    --accent: #1da1f2;
    --pos: #34d399;
    --neg: #f87171;
    --topic: #fbbf24;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
  }}
  header {{
    padding: 32px 48px;
    background: linear-gradient(135deg, #0c4a6e 0%, #164e63 100%);
    border-bottom: 1px solid #334155;
  }}
  header h1 {{ margin: 0 0 8px; font-size: 28px; }}
  header .meta {{ color: #cbd5e1; font-size: 14px; }}
  main {{ padding: 32px 48px; max-width: 1100px; margin: 0 auto; }}
  .summary-stats {{
    display: flex;
    gap: 16px;
    margin-bottom: 32px;
    flex-wrap: wrap;
  }}
  .stat {{
    background: var(--panel);
    padding: 16px 24px;
    border-radius: 8px;
    flex: 1;
    min-width: 180px;
  }}
  .stat .num {{ font-size: 28px; font-weight: 700; color: var(--accent); }}
  .stat .label {{ font-size: 13px; color: var(--muted); margin-top: 4px; }}
  .day {{ margin-bottom: 40px; }}
  .day h2 {{
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 8px;
    margin-bottom: 16px;
    font-size: 22px;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
  }}
  .day h2 .count {{
    font-size: 13px;
    font-weight: normal;
    color: var(--muted);
  }}
  .day-summary {{
    background: var(--panel);
    padding: 18px 22px;
    border-radius: 10px;
    margin-bottom: 16px;
    border-left: 4px solid var(--accent);
    white-space: pre-wrap;
    color: #cbd5e1;
  }}
  .pos-neg-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
  }}
  @media (max-width: 700px) {{ .pos-neg-grid {{ grid-template-columns: 1fr; }} }}
  .pos, .neg {{
    background: var(--panel-2);
    border-radius: 8px;
    padding: 12px 16px;
  }}
  .pos {{ border-left: 3px solid var(--pos); }}
  .neg {{ border-left: 3px solid var(--neg); }}
  .pos .label, .neg .label {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 6px;
  }}
  .pos .label {{ color: var(--pos); }}
  .neg .label {{ color: var(--neg); }}
  .pos ul, .neg ul {{ margin: 0; padding-left: 18px; }}
  .topics {{ margin-bottom: 16px; display: flex; flex-wrap: wrap; gap: 6px; }}
  .topic {{
    background: rgba(251, 191, 36, 0.15);
    color: var(--topic);
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 12px;
  }}
  .hot-tweets-label {{
    color: var(--muted);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
  }}
  .tweet {{
    background: var(--panel);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
    border-left: 3px solid var(--accent);
    font-size: 14px;
  }}
  .tweet .author {{
    color: var(--accent);
    font-weight: 600;
    margin-bottom: 4px;
    font-size: 13px;
  }}
  .tweet .text {{ color: #cbd5e1; white-space: pre-wrap; word-break: break-word; }}
  .tweet .stats {{
    color: var(--muted);
    font-size: 11px;
    margin-top: 6px;
  }}
  .tweet a {{ color: var(--accent); text-decoration: none; }}
  .tweet a:hover {{ text-decoration: underline; }}
  .empty-note {{ color: var(--muted); font-size: 13px; font-style: italic; }}
  footer {{
    text-align: center;
    color: var(--muted);
    font-size: 12px;
    padding: 24px;
    border-top: 1px solid #334155;
  }}
</style>
</head>
<body>
<header>
  <h1>Xツイートサマリ</h1>
  <div class="meta">対象期間: {since} 〜 {until}（{ndays}日間） / 生成日時: {generated}</div>
</header>
<main>
  <div class="summary-stats">
    <div class="stat"><div class="num">{n_tweets}</div><div class="label">ツイート総数</div></div>
    <div class="stat"><div class="num">{n_days}</div><div class="label">対象日数</div></div>
    <div class="stat"><div class="num">{n_pos}</div><div class="label">ポジ要素（合計）</div></div>
    <div class="stat"><div class="num">{n_neg}</div><div class="label">ネガ要素（合計）</div></div>
  </div>
  {body}
</main>
<footer>generated by youtube-summary (X module)</footer>
</body>
</html>
"""


def render_day(s: dict) -> str:
    date = html.escape(s["date"])
    n = s.get("n_tweets", 0)
    summary = html.escape(s.get("summary_3lines", "")).replace("\n", "<br>")
    pos = s.get("positive_themes", [])
    neg = s.get("negative_themes", [])
    topics = s.get("key_topics", [])
    hot = s.get("hot_tweets", [])

    pos_html = (
        "<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in pos) + "</ul>"
        if pos else '<div class="empty-note">特になし</div>'
    )
    neg_html = (
        "<ul>" + "".join(f"<li>{html.escape(x)}</li>" for x in neg) + "</ul>"
        if neg else '<div class="empty-note">特になし</div>'
    )
    topics_html = "".join(
        f'<span class="topic">{html.escape(t)}</span>' for t in topics
    )
    hot_html = ""
    for t in hot[:5]:
        url = html.escape(t.get("url", "#"))
        author_h = html.escape(t.get("author_handle", "?"))
        author_n = html.escape(t.get("author_name", ""))
        text = html.escape(t.get("text", "")).replace("\n", "<br>")
        likes = t.get("likes", 0)
        rts = t.get("retweets", 0)
        rep = t.get("replies", 0)
        hot_html += f"""
<div class="tweet">
  <div class="author">@{author_h} {f'<span style="color:#94a3b8;font-weight:normal">{author_n}</span>' if author_n else ''}</div>
  <div class="text">{text}</div>
  <div class="stats">♥ {likes} ／ ↻ {rts} ／ 💬 {rep} ・ <a href="{url}" target="_blank" rel="noopener">原文</a></div>
</div>
"""

    return f"""
<section class="day">
  <h2>{date}<span class="count">{n} ツイート</span></h2>
  <div class="day-summary">{summary or '<span class="empty-note">サマリなし</span>'}</div>
  <div class="pos-neg-grid">
    <div class="pos"><div class="label">ポジ要素</div>{pos_html}</div>
    <div class="neg"><div class="label">ネガ要素</div>{neg_html}</div>
  </div>
  {f'<div class="topics">{topics_html}</div>' if topics_html else ''}
  {f'<div class="hot-tweets-label">注目ツイート TOP{min(5,len(hot))}</div>{hot_html}' if hot else ''}
</section>
"""


def load_summaries(since: str, until: str):
    summaries = []
    for p in sorted(SUMMARIES_DIR.glob("*.json"), reverse=True):
        if since <= p.stem <= until:
            with p.open("r", encoding="utf-8") as f:
                summaries.append(json.load(f))
    return summaries


def render_index() -> None:
    files = sorted(REPORTS_DIR.glob("x_*.html"), reverse=True)
    files = [f for f in files if f.name != "x_index.html"]
    items = "".join(f'<li><a href="{f.name}">{f.name}</a></li>' for f in files)
    (REPORTS_DIR / "x_index.html").write_text(
        f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><title>Xレポート一覧</title>
<style>body{{font-family:sans-serif;max-width:600px;margin:40px auto;padding:0 16px}}
a{{color:#1da1f2}}</style></head>
<body><h1>Xレポート一覧</h1><ul>{items}</ul></body></html>""",
        encoding="utf-8",
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--daily", action="store_true")
    ap.add_argument("--weekly", action="store_true")
    ap.add_argument("--since")
    ap.add_argument("--until")
    args = ap.parse_args()

    today = datetime.now().date()
    if args.weekly or (not args.daily and not args.since):
        until = today
        since = today - timedelta(days=6)
        prefix = "x_weekly"
    elif args.daily:
        until = today
        since = today
        prefix = "x_daily"
    else:
        since = datetime.fromisoformat(args.since).date() if args.since else today
        until = datetime.fromisoformat(args.until).date() if args.until else today
        prefix = "x_custom"

    summaries = load_summaries(since.isoformat(), until.isoformat())
    body = "".join(render_day(s) for s in summaries) or '<p style="color:#94a3b8">この期間のサマリはまだありません。</p>'

    n_tweets = sum(s.get("n_tweets", 0) for s in summaries)
    n_pos = sum(len(s.get("positive_themes", [])) for s in summaries)
    n_neg = sum(len(s.get("negative_themes", [])) for s in summaries)

    html_out = HTML_TEMPLATE.format(
        since=since.isoformat(),
        until=until.isoformat(),
        ndays=(until - since).days + 1,
        generated=datetime.now().strftime("%Y-%m-%d %H:%M"),
        n_tweets=n_tweets,
        n_days=len(summaries),
        n_pos=n_pos,
        n_neg=n_neg,
        body=body,
    )
    out = REPORTS_DIR / f"{prefix}_{until.isoformat()}.html"
    out.write_text(html_out, encoding="utf-8")
    render_index()
    print(f"レポート生成: {out}")
    print(f"  対象: {since} 〜 {until} / {len(summaries)} 日 / {n_tweets} ツイート")


if __name__ == "__main__":
    main()
