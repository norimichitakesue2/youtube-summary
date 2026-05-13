#!/bin/bash
# 週次レポート生成用スクリプト
# 直近7日のHTMLレポートを reports/ に生成

set -e
cd "$(dirname "$0")/.."

echo "=== $(date) weekly_run start ==="
python3 scripts/generate_weekly_report.py --days 7
echo "=== done ==="
