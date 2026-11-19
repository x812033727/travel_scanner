---
id: 2026-11-19-curio-wave-85-wave-84-rechecks
title: Curio wave 85, wave 84 rechecks, so-that's-why G749-G756 and G746 rewrite
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-19T01:01:43Z
created_at: 2026-11-19T01:01:30Z
completed_at: 2026-11-19T01:01:44Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Curio wave 85, wave 84 rechecks, so-that's-why G749-G756 and G746 rewrite

## Why

站主 2026-11-19 PR #2168 合併後選：再擴一批奇聞、補查第八十四批待查、重寫 G746 記憶卡、原來如此再擴充。

## Definition of done

- [x] 第八十四批待查：N7835、N7863 升可收（一章、暫緩）；N7832、N7843、N7846、N7864 不收，重開條件寫進 dedup-decisions。
- [x] 奇聞第八十五批：40 個方向研究覆核，18 收、11 待查、11 不收；5 題單集題入選（4 題過 6.5，N7890 6.01 照前例保留），13 題一章暫緩。
- [x] 原來如此 G749–G756 八組 ready、定稿觀眾分 6.8–8.18，登記進備份分類表；G756 改片名。
- [x] G746 改稿重評 5.62 仍未過 6.5，維持 reserve。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```
