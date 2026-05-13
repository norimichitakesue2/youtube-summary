"""共通ユーティリティ：設定・状態・パス管理。"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
PENDING_DIR = DATA_DIR / "pending_summaries"
REPORTS_DIR = ROOT / "reports"
STATE_FILE = DATA_DIR / "state.json"
CHANNELS_FILE = ROOT / "channels.yaml"
LOG_FILE = ROOT / "video_log.xlsx"

for d in (DATA_DIR, TRANSCRIPTS_DIR, PENDING_DIR, REPORTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

load_dotenv(ROOT / ".env")


def get_api_key() -> str:
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        raise SystemExit("YOUTUBE_API_KEY が .env に設定されていません")
    return key


def load_channels() -> list[dict[str, Any]]:
    with CHANNELS_FILE.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return [c for c in (cfg or {}).get("channels", []) if c.get("enabled", True)]


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {}
    with STATE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict[str, Any]) -> None:
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
