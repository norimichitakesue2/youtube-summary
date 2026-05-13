"""X（Twitter）ログイン状態を保存する初回セットアップスクリプト。

使い方:
    python3 scripts/x_login.py

ブラウザが開くので、Xに手動でログインしてください。
ログイン後、ターミナルでEnterを押すと終了します。

セッション情報は data/x_browser_profile/ に永続保存されます（cookieやキャッシュ等）。
以後、x_fetch.py が同じプロファイルを使ってログイン済みでスクレイピングします。

セッションが切れた場合は、再度このスクリプトを実行してください。
"""
from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
USER_DATA_DIR = ROOT / "data" / "x_browser_profile"
USER_DATA_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print(f"プロファイル保存先: {USER_DATA_DIR}")
    print()
    print("ブラウザを起動します。Xに手動ログインしてください。")
    print("ログイン完了後、ターミナルに戻って Enter を押してください。")
    print()
    with sync_playwright() as p:
        # Mac標準の Google Chrome を使う（X の bot 検知を回避するため）
        # Chrome がインストールされていない場合は chromium-headless-shell にフォールバック
        try:
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=str(USER_DATA_DIR),
                channel="chrome",
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                ],
                ignore_default_args=["--enable-automation"],
                viewport={"width": 1280, "height": 900},
            )
            print("[info] Google Chrome を使用")
        except Exception as e:
            print(f"[warn] Chrome 起動失敗 ({e}) — chromium-headless-shell にフォールバック")
            ctx = p.chromium.launch_persistent_context(
                user_data_dir=str(USER_DATA_DIR),
                headless=False,
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
        # navigator.webdriver を消す
        ctx.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            """
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto("https://x.com/login")
        input("ログイン完了したら Enter を押してください > ")
        ctx.close()
        print(f"\n保存しました: {USER_DATA_DIR}")


if __name__ == "__main__":
    main()
