"""X（Twitter）から指定対象のツイートを取得し、data/tweets/ に保存する。

使い方:
    python3 scripts/x_fetch.py                  # since_hours=24 のデフォルト
    python3 scripts/x_fetch.py --hours 48
    python3 scripts/x_fetch.py --headed         # ブラウザ表示（デバッグ用）

前提:
    scripts/x_login.py を一度実行して data/x_state.json があること。

出力:
    data/tweets/<YYYY-MM-DD>__fetch.json   （その日の取得結果）
    data/tweets/all_tweets.jsonl           （全期間の蓄積、1行1ツイート）

各ツイートのスキーマ:
    {
      "tweet_id": "...",
      "url": "https://x.com/USER/status/...",
      "author_handle": "...",
      "author_name": "...",
      "text": "...",
      "created_at": "ISO8601",
      "likes": 0,
      "retweets": 0,
      "replies": 0,
      "source_type": "account" | "hashtag" | "keyword",
      "source_target": "@romasaga_rs" | "#ロマサガRS" | "ロマサガRS",
      "fetched_at": "ISO8601"
    }
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TWEETS_DIR = DATA_DIR / "tweets"
TWEETS_DIR.mkdir(parents=True, exist_ok=True)
USER_DATA_DIR = DATA_DIR / "x_browser_profile"
TARGETS_FILE = ROOT / "x_targets.yaml"
ALL_TWEETS_JSONL = TWEETS_DIR / "all_tweets.jsonl"


def load_targets() -> dict:
    with TARGETS_FILE.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_engagement(text: str) -> int:
    """X の数字表記 (1.2K, 5.3M, 100) を整数に。"""
    if not text:
        return 0
    text = text.strip()
    m = re.match(r"([\d.]+)\s*([KMkm]?)", text)
    if not m:
        return 0
    n = float(m.group(1))
    suf = m.group(2).lower()
    if suf == "k":
        n *= 1000
    elif suf == "m":
        n *= 1_000_000
    return int(n)


def parse_relative_time(text: str, now: datetime) -> datetime | None:
    """X の相対時刻 ("2分", "3h", "Apr 24") を datetime に変換。"""
    if not text:
        return None
    text = text.strip()
    # 相対表記
    m = re.match(r"(\d+)\s*([smhdyM])", text, re.IGNORECASE)
    if m:
        n = int(m.group(1))
        unit = m.group(2).lower()
        delta = {
            "s": timedelta(seconds=n),
            "m": timedelta(minutes=n),
            "h": timedelta(hours=n),
            "d": timedelta(days=n),
        }.get(unit)
        if delta:
            return now - delta
    # 日本語: 「2時間」「3分」
    m = re.match(r"(\d+)\s*(秒|分|時間|日)", text)
    if m:
        n = int(m.group(1))
        unit = m.group(2)
        delta = {
            "秒": timedelta(seconds=n),
            "分": timedelta(minutes=n),
            "時間": timedelta(hours=n),
            "日": timedelta(days=n),
        }.get(unit)
        if delta:
            return now - delta
    return None


def extract_tweets_from_page(page, source_type: str, source_target: str, max_n: int):
    """現在のページからツイート要素を抽出してyieldする。"""
    seen_ids = set()
    no_progress_rounds = 0
    last_count = 0

    while len(seen_ids) < max_n and no_progress_rounds < 5:
        # ツイート要素を取得
        articles = page.query_selector_all('article[data-testid="tweet"]')
        for art in articles:
            # tweet_id（リンクから抽出）
            link = art.query_selector('a[href*="/status/"]')
            if not link:
                continue
            href = link.get_attribute("href") or ""
            m = re.search(r"/status/(\d+)", href)
            if not m:
                continue
            tweet_id = m.group(1)
            if tweet_id in seen_ids:
                continue
            seen_ids.add(tweet_id)

            try:
                # author handle (URL の最初のセグメント)
                handle_match = re.match(r"/(\w+)/status/", href)
                author_handle = handle_match.group(1) if handle_match else ""

                # author display name
                name_el = art.query_selector('div[data-testid="User-Name"] span')
                author_name = name_el.inner_text() if name_el else author_handle

                # text
                text_el = art.query_selector('div[data-testid="tweetText"]')
                text = text_el.inner_text() if text_el else ""

                # created_at (datetime属性)
                time_el = art.query_selector("time")
                created_at = (
                    time_el.get_attribute("datetime") if time_el else None
                ) or ""

                # engagement
                def get_count(testid):
                    el = art.query_selector(f'[data-testid="{testid}"]')
                    if not el:
                        return 0
                    label = el.get_attribute("aria-label") or el.inner_text()
                    m = re.search(r"(\d[\d,.]*[KkMm]?)", label)
                    return parse_engagement(m.group(1)) if m else 0

                likes = get_count("like")
                retweets = get_count("retweet")
                replies = get_count("reply")

                yield {
                    "tweet_id": tweet_id,
                    "url": f"https://x.com{href.split('?')[0]}",
                    "author_handle": author_handle,
                    "author_name": author_name,
                    "text": text,
                    "created_at": created_at,
                    "likes": likes,
                    "retweets": retweets,
                    "replies": replies,
                    "source_type": source_type,
                    "source_target": source_target,
                }
            except Exception as e:
                print(f"    [skip] {tweet_id}: {e}", file=sys.stderr)
                continue

        # スクロール
        page.mouse.wheel(0, 3000)
        time.sleep(1.2)

        if len(seen_ids) == last_count:
            no_progress_rounds += 1
        else:
            no_progress_rounds = 0
        last_count = len(seen_ids)


def fetch_target(page, source_type: str, source_target: str, url: str, max_n: int):
    """指定URLにアクセスして、ツイートを抽出する。"""
    print(f"  → {source_target}  ({url})")
    page.goto(url, wait_until="domcontentloaded")
    # ツイート要素が出るまで待機
    try:
        page.wait_for_selector('article[data-testid="tweet"]', timeout=15000)
    except Exception:
        print(f"    [warn] ツイート要素が見つかりません")
        return []
    time.sleep(2)
    return list(extract_tweets_from_page(page, source_type, source_target, max_n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, help="何時間前までの投稿を対象にするか")
    ap.add_argument("--headed", action="store_true", help="ブラウザを表示する")
    args = ap.parse_args()

    if not USER_DATA_DIR.exists() or not any(USER_DATA_DIR.iterdir()):
        print(f"先に scripts/x_login.py を実行してログインしてください")
        sys.exit(1)

    cfg = load_targets()
    defaults = cfg.get("defaults", {}) or {}
    since_hours = args.hours or defaults.get("since_hours", 24)
    max_per_target = defaults.get("max_per_target", 100)
    lang = defaults.get("lang", "")

    cutoff = datetime.now(timezone.utc) - timedelta(hours=since_hours)
    fetched_at = datetime.now(timezone.utc).isoformat()

    targets = []
    for a in cfg.get("accounts", []) or []:
        if a.get("enabled", True):
            targets.append(("account", "@" + a["handle"], f"https://x.com/{a['handle']}"))
    for h in cfg.get("hashtags", []) or []:
        if h.get("enabled", True):
            tag = h["tag"]
            q = urllib.parse.quote(tag)
            url = f"https://x.com/search?q={q}&src=typed_query&f=live"
            targets.append(("hashtag", tag, url))
    for k in cfg.get("keywords", []) or []:
        if k.get("enabled", True):
            qstr = k["query"]
            if lang:
                qstr += f" lang:{lang}"
            q = urllib.parse.quote(qstr)
            url = f"https://x.com/search?q={q}&src=typed_query&f=live"
            targets.append(("keyword", k["query"], url))

    if not targets:
        print("有効なターゲットがありません。x_targets.yaml を確認してください")
        sys.exit(1)

    print(f"対象: {len(targets)} 件 / since={cutoff.isoformat()[:19]}")

    all_tweets = []
    with sync_playwright() as p:
        # Mac標準の Google Chrome を使う（X の bot 検知を回避するため）
        # Chrome 未インストールの場合は chromium-headless-shell にフォールバック
        try:
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=str(USER_DATA_DIR),
                channel="chrome",
                headless=not args.headed,
                args=[
                    "--disable-blink-features=AutomationControlled",
                ],
                ignore_default_args=["--enable-automation"],
                viewport={"width": 1280, "height": 900},
            )
        except Exception as e:
            print(f"[warn] Chrome 起動失敗 ({e}) — chromium-headless-shell にフォールバック")
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=str(USER_DATA_DIR),
                headless=not args.headed,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-features=IsolateOrigins,site-per-process",
                ],
                ignore_default_args=["--enable-automation"],
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/130.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 900},
            )
        ctx.add_init_script(
            "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for source_type, source_target, url in targets:
            try:
                tweets = fetch_target(page, source_type, source_target, url, max_per_target)
            except Exception as e:
                print(f"    [error] {source_target}: {e}")
                continue
            # cutoff より新しいものだけ
            for t in tweets:
                t["fetched_at"] = fetched_at
                created = t.get("created_at", "")
                if created:
                    try:
                        ct = datetime.fromisoformat(created.replace("Z", "+00:00"))
                        if ct < cutoff:
                            continue
                    except ValueError:
                        pass
                all_tweets.append(t)
            print(f"    取得 {len(tweets)} 件（cutoff後 {len([t for t in tweets if t.get('created_at','') and datetime.fromisoformat(t['created_at'].replace('Z','+00:00')) >= cutoff])} 件）")
        ctx.close()

    # dedupe by tweet_id
    by_id = {}
    for t in all_tweets:
        if t["tweet_id"] in by_id:
            # source_targetが複数の場合はマージ
            existing = by_id[t["tweet_id"]]
            existing.setdefault("also_matched", []).append(
                f"{t['source_type']}:{t['source_target']}"
            )
        else:
            by_id[t["tweet_id"]] = t
    deduped = list(by_id.values())

    today = datetime.now().strftime("%Y-%m-%d")
    out = TWEETS_DIR / f"{today}__fetch.json"
    with out.open("w", encoding="utf-8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)

    # 全期間jsonlにも追記
    existing_ids = set()
    if ALL_TWEETS_JSONL.exists():
        with ALL_TWEETS_JSONL.open("r", encoding="utf-8") as f:
            for line in f:
                try:
                    existing_ids.add(json.loads(line)["tweet_id"])
                except Exception:
                    pass
    new_count = 0
    with ALL_TWEETS_JSONL.open("a", encoding="utf-8") as f:
        for t in deduped:
            if t["tweet_id"] not in existing_ids:
                f.write(json.dumps(t, ensure_ascii=False) + "\n")
                new_count += 1

    print(f"\n保存: {out}")
    print(f"  ユニーク {len(deduped)} 件（うち新規 {new_count} 件）")


if __name__ == "__main__":
    main()
