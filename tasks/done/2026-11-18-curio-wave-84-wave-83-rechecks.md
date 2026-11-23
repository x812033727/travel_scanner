---
id: 2026-11-18-curio-wave-84-wave-83-rechecks
title: Curio wave 84, wave 83 rechecks, so-that's-why G736/G738 reinforcement and G741-G748
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-18T16:34:41Z
created_at: 2026-11-18T16:34:28Z
completed_at: 2026-11-18T16:34:42Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
  - apps/api/uv.lock
---

# Curio wave 84, wave 83 rechecks, so-that's-why G736/G738 reinforcement and G741-G748

## Why

站主 2026-11-18 合併 PR #2166 後選：再擴一批奇聞、補查第八十三批待查、補強原來如此薄題、原來如此再擴充。

## Definition of done

- [x] 第八十三批待查：N7799、N7803、N7805、N7813、N7817、N7818 升可收（一章、暫緩）；N7792、N7822 仍待查；N7794、N7795、N7816 不收。
- [x] 奇聞第八十四批：40 個方向研究覆核，23 收、6 待查、11 不收；9 題單集題入選（8 題過 6.5，N7839 5.92 照前例保留），14 題一章暫緩。
- [x] 原來如此 G736（11.5→12.75）、G738（13.25，補台灣級距與夏月出處）補強。
- [x] CI 的 pip-audit 抓到 dnspython 2.9.0、opentelemetry-api 1.45.1 新 CVE（main 也有），uv.lock 升到 2.9.2、1.45.2。
- [x] 原來如此 G741–G745、G747、G748 七組 ready、定稿觀眾分 6.7–8.28，登記進備份分類表；G744 改片名；G746 定稿觀眾分 5.87 未過 6.5，不收。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```
