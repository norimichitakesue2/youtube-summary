"""X検索ページの状態を診断する。

使い方:
    cd ~/youtube-summary && source .venv/bin/activate
    python3 scripts/x_diag_search.py

挙動:
    既存のログイン済みプロファイルで検索URLを開き、
        - スクリーンショット (data/diag/<target>.png)
        - HTML (data/diag/<target>.html)
        - 主要な testid の出現件数
        - 検出されたエラーバナー文字列
    を保存・出力する。
"""
from __future__ import annotations

import sys
import time
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
USER_DATA_DIR = ROOT / "data" / "x_browser_profile"
DIAG_DIR = ROOT / "data" / "diag"
DIAG_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("hashtag_romasagars", f"https://x.com/search?q={urllib.parse.quote('#ロマサガRS')}&src=typed_query&f=live"),
    ("hashtag_romasagars_nofilter", f"https://x.com/search?q={urllib.parse.quote('#ロマサガRS')}&src=typed_query"),
    ("keyword_romasagars", f"https://x.com/search?q={urllib.parse.quote('ロマサガRS')}&src=typed_query&f=live"),
    ("keyword_romasagars_top", f"https://x.com/search?q={urllib.parse.quote('ロマサガRS')}&src=typed_query"),
    ("home", "https://x.com/home"),
]

ERROR_HINTS = [
    "Something went wrong",
    "うまくいきませんでした",
    "Try reloading",
    "リロードしてください",
    "Sign in",
    "ログイン",
    "アカウントを作成",
    "Rate limit",
    "レート制限",
    "Try again",
    "やり直してください",
    "このアカウント",
    "Restricted",
    "制限されています",
]


def main():
    if not USER_DATA_DIR.exists():
        print("先に scripts/x_login.py を実行してください")
        sys.exit(1)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=False,
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        for name, url in TARGETS:
            print(f"\n=== {name} ===")
            print(f"  URL: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
            except Exception as e:
                print(f"  goto error: {e}")
                continue

            # 画面が描画されるのを待つ（ツイートが出るとは限らない）
            time.sleep(6)

            # スクショ＆HTML保存
            png = DIAG_DIR / f"{name}.png"
            html = DIAG_DIR / f"{name}.html"
            try:
                page.screenshot(path=str(png), full_page=False)
            except Exception as e:
                print(f"  screenshot error: {e}")
            try:
                content = page.content()
                html.write_text(content, encoding="utf-8")
            except Exception as e:
                print(f"  html error: {e}")
                content = ""

            # testid 集計
            for testid in ["tweet", "cellInnerDiv", "primaryColumn", "emptyState",
                            "error-detail", "loginButton", "SignupButton",
                            "TopNavBar", "tweetTextarea_0"]:
                try:
                    n = len(page.query_selector_all(f'[data-testid="{testid}"]'))
                except Exception:
                    n = -1
                print(f"    [data-testid=\"{testid}\"]: {n}")

            # エラーバナー検出
            hits = []
            for hint in ERROR_HINTS:
                if hint in content:
                    hits.append(hint)
            if hits:
                print(f"  検出文字列: {hits[:8]}")

            # 現在のURL（リダイレクトされていないか）
            print(f"  最終URL: {page.url}")
            print(f"  保存: {png.name} / {html.name}")

        ctx.close()
    print("\n保存先: data/diag/")


if __name__ == "__main__":
    main()
