---
id: 2026-11-19-extend-curio-wave-87-and-so
title: Extend Curio wave 87 and So Thats Why wave 116 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T05:21:16Z
created_at: 2026-11-19T05:21:12Z
completed_at: 2026-11-19T05:51:30Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 87 and So Thats Why wave 116 on PR 2177

## Why

延續 PR #2177 的兩池擴充，在同一個分支追加新批次。保留前批的題卡、排名依據和後備紀錄。

## Definition of done

- [x] 新核心可追溯至實讀來源，並經非作者比對兩池舊題、查核事實與適用範圍。
- [x] 單集與長片題案完成素材與觀眾評估；新增卡可由搜尋頁及後台查到。

## Steps

- [x] 核對 PR #2177 分支與前一批存檔點。
- [x] 收錄兩池新題、留存退題判斷及評分。
- [x] 重建輸出、核對既有選題與題案、執行驗證。

## Result

奇聞第 87 批新增四個單集與兩個章節，入選達 1,800。原來如此第 116 批的 45 張新卡使入選達 7,147，G758 地震警報與 G759 國際電話首零各通過長題門檻，長題可成題數達 104。確認前批入選 ID 與順序均保留，舊題案只調整全池排名欄位。桌面及手機尺寸均已實際搜尋題目與切換新長片題案。

測試通過 67 項 Node、4 項語意索引與 92 項 API 測試。備份分類檔亦通過 Ruff、mypy。

## How to verify

```sh
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
node --test tools/video/{curio,so-thats-why}/pool/pool.test.mjs tools/video/pool-admin/bundle.test.mjs
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```
