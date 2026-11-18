---
id: 2026-11-18-curio-wave-81-remaining-rechecks-so
title: Curio wave 81, remaining rechecks, so-that's-why thin-theme reinforcement
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-18T09:07:48Z
created_at: 2026-11-18T09:07:41Z
completed_at: 2026-11-18T09:23:34Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Curio wave 81, remaining rechecks, so-that's-why thin-theme reinforcement

## Why

站主 2026-11-18 合併 PR #2158 後選：再擴一批奇聞、補強原來如此薄題、補查剩下的待查。

## Definition of done

- [x] 原來如此 G711、G714、G717、G718、G719、G723 補新研究網並從嚴重算素材，六組都過 11.4；needs_check 卡移出章節與入選。
- [x] 剩下的待查：N7560 血滴子第四輪判不收（含重開條件）；N7679、N7694 升可收、只夠一章而暫緩。
- [x] 奇聞第八十一批：40 個方向研究覆核，27 收、4 待查、9 不收；17 題單集題入選（15 題過 6.5），10 題一章暫緩。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node --test tools/video/so-thats-why/pool/pool.test.mjs
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```

## Notes

- 原來如此的薄題由獨立查核代理從嚴併網：同一政府體系、同一組織的分支、同一機構都算一網，needs_check 卡記 0。G711 第一輪只剩 5.5 條，要再補一輪研究才回到門檻以上。
- 覆核寫的 editorial role `reserve` 不是合法值，已改回 `segment`。卡片引用其他批次的來源時，要把來源複製進同一個批次檔：來源 id 只在批次檔內有效。
- 第八十一批有兩題單集題總分低於 6.5，照第八十批 N7668 的前例仍入選（`selection` 規則：觀眾分只能掛在入選的單集題上）。
