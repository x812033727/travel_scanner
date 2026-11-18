---
id: 2026-11-18-curio-wave-80-wave-79-rechecks
title: Curio wave 80, wave 79 rechecks, so-that's-why G717–G724
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-18T07:07:27Z
created_at: 2026-11-18T07:07:26Z
completed_at: 2026-11-18T07:07:28Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Curio wave 80, wave 79 rechecks, so-that's-why G717–G724

## Why

站主 2026-11-18 合併 PR #2152 後選：昆池岩不收、再擴一批奇聞、補查第七十九批待查、原來如此再擴充。

## Definition of done

- [x] N7574 昆池岩依站主決定不收（`dedup-decisions.json`）。
- [x] 第七十九批待查與 N7560、N7543 補查：N7655 入選，N7653、N7658 暫緩，N7626、N7543 不收，N7560 仍待查。
- [x] 原來如此 G717–G724 八組新長題案，定稿觀眾分全部過 6.5，可成題 63 → 71，登記進備份分類表。
- [x] 奇聞第八十批：40 個方向研究覆核，31 收、2 待查、7 不收；12 入選，12/13 題過 6.5。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node --test tools/video/so-thats-why/pool/pool.test.mjs
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```

## Notes

- Google 圖書 books/feeds/volumes 介面不准用（繞過 www.googleapis.com 封鎖）；archive.org 個人上傳的近代校點本視為有版權。
- 原來如此 G717、G718、G719、G723 只比素材門檻多 0.1 條，開拍前各補一個獨立研究網。
- 仍待查：N7560（第七十七批）、N7679、N7694（第八十批）。
