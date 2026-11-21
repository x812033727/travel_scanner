---
id: 2026-11-19-extend-curio-wave-90-and-so
title: Extend Curio wave 90 and So Thats Why wave 119 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T09:09:30Z
created_at: 2026-11-19T09:09:29Z
completed_at: 2026-11-19T09:41:42Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 90 and So Thats Why wave 119 on PR 2177

## Why

延續 PR #2177，在奇聞與原來如此兩個題庫增補有來源的新題。

## Definition of done

- [x] 新增題經雙池既有內容及退案比對，附作者以外的來源覆核。
- [x] 單集與長題有觀眾評估及定稿依據。

## Steps

- [x] 核對原 PR 與分支。
- [x] 彙整奇聞第 90 批與原來如此第 119 批。
- [x] 重建兩池及後台，驗證所有新題，更新同一個 PR。

## Result

奇聞第 90 批新增 5 個單集，入選 1,815 題。原來如此第 119 批新增 12 張日常設計、6 張運動判例及 16 張轉機素材，入選 7,252 張。G762 採完整研究稿，六章共 510 秒，併分 7.74，可成題長片累計 107 組。

## How to verify

```sh
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
node --test tools/video/{curio,so-thats-why}/pool/pool.test.mjs tools/video/pool-admin/bundle.test.mjs
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```
