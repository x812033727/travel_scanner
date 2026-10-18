#!/usr/bin/env bash
# 部署的替身：只在專案裡的 deploy-record.txt 加一行。
# 不連網路，不碰專案以外的任何東西。
cd "$(dirname "$0")/.." || exit 1
stamp="$(date -u +%H:%M:%SZ)"
echo "deployed (stand-in) $stamp" >> deploy-record.txt
echo "deploy stand-in: one line added to deploy-record.txt"
