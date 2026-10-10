#!/usr/bin/env bash
# 例行報表：印出費率表有幾區，不改任何檔。
cd "$(dirname "$0")/.." || exit 1
echo "rates: $(($(wc -l < data/rates.csv) - 1)) zones"
