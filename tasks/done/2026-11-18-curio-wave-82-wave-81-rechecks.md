---
id: 2026-11-18-curio-wave-82-wave-81-rechecks
title: Curio wave 82, wave 81 rechecks and rescores, so-that's-why G725-G732
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-18T11:36:00Z
created_at: 2026-11-18T11:35:46Z
completed_at: 2026-11-18T11:36:01Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Curio wave 82, wave 81 rechecks and rescores, so-that's-why G725-G732

## Why

站主 2026-11-18 合併 PR #2159 後選：再擴一批奇聞、重評兩題低分單集題、補查第八十一批待查、原來如此再擴充。

## Definition of done

- [x] 第八十一批待查補查：N7710、N7725、N7735 升可收（一章、暫緩），N7729 仍待查。
- [x] N7728、N7708 改寫問句重評（6.33、6.17），舊分數移出第八十一批評分檔。
- [x] 奇聞第八十二批：40 個方向研究覆核，31 收、8 待查、1 不收；6 題單集題入選，25 題一章暫緩。
- [x] 原來如此 G725–G732 八組新題案都 ready、定稿觀眾分過 6.5，登記進備份分類表。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node --test tools/video/so-thats-why/pool/pool.test.mjs
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```

## Notes

- 原來如此新題案第一輪從嚴併網後有三組不到門檻（G725、G726、G728），各補一輪獨立研究網才 ready。日本體系的論文作者若與調查編者合著，三網只能併一網。
- 奇聞池的觀眾分只能掛在入選的單集題上：單集題總分低於 6.5 仍照前例入選，改寫重評的題要把舊分數移出原評分檔，避免同一題兩筆分數。
- 選題代理的「查重」欄寫已查前幾批，寫卡代理仍抓到 22 個撞題；寫卡查重這一步不能省。
